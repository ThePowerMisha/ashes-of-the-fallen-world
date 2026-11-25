"""Visual Pufferfish mastery tree and clickable vanilla class menu.
The existing scoreboard rank is authoritative; mastery grants up to nine spendable points.
"""
import json
CLASSES=[
('paladin','Паладин','shield','gold',('Стальной дозор','Щит последней надежды','Несокрушимый'),('generic.armor',0.5,'Броня +0,5'),('generic.knockback_resistance',0.03,'Сопротивление отбрасыванию +3%'),('generic.max_health',1,'Здоровье +1')),
('mage','Архимаг','amethyst_shard','light_purple',('Ученик ордена','Память Селены','Свет над бездной'),('generic.max_health',1,'Здоровье +1'),('generic.movement_speed',0.003,'Скорость +0,003'),('generic.armor',0.5,'Броня +0,5')),
('engineer','Инженер','repeater','aqua',('Механик','Мастер привода','Сердце машины'),('generic.attack_speed',0.05,'Скорость атаки +0,05'),('generic.knockback_resistance',0.03,'Сопротивление отбрасыванию +3%'),('generic.armor',0.5,'Броня +0,5')),
('ranger','Следопыт','compass','green',('Зов дороги','Тихий шаг','Глаз горизонта'),('generic.movement_speed',0.003,'Скорость +0,003'),('generic.attack_speed',0.05,'Скорость атаки +0,05'),('generic.max_health',1,'Здоровье +1')),
('builder','Архитектор','bricks','yellow',('Камень основания','Хранитель очага','Город рассвета'),('generic.knockback_resistance',0.03,'Сопротивление отбрасыванию +3%'),('generic.max_health',1,'Здоровье +1'),('generic.armor',0.5,'Броня +0,5')),
('occultist','Оккультист','echo_shard','dark_purple',('Шёпот тени','Печать тьмы','Власть над страхом'),('generic.attack_damage',0.15,'Урон +0,15'),('generic.max_health',1,'Здоровье +1'),('generic.attack_speed',0.05,'Скорость атаки +0,05'))]
# Title, compact tooltip, necessary class rank, effect list.
TALENTS = (
    (('Каменная кожа', 'Сопротивление на 12 с', 2, (('resistance',12,0),)),
     ('Щит света', 'Поглощение II на 20 с', 3, (('absorption',20,1),)),
     ('Стойка дозора', 'Неподвижный бастион: сопротивление II и замедление на 7 с', 2, (('resistance',7,1),('slowness',7,0))),
     ('Защитник каравана', 'Поглощение и регенерация', 3, (('absorption',20,0),('regeneration',8,0)))),
    (('Живительный свет', 'Регенерация на 10 с', 2, (('regeneration',10,0),)),
     ('Огненная печать', 'Огнестойкость на 30 с', 3, (('fire_resistance',30,0),)),
     ('Нить эфира', 'Плавное падение и ночное зрение', 2, (('slow_falling',18,0),('night_vision',30,0))),
     ('Сфера Селены', 'Спешка и поглощение', 3, (('haste',24,0),('absorption',25,0)))),
    (('Форсаж', 'Спешка II на 25 с', 2, (('haste',25,1),)),
     ('Аварийная броня', 'Сопротивление на 20 с', 3, (('resistance',20,0),)),
     ('Пожарный контур', 'Огнестойкость на 25 с', 2, (('fire_resistance',25,0),)),
     ('Ударный привод', 'Сила и спешка', 3, (('strength',15,0),('haste',15,1)))),
    (('Стремительный шаг', 'Скорость II на 20 с', 2, (('speed',20,1),)),
     ('Глаз ночи', 'Ночное зрение на 45 с', 3, (('night_vision',45,0),)),
     ('Переправа', 'Подводное дыхание и скорость', 2, (('water_breathing',35,0),('speed',12,0))),
     ('Без следа', 'Невидимость и плавное падение', 3, (('invisibility',16,0),('slow_falling',16,0)))),
    (('Рабочий ритм', 'Спешка на 20 с', 2, (('haste',20,0),)),
     ('Второе дыхание', 'Регенерация на 12 с', 3, (('regeneration',12,0),)),
     ('Монтажный пояс', 'Плавное падение и прыгучесть', 2, (('slow_falling',25,0),('jump_boost',15,0))),
     ('Подмости', 'Сопротивление и спешка', 3, (('resistance',18,0),('haste',30,0)))),
    (('Сила тени', 'Сила на 12 с', 2, (('strength',12,0),)),
     ('Покров бездны', 'Сопротивление на 16 с', 3, (('resistance',16,0),)),
     ('Ночной пакт', 'Невидимость и ночное зрение', 2, (('invisibility',15,0),('night_vision',35,0))),
     ('Цена эха', 'Сила II на 8 с и замедление на 12 с', 3, (('strength',8,1),('slowness',12,0)))),
)

