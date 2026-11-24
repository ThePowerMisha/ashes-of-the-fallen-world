execute if score @s aclass matches 1 if score @s atalent matches 1 run effect give @s minecraft:resistance 12 0 true
execute if score @s aclass matches 1 if score @s atalent matches 2 run effect give @s minecraft:absorption 20 1 true
execute if score @s aclass matches 2 if score @s atalent matches 1 run effect give @s minecraft:regeneration 10 0 true
execute if score @s aclass matches 2 if score @s atalent matches 2 run effect give @s minecraft:fire_resistance 30 0 true
execute if score @s aclass matches 3 if score @s atalent matches 1 run effect give @s minecraft:haste 25 1 true
execute if score @s aclass matches 3 if score @s atalent matches 2 run effect give @s minecraft:resistance 20 0 true
execute if score @s aclass matches 4 if score @s atalent matches 1 run effect give @s minecraft:speed 20 1 true
execute if score @s aclass matches 4 if score @s atalent matches 2 run effect give @s minecraft:night_vision 45 0 true
execute if score @s aclass matches 5 if score @s atalent matches 1 run effect give @s minecraft:haste 20 0 true
execute if score @s aclass matches 5 if score @s atalent matches 2 run effect give @s minecraft:regeneration 12 0 true
execute if score @s aclass matches 6 if score @s atalent matches 1 run effect give @s minecraft:strength 12 0 true
execute if score @s aclass matches 6 if score @s atalent matches 2 run effect give @s minecraft:resistance 16 0 true
scoreboard players set @s aability_cd 90
tellraw @s {"text": "Талант активирован. Перезарядка 90 секунд.", "color": "gold"}
particle minecraft:enchant ~ ~1 ~ 0.5 0.8 0.5 0.15 32 normal @a[distance=..24]
playsound minecraft:block.amethyst_block.chime player @a[distance=..16] ~ ~ ~ 0.5 1.1
