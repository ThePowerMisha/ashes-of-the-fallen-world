function ashes:remove_modifiers
scoreboard players set @s aclass 1
scoreboard players set @s aapplied 0
scoreboard players set @s acool 600
tellraw @s {"text": "Выбран класс: Паладин", "color": "gold"}