ROLES = (
    ('Защита отряда', 'Броня', 'победы над мобами'),
    ('Магия и поддержка', 'Здоровье', 'зачарования'),
    ('Добыча и механизмы', 'Скорость атаки', 'добыча камня'),
    ('Разведка и дальний бой', 'Скорость передвижения', 'пройденный путь'),
    ('Строительство и выживание', 'Стойкость к отбрасыванию', 'установка каменных кирпичей'),
    ('Магический урон и риск', 'Урон', 'победы над мобами'),
)

# Two specialization routes of three perks branch off from each original root.
# Values are additive. Vanilla fractional knockback is documented as a percent.
BRANCHES = (
    (('Кольчуга дозора','generic.armor',1,'Броня +1'),
     ('Железная выправка','generic.knockback_resistance',.04,'Сопротивление отбрасыванию +4%'),
     ('Закалённый щит','generic.armor_toughness',1,'Твёрдость брони +1'),
     ('Сердце каравана','generic.max_health',2,'Здоровье +2'),
     ('Ответный удар','generic.attack_damage',.5,'Урон +0,5'),
     ('Передовая','generic.armor',1.5,'Броня +1,5')),
    (('Школа Селены','puffish_attributes:magic_damage',.05,'Магический урон +5 процентных пунктов'),
     ('Защитные письмена','puffish_attributes:magic_resistance',.03,'Сопротивление магии +3 процентных пункта'),
     ('Печать заклинателя','puffish_attributes:magic_damage',.07,'Магический урон +7 процентных пунктов'),
     ('Спокойное дыхание','generic.max_health',2,'Здоровье +2'),
     ('Шаг над углями','generic.movement_speed',.004,'Скорость +0,004'),
     ('Второй оберег','generic.armor_toughness',1,'Твёрдость брони +1')),
    (('Точная кирка','puffish_attributes:pickaxe_speed',.08,'Скорость кирки +8 процентных пунктов'),
     ('Свежая оснастка','puffish_attributes:mining_speed',.07,'Скорость добычи +7 процентных пунктов'),
     ('Натяжение привода','puffish_attributes:pickaxe_speed',.10,'Скорость кирки +10 процентных пунктов'),
     ('Стальной фартук','generic.armor',1,'Броня +1'),
     ('Отдача механизма','generic.knockback_resistance',.04,'Сопротивление отбрасыванию +4%'),
     ('Холодный пуск','generic.attack_speed',.12,'Скорость атаки +0,12')),
    (('Дальний дозор','puffish_attributes:ranged_damage',.06,'Дальний урон +6 процентных пунктов'),
     ('Бег по осыпи','generic.movement_speed',.005,'Скорость +0,005'),
     ('Глаз сокола','puffish_attributes:bow_projectile_speed',.08,'Скорость стрелы +8 процентных пунктов'),
     ('Мягкая посадка','puffish_attributes:fall_reduction',.06,'Снижение урона от падения +6 процентных пунктов'),
     ('Лёгкая тропа','generic.movement_speed',.004,'Скорость +0,004'),
     ('Дальний привал','generic.max_health',2,'Здоровье +2')),
    (('Каменная стяжка','generic.knockback_resistance',.04,'Сопротивление отбрасыванию +4%'),
     ('Точный шурф','puffish_attributes:shovel_speed',.10,'Скорость лопаты +10 процентных пунктов'),
     ('Врубка опор','puffish_attributes:axe_speed',.10,'Скорость топора +10 процентных пунктов'),
     ('Надёжные подмости','puffish_attributes:fall_reduction',.08,'Снижение урона от падения +8 процентных пунктов'),
     ('Крепкие руки','generic.max_health',2,'Здоровье +2'),
     ('Хранитель стен','generic.armor',1.25,'Броня +1,25')),
    (('Взыскание долга','puffish_attributes:magic_damage',.05,'Магический урон +5 процентных пунктов'),
     ('Коготь эха','generic.attack_damage',.5,'Урон +0,5'),
     ('Резонанс бездны','puffish_attributes:magic_damage',.08,'Магический урон +8 процентных пунктов'),
     ('Навстречу шёпоту','puffish_attributes:magic_resistance',.04,'Сопротивление магии +4 процентных пункта'),
     ('Шаг за завесу','generic.movement_speed',.004,'Скорость +0,004'),
     ('Теневая выносливость','generic.max_health',2,'Здоровье +2')),
)

POINTS_BY_RANK = (3, 6, 9)

