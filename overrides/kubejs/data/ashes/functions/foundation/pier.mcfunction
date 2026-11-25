execute if block ~ ~ ~ #ashes:foundation_replaceable run setblock ~ ~ ~ minecraft:stone_bricks
scoreboard players remove @s ashes_gap 1
execute if score @s ashes_gap matches 1.. positioned ~ ~-1 ~ run function ashes:foundation/pier
