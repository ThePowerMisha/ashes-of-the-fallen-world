"""Collectible fixtures and recoverable supplies, one set per lore site."""

# The first pair are placed blocks. The last pair are possible extra keepsakes
# in the story chest. Every block has its ordinary mod loot table.
SITE_FIXTURES = {
    'silent_hamlet': (('farmersdelight:cabbage_crate', 'supplementaries:sack'), ('farmersdelight:cabbage_seeds', 'minecraft:lantern')),
    'last_stand': (('immersiveengineering:sheetmetal_steel', 'create:industrial_iron_block'), ('immersiveengineering:plate_steel', 'minecraft:spectral_arrow')),
    'nameless_graves': (('botania:chiseled_livingrock_bricks', 'supplementaries:pedestal'), ('botania:white_petal', 'minecraft:soul_lantern')),
    'three_seals_altar': (('ars_nouveau:arcane_pedestal', 'botania:polished_livingrock'), ('ars_nouveau:source_gem', 'botania:livingrock')),
    'broken_watch': (('create:framed_glass', 'supplementaries:globe'), ('create:copper_sheet', 'minecraft:spyglass')),
    'sealed_archive': (('supplementaries:sack', 'create:andesite_casing'), ('create:andesite_alloy', 'immersiveengineering:wire_copper')),
    'fallen_capital': (('create:copper_casing', 'supplementaries:pedestal'), ('create:copper_sheet', 'supplementaries:globe')),
    'mechanists_keep': (('immersiveengineering:craftingtable', 'create:framed_glass'), ('create:shaft', 'create:andesite_alloy')),
    'keepers_keep': (('botania:glimmering_livingwood', 'farmersdelight:onion_crate'), ('botania:manasteel_ingot', 'farmersdelight:onion')),
    'archmages_keep': (('ars_nouveau:arcane_pedestal', 'ars_nouveau:gilded_sourcestone_mosaic'), ('ars_nouveau:source_gem', 'irons_spellbooks:arcane_essence')),
    'limit_lab': (('create:industrial_iron_block', 'immersiveengineering:circuit_table'), ('immersiveengineering:wire_copper', 'mekanism:basic_control_circuit')),
    'infected_hamlet': (('farmersdelight:cabbage_crate', 'supplementaries:sack'), ('farmersdelight:apple_cider', 'minecraft:charcoal')),
    'catacombs': (('botania:mossy_livingrock_bricks', 'supplementaries:pedestal'), ('botania:livingrock', 'minecraft:candle')),
    'surviving_hamlet': (('farmersdelight:stove', 'supplementaries:planter'), ('farmersdelight:cabbage_seeds', 'farmersdelight:onion')),
    'ancient_mine': (('create:andesite_casing', 'immersiveengineering:sheetmetal_iron'), ('create:raw_zinc', 'immersiveengineering:plate_steel')),
    'abyss_temple': (('ars_nouveau:gilded_sourcestone_mosaic', 'botania:polished_livingrock'), ('irons_spellbooks:arcane_essence', 'minecraft:echo_shard')),
    'drowned_city': (('create:copper_casing', 'immersiveengineering:sheetmetal_copper'), ('create:copper_sheet', 'minecraft:nautilus_shell')),
    'observatory': (('create:framed_glass', 'supplementaries:globe'), ('create:copper_sheet', 'minecraft:spyglass')),
}
