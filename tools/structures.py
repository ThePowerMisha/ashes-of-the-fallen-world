"""Deterministic 1.20.1 structure templates; only Python stdlib needed.
Sparse templates deliberately omit the sky, and clear only small interior spaces.
"""
from dataclasses import dataclass
from pathlib import Path
import gzip, io, json, random, struct
from site_terrain import enhance_site
from site_supplies import SITE_FIXTURES
from site_supports import foundation_jobs
from site_levels import BURIAL_RESERVE, FLOOR_RESERVE, TERRACES, VARIANTS, level_layouts, terraform_levels

def st(name, **props):
    return {'Name': name if ':' in name else 'minecraft:'+name, **({'Properties':props} if props else {})}
def string(s):
    b=s.encode('utf-8'); return struct.pack('>H',len(b))+b
def kind(v):
    return {int:3,float:6,str:8,list:9,dict:10}[type(v)]
def payload(v):
    if type(v)==int: return struct.pack('>i',v)
    if type(v)==float: return struct.pack('>d',v)
    if type(v)==str: return string(v)
    if type(v)==list:
        t=kind(v[0]) if v else 10
        assert all(kind(x)==t for x in v)
        return bytes([t])+struct.pack('>i',len(v))+b''.join(payload(x) for x in v)
    return b''.join(bytes([kind(x)])+string(k)+payload(x) for k,x in v.items())+b'\0'
def nbt(v): return b'\x0a\0\0'+payload(v)

class Build:
    def __init__(self, size, seed, style):
        self.size=size; self.r=random.Random(seed); self.blocks={}; self.style=style
        self.entities = []
        self.extra_depth = None
        self.entrance_steps = []
        self.walkways = {}
        self.stone=('stone_bricks','cracked_stone_bricks','mossy_stone_bricks','cobblestone') if style==0 else ('cobbled_deepslate','deepslate_bricks','cracked_deepslate_bricks','tuff')
        self.wood='spruce' if style==0 else 'dark_oak'
    def put(self,x,y,z,block,props=None,tag=None):
        assert all(0<=p<n for p,n in zip((x,y,z),self.size)),(x,y,z,self.size)
        self.blocks[x,y,z]=(st(block,**(props or {})),tag)
    def fill(self,x0,y0,z0,x1,y1,z1,block,props=None):
        for y in range(y0,y1+1):
            for z in range(z0,z1+1):
                for x in range(x0,x1+1): self.put(x,y,z,block,props)
    def rubble(self,x,y,z): self.put(x,y,z,self.r.choices(self.stone,[5,3,2,2])[0])
    def footing(self,x0,z0,x1,z1):
        # Two foundation layers plus a ruined floor, at y=2 the walking surface.
        for x in range(x0,x1+1):
            for z in range(z0,z1+1):
                for y in (0,1,2): self.rubble(x,y,z)
    def path(self,x0,z0,x1,z1):
        self.mark_walkway(x0, z0, x1, z1, 2)
        for x in range(x0,x1+1):
            for z in range(z0,z1+1):
                self.put(x,1,z,'cobblestone')
                self.put(x,2,z,self.r.choice(['gravel','coarse_dirt','cobblestone','mossy_cobblestone']))
    def mark_walkway(self, x0, z0, x1, z1, y, *, perimeter=False):
        along_x = x1 - x0 >= z1 - z0
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                edge = x in (x0, x1) or z in (z0, z1)
                if perimeter and not edge:
                    continue
                if perimeter:
                    pier = ((z in (z0, z1) and (x - x0) % 4 == 0)
                            or (x in (x0, x1) and (z - z0) % 4 == 0)
                            or (x in (x0, x1) and z in (z0, z1)))
                else:
                    along, end = (x - x0, x1 - x0) if along_x else (z - z0, z1 - z0)
                    pier = along % 4 == 0 or along == end
                self.walkways[x, y, z] = self.walkways.get((x, y, z), False) or pier
    def pillar(self,x,z,h,base=3):
        for y in range(base,base+h): self.rubble(x,y,z)
    def chest(self, x, y, z, site, facing='north', *, supplies=False, submerged=False):
        table = site + ('_supplies' if supplies else '')
        self.put(x, y, z, 'chest', {
            'facing': facing, 'type': 'single', 'waterlogged': str(submerged).lower()
        }, {'id': 'minecraft:chest', 'LootTable': 'ashes:lore/'+table})
    def villager(self, x, y, z):
        self.entities.append({
            'pos': [x + .5, float(y), z + .5],
            'blockPos': [x, y, z],
            'nbt': {'id': 'minecraft:villager', 'VillagerData': {
                'type': 'minecraft:plains', 'profession': 'minecraft:none', 'level': 1
            }}
        })
    def house(self,x0,z0,x1,z1,door,roof=True, *, ruined=True):
        self.footing(x0,z0,x1,z1)
        self.fill(x0+1,3,z0+1,x1-1,6,z1-1,'air')
        for x in range(x0,x1+1):
            for z in range(z0,z1+1):
                if x not in (x0,x1) and z not in (z0,z1): continue
                corner=x in (x0,x1) and z in (z0,z1)
                for y in range(3,7):
                    if z==z0 and x==door and y<=4: self.put(x,y,z,'air'); continue
                    if y==5 and not corner and ((x+z)%4==0): self.put(x,y,z,'air'); continue
                    if ruined and y>=5 and not corner and self.r.random()<.19: continue
                    if corner: self.put(x,y,z,self.wood+'_log',{'axis':'y'})
                    elif y<=4: self.rubble(x,y,z)
                    else: self.put(x,y,z,self.wood+'_planks')
        if roof:
            for x in range(x0,x1+1):
                y=7+min(x-x0,x1-x)
                for z in range(z0,z1+1):
                    if not ruined or self.r.random()>.27: self.put(x,y,z,self.wood+'_planks')
            for z in (z0,z1):
                for x in range(x0+1,x1):
                    for y in range(7,7+min(x-x0,x1-x)):
                        if not ruined or self.r.random()>.28: self.put(x,y,z,self.wood+'_planks')
    def export(self):
        palette=[]; lookup={}; blocks=[]
        # Minecraft template ordering: full blocks, other blocks, block entities.
        def order(entry):
            (x,y,z),(s,tag)=entry
            return (2 if tag else 1 if s['Name'].endswith(('_slab','_stairs','_fence','_wall','_lantern','_torch')) or s['Name']=='minecraft:air' else 0,y,x,z)
        for pos,(state,tag) in sorted(self.blocks.items(),key=order):
            k=json.dumps(state,sort_keys=True)
            if k not in lookup: lookup[k]=len(palette);palette.append(state)
            blocks.append({'pos':list(pos),'state':lookup[k],**({'nbt':tag} if tag else {})})
        return {'DataVersion':3465,'size':list(self.size),'palette':palette,'blocks':blocks,'entities':self.entities}

