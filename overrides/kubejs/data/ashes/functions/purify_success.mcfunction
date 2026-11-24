effect clear @s minecraft:poison
effect clear @s minecraft:wither
effect clear @s minecraft:weakness
effect clear @s minecraft:darkness
effect clear @s minecraft:slowness
effect clear @s minecraft:blindness
effect give @s minecraft:regeneration 5 0 true
particle minecraft:happy_villager ~ ~1 ~ 0.6 0.8 0.6 0.1 20 force @s
tellraw @s {"text": "Знак очищения рассеял скверну с тебя. Для земли используй средства Sculk Horde.", "color": "gold"}
