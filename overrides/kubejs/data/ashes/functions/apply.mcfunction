function ashes:remove_modifiers
execute if score @s aclass matches 1 if score @s arank matches 1 run attribute @s minecraft:generic.armor modifier add 6a5e0000-3c3a-4b00-8000-000000000001 ashes_class 1.0000 add
execute if score @s aclass matches 1 if score @s arank matches 2 run attribute @s minecraft:generic.armor modifier add 6a5e0000-3c3a-4b00-8000-000000000001 ashes_class 2.0000 add
execute if score @s aclass matches 1 if score @s arank matches 3 run attribute @s minecraft:generic.armor modifier add 6a5e0000-3c3a-4b00-8000-000000000001 ashes_class 3.0000 add
execute if score @s aclass matches 2 if score @s arank matches 1 run attribute @s minecraft:generic.max_health modifier add 6a5e0000-3c3a-4b00-8000-000000000002 ashes_class 2.0000 add
execute if score @s aclass matches 2 if score @s arank matches 2 run attribute @s minecraft:generic.max_health modifier add 6a5e0000-3c3a-4b00-8000-000000000002 ashes_class 4.0000 add
execute if score @s aclass matches 2 if score @s arank matches 3 run attribute @s minecraft:generic.max_health modifier add 6a5e0000-3c3a-4b00-8000-000000000002 ashes_class 6.0000 add
execute if score @s aclass matches 3 if score @s arank matches 1 run attribute @s minecraft:generic.attack_speed modifier add 6a5e0000-3c3a-4b00-8000-000000000003 ashes_class 0.1000 add
execute if score @s aclass matches 3 if score @s arank matches 2 run attribute @s minecraft:generic.attack_speed modifier add 6a5e0000-3c3a-4b00-8000-000000000003 ashes_class 0.2000 add
execute if score @s aclass matches 3 if score @s arank matches 3 run attribute @s minecraft:generic.attack_speed modifier add 6a5e0000-3c3a-4b00-8000-000000000003 ashes_class 0.3000 add
execute if score @s aclass matches 4 if score @s arank matches 1 run attribute @s minecraft:generic.movement_speed modifier add 6a5e0000-3c3a-4b00-8000-000000000004 ashes_class 0.0080 add
execute if score @s aclass matches 4 if score @s arank matches 2 run attribute @s minecraft:generic.movement_speed modifier add 6a5e0000-3c3a-4b00-8000-000000000004 ashes_class 0.0160 add
execute if score @s aclass matches 4 if score @s arank matches 3 run attribute @s minecraft:generic.movement_speed modifier add 6a5e0000-3c3a-4b00-8000-000000000004 ashes_class 0.0240 add
execute if score @s aclass matches 5 if score @s arank matches 1 run attribute @s minecraft:generic.knockback_resistance modifier add 6a5e0000-3c3a-4b00-8000-000000000005 ashes_class 0.0400 add
execute if score @s aclass matches 5 if score @s arank matches 2 run attribute @s minecraft:generic.knockback_resistance modifier add 6a5e0000-3c3a-4b00-8000-000000000005 ashes_class 0.0800 add
execute if score @s aclass matches 5 if score @s arank matches 3 run attribute @s minecraft:generic.knockback_resistance modifier add 6a5e0000-3c3a-4b00-8000-000000000005 ashes_class 0.1200 add
execute if score @s aclass matches 6 if score @s arank matches 1 run attribute @s minecraft:generic.attack_damage modifier add 6a5e0000-3c3a-4b00-8000-000000000006 ashes_class 0.5000 add
execute if score @s aclass matches 6 if score @s arank matches 2 run attribute @s minecraft:generic.attack_damage modifier add 6a5e0000-3c3a-4b00-8000-000000000006 ashes_class 1.0000 add
execute if score @s aclass matches 6 if score @s arank matches 3 run attribute @s minecraft:generic.attack_damage modifier add 6a5e0000-3c3a-4b00-8000-000000000006 ashes_class 1.5000 add
scoreboard players operation @s aapplied = @s arank
tellraw @s {"text": "Бонус специализации обновлён.", "color": "gold"}
