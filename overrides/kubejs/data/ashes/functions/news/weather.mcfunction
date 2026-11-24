scoreboard players set #weather anews 0
execute if predicate ashes:news/rain run scoreboard players set #weather anews 1
execute if predicate ashes:news/thunder run scoreboard players set #weather anews 2
execute unless score #weather_ready anews matches 1 run scoreboard players operation #lastweather anews = #weather anews
scoreboard players set #weather_ready anews 1
execute unless score #weather anews = #lastweather anews if score #weather anews matches 0 run tellraw @a[distance=0..,tag=!ashes_news_muted] {"text": "[Хроники] Небо прояснилось. Путники могут продолжить путь.", "color": "dark_aqua"}
execute unless score #weather anews = #lastweather anews if score #weather anews matches 1 run tellraw @a[distance=0..,tag=!ashes_news_muted] {"text": "[Хроники] Над долинами идёт дождь. Укройте припасы и приготовьте факелы.", "color": "dark_aqua"}
execute unless score #weather anews = #lastweather anews if score #weather anews matches 2 run tellraw @a[distance=0..,tag=!ashes_news_muted] {"text": "[Хроники] Гроза над рубежом. Вдали гремят раскаты; лучше переждать бурю под крышей.", "color": "gold"}
scoreboard players operation #lastweather anews = #weather anews
