effect give @s minecraft:saturation 1 1 true
effect give @s minecraft:regeneration 8 0 true
scoreboard players set @s akit_cd 30
tellraw @s {"text": "Полевой комплект применён. Восстановление припасов 30 секунд.", "color": "gold"}
