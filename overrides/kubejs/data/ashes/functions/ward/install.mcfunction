summon minecraft:marker ~ ~ ~ {Tags:["ashes_ward"]}
clear @s kubejs:ward_charm 1
advancement grant @s only ashes:ward/registered
particle minecraft:happy_villager ~ ~1 ~ 0.7 0.8 0.7 0.1 40 normal @a[distance=..24]
playsound minecraft:block.beacon.activate player @a[distance=..24] ~ ~ ~ 0.8 1
tellraw @s {"text": "Рубеж активен. Радиус поддержки 24 блока. Для земли возведи штатный защитный контур.", "color": "aqua"}
