"""Deterministic 1.20.1 structure templates; only Python stdlib needed.
Sparse templates deliberately omit the sky, and clear only small interior spaces.
"""
from pathlib import Path
import gzip, io, json, random, struct

# Vanilla block states and the 1.20.1 structure NBT format (DataVersion 3465).
def st(name, **props):
    return {'Name':'minecraft:'+name, **({'Properties':props} if props else {})}
def string(s):
    b=s.encode('utf-8'); return struct.pack('>H',len(b))+b
def kind(v):
    return {int:3,str:8,list:9,dict:10}[type(v)]
def payload(v):
    if type(v)==int: return struct.pack('>i',v)
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
        for x in range(x0,x1+1):
            for z in range(z0,z1+1):
                self.put(x,1,z,'cobblestone')
                self.put(x,2,z,self.r.choice(['gravel','coarse_dirt','cobblestone','mossy_cobblestone']))
    def pillar(self,x,z,h,base=3):
        for y in range(base,base+h): self.rubble(x,y,z)
    def chest(self,x,y,z,site,facing='north'):
        self.put(x,y,z,'chest',{'facing':facing,'type':'single','waterlogged':'false'}, {'id':'minecraft:chest','LootTable':'ashes:lore/'+site})
    def house(self,x0,z0,x1,z1,door,roof=True):
        self.footing(x0,z0,x1,z1)
        self.fill(x0+1,3,z0+1,x1-1,6,z1-1,'air')
        for x in range(x0,x1+1):
            for z in range(z0,z1+1):
                if x not in (x0,x1) and z not in (z0,z1): continue
                corner=x in (x0,x1) and z in (z0,z1)
                for y in range(3,7):
                    if z==z0 and x==door and y<=4: self.put(x,y,z,'air'); continue
                    if y==5 and not corner and ((x+z)%4==0): self.put(x,y,z,'air'); continue
                    if y>=5 and not corner and self.r.random()<.19: continue
                    if corner: self.put(x,y,z,self.wood+'_log',{'axis':'y'})
                    elif y<=4: self.rubble(x,y,z)
                    else: self.put(x,y,z,self.wood+'_planks')
        if roof:
            for x in range(x0,x1+1):
                y=7+min(x-x0,x1-x)
                for z in range(z0,z1+1):
                    if self.r.random()>.27: self.put(x,y,z,self.wood+'_planks')
            for z in (z0,z1):
                for x in range(x0+1,x1):
                    for y in range(7,7+min(x-x0,x1-x)):
                        if self.r.random()>.28: self.put(x,y,z,self.wood+'_planks')
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
        return {'DataVersion':3465,'size':list(self.size),'palette':palette,'blocks':blocks,'entities':[]}

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
    b.chest(5,3,8,'silent_hamlet'); b.chest(23,3,25,'silent_hamlet')

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
    b.chest(6,3,7,'last_stand'); b.chest(20,3,22,'last_stand')

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

def altar(b):
    for x in range(2,15):
        for z in range(2,15):
            if (x-8)**2+(z-8)**2<=42:
                for y in (0,1,2): b.rubble(x,y,z)
                if (x+z)%4==0: b.put(x,2,z,'chiseled_stone_bricks')
    for x,z in [(4,4),(12,4),(4,12),(12,12),(8,2),(8,14)]:
        b.pillar(x,z,b.r.randint(3,5));b.put(x,3,z,'chiseled_stone_bricks')
    b.fill(7,3,7,9,3,9,'polished_deepslate');b.fill(7,4,7,9,4,9,'chiseled_deepslate')
    b.put(8,5,8,'amethyst_block');b.put(8,6,8,'amethyst_cluster',{'facing':'up','waterlogged':'false'})
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
    b.chest(10,3,10,'broken_watch');b.chest(10,9,10,'broken_watch')
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
    b.chest(8,3,15,'sealed_archive');b.chest(12,3,15,'sealed_archive')

# slug, name, size, builder, biome group, weight, guaranteed modest lore item, text.
SITES=[
('silent_hamlet','Деревня последнего колокола',(31,12,31),village,'lowland',4,'archive_fragment','Ильма велела оставить колокол у дороги. Мы ушли до рассвета. Если кто-то вернётся, пусть не разжигает печи, пока не проверит подвал.'),
('last_stand','Поле последнего рубежа',(29,8,29),battlefield,'lowland',3,'scout_report','Дозор удерживал перевал, пока уходили караваны. Приказ был прост: не преследовать голоса из тумана. Последний гонец так и не пришёл.'),
('nameless_graves','Кладбище безымянных',(21,9,23),graveyard,'woodland',4,'nature_dossier','Хранители записали имена на бумаге, когда камни начали повторять шёпот. Здесь покоятся те, кого не успели вывезти из долины.'),
('three_seals_altar','Алтарь трёх печатей',(17,9,17),altar,'woodland',2,'mage_dossier','Селена: ни один орден не должен владеть единственным ключом. Печати надлежит хранить порознь. В этом круге мы дали последнее обещание.'),
('broken_watch','Сломанная дозорная башня',(17,16,17),tower,'highland',4,'expedition_seal','В третий удар башня перестала отвечать. В журнале осталась карта безопасных троп. Следуйте к огням, а не к голосам.'),
('sealed_archive','Запечатанный архив механиков',(21,12,21),archive,'woodland',2,'mechanic_dossier','Варден: приборы показали отклонение до запуска. Совет велел продолжать. Копии протокола спрятаны отдельно; никогда не собирайте Предел снова.')]
BIOMES={
 'lowland':['plains','sunflower_plains','savanna','meadow','forest','birch_forest'],
 'woodland':['forest','birch_forest','old_growth_birch_forest','dark_forest','taiga','old_growth_pine_taiga','old_growth_spruce_taiga','cherry_grove','meadow'],
 'highland':['meadow','windswept_hills','windswept_forest','windswept_gravelly_hills','grove','snowy_slopes','stony_peaks']}
