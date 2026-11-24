execute store result score @s aclean run clear @s kubejs:purity_sigil 1
execute if score @s aclean matches 0 run tellraw @s {"text": "Нужен знак очищения в инвентаре.", "color": "gold"}
execute if score @s aclean matches 1 run function ashes:purify_success
