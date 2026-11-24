execute if block ~ ~-1 ~ minecraft:sculk run function ashes:cleanse_block
execute unless block ~ ~-1 ~ minecraft:sculk unless score @s aritus_cd matches 1.. run tellraw @s {"text": "Встань на ванильный скалк вне построек. Штатные блоки орды очищаются модом.", "color": "gold"}
