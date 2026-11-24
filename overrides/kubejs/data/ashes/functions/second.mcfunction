scoreboard players set #seconds acool 0
execute as @a at @s run function ashes:player
execute in minecraft:overworld as @e[type=minecraft:marker,tag=ashes_ward] at @s run function ashes:ward/tick
