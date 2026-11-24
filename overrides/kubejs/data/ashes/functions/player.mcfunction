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
scoreboard players add @s atalent 0
scoreboard players add @s aability_cd 0
scoreboard players add @s aritus_cd 0
scoreboard players add @s aritus_have 0
scoreboard players add @s aritus_blocks 0
scoreboard players add @s aritus_tmp 0
scoreboard players enable @s ashes_talent
scoreboard players enable @s ashes_ability
scoreboard players enable @s ashes_cleanse
execute if score @s aability_cd matches 1.. run scoreboard players remove @s aability_cd 1
execute if score @s aritus_cd matches 1.. run scoreboard players remove @s aritus_cd 1
execute if score @s ashes_talent matches 1 if score @s arank matches 2.. run scoreboard players set @s atalent 1
execute if score @s ashes_talent matches 2 if score @s arank matches 3.. run scoreboard players set @s atalent 2
execute if score @s ashes_talent matches 1..2 run tellraw @s {"text": "Выбор таланта зависит от ранга. /trigger ashes_status — текущий талант.", "color": "gold"}
scoreboard players set @s ashes_talent 0
execute if score @s ashes_ability matches 1.. run function ashes:ability
scoreboard players set @s ashes_ability 0
execute if score @s ashes_cleanse matches 1.. run function ashes:cleanse
scoreboard players set @s ashes_cleanse 0
scoreboard players add @s amastery 0
scoreboard players add @s amastery_ok 0
scoreboard players enable @s ashes_menu
scoreboard players enable @s ashes_skills
execute if score @s ashes_skills matches 1.. run puffish_skills open @s
scoreboard players set @s ashes_skills 0
execute if score @s ashes_menu matches 1.. run function ashes:skills/menu
scoreboard players set @s ashes_menu 0
scoreboard players add @s amastery_retry 0
execute if score @s amastery_retry matches 1.. run scoreboard players remove @s amastery_retry 1
execute if score @s aclass matches 1..6 if score @s arank > @s amastery if score @s amastery_retry matches 0 run function ashes:skills/grant
scoreboard players enable @s ashes_ward
execute if score @s ashes_ward matches 1 run function ashes:ward/request
execute if score @s ashes_ward matches 2 run function ashes:ward/status
scoreboard players set @s ashes_ward 0
