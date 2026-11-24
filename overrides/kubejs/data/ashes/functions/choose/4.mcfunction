function ashes:remove_modifiers
scoreboard players set @s aclass 4
scoreboard players set @s aapplied 0
scoreboard players set @s acool 600
tellraw @s {"text": "Выбран класс: Следопыт", "color": "gold"}
scoreboard players set @s atalent 0
