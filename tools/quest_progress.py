"""Inventory alternatives and links between compatible FTB quest routes."""
import re

FILTER_ID = 'ftbfiltersystem:smart_filter'
FILTER_KEY = 'ftbfiltersystem:filter'

FAMILIES = {
    'beds': ('любая кровать', ('#minecraft:beds',)),
    'banners': ('знамёна любого цвета', ('#minecraft:banners',)),
    'planks': ('доски любой породы', ('#minecraft:planks',)),
    'fences': ('заборы любой породы', ('#minecraft:wooden_fences',)),
    'saplings': ('саженцы любых пород', ('#minecraft:saplings',)),
    'wooden_chests': ('обычные деревянные сундуки', ('minecraft:chest', '#forge:chests/wooden')),
    'boats': ('обычные лодки и лодки с сундуком', ('#minecraft:boats', '#minecraft:chest_boats')),
    'waystones': ('обычные, мшистые, песчаниковые, глубинные, чернитовые или эндерняковые путевые камни',
                  tuple('waystones:' + name + 'waystone' for name in ('', 'mossy_', 'sandy_', 'deepslate_', 'blackstone_', 'end_stone_'))),
    'mushrooms': ('красные и коричневые грибы', ('minecraft:red_mushroom', 'minecraft:brown_mushroom')),
    'provisions': ('хлеб, печёный картофель или жареное мясо',
                   ('minecraft:bread', 'minecraft:baked_potato', 'minecraft:cooked_beef',
                    'minecraft:cooked_porkchop', 'minecraft:cooked_chicken', 'minecraft:cooked_mutton')),
    'campfires': ('обычные костры и костры душ', ('minecraft:campfire', 'minecraft:soul_campfire')),
    'lanterns': ('обычные фонари и фонари душ', ('minecraft:lantern', 'minecraft:soul_lantern')),
    'brickwork': ('каменные кирпичи, их мшистые и потрескавшиеся варианты, а также глубинные кирпичи',
                  ('minecraft:stone_bricks', 'minecraft:mossy_stone_bricks',
                   'minecraft:cracked_stone_bricks', 'minecraft:deepslate_bricks')),
    'copper': ('медные слитки из общего тега Forge', ('#forge:ingots/copper',)),
    'steel': ('стальные слитки из общего тега Forge', ('#forge:ingots/steel',)),
    'stone': ('обычный камень, глубинный сланец, андезит, гранит и диорит',
              ('minecraft:stone', 'minecraft:deepslate', 'minecraft:andesite',
               'minecraft:granite', 'minecraft:diorite')),
    'glass': ('прозрачное и цветное стекло', ('#forge:glass',)),
    'building_bridges': ('деревянные мосты Macaw’s', tuple(
        f'mcwbridges:{wood}_{kind}' for wood in ('oak', 'spruce', 'birch', 'jungle', 'acacia', 'dark_oak')
        for kind in ('log_bridge_middle', 'rail_bridge'))),
}

COMMON_ITEMS = {
    'minecraft:white_bed': 'beds', 'minecraft:white_banner': 'banners',
    'minecraft:oak_planks': 'planks', 'minecraft:oak_fence': 'fences',
    'minecraft:oak_sapling': 'saplings', 'minecraft:chest': 'wooden_chests',
    'minecraft:oak_boat': 'boats', 'minecraft:red_mushroom': 'mushrooms',
    'minecraft:copper_ingot': 'copper', 'mekanism:ingot_steel': 'steel',
    'minecraft:glass': 'glass', 'waystones:waystone': 'waystones',
    'minecraft:stone_bricks': 'brickwork',
}
CONTEXT_FAMILIES = {
    ('01_survival', 'Запасы'): 'provisions',
    ('35_parkour', 'Запас выносливости'): 'provisions',
    ('01_survival', 'Огонь в ночи'): 'campfires',
    ('21_expeditions', 'Лесной приют'): 'campfires',
    ('10_supply', 'Свет на дорогах'): 'lanterns',
    ('05_colony', 'Место для дома'): 'lanterns',
    ('23_city', 'Общественный свет'): 'lanterns',
    ('38_aircraft', 'Взлётная площадка'): 'lanterns',
    ('36_colony_styles', 'Каменоломня'): 'stone',
}

