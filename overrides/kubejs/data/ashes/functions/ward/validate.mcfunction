execute store result score @s award_have run clear @s kubejs:ward_charm 0
execute store result score @s award_count if entity @e[type=minecraft:marker,tag=ashes_ward]
execute if entity @e[type=minecraft:marker,tag=ashes_ward,distance=..32] run tellraw @s {"text": "В пределах 32 блоков уже есть рубеж.", "color": "aqua"}
execute if score @s award_have matches 0 run tellraw @s {"text": "Изготовь оберег рубежа.", "color": "aqua"}
execute if score @s award_count matches 64.. run tellraw @s {"text": "Достигнут предел 64 загруженных обелисков.", "color": "aqua"}
execute unless entity @e[type=minecraft:marker,tag=ashes_ward,distance=..32] if score @s award_have matches 1.. if score @s award_count matches ..63 run function ashes:ward/install
