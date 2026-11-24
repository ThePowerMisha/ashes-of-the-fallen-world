"""Visual Pufferfish mastery tree and clickable vanilla class menu.
The existing scoreboard rank is authoritative; mastery grants at most three small perks.
"""
import json
CLASSES=[
('paladin','Паладин','shield','gold',('Стальной дозор','Щит последней надежды','Несокрушимый'),('generic.armor',0.5,'Броня +0,5'),('generic.knockback_resistance',0.03,'Сопротивление отбрасыванию +3%'),('generic.max_health',1,'Здоровье +1')),
('mage','Архимаг','amethyst_shard','light_purple',('Ученик ордена','Память Селены','Свет над бездной'),('generic.max_health',1,'Здоровье +1'),('generic.movement_speed',0.003,'Скорость +0,003'),('generic.armor',0.5,'Броня +0,5')),
('engineer','Инженер','repeater','aqua',('Механик','Мастер привода','Сердце машины'),('generic.attack_speed',0.05,'Скорость атаки +0,05'),('generic.knockback_resistance',0.03,'Сопротивление отбрасыванию +3%'),('generic.armor',0.5,'Броня +0,5')),
('ranger','Следопыт','compass','green',('Зов дороги','Тихий шаг','Глаз горизонта'),('generic.movement_speed',0.003,'Скорость +0,003'),('generic.attack_speed',0.05,'Скорость атаки +0,05'),('generic.max_health',1,'Здоровье +1')),
('builder','Архитектор','bricks','yellow',('Камень основания','Хранитель очага','Город рассвета'),('generic.knockback_resistance',0.03,'Сопротивление отбрасыванию +3%'),('generic.max_health',1,'Здоровье +1'),('generic.armor',0.5,'Броня +0,5')),
('occultist','Оккультист','echo_shard','dark_purple',('Шёпот тени','Печать тьмы','Власть над страхом'),('generic.attack_damage',0.15,'Урон +0,15'),('generic.max_health',1,'Здоровье +1'),('generic.attack_speed',0.05,'Скорость атаки +0,05'))]
TALENTS=[('Каменная кожа','Щит света'),('Живительный свет','Огненная печать'),('Форсаж','Аварийная броня'),('Стремительный шаг','Глаз ночи'),('Рабочий ритм','Второе дыхание'),('Сила тени','Покров бездны')]

