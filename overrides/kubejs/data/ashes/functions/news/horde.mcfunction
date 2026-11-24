execute if score #horde_defeated anews matches 0 if entity @a[advancements={sculkhorde:sculk_horde_defeat=true}] run function ashes:news/horde_defeat
execute if score #horde_started anews matches 0 if score #horde_defeated anews matches 0 if entity @a[advancements={sculkhorde:sculk_horde_start=true}] run function ashes:news/horde_start