def generate_skills(DATA,F,fn,js,msg):
    base=DATA/'ashes'/'puffish_skills'; cat=base/'categories'/'mastery'
    # v3 of the Pufferfish schema supports grouped normal/exclusive connections.
    js(base/'config.json',{'version':3,'categories':['mastery']})
    js(cat/'category.json',{'title':'Наследие трёх орденов','description':'Шесть путей мастерства. Каждый ранг даёт три очка. Навыки можно сочетать; активные таланты закреплены за классом.','icon':{'type':'item','data':{'item':'minecraft:enchanted_book'}},'background':'minecraft:textures/block/deepslate.png','unlocked_by_default':True,'starting_points':0,'spent_points_limit':max(POINTS_BY_RANK),'exclusive_root':False})
    defs, nodes, edges = {}, {}, []
    for i, (key, name, icon, color, titles, *perks) in enumerate(CLASSES):
        x, y = (i%3-1)*200, (i//3)*225-155
        route = list(zip(titles, perks)) + [(title,(attr,value,desc)) for title,attr,value,desc in BRANCHES[i]]
        for j, (title, (attr,value,desc)) in enumerate(route, 1):
            n = f'{key}_{j}'
            frame = ['task', 'goal', 'challenge'][(j-1)%3]
            attribute = attr if ':' in attr else 'minecraft:'+attr
            defs[n] = {
                'title':title, 'description':f'{name} · {desc}.',
                'icon':{'type':'item','data':{'item':'minecraft:'+icon}},
                'frame':{'type':'advancement','data':{'frame':frame}},'size':1.0,'cost':1,
                'rewards':[{'type':'puffish_skills:attribute','data':{'attribute':attribute,'value':value,'operation':'addition'}}],
            }
            offset = 0 if j<=3 else -60 if j<=6 else 60
            depth = j-1 if j<=3 else (j-1)%3+1
            nodes[n] = {'definition':n,'x':x+offset,'y':y+depth*46,'root':j==1}
            if j>1:
                edges.append([f'{key}_{1 if j in (4,7) else j-1}', n])
    js(cat/'definitions.json',defs);js(cat/'skills.json',nodes);js(cat/'connections.json',{'normal':{'bidirectional':[],'unidirectional':edges},'exclusive':{'bidirectional':[],'unidirectional':[]}})
    def append(p,lines):
        path=F/(p+'.mcfunction');path.write_text(path.read_text(encoding='utf-8')+'\n'.join(lines)+'\n',encoding='utf-8')
    def tell(parts):return 'tellraw @s '+json.dumps(parts,ensure_ascii=False)
    def button(text,cmd,color,hover):return {'text':text,'color':color,'bold':True,'clickEvent':{'action':'run_command','value':cmd},'hoverEvent':{'action':'show_text','contents':{'text':hover}}}
    append('load',['scoreboard objectives add ashes_menu trigger','scoreboard objectives add ashes_skills trigger','scoreboard objectives add amastery dummy','scoreboard objectives add amastery_ok dummy'])
    append('player',['scoreboard players add @s amastery 0','scoreboard players add @s amastery_ok 0','scoreboard players enable @s ashes_menu','scoreboard players enable @s ashes_skills','execute if score @s ashes_skills matches 1.. run puffish_skills open @s','scoreboard players set @s ashes_skills 0','execute if score @s ashes_menu matches 1.. run function ashes:skills/menu','scoreboard players set @s ashes_menu 0','execute if score @s aclass matches 1..6 if score @s arank > @s amastery run function ashes:skills/grant'])
    # Recalculate the same named points source for legacy worlds; unlocked node IDs stay stable.
    fn('skills/grant',[*[f'execute if score @s arank matches {i} store success score @s amastery_ok run puffish_skills points set @s ashes:mastery {points} ashes:rank' for i,points in enumerate(POINTS_BY_RANK,1)],'execute if score @s amastery_ok matches 1 run scoreboard players operation @s amastery = @s arank','execute if score @s amastery_ok matches 1 run scoreboard players set @s amastery_v2 1','execute if score @s amastery_ok matches 1 run '+msg('Доступны очки мастерства за ранг. Открой /trigger ashes_skills.')])
    # Failure can otherwise spam command logs each second: retry at most once per 60 seconds.
    append('load',['scoreboard objectives add amastery_retry dummy','scoreboard objectives add amastery_v2 dummy'])
    path=F/'player.mcfunction'
    old=path.read_text(encoding='utf-8')
    check='execute if score @s aclass matches 1..6 if score @s arank > @s amastery run function ashes:skills/grant'
    scheduled=[
        'scoreboard players add @s amastery_retry 0',
        'execute if score @s amastery_retry matches 1.. run scoreboard players remove @s amastery_retry 1',
        'execute if score @s aclass matches 1..6 if score @s amastery_retry matches 0 unless score @s amastery_v2 matches 1 run function ashes:skills/grant',
        'execute if score @s aclass matches 1..6 if score @s amastery_retry matches 0 if score @s arank > @s amastery run function ashes:skills/grant',
    ]
    assert check in old
    path.write_text(old.replace(check,'\n'.join(scheduled)),encoding='utf-8')
    append('skills/grant',['scoreboard players set @s amastery_retry 60'])
    append('load',['scoreboard objectives add ashes_role trigger'])
    append('player', ['scoreboard players enable @s ashes_role',
                      *[f'execute if score @s ashes_role matches {i} run function ashes:skills/role_{i}' for i in range(1,7)],
                      'scoreboard players set @s ashes_role 0'])
    menu=[
        tell([{'text':'◆ Классы и мастерство','color':'gold','bold':True}]),
        'execute unless score @s aclass matches 1..6 run '+tell([{'text':'Выбери специализацию, чтобы посмотреть её бонусы.','color':'gray'}]),
    ]
    for i, (_,name,_,color,*_) in enumerate(CLASSES,1):
        role, stat, metric = ROLES[i-1]
        summary=[{'text':name+' · ','color':color,'bold':True},{'text':'ранг ','color':'gray'},
                 {'score':{'name':'@s','objective':'arank'}},{'text':' · очки мастерства 3 / 6 / 9','color':'gray'}]
        menu.append(f'execute if score @s aclass matches {i} run '+tell(summary))
        role_page=[tell([{'text':name,'color':color,'bold':True},{'text':' · '+role,'color':'white'}]),
                   tell([{'text':f'Бонус ранга: {stat}. Для повышения: {metric}.','color':'gray'}]),
                   f'execute unless score @s aclass matches {i} run '+tell([
                       button('[Выбрать класс]',f'/trigger ashes_class set {i}',color,'Подтвердить выбор. Смена раз в 10 минут игры.')]),
                   f'execute if score @s aclass matches {i} run '+tell([
                       {'text':'Твой активный класс. Нажми на талант ниже.','color':'gray'}])]
        for slot,(title,desc,rank,_) in enumerate(TALENTS[i-1],1):
            talent_button=button(f'[{title}]',f'/trigger ashes_talent set {slot}',color,desc)
            role_page.extend([
                f'execute if score @s aclass matches {i} if score @s arank matches {rank}.. run '+tell([talent_button,{'text':' '+desc,'color':'gray'}]),
                f'execute unless score @s aclass matches {i} run '+tell([{'text':f'{title} · ранг {rank} · {desc}','color':'gray'}]),
                f'execute if score @s aclass matches {i} unless score @s arank matches {rank}.. run '+tell([
                    {'text':f'{title} · откроется на ранге {rank}','color':'dark_gray'}]),
            ])
        for slot,(title,_,_,_) in enumerate(TALENTS[i-1],1):
            role_page.append(f'execute if score @s aclass matches {i} if score @s atalent matches {slot} run '+tell([
                {'text':'Выбран: '+title,'color':'gold'}]))
        role_page.append(tell([button('[Назад]','/trigger ashes_menu','gold','Вернуться к меню классов'),
                               {'text':'  '},button('[Применить талант]','/trigger ashes_ability','aqua','Перезарядка 90 секунд')]))
        fn(f'skills/role_{i}',role_page)
    for offset in (0,3):
        menu.append(tell([part for idx, (_,name,_,color,*_) in enumerate(CLASSES[offset:offset+3],offset+1)
                          for part in (button(f'[{name}]',f'/trigger ashes_role set {idx}',color,ROLES[idx-1][0]), {'text':'  '})]))
    menu.append(tell([button('[Дерево мастерства]','/trigger ashes_skills','gold','Открыть визуальное дерево'),
                      {'text':'  '},button('[Применить талант]','/trigger ashes_ability','aqua','Перезарядка 90 секунд'),
                      {'text':'  '},button('[Статус]','/trigger ashes_status','yellow','Ранг и время смены класса')]))
    fn('skills/menu',menu)
    append('intro',[tell([button('[Открыть меню классов]','/trigger ashes_menu','gold','Выбор класса, таланта, статус')])])
    # Add audible/visible casting feedback; scoped to players near the caster, no global spam.
    append('ability_cast',['particle minecraft:enchant ~ ~1 ~ 0.5 0.8 0.5 0.15 32 normal @a[distance=..24]','playsound minecraft:block.amethyst_block.chime player @a[distance=..16] ~ ~ ~ 0.5 1.1'])