# Optional IDs deliberately don't hard-depend on a particular Terralith release.
TERRALITH={'lowland':['blooming_valley','lavender_valley','shield','steppe'],'woodland':['alpine_grove','blooming_plateau','siberian_grove','sakura_grove','temperate_highlands'],'highland':['alpine_highlands','skylands_spring','rocky_mountains','highlands','wintry_forest']}

def generate_structures(root):
    data=root/'overrides/kubejs/data/ashes'
    def write(path,obj):
        p=data/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for group,biomes in BIOMES.items():
        write(f'tags/worldgen/biome/lore/{group}.json',{'replace':False,'values':['minecraft:'+b for b in biomes]+[{'id':'terralith:'+b,'required':False} for b in TERRALITH[group]]})
    entries=[]; report=[]
    for n,(slug,title,size,builder,group,weight,item,lore) in enumerate(SITES):
        templates=[]
        for style in (0,1):
            b=Build(size,20261124+n*101+style,style);builder(b);obj=b.export()
            assert len(obj['blocks'])==len({tuple(v['pos']) for v in obj['blocks']})
            assert any(v.get('nbt',{}).get('LootTable')=='ashes:lore/'+slug for v in obj['blocks'])
            name=f'lore/{slug}_{style+1}';p=data/'structures'/f'{name}.nbt';p.parent.mkdir(parents=True,exist_ok=True)
            raw=nbt(obj);buf=io.BytesIO()
            with gzip.GzipFile(fileobj=buf,mode='wb',filename='',mtime=0,compresslevel=9) as f:f.write(raw)
            # Avoid gzip header/compressor differences on other platforms if data already matches.
            if not p.exists() or gzip.decompress(p.read_bytes())!=raw:p.write_bytes(buf.getvalue())
            assert gzip.decompress(p.read_bytes())==raw
            templates.append({'weight':1,'element':{'element_type':'minecraft:single_pool_element','location':'ashes:'+name,'processors':{'processors':[]},'projection':'rigid'}})
            report.append({'template':name,'size':list(size),'blocks':len(obj['blocks']),'chests':sum('nbt' in v for v in obj['blocks'])})
        write(f'worldgen/template_pool/lore/{slug}.json',{'fallback':'minecraft:empty','elements':templates})
        write(f'worldgen/structure/{slug}.json',{'type':'minecraft:jigsaw','biomes':'#ashes:lore/'+group,'step':'surface_structures','spawn_overrides':{},'terrain_adaptation':'beard_thin','start_pool':'ashes:lore/'+slug,'size':0,'start_height':{'absolute':-2},'project_start_to_heightmap':'WORLD_SURFACE_WG','max_distance_from_center':48,'use_expansion_hack':False})
        entries.append({'structure':'ashes:'+slug,'weight':weight})
        # Written book with JSON text pages in 1.20.1 SNBT; use a title unique to the site.
        page=json.dumps({'text':lore},ensure_ascii=False,separators=(',',':'))
        def q(s):return "'"+s.replace('\\','\\\\').replace("'","\\'")+"'"
        booktag='{title:'+q(title)+',author:'+q('Архивисты')+',pages:['+q(page)+'],resolved:1b}'
        def loot(name,weight=1,lo=1,hi=1):
            e={'type':'minecraft:item','name':name,'weight':weight}
            if lo!=1 or hi!=1:e['functions']=[{'function':'minecraft:set_count','count':{'type':'minecraft:uniform','min':lo,'max':hi}}]
            return e
        write(f'loot_tables/lore/{slug}.json',{'type':'minecraft:chest','pools':[
            {'rolls':1,'entries':[{'type':'minecraft:item','name':'minecraft:written_book','functions':[{'function':'minecraft:set_nbt','tag':booktag}]}]},
            {'rolls':1,'entries':[loot('kubejs:'+item)]},
            {'rolls':{'type':'minecraft:uniform','min':2,'max':4},'entries':[loot('minecraft:bread',5,1,3),loot('minecraft:iron_nugget',5,3,8),loot('minecraft:torch',5,2,6),loot('minecraft:bone',3,1,3),loot('minecraft:paper',4,1,4),loot('minecraft:coal',3,1,3)]}]})
        write(f'advancements/lore/{slug}.json',{'criteria':{'visit':{'trigger':'minecraft:location','conditions':{'player':[{'condition':'minecraft:entity_properties','entity':'this','predicate':{'location':{'structure':'ashes:'+slug}}}]}}},'rewards':{'function':'ashes:news/lore/'+slug}})
        p=data/'functions/news/lore'/f'{slug}.mcfunction';p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text('tellraw @s[tag=!ashes_news_muted] '+json.dumps({'text':'[Хроники] Найдено место памяти: '+title+'. Отыщи свидетельство прежней эпохи.','color':'dark_aqua'},ensure_ascii=False)+'\n',encoding='utf-8')
    write('worldgen/structure_set/lore_sites.json',{'structures':entries,'placement':{'type':'minecraft:random_spread','spacing':40,'separation':18,'salt':185628321}})
    p=root/'docs/lore-structures.json';p.parent.mkdir(exist_ok=True);p.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Generated {len(SITES)} sites / {len(report)} templates / {sum(x["blocks"] for x in report)} block records')

if __name__=='__main__':generate_structures(Path(__file__).resolve().parents[1])
