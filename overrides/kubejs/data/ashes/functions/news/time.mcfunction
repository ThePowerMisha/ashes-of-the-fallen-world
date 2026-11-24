execute store result score #tod anews run time query daytime
execute store result score #day anews run time query day
scoreboard players set #phase anews 0
execute if score #tod anews matches 12000..23999 run scoreboard players set #phase anews 1
scoreboard players operation #moon anews = #day anews
scoreboard players operation #moon anews %= #eight anews
execute unless score #time_ready anews matches 1 run scoreboard players operation #lastphase anews = #phase anews
scoreboard players set #time_ready anews 1
execute unless score #phase anews = #lastphase anews if score #phase anews matches 0 run tellraw @a[distance=0..,tag=!ashes_news_muted] {"text": "[Хроники] Новый рассвет. В убежищах снова зажигают печи.", "color": "dark_aqua"}
execute unless score #phase anews = #lastphase anews if score #phase anews matches 1 unless score #moon anews matches 0 run tellraw @a[distance=0..,tag=!ashes_news_muted] {"text": "[Хроники] Сумерки опускаются на старые дороги. Возвращайтесь к огням поселений.", "color": "gray"}
execute unless score #phase anews = #lastphase anews if score #phase anews matches 1 if score #moon anews matches 0 run tellraw @a[distance=0..,tag=!ashes_news_muted] {"text": "[Хроники] Полная луна поднялась над руинами. Дозорные заняли свои посты.", "color": "gold"}
scoreboard players operation #lastphase anews = #phase anews
