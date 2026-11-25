execute if score @s aability_cd matches 1.. run tellraw @s {"text": "Талант ещё восстанавливается.", "color": "gold"}
execute if score @s atalent matches 0 run tellraw @s {"text": "Выбери талант класса на ранге II.", "color": "gold"}
execute if score @s aclass matches 1..6 if score @s atalent matches 1..4 if score @s aability_cd matches 0 run function ashes:ability_cast
