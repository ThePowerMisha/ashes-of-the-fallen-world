execute if score @s arank matches 1 store success score @s amastery_ok run puffish_skills points set @s ashes:mastery 1 ashes:rank
execute if score @s arank matches 2 store success score @s amastery_ok run puffish_skills points set @s ashes:mastery 2 ashes:rank
execute if score @s arank matches 3 store success score @s amastery_ok run puffish_skills points set @s ashes:mastery 3 ashes:rank
execute if score @s amastery_ok matches 1 run scoreboard players operation @s amastery = @s arank
execute if score @s amastery_ok matches 1 run tellraw @s {"text": "Доступны очки мастерства за ранг. Открой /trigger ashes_skills.", "color": "gold"}
scoreboard players set @s amastery_retry 60
