execute if entity @e[type=minecraft:marker,tag=ashes_ward,distance=..24] run tellraw @s {"text": "Ты внутри радиуса поддержки обелиска.", "color": "aqua"}
execute unless entity @e[type=minecraft:marker,tag=ashes_ward,distance=..24] run tellraw @s {"text": "Поблизости нет активного обелиска.", "color": "aqua"}
