effect give @a[distance=..24] minecraft:resistance 3 0 true
effect give @e[type=#ashes:residents,distance=..24] minecraft:resistance 3 0 true
effect give @e[type=#ashes:horde,distance=..24] minecraft:weakness 3 0 true
effect give @e[type=#ashes:horde,distance=..24] minecraft:slowness 3 0 true
execute if score @s award_cd matches 0 run function ashes:ward/alert
