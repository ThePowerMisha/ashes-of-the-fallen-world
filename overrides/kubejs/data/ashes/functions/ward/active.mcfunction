scoreboard players add @s award_cd 0
execute if score @s award_cd matches 1.. run scoreboard players remove @s award_cd 1
execute if entity @a[distance=..48] if entity @e[type=#ashes:horde,distance=..32] run function ashes:ward/defend
