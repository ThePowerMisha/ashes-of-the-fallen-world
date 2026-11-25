scoreboard players set @s ashes_gap 0
tag @s remove ashes_wet
execute unless block ~ ~ ~ #ashes:foundation_replaceable positioned ~ ~-1 ~ run function ashes:foundation/probe
execute if score @s ashes_gap matches 1..5 unless entity @s[tag=ashes_wet] positioned ~ ~-1 ~ run function ashes:foundation/bank
execute if score @s ashes_gap matches 1..5 if entity @s[tag=ashes_wet,tag=ashes_pier] positioned ~ ~-1 ~ run function ashes:foundation/pier
execute if score @s ashes_gap matches 6..383 if entity @s[tag=ashes_pier] positioned ~ ~-1 ~ run function ashes:foundation/pier
scoreboard players reset @s ashes_gap
kill @s
