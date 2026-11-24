execute store result score @s aritus_have run clear @s kubejs:cleansing_charge 0
execute if score @s aritus_cd matches 1.. run tellraw @s {"text": "Ритуал перезаряжается.", "color": "gold"}
execute if score @s aritus_have matches 0 run tellraw @s {"text": "Нужен заряд очищения.", "color": "gold"}
execute if score @s aritus_cd matches 0 if score @s aritus_have matches 1.. run function ashes:cleanse_area