# Links in the quest book preserve the existing progression graph on a live save.
ROUTES = {
    '01_survival': ('39_field_manual', '35_parkour', '43_survey', '44_homestead'),
    '02_ruins': ('21_expeditions', '43_survey', '40_lore_sites', '37_twilight'),
    '03_industry': ('13_create', '14_mekanism', '15_immersive', '17_power', '45_networks'),
    '04_magic': ('18_ars', '19_spells', '20_botania'),
    '05_colony': ('23_city', '36_colony_styles', '41_people', '42_workshops', '34_wards'),
    '07_war': ('22_bosses', '31_forge'),
    '10_supply': ('16_storage', '24_food', '44_homestead', '45_networks', '38_aircraft'),
    '13_create': ('45_networks', '38_aircraft'),
    '14_mekanism': ('17_power', '45_networks'),
    '16_storage': ('45_networks', '17_power'),
    '21_expeditions': ('43_survey', '40_lore_sites'),
    '23_city': ('36_colony_styles', '41_people', '42_workshops'),
    '24_food': ('44_homestead', '41_people'),
    '36_colony_styles': ('42_workshops', '41_people'),
    '41_people': ('23_city', '44_homestead'),
    '42_workshops': ('23_city', '36_colony_styles'),
    '43_survey': ('21_expeditions', '40_lore_sites'),
    '44_homestead': ('24_food', '10_supply'),
    '45_networks': ('13_create', '16_storage', '17_power'),
}


def family_for(chapter, title, item):
    if item and item.startswith('#ashes:quest/'):
        return item.removeprefix('#ashes:quest/')
    return CONTEXT_FAMILIES.get((chapter, title), COMMON_ITEMS.get(item))


GUIDE_NOTES = {
    ('39_field_manual', 'Справочник рецептов'):
        'В JEI можно посмотреть ресурсы, профессии и мультиблоки Mekanism. При совпадении рецептов проверь переключатель Polymorph и единые материалы Almost Unified.',
    ('39_field_manual', 'Подсказки'):
        'Jade показывает блок и его состояние. GuideME открывает справочник AE2. Lootr выдаёт личную добычу, а Corpse оставляет вещи в месте гибели.',
    ('43_survey', 'Развилки атласа'):
        'Для большого маршрута отметь по одному ориентиру в каждом типе руин.',
    ('41_people', 'Первый разговор'):
        'Совместимость MCA с другими мобами проверяй по реакции жителей, когда рядом появляется опасное существо.',
}


def bind_alternatives(chapter, quest):
    if note := GUIDE_NOTES.get((chapter, quest['title'])):
        quest['description'].append(note)
    task = quest['tasks'][0]
    if task['type'] != 'item':
        return
    key = family_for(chapter, quest['title'], task['item'])
    if key is None:
        return
    title, _ = FAMILIES[key]
    task['item'] = {'id': FILTER_ID, 'Count': 1,
                    'tag': {FILTER_KEY: f'item_tag(ashes:quest/{key})'}}
    quest['description'].append(f'Подходящие варианты — {title}. Их можно собрать в любом сочетании.')


def links_for(chapter, uid):
    return [{'id': uid(f'{chapter}/link/{target}'), 'linked_quest': uid(f'{target}/0'), 'x': 9.0, 'y': n * 2.0}
            for n, target in enumerate(ROUTES.get(chapter, ()))]


def tag_files(data, write):
    for key, (_, values) in FAMILIES.items():
        write(data / 'ashes/tags/items/quest' / (key + '.json'), {'replace': False, 'values': values})


def item_id(value):
    return value['id'] if isinstance(value, dict) else value


def task_family(task):
    item = task.get('item')
    if not isinstance(item, dict) or item_id(item) != FILTER_ID:
        return None
    return re.fullmatch(r'item_tag\(ashes:quest/([a-z_]+)\)', item['tag'][FILTER_KEY])[1]
