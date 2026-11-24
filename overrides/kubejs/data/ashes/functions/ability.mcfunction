execute if score @s aclass matches 1..6 if score @s atalent matches 1..2 if score @s aability_cd matches 0 run function ashes:ability_cast
execute if score @s atalent matches 0 run tellraw @s {"text": "Сначала выбери талант на втором ранге.", "color": "gold"}