def village(b):
    b.path(14,3,16,27); b.path(3,14,27,16)
    for x,z in [(3,3),(20,3),(3,20),(20,20)]:
        b.house(x,z,x+7,z+7,x+3,roof=(x!=20 or z!=20))
        b.put(x+2,3,z+5,'barrel',{'facing':'up','open':'false'})
        b.put(x+5,3,z+5,'crafting_table')
    b.footing(12,12,18,18)
    for x,z in [(13,13),(17,13),(13,17),(17,17)]: b.pillar(x,z,3)
    b.put(15,3,15,'bell',{'attachment':'floor','facing':'north','powered':'false'})
    for x in (3,25):
        for z in range(12,19): b.put(x,3,z,'hay_block',{'axis':'y'}) if z%3==0 else None
    b.put(7,3,8,'farmersdelight:cutting_board',{'facing':'north'})
    b.fill(24,2,13,26,2,17,'farmersdelight:rich_soil')
    b.chest(5,3,8,'silent_hamlet'); b.chest(23,3,25,'silent_hamlet',supplies=True)

def battlefield(b):
    b.path(2,13,26,15)
    for x0,z0 in [(3,5),(18,5),(3,20),(18,20)]:
        b.footing(x0,z0,x0+6,z0+3)
        for x in range(x0,x0+7):
            for y in range(3,3+b.r.randint(1,3)):
                if b.r.random()>.18: b.rubble(x,y,z0)
        b.put(x0+2,3,z0+2,'barrel',{'facing':'up','open':'false'})
        b.put(x0+4,3,z0+2,'bone_block',{'axis':'x'})
    b.footing(12,11,16,17)
    for x,z in [(12,11),(16,17)]: b.pillar(x,z,3)
    b.put(14,3,14,'anvil',{'facing':'north'})
    for x,z in [(5,11),(9,17),(19,11),(22,18),(15,6)]:
        b.put(x,2,z,'coarse_dirt'); b.put(x,3,z,b.r.choice(['bone_block','cobbled_deepslate','gravel']))
    for x,z in [(7,6),(21,21)]:
        b.put(x,3,z,'immersiveengineering:treated_wood_horizontal')
        b.put(x+1,3,z,'create:industrial_iron_block')
    b.chest(6,3,7,'last_stand'); b.chest(20,3,22,'last_stand',supplies=True)

