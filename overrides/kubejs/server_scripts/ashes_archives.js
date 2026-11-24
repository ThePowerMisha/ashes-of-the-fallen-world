// Additional rewards in vanilla structure chests; never replace existing loot pools.
LootJS.modifiers(event => {
  event.addLootTableModifier('minecraft:chests/simple_dungeon').randomChance(0.35).addLoot('kubejs:archive_fragment')
  event.addLootTableModifier('minecraft:chests/abandoned_mineshaft').randomChance(0.25).addLoot('kubejs:mechanic_dossier')
  event.addLootTableModifier('minecraft:chests/ancient_city').randomChance(0.45).addLoot('kubejs:mage_dossier')
  event.addLootTableModifier('minecraft:chests/stronghold_library').randomChance(0.45).addLoot('kubejs:archive_fragment')
  event.addLootTableModifier('minecraft:chests/jungle_temple').randomChance(0.35).addLoot('kubejs:nature_dossier')
  event.addLootTableModifier('minecraft:chests/pillager_outpost').randomChance(0.30).addLoot('kubejs:scout_report')
})
