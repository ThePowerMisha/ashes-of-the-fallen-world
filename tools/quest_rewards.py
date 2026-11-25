"""Supplies for the next activity, matched to the tools available in each route."""
from quest_progress import FAMILIES, family_for

# Rewards are ingredients and consumables. Milestone machines still belong to their tasks.
SUPPLY_PROFILES = {
    'camp': (('torch', 8), ('cooked_beef', 3), ('coal', 4), ('leather', 2),
             ('string', 3), ('iron_nugget', 6), ('stick', 8), ('charcoal', 3)),
    'survey': (('torch', 8), ('cooked_porkchop', 4), ('paper', 6), ('soul_torch', 6),
               ('arrow', 8), ('lead', 1), ('leather', 2), ('compass', 1)),
    'machines': (('iron_ingot', 3), ('copper_ingot', 4), ('redstone', 4), ('glass', 4),
                 ('charcoal', 4), ('quartz', 3), ('iron_nugget', 9), ('gold_nugget', 6)),
    'create': (('iron_ingot', 3), ('andesite', 6), ('create:iron_sheet', 2), ('dried_kelp', 3),
               ('copper_ingot', 3), ('redstone', 4), ('gold_nugget', 6), ('andesite', 4)),
    'mechanical': (('mekanism:dust_coal', 3), ('iron_ingot', 3), ('redstone', 4),
                   ('glass', 4), ('gold_ingot', 2), ('copper_ingot', 3),
                   ('mekanism:dust_osmium', 2), ('charcoal', 4)),
    'magical': (('paper', 5), ('lapis_lazuli', 3), ('amethyst_shard', 2), ('glass_bottle', 4),
                ('book', 1), ('redstone', 3), ('leather', 2), ('glowstone_dust', 2)),
    'garden': (('bone_meal', 5), ('clay_ball', 4), ('glass_bottle', 3), ('brown_mushroom', 3),
               ('charcoal', 4), ('cake', 1), ('shears', 1), ('string', 4)),
    'builders': (('oak_log', 6), ('iron_nugget', 8), ('clay_ball', 6), ('gravel', 6),
                 ('moss_block', 2), ('torch', 8), ('oak_planks', 6), ('iron_ingot', 2)),
    'battle': (('cooked_beef', 4), ('arrow', 12), ('glowstone_dust', 3), ('iron_ingot', 2),
               ('golden_carrot', 3), ('spectral_arrow', 6), ('glass_bottle', 4), ('shield', 1)),
    'horde': (('golden_carrot', 3), ('soul_torch', 8), ('arrow', 10), ('iron_ingot', 3),
              ('cooked_beef', 4), ('glowstone_dust', 3), ('gold_nugget', 6), ('spectral_arrow', 6)),
}
CHAPTER_SUPPLIES = (
    'camp survey create magical builders horde battle battle survey camp battle garden '
    'create mechanical machines machines machines magical magical garden survey battle builders garden '
    'battle magical machines survey builders magical battle horde horde horde survey builders '
    'battle machines camp survey garden builders survey garden machines'
).split()

NEXT_INGREDIENTS = {
    'minecraft:campfire': ('stick', 4),
    'minecraft:white_bed': ('string', 4),
    'minecraft:iron_pickaxe': ('raw_iron', 3),
    'waystones:waystone': ('obsidian', 1),
    'create:shaft': ('andesite', 4),
    'create:cogwheel': ('oak_planks', 2),
    'create:mechanical_press': ('create:andesite_casing', 1),
    'create:mechanical_mixer': ('create:cogwheel', 2),
    'create:brass_funnel': ('dried_kelp', 2),
    'create:track_station': ('create:copper_sheet', 2),
    'mekanism:metallurgic_infuser': ('redstone', 4),
    'mekanism:basic_control_circuit': ('redstone', 3),
    'mekanism:basic_universal_cable': ('redstone', 3),
    'mekanism:energized_smelter': ('glass', 4),
    'ae2:controller': ('ae2:sky_stone_block', 2),
    'ae2:storage_bus': ('iron_ingot', 3),
    'ae2:fluix_crystal': ('quartz', 3),
    'ae2:logic_processor': ('gold_ingot', 2),
    'ae2:calculation_processor': ('ae2:silicon', 2),
    'ae2:engineering_processor': ('ae2:silicon', 2),
    'ars_nouveau:scribes_table': ('gold_nugget', 6),
    'ars_nouveau:source_jar': ('glass', 4),
    'botania:apothecary_default': ('cobblestone', 4),
    'botania:mana_pool': ('stone', 4),
    'botania:endoflame': ('wheat_seeds', 4),
    'farmersdelight:cooking_pot': ('brick', 3),
    'farmersdelight:cutting_board': ('stick', 3),
    'minecraft:composter': ('oak_slab', 3),
    'immersive_aircraft:engine': ('iron_ingot', 3),
    'immersive_aircraft:airship': ('string', 4),
    'kubejs:expedition_seal': ('paper', 4),
}


def namespaced(item):
    return item if ':' in item else f'minecraft:{item}'


def choose_reward(chapter, order, position, rows):
    targets = {row[1] for row in rows}
    for name, item, *_ in rows:
        family = family_for(chapter, name, item)
        if family:
            targets.update(FAMILIES[family][1])
    if position + 1 < len(rows):
        ingredient = NEXT_INGREDIENTS.get(rows[position + 1][1])
        if ingredient and namespaced(ingredient[0]) not in targets:
            return namespaced(ingredient[0]), ingredient[1]
    kind = CHAPTER_SUPPLIES[order]
    options = [(namespaced(item), count) for item, count in SUPPLY_PROFILES[kind]
               if namespaced(item) not in targets]
    assert options, chapter
    return options[(order + position) % len(options)]