def graveyard(b):
    b.path(9,2,11,20)
    for x in range(2,19):
        for z in (2,20):
            if z==2 and 8<=x<=12: continue
            b.pillar(x,z,b.r.randint(1,3))
    for z in range(3,20):
        for x in (2,18): b.pillar(x,z,b.r.randint(1,3))
    for x in (5,14):
        for z in (5,9,13,17):
            b.path(x,z,x+1,z+2)
            b.put(x,3,z,'stone_brick_wall')
            b.put(x+1,3,z,'stone_brick_wall')
            b.put(x,3,z+1,'mossy_stone_brick_slab',{'type':'bottom','waterlogged':'false'})
    b.footing(8,17,12,21)
    for x,z in [(8,17),(12,17),(8,21),(12,21)]: b.pillar(x,z,4)
    b.fill(8,7,17,12,7,21,'stone_brick_slab',{'type':'bottom','waterlogged':'false'})
    b.put(10,3,20,'soul_lantern',{'hanging':'false','waterlogged':'false'})
    b.chest(10,3,19,'nameless_graves')
    b.put(8,6,17,'botania:livingrock')
    b.put(12,6,17,'botania:livingrock')

def altar(b):
    for x in range(2,15):
        for z in range(2,15):
            if (x-8)**2+(z-8)**2<=42:
                for y in (0,1,2): b.rubble(x,y,z)
                if (x+z)%4==0: b.put(x,2,z,'chiseled_stone_bricks')
    for x,z in [(4,4),(12,4),(4,12),(12,12),(8,2),(8,14)]:
        b.pillar(x,z,b.r.randint(3,5));b.put(x,3,z,'chiseled_stone_bricks')
    b.fill(7,3,7,9,3,9,'polished_deepslate');b.fill(7,4,7,9,4,9,'chiseled_deepslate')
    b.put(8,5,8,'ars_nouveau:source_gem_block');b.put(8,6,8,'amethyst_cluster',{'facing':'up','waterlogged':'false'})
    b.put(6,4,8,'create:brass_casing')
    b.put(10,4,8,'botania:livingrock')
    for x,z in [(6,8),(10,8),(8,6),(8,10)]: b.put(x,3,z,'soul_lantern',{'hanging':'false','waterlogged':'false'})
    b.chest(8,3,11,'three_seals_altar')

def tower(b):
    b.footing(3,3,13,13);b.fill(5,3,5,11,12,11,'air')
    for x in range(3,14):
        for z in range(3,14):
            if x not in (3,4,12,13) and z not in (3,4,12,13):continue
            for y in range(3,14):
                if z in (3,4) and 7<=x<=9 and y<=5: continue
                if y in (7,8,11) and (x==8 or z==8):continue
                if y>=11 and b.r.random()<.27:continue
                b.rubble(x,y,z)
    b.fill(5,8,5,11,8,11,b.wood+'_planks'); b.fill(5,8,6,5,8,6,'air')
    for y in range(3,13): b.put(5,y,6,'ladder',{'facing':'east','waterlogged':'false'})
    for x in range(3,14,2):
        b.rubble(x,14,3); b.rubble(x,14,13)
    for z in range(5,13,2): b.rubble(3,14,z);b.rubble(13,14,z)
    b.chest(10,3,10,'broken_watch',supplies=True);b.chest(10,9,10,'broken_watch')
    for x in (6,10):
        b.put(x,9,7,'create:copper_casing')
    b.put(8,9,8,'cartography_table')

