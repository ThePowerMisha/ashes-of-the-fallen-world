scoreboard players set #seconds acool 0
execute as @a at @s run function ashes:player
execute in minecraft:overworld as @e[type=minecraft:marker,tag=ashes_ward] at @s run function ashes:ward/tick
execute in minecraft:overworld if entity @a[distance=0..] run function ashes:news/weather
execute in minecraft:overworld if entity @a[distance=0..] run function ashes:news/time
execute if entity @a run function ashes:news/horde
