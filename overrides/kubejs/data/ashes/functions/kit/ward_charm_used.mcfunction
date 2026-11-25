effect give @s minecraft:absorption 30 0 true
effect give @s minecraft:resistance 12 0 true
scoreboard players set @s akit_cd 30
tellraw @s {"text": "Оберег рубежа применён. Восстановление припасов 30 секунд.", "color": "gold"}