def archive(b):
    b.footing(2,2,18,18); b.fill(4,3,4,16,8,16,'air')
    for x in range(2,19):
        for z in range(2,19):
            if x not in (2,3,17,18) and z not in (2,3,17,18):continue
            for y in range(3,10):
                if z in (2,3) and 9<=x<=11 and y<=6:continue
                if y>=7 and b.r.random()<.24:continue
                b.rubble(x,y,z)
    for x in (5,15):
        for z in range(5,16):
            if z%4!=0:b.fill(x,3,z,x,5,z,'bookshelf')
    for x,z in [(7,7),(13,7),(7,13),(13,13)]:b.pillar(x,z,6)
    for x in range(3,18):
        for z in range(3,18):
            if (x<7 or x>13 or z>13) and b.r.random()>.25:b.rubble(x,9,z)
    b.put(10,3,10,'lectern',{'facing':'north','has_book':'false','powered':'false'})
    for x in (8,12):
        b.put(x,3,10,'create:andesite_casing')
        b.put(x,4,10,'immersiveengineering:coil_lv')
    b.chest(8,3,15,'sealed_archive');b.chest(12,3,15,'sealed_archive',supplies=True)

from structure_sites import (
    abyss_temple, ancient_mine, archmages_keep, catacombs, drowned_city, fallen_capital,
    infected_hamlet, keepers_keep, limit_lab, mechanists_keep, observatory, surviving_hamlet,
)


@dataclass(frozen=True)
class Site:
    slug: str
    title: str
    dimensions: tuple
    build: object
    biomes: str
    region: str
    weight: int
    memento: str
    author: str
    pages: tuple
    supplies: tuple
    surface: int = 2


