scoreboard players enable @s ashes_news
execute if score @s ashes_news matches 1 run tag @s remove ashes_news_muted
execute if score @s ashes_news matches 1 run tellraw @s {"text": "[Хроники] Сообщения хроник включены.", "color": "dark_aqua"}
execute if score @s ashes_news matches 2 run tag @s add ashes_news_muted
execute if score @s ashes_news matches 2 run tellraw @s {"text": "[Хроники] Сообщения хроник отключены. /trigger ashes_news set 1 — включить.", "color": "dark_aqua"}
scoreboard players set @s ashes_news 0
execute if dimension minecraft:overworld if entity @s[tag=!ashes_news_seen,tag=!ashes_news_muted] run function ashes:news/welcome
execute if dimension twilightforest:twilight_forest unless entity @s[tag=ashes_twilight_seen] run function ashes:news/twilight
execute if dimension minecraft:the_nether unless entity @s[tag=ashes_nether_seen] run function ashes:news/nether
execute if dimension minecraft:the_end unless entity @s[tag=ashes_end_seen] run function ashes:news/end
