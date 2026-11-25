scoreboard players add @s akit_cd 0
execute if score @s akit_cd matches 1.. run tellraw @s {"text": "Припасы восстанавливаются. Попробуй через несколько секунд.", "color": "gold"}
execute if score @s akit_cd matches 0 store result score @s akit_used run clear @s kubejs:source_capacitor 1
execute if score @s akit_cd matches 0 if score @s akit_used matches 1 run function ashes:kit/source_capacitor_used
