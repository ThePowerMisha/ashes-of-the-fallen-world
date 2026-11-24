scoreboard players set @s arank 1
execute if score @s aclass matches 1 run scoreboard players operation @s apoints = @s akills
execute if score @s aclass matches 1 if score @s apoints matches 50.. run scoreboard players set @s arank 2
execute if score @s aclass matches 1 if score @s apoints matches 200.. run scoreboard players set @s arank 3
execute if score @s aclass matches 2 run scoreboard players operation @s apoints = @s aenchant
execute if score @s aclass matches 2 if score @s apoints matches 10.. run scoreboard players set @s arank 2
execute if score @s aclass matches 2 if score @s apoints matches 30.. run scoreboard players set @s arank 3
execute if score @s aclass matches 3 run scoreboard players operation @s apoints = @s amine
execute if score @s aclass matches 3 if score @s apoints matches 500.. run scoreboard players set @s arank 2
execute if score @s aclass matches 3 if score @s apoints matches 2000.. run scoreboard players set @s arank 3
execute if score @s aclass matches 4 run scoreboard players operation @s apoints = @s awalk
execute if score @s aclass matches 4 if score @s apoints matches 100000.. run scoreboard players set @s arank 2
execute if score @s aclass matches 4 if score @s apoints matches 500000.. run scoreboard players set @s arank 3
execute if score @s aclass matches 5 run scoreboard players operation @s apoints = @s abuild
execute if score @s aclass matches 5 if score @s apoints matches 100.. run scoreboard players set @s arank 2
execute if score @s aclass matches 5 if score @s apoints matches 400.. run scoreboard players set @s arank 3
execute if score @s aclass matches 6 run scoreboard players operation @s apoints = @s akills
execute if score @s aclass matches 6 if score @s apoints matches 50.. run scoreboard players set @s arank 2
execute if score @s aclass matches 6 if score @s apoints matches 200.. run scoreboard players set @s arank 3
execute unless score @s adeath = @s alastdeath run scoreboard players set @s aapplied 0
scoreboard players operation @s alastdeath = @s adeath
execute unless score @s arank = @s aapplied run function ashes:apply