# Loot entries contain an item ID, a weight, and the minimum and maximum count.
SITES = (
    Site('silent_hamlet', 'Деревня последнего колокола', (31, 12, 31), village, 'lowland', 'lore_sites', 4,
         'archive_fragment', 'Староста Рада',
         ('Ильма велела оставить колокол у дороги. Мы ушли до рассвета. Ключ от амбара я оставила возле разделочной доски.',
          'За нами не посылайте. Караван забрал всех, кто успел к первому удару. Если кто вернётся, на грядках ещё можно найти семена.'),
         (('farmersdelight:cabbage_seeds', 5, 1, 3), ('farmersdelight:onion', 5, 1, 3),
          ('farmersdelight:apple_cider', 2, 1, 1))),
    Site('last_stand', 'Поле последнего рубежа', (29, 8, 29), battlefield, 'lowland', 'lore_sites', 3,
         'scout_report', 'Дозорный Лев',
         ('Дозор удерживал дорогу, пока уходили караваны. Приказ был прост: не преследовать голоса из тумана.',
          'К рассвету люди Ильмы должны пройти перевал. Положите три стрелы на камень у мельницы, если дорога открыта.'),
         (('minecraft:arrow', 5, 3, 8), ('minecraft:shield', 1, 1, 1),
          ('immersiveengineering:plate_steel', 2, 1, 2))),
    Site('nameless_graves', 'Кладбище безымянных', (21, 9, 23), graveyard, 'woodland', 'lore_sites', 4,
         'nature_dossier', 'Архивист Домна',
         ('На третью ночь надгробия начали шептать. Имена я переписала в книгу, а камни развернула к лесу.',
          'Принесённые Ильмой цветы не увяли за зиму. Мы продолжаем приходить, даже когда за оградой повторяют наши шаги.'),
         (('botania:white_petal', 5, 1, 3), ('botania:livingrock', 3, 1, 3),
          ('minecraft:glow_berries', 4, 1, 3))),
    Site('three_seals_altar', 'Алтарь трёх печатей', (17, 9, 17), altar, 'woodland', 'lore_sites', 2,
         'mage_dossier', 'Селена',
         ('Камень хранителей, латунь механиков, кристалл архимагов. Три места в круге и три решения.',
          'Когда мы дали обещание хранить печати порознь, Варден попросил записать и его несогласие. Я записала оба.'),
         (('ars_nouveau:source_gem', 4, 1, 2), ('irons_spellbooks:arcane_essence', 3, 1, 3),
          ('minecraft:amethyst_shard', 5, 1, 3))),
    Site('broken_watch', 'Сломанная дозорная башня', (17, 16, 17), tower, 'highland', 'lore_sites', 4,
         'expedition_seal', 'Смотритель Егор',
         ('До третьего удара я видел огонь с обсерватории. После удара с перевала ответили тем же сигналом дважды.',
          'Сигнальная линза осталась на втором этаже. Дожидайтесь белого света и сверяйте тропу с картой.'),
         (('minecraft:spyglass', 2, 1, 1), ('create:copper_sheet', 4, 1, 3),
          ('minecraft:compass', 2, 1, 1))),
    Site('sealed_archive', 'Запечатанный архив механиков', (21, 12, 21), archive, 'woodland', 'lore_sites', 3,
         'mechanic_dossier', 'Варден',
         ('Приборы показали отклонение до запуска. Совет велел продолжать. Подлинник остался в столице.',
          'Копии протокола хранятся здесь и в лаборатории. Ищите спуск под каменной аркой, у которой нет ворот.'),
         (('create:andesite_alloy', 5, 1, 3), ('create:cogwheel', 4, 1, 2),
          ('immersiveengineering:wire_copper', 3, 1, 4))),
    Site('fallen_capital', 'Столица Трёх Колоколов', (45, 15, 45), fallen_capital, 'lowland', 'lore_landmarks', 2,
         'archive_fragment', 'Секретарь Совета',
         ('Я записывал заседания в южной галерее. В тот вечер Совет узнал о сигнале и решил, что отключение Предела погубит города зимой.',
          'Мы спрятали протокол за трибуной. На обратной стороне есть имена тех, кто голосовал против. Их было больше, чем принято считать.'),
         (('create:brass_ingot', 3, 1, 2), ('farmersdelight:apple_cider', 3, 1, 2),
          ('minecraft:emerald', 2, 1, 2))),
    Site('mechanists_keep', 'Крепость Медных Ворот', (33, 15, 33), mechanists_keep, 'lowland', 'lore_landmarks', 4,
         'mechanic_dossier', 'Мастер Федот',
         ('Внутренний двор служил цехом. Если ветер гнал дым к воротам, провода отсоединяли и открывали боковые пролёты.',
          'Варден увёз головной привод, а мы спрятали запасные детали у печи. Пусть они пригодятся для мельницы.'),
         (('create:shaft', 5, 1, 3), ('create:cogwheel', 4, 1, 3),
          ('create:brass_sheet', 2, 1, 2), ('immersiveengineering:wire_copper', 4, 1, 4))),
    Site('keepers_keep', 'Крепость Живых Корней', (33, 12, 33), keepers_keep, 'woodland', 'lore_landmarks', 4,
         'nature_dossier', 'Ильма',
         ('Первую изгородь мы вырастили за лето. После Раскола сюда приносили семена даже те, кто прежде спорил с хранителями.',
          'Запас с западной грядки лучше отдать людям. Восточную оставьте такой, какой её застали.'),
         (('botania:livingrock', 4, 1, 3), ('botania:green_petal', 4, 1, 3),
          ('farmersdelight:tomato_seeds', 5, 1, 3), ('botania:manasteel_ingot', 1, 1, 1))),
    Site('archmages_keep', 'Крепость Тихих Звёзд', (33, 14, 33), archmages_keep, 'upland', 'lore_landmarks', 4,
         'mage_dossier', 'Селена',
         ('Четыре кристалла отражали свет над двором. По их цвету ученики сверяли направление волны.',
          'На третью ночь отражение запоздало. Мы закрыли книги, вывели учеников и оставили записи у кафедры.'),
         (('ars_nouveau:source_gem', 4, 1, 2), ('irons_spellbooks:arcane_essence', 4, 1, 3),
          ('minecraft:amethyst_shard', 4, 1, 3))),
    Site('limit_lab', 'Лаборатория Предела', (31, 18, 33), limit_lab, 'woodland', 'lore_landmarks', 3,
         'mechanic_dossier', 'Варден',
         ('Четыре катушки, две исправны. Кристалл загорелся раньше подачи тока, когда техник назвал своё имя.',
          'Верхняя арка ещё держится. Выведите людей по южной лестнице, а счётчики оставьте на месте. Я поднимусь последним.'),
         (('create:cogwheel', 4, 1, 3), ('immersiveengineering:wire_copper', 4, 1, 4),
          ('ars_nouveau:source_gem', 3, 1, 2), ('create:brass_sheet', 2, 1, 2)), surface=12),
    Site('infected_hamlet', 'Поселение Глухой Ручей', (29, 12, 29), infected_hamlet, 'woodland', 'lore_frontier', 4,
         'scout_report', 'Дозорный Лев',
         ('Воду из ручья мы больше не пьём. В тёмном доме шевелились пятна, хотя все ушли с последним возом.',
          'Уцелевший журнал положил в южной избе. Стучать в окна бесполезно: иногда оттуда стучат в ответ.'),
         (('farmersdelight:canvas', 5, 1, 3), ('minecraft:torch', 5, 2, 5),
          ('minecraft:amethyst_shard', 2, 1, 2))),
    Site('catacombs', 'Катакомбы Первых Хранителей', (27, 17, 31), catacombs, 'woodland', 'lore_frontier', 4,
         'nature_dossier', 'Архивист Домна',
         ('В склепах были четыре лампы. Я зажгла их одну за другой, пока проводник читал имена.',
          'Спрятала переписанные имена в конце центрального коридора. Кто найдёт книгу, пусть оставит здесь свежие берёзовые ветви.'),
         (('botania:livingrock', 4, 1, 4), ('minecraft:candle', 5, 1, 3),
          ('irons_spellbooks:arcane_essence', 2, 1, 2)), surface=11),
    Site('surviving_hamlet', 'Слобода Ильмы', (31, 12, 31), surviving_hamlet, 'lowland', 'lore_frontier', 5,
         'settlement_charter', 'Староста Рада',
         ('После Раскола мы выбрали место вдали от старой дороги. У западного дома общая кухня, у восточного сад.',
          'Путникам рады. Семена берите из общей корзины, если готовы оставить такую же горсть для следующего каравана.'),
         (('farmersdelight:onion', 5, 1, 3), ('farmersdelight:cabbage_seeds', 5, 1, 3),
          ('farmersdelight:apple_cider', 3, 1, 1))),
    Site('ancient_mine', 'Шахта Пустых Вагонеток', (27, 16, 32), ancient_mine, 'upland', 'lore_frontier', 5,
         'archive_fragment', 'Шахтёр Мирон',
         ('В третьем штреке пропал звук вагонеток. Колея доходит до перекрёстка, дальше дорога упирается в старый завал.',
          'Инструмент оставили у цинка. Хорошо помню последний счёт в забое: ответов было на один больше, чем людей.'),
         (('create:raw_zinc', 5, 1, 4), ('minecraft:raw_copper', 5, 2, 5),
          ('create:andesite_alloy', 3, 1, 2)), surface=10),
    Site('abyss_temple', 'Храм Глухого Эха', (29, 11, 29), abyss_temple, 'woodland', 'lore_frontier', 3,
         'mage_dossier', 'Неизвестный переписчик',
         ('На седьмой день мы отказались от имён. Сейчас на наши вопросы отвечает только камень.',
          'Я написал это у алтаря. Если кто прочтёт, уведите остальных в тишине. Больше нельзя просить Эхо о помощи.'),
         (('ars_nouveau:source_gem', 4, 1, 2), ('irons_spellbooks:arcane_essence', 4, 1, 2),
          ('minecraft:amethyst_shard', 5, 1, 3))),
    Site('drowned_city', 'Затонувшие Медные Причалы', (39, 11, 39), drowned_city, 'deep_ocean', 'lore_ocean', 1,
         'archive_fragment', 'Смотритель причалов',
         ('Пока горели фонари, суда входили между двумя рядами арок. Новый медный причал открыли за день до Раскола.',
          'Берег ушёл под воду за одну ночь. Смотрительскую книгу я отнёс к медной платформе у южних фонарей.'),
         (('alexsmobs:shark_tooth', 2, 1, 1), ('minecraft:prismarine_shard', 5, 2, 5),
          ('create:copper_sheet', 5, 1, 3), ('minecraft:nautilus_shell', 1, 1, 1))),
    Site('observatory', 'Обсерватория Дальнего Света', (23, 16, 23), observatory, 'highland', 'lore_frontier', 4,
         'scout_report', 'Смотритель Егор',
         ('Медная труба смотрит на старый перевал. По ней дозор мог увидеть огни столичных ворот.',
          'Последний сигнал из столицы был белым. После него на высоте снова воцарилась тишина. Линзу и журнал оставил возле карт.'),
         (('minecraft:spyglass', 2, 1, 1), ('create:copper_sheet', 5, 1, 3),
          ('minecraft:amethyst_shard', 4, 1, 4))),
)

