effect give @s minecraft:regeneration 10 0 true
effect give @s minecraft:absorption 25 1 true
scoreboard players set @s akit_cd 30
tellraw @s {"text": "Живое сердце применён. Восстановление припасов 30 секунд.", "color": "gold"}
