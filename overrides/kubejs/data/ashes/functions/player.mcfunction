scoreboard players add @s aclass 0
scoreboard players add @s arank 0
scoreboard players add @s aapplied 0
scoreboard players add @s acool 0
scoreboard players add @s apoints 0
scoreboard players add @s adeath 0
scoreboard players add @s alastdeath 0
scoreboard players add @s akills 0
scoreboard players add @s aenchant 0
scoreboard players add @s amine 0
scoreboard players add @s awalk 0
scoreboard players add @s abuild 0
scoreboard players add @s aclean 0
scoreboard players enable @s ashes_class
scoreboard players enable @s ashes_status
scoreboard players enable @s ashes_purify
execute if score @s acool matches 1.. run scoreboard players remove @s acool 1
execute unless entity @s[tag=ashes_intro] run function ashes:intro
execute if score @s ashes_class matches 1..6 if score @s acool matches 1.. run tellraw @s {"text": "Смена класса пока недоступна. /trigger ashes_status покажет прогресс.", "color": "gold"}
execute if score @s ashes_class matches 1 if score @s acool matches 0 run function ashes:choose/1
execute if score @s ashes_class matches 2 if score @s acool matches 0 run function ashes:choose/2
execute if score @s ashes_class matches 3 if score @s acool matches 0 run function ashes:choose/3
execute if score @s ashes_class matches 4 if score @s acool matches 0 run function ashes:choose/4
execute if score @s ashes_class matches 5 if score @s acool matches 0 run function ashes:choose/5
execute if score @s ashes_class matches 6 if score @s acool matches 0 run function ashes:choose/6
scoreboard players set @s ashes_class 0
execute if score @s aclass matches 1..6 run function ashes:rank
execute if score @s ashes_status matches 1.. run function ashes:status
scoreboard players set @s ashes_status 0
execute if score @s ashes_purify matches 1.. run function ashes:purify
scoreboard players set @s ashes_purify 0
