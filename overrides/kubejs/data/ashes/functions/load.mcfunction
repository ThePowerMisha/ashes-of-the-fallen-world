scoreboard objectives add ashes_class trigger
scoreboard objectives add ashes_status trigger
scoreboard objectives add ashes_purify trigger
scoreboard objectives add aclass dummy
scoreboard objectives add arank dummy
scoreboard objectives add aapplied dummy
scoreboard objectives add acool dummy
scoreboard objectives add apoints dummy
scoreboard objectives add adeath deathCount
scoreboard objectives add alastdeath dummy
scoreboard objectives add akills minecraft.custom:minecraft.mob_kills
scoreboard objectives add aenchant minecraft.custom:minecraft.enchant_item
scoreboard objectives add amine minecraft.mined:minecraft.stone
scoreboard objectives add awalk minecraft.custom:minecraft.walk_one_cm
scoreboard objectives add abuild minecraft.used:minecraft.stone_bricks
scoreboard objectives add aclean dummy
scoreboard players set #seconds acool 0
scoreboard objectives add ashes_talent trigger
scoreboard objectives add ashes_ability trigger
scoreboard objectives add ashes_cleanse trigger
scoreboard objectives add atalent dummy
scoreboard objectives add aability_cd dummy
scoreboard objectives add aritus_cd dummy
scoreboard objectives add aritus_have dummy
scoreboard objectives add aritus_blocks dummy
scoreboard objectives add aritus_tmp dummy
execute unless score #configured aclass matches 1 run function ashes:world_defaults
scoreboard objectives add ashes_menu trigger
scoreboard objectives add ashes_skills trigger
scoreboard objectives add amastery dummy
scoreboard objectives add amastery_ok dummy
scoreboard objectives add amastery_retry dummy
scoreboard objectives add amastery_v2 dummy
scoreboard objectives add ashes_role trigger
scoreboard objectives add akit_cd dummy
scoreboard objectives add akit_used dummy
scoreboard objectives add ashes_ward trigger
scoreboard objectives add award_have dummy
scoreboard objectives add award_cd dummy
scoreboard objectives add award_count dummy
scoreboard objectives add anews dummy
scoreboard objectives add ashes_news trigger
scoreboard players set #eight anews 8
scoreboard players add #horde_started anews 0
scoreboard players add #horde_defeated anews 0
scoreboard objectives add ashes_gap dummy