BIOMES = {
    'lowland': ['plains', 'sunflower_plains', 'savanna', 'meadow', 'forest', 'birch_forest'],
    'woodland': ['forest', 'birch_forest', 'old_growth_birch_forest', 'dark_forest', 'taiga',
                 'old_growth_pine_taiga', 'old_growth_spruce_taiga', 'cherry_grove', 'meadow'],
    'highland': ['meadow', 'windswept_hills', 'windswept_forest', 'windswept_gravelly_hills',
                 'grove', 'snowy_slopes', 'stony_peaks'],
    'upland': ['plains', 'forest', 'meadow', 'taiga', 'windswept_hills', 'windswept_forest', 'grove'],
    'deep_ocean': ['deep_ocean', 'deep_cold_ocean', 'deep_lukewarm_ocean', 'deep_frozen_ocean'],
}

TERRALITH = {
    'lowland': ['blooming_valley', 'lavender_valley', 'shield', 'steppe'],
    'woodland': ['alpine_grove', 'blooming_plateau', 'siberian_grove', 'sakura_grove', 'temperate_highlands'],
    'highland': ['alpine_highlands', 'skylands_spring', 'rocky_mountains', 'highlands', 'wintry_forest'],
    'upland': ['shield', 'alpine_grove', 'temperate_highlands', 'highlands'],
}
PLACEMENT = {
    'lore_sites': (40, 18, 185628321),
    'lore_landmarks': (70, 31, 185628322),
    'lore_frontier': (49, 22, 185628323),
    'lore_ocean': (48, 21, 185628324),
}