def generate_skills(DATA,F,fn,js,msg):
    base=DATA/'ashes'/'puffish_skills'; cat=base/'categories'/'mastery'
    # v3 of the Pufferfish schema supports grouped normal/exclusive connections.
    js(base/'config.json',{'version':3,'categories':['mastery']})
    js(cat/'category.json',{'title':'Наследие трёх орденов','description':'Три очка мастерства за ранги I–III. Шесть путей; можно сочетать небольшие бонусы, не меняя основной класс.','icon':{'type':'item','data':{'item':'minecraft:enchanted_book'}},'background':'minecraft:textures/block/deepslate.png','unlocked_by_default':True,'starting_points':0,'spent_points_limit':3,'exclusive_root':False})
    defs={}; nodes={}; edges=[]
    # Two rows, three branches each; each branch is a vertical chain of three.
    for i,(key,name,icon,color,titles,*perks) in enumerate(CLASSES):
        x=(i%3-1)*112; y=(i//3)*160-120
        for j,(title,(attr,value,desc)) in enumerate(zip(titles,perks),1):
            n=f'{key}_{j}'
            defs[n]={'title':title,'description':f'{name} · {desc}. Мастерство не заменяет класс.','icon':{'type':'item','data':{'item':'minecraft:'+icon}},'frame':{'type':'advancement','data':{'frame':['task','goal','challenge'][j-1]}},'size':1.0,'cost':1,'rewards':[{'type':'puffish_skills:attribute','data':{'attribute':'minecraft:'+attr,'value':value,'operation':'addition'}}]}
            nodes[n]={'definition':n,'x':x,'y':y+(j-1)*48,'root':j==1}
            if j>1:edges.append([f'{key}_{j-1}',n])
    js(cat/'definitions.json',defs);js(cat/'skills.json',nodes);js(cat/'connections.json',{'normal':{'bidirectional':[],'unidirectional':edges},'exclusive':{'bidirectional':[],'unidirectional':[]}})
    def append(p,lines):
        path=F/(p+'.mcfunction');path.write_text(path.read_text(encoding='utf-8')+'\n'.join(lines)+'\n',encoding='utf-8')
    def tell(parts):return 'tellraw @s '+json.dumps(parts,ensure_ascii=False)
    def button(text,cmd,color,hover):return {'text':text,'color':color,'bold':True,'clickEvent':{'action':'run_command','value':cmd},'hoverEvent':{'action':'show_text','contents':{'text':hover}}}
    append('load',['scoreboard objectives add ashes_menu trigger','scoreboard objectives add ashes_skills trigger','scoreboard objectives add amastery dummy','scoreboard objectives add amastery_ok dummy'])
    append('player',['scoreboard players add @s amastery 0','scoreboard players add @s amastery_ok 0','scoreboard players enable @s ashes_menu','scoreboard players enable @s ashes_skills','execute if score @s ashes_skills matches 1.. run puffish_skills open @s','scoreboard players set @s ashes_skills 0','execute if score @s ashes_menu matches 1.. run function ashes:skills/menu','scoreboard players set @s ashes_menu 0','execute if score @s aclass matches 1..6 if score @s arank > @s amastery run function ashes:skills/grant'])
    # Once per rank across all classes; only advance bookkeeping if command succeeds.
    fn('skills/grant',[*[f'execute if score @s arank matches {i} store success score @s amastery_ok run puffish_skills points set @s ashes:mastery {i} ashes:rank' for i in range(1,4)],'execute if score @s amastery_ok matches 1 run scoreboard players operation @s amastery = @s arank','execute if score @s amastery_ok matches 1 run '+msg('Доступны очки мастерства за ранг. Открой /trigger ashes_skills.')])
    # Failure can otherwise spam command logs each second: retry at most once per 60 seconds.
    append('load',['scoreboard objectives add amastery_retry dummy'])
    p=F/'player.mcfunction';s=p.read_text(encoding='utf-8').replace('execute if score @s aclass matches 1..6 if score @s arank > @s amastery run function ashes:skills/grant','scoreboard players add @s amastery_retry 0\nexecute if score @s amastery_retry matches 1.. run scoreboard players remove @s amastery_retry 1\nexecute if score @s aclass matches 1..6 if score @s arank > @s amastery if score @s amastery_retry matches 0 run function ashes:skills/grant');p.write_text(s,encoding='utf-8')
    append('skills/grant',['scoreboard players set @s amastery_retry 60'])
    menu=[tell([{'text':'◆ Наследие трёх орденов ◆','color':'gold','bold':True}]),tell([{'text':'Текущий класс: ','color':'gray'},{'score':{'name':'@s','objective':'aclass'}},{'text':' | ранг: ','color':'gray'},{'score':{'name':'@s','objective':'arank'}},{'text':' | очков выдано: ','color':'gray'},{'score':{'name':'@s','objective':'amastery'}}])]
    for i,(_,name,_,color,*_) in enumerate(CLASSES,1):
        menu.append(tell([button(f'[{i} {name}]',f'/trigger ashes_class set {i}',color,'Смена класса: 600 секунд онлайн.')]))
        a,b=TALENTS[i-1];menu.append(f'execute if score @s aclass matches {i} run '+tell([{'text':'  Таланты: ','color':'gray'},button(f'[{a}]','/trigger ashes_talent set 1',color,'Ранг II'),{'text':'  '},button(f'[{b}]','/trigger ashes_talent set 2',color,'Ранг III')]))
    menu.append(tell([button('[Применить талант]','/trigger ashes_ability','aqua','Перезарядка 90 секунд'),{'text':'  '},button('[Мой статус]','/trigger ashes_status','yellow','Статистика класса')]))
    menu.append(tell([button('[Дерево мастерства]','/trigger ashes_skills','gold','Открыть визуальное дерево Pufferfish')]))
    fn('skills/menu',menu)
    append('intro',[tell([button('[Открыть меню классов]','/trigger ashes_menu','gold','Выбор класса, таланта, статус')])])
    # Add audible/visible casting feedback; scoped to players near the caster, no global spam.
    append('ability_cast',['particle minecraft:enchant ~ ~1 ~ 0.5 0.8 0.5 0.15 32 normal @a[distance=..24]','playsound minecraft:block.amethyst_block.chime player @a[distance=..16] ~ ~ ~ 0.5 1.1'])
