tag @s add ashes_news_seen
execute store result score #join_time anews run time query daytime
execute if score #join_time anews matches 0..11999 run tellraw @s {"text":"[Хроники] Сейчас день. Выходи на тракт, пока дорога освещена.","color":"dark_aqua"}
execute if score #join_time anews matches 12000..23999 run tellraw @s {"text":"[Хроники] Сейчас ночь. Веди отряд по освещённой тропе.","color":"gray"}
execute if predicate ashes:news/rain unless predicate ashes:news/thunder run tellraw @s {"text":"[Хроники] Над долиной идёт дождь.","color":"dark_aqua"}
execute if predicate ashes:news/thunder run tellraw @s {"text":"[Хроники] На рубеже гроза.","color":"gold"}