def item_entry(name, weight, low=1, high=1):
    entry = {'type': 'minecraft:item', 'name': name, 'weight': weight}
    if (low, high) != (1, 1):
        entry['functions'] = [{'function': 'minecraft:set_count', 'count': {
            'type': 'minecraft:uniform', 'min': low, 'max': high,
        }}]
    return entry


def theme_pool(site):
    return {'rolls': 2, 'entries': [item_entry(*supply) for supply in site.supplies]}


def lore_loot(site):
    def quote(text):
        return "'" + text.replace('\\', '\\\\').replace("'", "\\'") + "'"

    assert len(site.title) <= 32
    pages = [quote(json.dumps({'text': page}, ensure_ascii=False)) for page in site.pages]
    tag = f'{{title:{quote(site.title)},author:{quote(site.author)},pages:[{",".join(pages)}],resolved:1b}}'
    entry = item_entry('minecraft:written_book', 1)
    entry['functions'] = [{'function': 'minecraft:set_nbt', 'tag': tag}]
    return {'type': 'minecraft:chest', 'pools': [
        {'rolls': 1, 'entries': [entry]},
        {'rolls': 1, 'entries': [item_entry('kubejs:' + site.memento, 1)]},
        theme_pool(site),
        {'rolls': 1, 'entries': [item_entry(name, 1) for name in SITE_FIXTURES[site.slug][1]]},
    ]}


