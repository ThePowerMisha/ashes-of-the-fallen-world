function ashes:remove_modifiers
scoreboard players set @s aclass 2
scoreboard players set @s aapplied 0
scoreboard players set @s acool 600
tellraw @s {"text": "Выбран класс: Архимаг", "color": "gold"}
scoreboard players set @s atalent 0
