clear @s kubejs:cleansing_charge 1
give @s kubejs:purified_sample 1
scoreboard players set @s aritus_cd 60
particle minecraft:happy_villager ~ ~1 ~ 0.4 0.7 0.4 0.1 20 force @s
tellraw @s {"text": "Образец получен. Для распространения орды применяй штатный очиститель.", "color": "gold"}