def generate_structures(root):
    data = root / 'overrides/kubejs/data/ashes'

    def write(path, obj):
        dest = data / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    for group, biomes in BIOMES.items():
        write(f'tags/worldgen/biome/lore/{group}.json', {
            'replace': False,
            'values': ['minecraft:' + biome for biome in biomes] +
                      [{'id': 'terralith:' + biome, 'required': False} for biome in TERRALITH.get(group, ())],
        })

    entries = {region: [] for region in PLACEMENT}
    report = []
    for index, site in enumerate(SITES):
        templates = []
        table = 'ashes:lore/' + site.slug
        supplies = False
        buried = site.surface != 2
        layouts = level_layouts(site.slug)
        terrace_end = 2 + VARIANTS
        version_count = terrace_end if buried else terrace_end + VARIANTS
        for number in range(version_count):
            supported = number >= terrace_end
            variant = number - VARIANTS if supported else number
            terraced = variant >= 2
            active = supported or (buried and terraced)
            style = variant % 2
            seed = 20261124 + index * 101 + (variant * 17 if terraced else style)
            builder = Build(site.dimensions, seed, style)
            levels = layouts[variant - 2] if terraced else None
            if terraced and buried:
                x, height, z = site.dimensions
                builder.size = (x, height + BURIAL_RESERVE, z + BURIAL_RESERVE)
                builder.extra_depth = levels[0]
            site.build(builder)
            entrances = set()
            if terraced and not buried:
                entrances = {col for section, rise in zip(TERRACES[site.slug], levels, strict=True)
                             for col in section.approach(rise)}
            terrain_offset = enhance_site(builder, site, entrances)
            routes = []
            if terraced:
                if buried:
                    terrain_offset = BURIAL_RESERVE
                    routes = [builder.entrance_steps]
                else:
                    routes = terraform_levels(builder, site, levels)
                    terrain_offset += FLOOR_RESERVE
            if buried:
                x, _, z = site.dimensions
                # Match the starting biome at ground level instead of sampling the buried room.
                builder.put(x // 2, site.surface + terrain_offset, z // 2, 'jigsaw', {'orientation': 'up_north'}, {
                    'id': 'minecraft:jigsaw', 'name': 'ashes:surface_anchor', 'target': 'minecraft:empty',
                    'pool': 'minecraft:empty', 'final_state': 'minecraft:structure_void', 'joint': 'rollable',
                })
            support_count = foundation_jobs(builder) if supported else 0
            obj = builder.export()
            tables = [block['nbt']['LootTable'] for block in obj['blocks'] if 'LootTable' in block.get('nbt', {})]
            assert tables.count(table) == 1 and set(tables) <= {table, table + '_supplies'}, site.slug
            supplies = supplies or table + '_supplies' in tables
            name = f'lore/{site.slug}_{number + 1}'
            dest = data / 'structures' / f'{name}.nbt'
            dest.parent.mkdir(parents=True, exist_ok=True)
            raw = nbt(obj)
            if not dest.exists() or gzip.decompress(dest.read_bytes()) != raw:
                buf = io.BytesIO()
                with gzip.GzipFile(fileobj=buf, mode='wb', filename='', mtime=0, compresslevel=9) as stream:
                    stream.write(raw)
                dest.write_bytes(buf.getvalue())
            row = {'template': name, 'size': obj['size'], 'blocks': len(obj['blocks']),
                   'chests': len(tables), 'entities': len(obj['entities'])}
            if active:
                templates.append({'weight': 1, 'element': {
                    'element_type': 'minecraft:single_pool_element',
                    'location': 'ashes:' + name, 'processors': {'processors': []}, 'projection': 'rigid',
                }})
                row.update(levels=levels, routes=routes, foundations=support_count)
            report.append(row)
        write(f'worldgen/template_pool/lore/{site.slug}.json', {'fallback': 'minecraft:empty', 'elements': templates})
        sea = site.biomes == 'deep_ocean'
        structure = {
            'type': 'minecraft:jigsaw', 'biomes': '#ashes:lore/' + site.biomes,
            'step': 'surface_structures', 'spawn_overrides': {},
            'terrain_adaptation': 'none' if (sea or buried) else 'beard_thin',
            'start_pool': table,
            # A depth of zero creates an empty start in Java 1.20.1.
            'size': 1, 'start_height': {'absolute': -site.surface - terrain_offset},
            'project_start_to_heightmap': 'OCEAN_FLOOR_WG' if sea else 'WORLD_SURFACE_WG',
            'max_distance_from_center': 48, 'use_expansion_hack': False,
        }
        if buried:
            structure['start_jigsaw_name'] = 'ashes:surface_anchor'
        write(f'worldgen/structure/{site.slug}.json', structure)
        entries[site.region].append({'structure': 'ashes:' + site.slug, 'weight': site.weight})
        write(f'loot_tables/lore/{site.slug}.json', lore_loot(site))
        if supplies:
            write(f'loot_tables/lore/{site.slug}_supplies.json', {'type': 'minecraft:chest', 'pools': [theme_pool(site)]})
        write(f'advancements/lore/{site.slug}.json', {
            'criteria': {'visit': {'trigger': 'minecraft:location', 'conditions': {'player': [{
                'condition': 'minecraft:entity_properties', 'entity': 'this',
                'predicate': {'location': {'structure': 'ashes:' + site.slug}},
            }]}}},
            'rewards': {'function': f'ashes:news/lore/{site.slug}'},
        })
        message = {'text': f'[Хроники] Открыто место: {site.title}.', 'color': 'dark_aqua'}
        dest = data / 'functions/news/lore' / f'{site.slug}.mcfunction'
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text('tellraw @s[tag=!ashes_news_muted] ' + json.dumps(message, ensure_ascii=False) + '\n',
                        encoding='utf-8')

    for region, (spacing, separation, salt) in PLACEMENT.items():
        write(f'worldgen/structure_set/{region}.json', {
            'structures': entries[region],
            'placement': {'type': 'minecraft:random_spread', 'spacing': spacing, 'separation': separation, 'salt': salt},
        })

    dest = root / 'docs/lore-structures.json'
    dest.parent.mkdir(exist_ok=True)
    dest.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Generated {len(SITES)} sites / {len(report)} templates / {sum(row["blocks"] for row in report)} blocks')


if __name__ == '__main__':
    generate_structures(Path(__file__).resolve().parents[1])
