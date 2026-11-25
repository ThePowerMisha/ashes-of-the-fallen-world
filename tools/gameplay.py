from pathlib import Path
import json
from skills import TALENTS

def generate_gameplay(root,K,F,DATA,fn,js,msg):
    # Talent tree: rank-gated alternative abilities; individual cooldown, no damage to others.
    objectives={'ashes_talent':'trigger','ashes_ability':'trigger','ashes_cleanse':'trigger','atalent':'dummy','aability_cd':'dummy','aritus_cd':'dummy','aritus_have':'dummy','aritus_blocks':'dummy','aritus_tmp':'dummy'}
    def append(path,lines):
        p=F/(path+'.mcfunction');p.write_text(p.read_text(encoding='utf-8')+'\n'.join(lines)+'\n',encoding='utf-8')
    append('load',[f'scoreboard objectives add {k} {v}' for k,v in objectives.items()])
    append('load',['execute unless score #configured aclass matches 1 run function ashes:world_defaults'])
    fn('world_defaults',['gamerule playersSleepingPercentage 50','gamerule keepInventory false','gamerule doFireTick false','gamerule mobGriefing true','scoreboard players set #configured aclass 1'])
    append('intro',[msg('Выбирай таланты в меню /trigger ashes_menu. /trigger ashes_ability применяет выбранный талант; /trigger ashes_cleanse собирает образец.')])
    for i in range(1,7):append(f'choose/{i}',['scoreboard players set @s atalent 0'])
    append('status',['tellraw @s '+json.dumps([{'text':'Талант: '},{'score':{'name':'@s','objective':'atalent'}},{'text':' | Перезарядка: '},{'score':{'name':'@s','objective':'aability_cd'}}],ensure_ascii=False)])
    lines=[f'scoreboard players add @s {k} 0' for k,v in objectives.items() if v=='dummy']+[f'scoreboard players enable @s {k}' for k,v in objectives.items() if v=='trigger']
    lines += ['execute if score @s aability_cd matches 1.. run scoreboard players remove @s aability_cd 1',
              'execute if score @s aritus_cd matches 1.. run scoreboard players remove @s aritus_cd 1',
              'execute if score @s ashes_talent matches 1..4 run function ashes:talents/select',
              'scoreboard players set @s ashes_talent 0',
              'execute if score @s ashes_ability matches 1.. run function ashes:ability',
              'scoreboard players set @s ashes_ability 0',
              'execute if score @s ashes_cleanse matches 1.. run function ashes:cleanse',
              'scoreboard players set @s ashes_cleanse 0']
    append('player',lines)
    fn('ability',[
        'execute if score @s aability_cd matches 1.. run '+msg('Талант ещё восстанавливается.'),
        'execute if score @s atalent matches 0 run '+msg('Выбери талант класса на ранге II.'),
        'execute if score @s aclass matches 1..6 if score @s atalent matches 1..4 if score @s aability_cd matches 0 run function ashes:ability_cast',
    ])
    selection, casts = [], []
    for i, options in enumerate(TALENTS,1):
        for slot, (title, _, rank, effects) in enumerate(options,1):
            choose=f'execute if score @s aclass matches {i} if score @s ashes_talent matches {slot}'
            selection += [
                f'{choose} if score @s arank matches {rank}.. run scoreboard players set @s atalent {slot}',
                f'{choose} if score @s arank matches {rank}.. run '+msg('Выбран талант '+title+'.'),
                f'{choose} unless score @s arank matches {rank}.. run '+msg(f'Нужен ранг {rank}.'),
            ]
            casts.extend(f'execute if score @s aclass matches {i} if score @s atalent matches {slot} run effect give @s minecraft:{effect} {duration} {amp} true'
                         for effect,duration,amp in effects)
    fn('talents/select',selection)
    fn('ability_cast',casts+['scoreboard players set @s aability_cd 90',msg('Талант активирован. Перезарядка 90 секунд.')])
    # Sampling ritual: checks vanilla sculk, consumes charge, never writes blocks.
    fn('cleanse',['execute store result score @s aritus_have run clear @s kubejs:cleansing_charge 0','execute if score @s aritus_cd matches 1.. run '+msg('Ритуал перезаряжается.'),'execute if score @s aritus_have matches 0 run '+msg('Нужен заряд очищения.'),'execute if score @s aritus_cd matches 0 if score @s aritus_have matches 1.. run function ashes:cleanse_area'])
    # Never remove catalysts/shriekers/sensors or mod blocks; excludes containers by filter.
    # No block changes; respects claims by not editing terrain.
    fn('cleanse_area',['execute if block ~ ~-1 ~ minecraft:sculk run function ashes:cleanse_block','execute unless block ~ ~-1 ~ minecraft:sculk unless score @s aritus_cd matches 1.. run '+msg('Встань на ванильный скалк вне построек. Штатные блоки орды очищаются модом.')])
    fn('cleanse_block',['clear @s kubejs:cleansing_charge 1','give @s kubejs:purified_sample 1','scoreboard players set @s aritus_cd 60','particle minecraft:happy_villager ~ ~1 ~ 0.4 0.7 0.4 0.1 20 force @s',msg('Образец получен. Для распространения орды применяй штатный очиститель.')])
    # Actual lore drops: Forge global loot modifiers via KubeJS loot table injection is version-sensitive.
    # Vanilla advancement rewards are reliable for the 1.20.1 data format and do not replace third-party loot.
    lore=[('ruins','minecraft:adventure/kill_a_mob','archive_fragment'),('deep','minecraft:adventure/avoid_vibration','mage_dossier'),('nether','minecraft:nether/root','mechanic_dossier'),('nature','minecraft:husbandry/plant_seed','nature_dossier')]
    for key,adv,item in lore:
        js(DATA/'ashes'/'advancements'/'archives'/(key+'.json'),{'criteria':{'witness':{'trigger':'minecraft:tick','conditions':{'player':{'type_specific':{'type':'player','advancements':{adv:True}}}}}},'rewards':{'function':f'ashes:archive/{key}'}})
        fn(f'archive/{key}',[f'give @s kubejs:{item} 1',msg('Восстановлено свидетельство Раскола. Открой архивы квестовой книги.')])
