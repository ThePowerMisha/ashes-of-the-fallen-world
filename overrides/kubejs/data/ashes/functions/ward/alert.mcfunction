scoreboard players set @s award_cd 30
title @a[distance=..48] actionbar {"text":"⚠ Скверна приближается к рубежу!","color":"red"}
playsound minecraft:block.bell.use player @a[distance=..48] ~ ~ ~ 1 0.7
particle minecraft:soul_fire_flame ~ ~1 ~ 0.6 0.8 0.6 0.04 25 normal @a[distance=..48]
