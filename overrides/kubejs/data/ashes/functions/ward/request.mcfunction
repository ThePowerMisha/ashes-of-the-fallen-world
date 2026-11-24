execute unless dimension minecraft:overworld run tellraw @s {"text": "Обелиски работают только в обычном мире.", "color": "aqua"}
execute if dimension minecraft:overworld unless block ~ ~-1 ~ minecraft:lodestone run tellraw @s {"text": "Встань на магнетит. Нужен один оберег рубежа.", "color": "aqua"}
execute if dimension minecraft:overworld if block ~ ~-1 ~ minecraft:lodestone align xyz positioned ~0.5 ~-1 ~0.5 run function ashes:ward/validate
