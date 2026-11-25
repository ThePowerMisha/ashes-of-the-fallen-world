execute if block ~ ~ ~ minecraft:water run tag @s add ashes_wet
scoreboard players add @s ashes_gap 1
execute if score @s ashes_gap matches ..5 unless entity @s[tag=ashes_pier] positioned ~ ~-1 ~ run function ashes:foundation/probe
execute if score @s ashes_gap matches ..383 if entity @s[tag=ashes_pier] positioned ~ ~-1 ~ run function ashes:foundation/probe
