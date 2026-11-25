from pathlib import Path
import json, hashlib, zipfile, csv
from extension import EXTRA_ITEMS, EXTRA_RECIPES
from quest_content import decorate_quest
from quest_coverage import write_coverage
from quest_progress import bind_alternatives, links_for, tag_files, task_family
from artifacts import ARTIFACT_RECIPES, generate_artifacts, usage_tooltips
ROOT=Path(__file__).resolve().parents[1]; O=ROOT/'overrides'; K=O/'kubejs'; DATA=K/'data'; F=DATA/'ashes'/'functions'; Q=O/'config'/'ftbquests'/'quests'/'chapters'
def put(p,s):
 p.parent.mkdir(parents=True,exist_ok=True); p.write_text(s,encoding='utf-8')
def js(p,x): put(p,json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def fn(name,lines): put(F/(name+'.mcfunction'),'\n'.join(lines)+'\n')
def msg(s): return 'tellraw @s '+json.dumps({'text':s,'color':'gold'},ensure_ascii=False)
items={
 'archive_fragment':('Обломок архива','paper'), 'mechanic_seal':('Печать механиков','iron_ingot'), 'nature_seal':('Печать хранителей','emerald'), 'mage_seal':('Печать архимагов','amethyst_shard'), 'concord_core':('Ядро согласия','echo_shard'), 'purity_sigil':('Знак очищения','prismarine_crystals'), 'renewal_heart':('Сердце возрождения','nether_star'), 'mechanic_dossier':('Досье: Последний пуск','book'), 'nature_dossier':('Досье: Корни тишины','book'), 'mage_dossier':('Досье: Голос под камнем','book'), 'expedition_seal':('Печать экспедиции','compass'), 'purifier_matrix':('Матрица очищения','prismarine_shard'), 'settlement_charter':('Хартия поселения','paper'), 'memory_lens':('Линза памяти','spyglass')}
items.update(EXTRA_ITEMS)
put(K/'startup_scripts'/'ashes_items.js', 'StartupEvents.registry(\'item\', event => {\n'+''.join(f"  event.create('{i}').displayName('{n}').texture('kubejs:item/{i}')\n" for i,(n,t) in items.items())+'})\n')
recipes={
 'archive_fragment': ['minecraft:paper','minecraft:ink_sac','minecraft:charcoal'],
 'mechanic_seal':['kubejs:archive_fragment','create:precision_mechanism','mekanism:basic_control_circuit'],
 'nature_seal':['kubejs:archive_fragment','minecraft:glow_berries','minecraft:emerald','minecraft:honeycomb'],
 'mage_seal':['kubejs:archive_fragment','ars_nouveau:source_gem','minecraft:amethyst_shard'],
 'concord_core':['kubejs:mechanic_seal','kubejs:nature_seal','kubejs:mage_seal','minecraft:echo_shard'],
 'purity_sigil':['kubejs:concord_core','minecraft:glowstone_dust','minecraft:gold_ingot'],
 'renewal_heart':['kubejs:concord_core','minecraft:nether_star','minecraft:dragon_breath','minecraft:totem_of_undying']}
# Core is a reusable catalyst for sigils: use an alternate cheap formula after researching the three orders, without consuming the core.
recipes['purity_sigil']=['minecraft:amethyst_shard','minecraft:glowstone_dust','minecraft:gold_ingot','minecraft:honeycomb']
recipes.update({
 'mechanic_dossier':['minecraft:book','kubejs:archive_fragment','minecraft:redstone','minecraft:copper_ingot'],
 'nature_dossier':['minecraft:book','kubejs:archive_fragment','minecraft:glow_berries','minecraft:oak_sapling'],
 'mage_dossier':['minecraft:book','kubejs:archive_fragment','ars_nouveau:source_gem','minecraft:amethyst_shard'],
 'expedition_seal':['minecraft:compass','minecraft:leather','minecraft:iron_ingot','kubejs:archive_fragment'],
 'purifier_matrix':['kubejs:purity_sigil','minecraft:prismarine_crystals','minecraft:gold_ingot','minecraft:amethyst_shard'],
 'settlement_charter':['minecraft:paper','minecraft:ink_sac','minecraft:emerald','kubejs:archive_fragment'],
 'memory_lens':['minecraft:spyglass','minecraft:echo_shard','minecraft:amethyst_shard']})
recipes.update(EXTRA_RECIPES)
artifact_recipes = ''.join(f"  event.shapeless('{out}', {json.dumps(ingredients)}).id('ashes:{key}')\n"
                           for key,(out,ingredients) in ARTIFACT_RECIPES.items())
put(K/'server_scripts'/'ashes_recipes.js',"ServerEvents.recipes(event => {\n"+''.join(f"  event.shapeless('{ '4x ' if i=='purity_sigil' else ''}kubejs:{i}', {json.dumps(v)}).id('ashes:{i}')\n" for i,v in recipes.items())+artifact_recipes+"""
  event.shapeless('4x minecraft:golden_carrot', ['minecraft:gold_ingot','minecraft:carrot','minecraft:carrot','minecraft:carrot','minecraft:carrot']).id('ashes:field_rations')
  event.shapeless('2x minecraft:lantern', ['minecraft:iron_ingot','minecraft:torch','minecraft:torch']).id('ashes:recovery_lanterns')
  event.shapeless('2x kubejs:purity_sigil', ['kubejs:purifier_matrix','minecraft:glowstone_dust']).id('ashes:matrix_recovery')
})
""")
# Localized lore tooltips: purely visual, no game state or server privileges.
flavor = {'mechanic_dossier': 'Последний пуск. Главный инженер Варден признал, что сигнал пришёл снизу раньше включения машин.', 'nature_dossier': 'Корни тишины. Хранительница Ильма велела эвакуировать деревни, но совет запретил поднимать тревогу.', 'mage_dossier': 'Голос под камнем. Архимаг Селена услышала собственный голос из глубин; источник подражал живым.', 'expedition_seal': 'Памятный знак экспедиции. Не открывает сооружения и не телепортирует.', 'purifier_matrix': 'Компонент повторной переработки знаков. Не очищает блоки самостоятельно.', 'settlement_charter': 'Символ союза выживших. Ратуша MineColonies строится отдельно.', 'memory_lens': 'Реликвия архивистов. Не заменяет подзорную трубу.', 'renewal_heart': 'Память о трёх орденах. Символ победы, а не автоматический триггер поражения орды.'}
for item, usage in usage_tooltips().items():
 flavor[item] = (flavor[item]+' ' if item in flavor else '') + usage
put(K/'client_scripts'/'ashes_lore.js', "ItemEvents.tooltip(event => {\n"+''.join(f"  event.add('kubejs:{i}', {json.dumps(v,ensure_ascii=False)})\n" for i,v in flavor.items())+"})\n")
# Individual classes, using Minecraft scoreboards and modifiers. No client scripts or mod-specific attribute guesses.
classes=[('Паладин','akills','minecraft:generic.armor',1.0),('Архимаг','aenchant','minecraft:generic.max_health',2.0),('Инженер','amine','minecraft:generic.attack_speed',.10),('Следопыт','awalk','minecraft:generic.movement_speed',.008),('Архитектор','abuild','minecraft:generic.knockback_resistance',.04),('Оккультист','akills','minecraft:generic.attack_damage',.5)]
criteria={'ashes_class':'trigger','ashes_status':'trigger','ashes_purify':'trigger','aclass':'dummy','arank':'dummy','aapplied':'dummy','acool':'dummy','apoints':'dummy','adeath':'deathCount','alastdeath':'dummy','akills':'minecraft.custom:minecraft.mob_kills','aenchant':'minecraft.custom:minecraft.enchant_item','amine':'minecraft.mined:minecraft.stone','awalk':'minecraft.custom:minecraft.walk_one_cm','abuild':'minecraft.used:minecraft.stone_bricks','aclean':'dummy'}
js(DATA/'minecraft'/'tags'/'functions'/'load.json',{'values':['ashes:load']}); js(DATA/'minecraft'/'tags'/'functions'/'tick.json',{'values':['ashes:tick']})
fn('load',[f'scoreboard objectives add {k} {v}' for k,v in criteria.items()]+['scoreboard players set #seconds acool 0'])
fn('tick',['scoreboard players add #seconds acool 1','execute if score #seconds acool matches 20.. run function ashes:second'])
fn('second',['scoreboard players set #seconds acool 0','execute as @a at @s run function ashes:player'])
fn('player',[f'scoreboard players add @s {k} 0' for k in criteria if k not in ['ashes_class','ashes_status','ashes_purify']]+['scoreboard players enable @s ashes_class','scoreboard players enable @s ashes_status','scoreboard players enable @s ashes_purify','execute if score @s acool matches 1.. run scoreboard players remove @s acool 1','execute unless entity @s[tag=ashes_intro] run function ashes:intro','execute if score @s ashes_class matches 1..6 if score @s acool matches 1.. run '+msg('Смена класса пока недоступна. /trigger ashes_status покажет прогресс.')]+[f'execute if score @s ashes_class matches {i} if score @s acool matches 0 run function ashes:choose/{i}' for i in range(1,7)]+['scoreboard players set @s ashes_class 0','execute if score @s aclass matches 1..6 run function ashes:rank','execute if score @s ashes_status matches 1.. run function ashes:status','scoreboard players set @s ashes_status 0','execute if score @s ashes_purify matches 1.. run function ashes:purify','scoreboard players set @s ashes_purify 0'])
fn('intro',['tag @s add ashes_intro',msg('Пепел ушедшего мира. Выбери специализацию: /trigger ashes_class set 1–6'),msg('1 Паладин | 2 Архимаг | 3 Инженер | 4 Следопыт | 5 Архитектор | 6 Оккультист'),msg('Открой книгу FTB Quests. /trigger ashes_status — прогресс; /trigger ashes_purify — знак очищения.')])
for i,(name,metric,attr,amount) in enumerate(classes,1):
 fn(f'choose/{i}',['function ashes:remove_modifiers',f'scoreboard players set @s aclass {i}','scoreboard players set @s aapplied 0','scoreboard players set @s acool 600',msg('Выбран класс: '+name)])
# all six modifiers have stable UUIDs; removal may fail silently when absent (normal).
uids=[f'6a5e0000-3c3a-4b00-8000-{i:012x}' for i in range(1,7)]
fn('remove_modifiers',[f'attribute @s {c[2]} modifier remove {u}' for c,u in zip(classes,uids)])
thresholds=[(50,200),(10,30),(500,2000),(100000,500000),(100,400),(50,200)]
rank=['scoreboard players set @s arank 1']
for i,((name,metric,attr,amount),(a,b)) in enumerate(zip(classes,thresholds),1):
 rank.extend([f'execute if score @s aclass matches {i} run scoreboard players operation @s apoints = @s {metric}',f'execute if score @s aclass matches {i} if score @s apoints matches {a}.. run scoreboard players set @s arank 2',f'execute if score @s aclass matches {i} if score @s apoints matches {b}.. run scoreboard players set @s arank 3'])
rank.extend(['execute unless score @s adeath = @s alastdeath run scoreboard players set @s aapplied 0','scoreboard players operation @s alastdeath = @s adeath','execute unless score @s arank = @s aapplied run function ashes:apply'])
fn('rank',rank)
apply=['function ashes:remove_modifiers']
for i,((name,metric,attr,amount),u) in enumerate(zip(classes,uids),1):
 for l in range(1,4): apply.append(f'execute if score @s aclass matches {i} if score @s arank matches {l} run attribute @s {attr} modifier add {u} ashes_class {amount*l:.4f} add')
apply+=['scoreboard players operation @s aapplied = @s arank',msg('Бонус специализации обновлён.')]; fn('apply',apply)
fn('status',[msg('1 Паладин | 2 Архимаг | 3 Инженер | 4 Следопыт | 5 Архитектор | 6 Оккультист'), 'tellraw @s '+json.dumps([{'text':'Класс: '},{'score':{'name':'@s','objective':'aclass'}},{'text':' | Ранг: '},{'score':{'name':'@s','objective':'arank'}},{'text':' | Прогресс: '},{'score':{'name':'@s','objective':'apoints'}},{'text':' | Смена через (сек): '},{'score':{'name':'@s','objective':'acool'}}],ensure_ascii=False)])
fn('purify',['execute store result score @s aclean run clear @s kubejs:purity_sigil 1','execute if score @s aclean matches 0 run '+msg('Нужен знак очищения в инвентаре.'),'execute if score @s aclean matches 1 run function ashes:purify_success'])
fn('purify_success',[f'effect clear @s minecraft:{e}' for e in ['poison','wither','weakness','darkness','slowness','blindness']]+['effect give @s minecraft:regeneration 5 0 true','particle minecraft:happy_villager ~ ~1 ~ 0.6 0.8 0.6 0.1 20 force @s',msg('Знак очищения рассеял скверну с тебя. Для земли используй средства Sculk Horde.')])
# FTB quests source is data-driven. Each entry: title, item or None (explicit self-confirmation), count, description.
chapters=[
('01_survival','I. Последние выжившие','minecraft:campfire',[
('Пробуждение',None,1,'Ты очнулся среди руин. Мир помнит Великий Раскол. Открой карту и договорись с друзьями о месте встречи.'),('Огонь в ночи','minecraft:campfire',1,'Разожги костёр. Ночь опаснее, чем кажется.'),('Первое убежище','minecraft:white_bed',1,'Подготовь кровать и укрытие.'),('Камень и сталь','minecraft:iron_pickaxe',1,'Добудь железо и изготовь кирку. Ultimine ускоряет добычу.'),('Запасы','minecraft:bread',8,'Обеспечь команду едой.'),('Дорога домой','waystones:waystone',1,'Построй путевой камень; активируй его в общем поселении.'),('Выбрать путь',None,1,'Выбери класс командой /trigger ashes_class set 1–6. Используй /trigger ashes_status для проверки. Подтверди после выбора.'),('Следы истории','kubejs:archive_fragment',1,'Соедини бумагу, чернила и древесный уголь. Восстанови первые записи орденов.')]),
('02_ruins','II. Эхо старого мира','minecraft:spyglass',[
('На север от пепла','minecraft:spyglass',1,'Возьми подзорную трубу. Ищи руины в долинах.'),('Заброшенный замок',None,1,'Исследуй крупную крепость When Dungeons Arise. Установи точку на карте и сообщи друзьям.'),('Голоса под землёй',None,1,'Исследуй заброшенную шахту YUNG’s и найди следы нежити.'),('Хранилища старого мира','minecraft:gold_ingot',8,'Принеси золото из экспедиции или шахты.'),('Крипта',None,1,'Посети кладбище или склеп The Graveyard. Подтверди возвращение живым.'),('Архив механиков','minecraft:redstone',16,'Красная пыль была кровью машин.'),('Архив хранителей','minecraft:emerald',4,'Изумруд напоминает о союзе поселений.'),('Архив архимагов','minecraft:amethyst_shard',8,'Кристалл помнит голос бездны.'),('Три ордена','kubejs:archive_fragment',3,'Восстанови записи всех трёх орденов. Раскол произошёл по вине их общего эксперимента.')]),
('03_industry','III-A. Возрождение промышленности','create:precision_mechanism',[
('Колесо','create:water_wheel',1,'Поставь водяное колесо и передай вращение валом.'),('Валы','create:shaft',8,'Проложи привод к рабочему месту.'),('Пресс','create:mechanical_press',1,'Автоматизируй изготовление пластин.'),('Дробление','create:millstone',1,'Используй жернова для переработки ресурсов.'),('Бур','create:mechanical_drill',1,'Построй механический бур. Следи за нагрузкой.'),('Точная механика','create:precision_mechanism',1,'Освой последовательную сборку.'),('Первые провода',None,1,'Создай генератор и сеть Immersive Engineering. Подтверди после проверки.'),('Энергия','mekanismgenerators:heat_generator',1,'Построй генератор Mekanism и подай энергию.'),('Обогащение','mekanism:enrichment_chamber',1,'Перерабатывай руды с меньшими потерями.'),('Промышленная логика','mekanism:basic_control_circuit',4,'Освой управляющие схемы.'),('Добыча без шахтёра','mekanism:digital_miner',1,'Настрой фильтр Digital Miner и питание. Не размещай в чужих территориях.'),('Знак механиков','kubejs:mechanic_seal',1,'Объедини запись, точный механизм и управляющую схему.')]),
('04_magic','III-B. Искусство трёх орденов','minecraft:amethyst_shard',[
('Искра','ars_nouveau:source_gem',1,'Найди источник магии и добудь Source Gem.'),('Первые чары',None,1,'Изготовь книгу Ars Nouveau и испытай простое заклинание.'),('Боевая магия',None,1,'Изучи Iron’s Spells и примени первое боевое заклинание.'),('Защита','minecraft:shield',1,'Не забывай о щите и защите союзников.'),('Природный дар','minecraft:glow_berries',8,'Собери ягоды и исследуй живые пещеры.'),('Мана',None,1,'Настрой генерацию маны в Botania.'),('Тёмные искусства',None,1,'Изучи Goety. Вызывай слуг вдали от союзного поселения.'),('Алхимия','minecraft:brewing_stand',1,'Свари зелья перед экспедицией.'),('Печать природы','kubejs:nature_seal',1,'Соедини запись с дарами живого мира.'),('Печать магов','kubejs:mage_seal',1,'Соедини запись с кристаллами и Source Gem.')]),
('05_colony','III-C. Новая цивилизация','minecraft:lantern',[
('Место для дома','minecraft:lantern',8,'Выбери долину рядом с водой. Освети стартовую зону.'),('Команда',None,1,'Создай команду FTB Teams и согласуй доступ к чанкам.'),('Первый город',None,1,'Поставь Supply Camp MineColonies и основную ратушу.'),('Строитель',None,1,'Найми строителя и дострой его хижину.'),('Ферма','minecraft:wheat',32,'Обеспечь город зерном.'),('Кухня',None,1,'Освой Farmer’s Delight и готовь еду для экспедиций.'),('Дороги','minecraft:stone_bricks',64,'Соедини здания дорогами. Архитектор получает прогресс за установку каменных кирпичей.'),('Склад','minecraft:chest',16,'Организуй общий склад. Используй Sophisticated Storage.'),('Цифровое сердце','ae2:controller',1,'Построй ME-сеть и настрой её питание.'),('Безопасные стены',None,1,'Построй защиту, резервный склад и точку эвакуации.')]),
('06_horde','IV. Пробуждение бездны','minecraft:echo_shard',[
('Совет орденов','kubejs:concord_core',1,'Соедини три печати и осколок эха. Согласуй с друзьями экспедицию к источнику скверны.'),('Знак очищения','kubejs:purity_sigil',4,'Изготовь знаки. /trigger ashes_purify тратит один знак и снимает вредные эффекты с тебя.'),('Спящие глубины','minecraft:echo_shard',1,'Найди древний город. Не пробуждай орду до готовности команды.'),('План обороны',None,1,'Сделай резервную копию мира и подготовь убежища. Администратор проверяет настройки Sculk Horde.'),('Пробуждение',None,1,'Вместе активируйте орду штатной механикой Sculk Horde. Не подтверждай до фактической активации.'),('Противоядие',None,1,'Освой штатные средства очищения Sculk Horde по внутриигровым рецептам JEI.'),('Первая очищенная зона',None,1,'Уничтожь очаг и очисти заражённые блоки штатным очистителем. Подтверди после осмотра зоны.'),('Второй рубеж',None,1,'Освободи ещё один очаг, поставь точку на карте.'),('Подготовка войны','minecraft:golden_apple',4,'Снабди бойцов и обеспечь пути отступления.')]),
('07_war','V. Война за будущее','minecraft:netherite_ingot',[
('Кузница','minecraft:diamond_chestplate',1,'Обнови броню команды.'),('Сила реликвий',None,1,'Найди артефакт Artifacts и экипируй его.'),('Кузнец судьбы',None,1,'Улучши экипировку через Apotheosis.'),('Первый хранитель',None,1,'Победи босса Mowzie’s Mobs вместе с командой.'),('Хранитель катакомб',None,1,'Победи босса Cataclysm. Не подтверждай до победы.'),('Врата преисподней','minecraft:blaze_rod',8,'Заготовь ресурсы Нижнего мира.'),('Вершина стали','minecraft:netherite_ingot',1,'Подготовь снаряжение к последнему походу.'),('Падение древнего владыки','minecraft:nether_star',1,'Победи иссушителя и получи звезду.')]),
('08_final','VI–VII. Сердце тьмы и новая эпоха','kubejs:renewal_heart',[
('Дыхание края','minecraft:dragon_breath',1,'Отправляйся в Край и собери дыхание дракона.'),('Последний бастион','minecraft:totem_of_undying',1,'Подготовь тотем для финальной экспедиции.'),('Сердце тьмы',None,1,'Заверши штатную финальную механику Sculk Horde. Подтверди только после фактического поражения орды.'),('Возрождение','kubejs:renewal_heart',1,'Создай Сердце возрождения из ядра согласия, звезды, дыхания дракона и тотема.'),('Возвращение жизни',None,1,'Очисти оставшиеся ключевые территории, восстанови поселение.'),('Новая эпоха','minecraft:beacon',1,'Зажги маяк новой цивилизации. Мир принадлежит выжившим.')])]
chapters += [('09_archives', 'Архивы Раскола', 'minecraft:writable_book', [('Обет архивиста', 'kubejs:archive_fragment', 1, 'Я, Варден, оставляю этот протокол тому, кто найдёт его. Если сигнальный колокол прозвучит трижды, не запускайте установку.'), ('Последний пуск', 'kubejs:mechanic_dossier', 1, 'Запись 01. Механики построили проводники, чтобы освещать города и питать фабрики. В ночь запуска счётчики начали работать до подачи энергии.'), ('Корни тишины', 'kubejs:nature_dossier', 1, 'Запись 02. Ильма обнаружила, что растения поворачиваются к шахте, даже когда солнце светит с другой стороны. Совет счёл тревогу суеверием.'), ('Голос под камнем', 'kubejs:mage_dossier', 1, 'Запись 03. Селена слышала зов в собственном голосе. Она поняла: бездна не источник энергии, а организм, использующий память.'), ('Печать экспедиции', 'kubejs:expedition_seal', 1, 'Собери знак архивистов. Отметь безопасный путь и запасной выход перед исследованием руин.'), ('Линза памяти', 'kubejs:memory_lens', 1, 'Осколок эха хранит отголоски прошлого. Старые записи говорят о трёх независимых печатях.'), ('Правда Совета', None, 1, 'Обсудите с командой три свидетельства. Никто из орденов не был невиновен, но каждый пытался спасти свой народ.'), ('Свидетельство будущим', 'minecraft:writable_book', 1, 'Запишите свою историю в книгу. Оставьте копию в общем архиве поселения; не требуется сдавать оригинал.')]), ('10_supply', 'Логистика и снабжение', 'minecraft:chest', [('Склад припасов', 'minecraft:barrel', 4, 'Раздели продовольствие, инструменты и добычу. Склад общего пользования важнее личных сундуков.'), ('Кухня выживших', 'farmersdelight:cutting_board', 1, 'Освой разделочную доску. Готовьте разнообразную еду между экспедициями.'), ('Аварийные пайки', 'minecraft:golden_carrot', 4, 'Новый рецепт полевого пайка: один слиток золота и четыре моркови. Не требуется добыча из редких сундуков.'), ('Свет на дорогах', 'minecraft:lantern', 8, 'Авторский рецепт даёт два фонаря за слиток железа и два факела. Освети дороги между строениями.'), ('Передача энергии', 'mekanism:basic_universal_cable', 8, 'Проложи сеть к общим механизмам. Храни запас топлива.'), ('Хранилище ордена', 'ae2:drive', 1, 'Добавь ME Drive к цифровому складу. Не забудь обеспечить сеть энергией.'), ('Караван', None, 1, 'Организуйте перевозку из удалённой шахты в поселение: поезд Create или другой безопасный путь.'), ('Хартия', 'kubejs:settlement_charter', 1, 'Устав союза: общие склады, неприкосновенность личных вещей, общие цели и взаимная помощь.')]), ('11_class_trials', 'Испытания специализаций', 'minecraft:iron_sword', [('Воин дозора', 'minecraft:shield', 1, 'Паладин: защити союзника в настоящем бою. Это общий пробный квест, не ограничивающий выбор класса.'), ('Школа магии', 'ars_nouveau:source_gem', 4, 'Архимаг: подготовь заклинания поддержки и обеспечь команду магическими ресурсами.'), ('Мастер приводов', 'create:mechanical_press', 1, 'Инженер: поставь пресс, подключи вращение и изготовь пластины.'), ('След на карте', 'minecraft:compass', 1, 'Следопыт: нанеси безопасный маршрут и два опасных места.'), ('Первый квартал', 'minecraft:stone_bricks', 32, 'Архитектор: помоги строителям подготовить дорогу и площадку.'), ('Тень в руинах', 'minecraft:fermented_spider_eye', 1, 'Оккультист: исследуй тёмную магию; не призывай опасных существ у дома.'), ('Испытание союза', None, 1, 'Каждый выбирает удобную роль. Объедините усилия в экспедиции. Ранги проверяются отдельно командой /trigger ashes_status.')]), ('12_recovery', 'После долгой ночи', 'minecraft:prismarine_crystals', [('Матрица очищения', 'kubejs:purifier_matrix', 1, 'Создай экспериментальную матрицу. Она предназначена для переработки знаков, а не для автоматического удаления заражённых блоков.'), ('Полевой комплект', 'kubejs:purity_sigil', 8, 'Запаси знаки для участников. /trigger ashes_purify очищает только персонажа.'), ('Перепись очагов', None, 1, 'Вместе обозначьте очаги заражения на карте и оцените пути отхода.'), ('Земля снова дышит', None, 1, 'Примените штатный очиститель Sculk Horde на тестовом участке. Убедитесь, что блоки восстановлены.'), ('Зелёный рубеж', 'minecraft:oak_sapling', 16, 'Высади деревья на освобождённой территории. Верни жизнь в долину.'), ('Новая страница', 'minecraft:writable_book', 1, 'Запиши имена товарищей и историю первого освобождённого поселения. Это ваш собственный эпилог.')])]
# New chapters are independent of the existing graph and retain stable indices.
extra_parents={}
for line in (ROOT/'tools/campaign.txt').read_text(encoding='utf-8').splitlines():
 if not line.strip(): continue
 if line.startswith('@'):
  slug,title,icon,parent=line[1:].split('|'); rows=[]; chapters.append((slug,title,icon,rows));extra_parents[slug]=parent
 else:
  title,item,count,desc=line.split('|',3); rows.append((title,None if item=='-' else item,int(count),desc))
def uid(s): return format(int(hashlib.sha256(('ashes/'+s).encode()).hexdigest()[:16],16) & ((1<<63)-1),'016X')
# SNBT accepts JSON quoted strings/keys; numeric x,y rendered as doubles. Use explicit IDs stable across rebuilds.
allids=set(); refs=[]; index=[]; ends={}; total=0
for order,(slug,title,icon,rows) in enumerate(chapters):
 quests=[]; prev=None
 for i,(name,item,count,desc) in enumerate(rows):
  qid=uid(f'{slug}/{i}'); deps=[prev] if prev else []
  if not prev:
   if slug=='02_ruins': deps=[ends['01_survival']]
   elif slug in ('03_industry','04_magic','05_colony'): deps=[ends['02_ruins']]
   elif slug=='06_horde': deps=[ends[s] for s in ('03_industry','04_magic','05_colony')]
   elif slug=='07_war': deps=[ends['06_horde']]
   elif slug=='08_final': deps=[ends['07_war']]
   elif slug=='09_archives': deps=[ends['02_ruins']]
   elif slug=='10_supply': deps=[ends['01_survival']]
   elif slug=='11_class_trials': deps=[ends['01_survival']]
   elif slug=='12_recovery': deps=[ends['06_horde']]
   elif slug in extra_parents: deps=[uid(extra_parents[slug]+'/0')] if slug not in ('32_abyss','33_finale') else [ends[extra_parents[slug]]]
  if slug=='40_lore_sites' and i%2==0: deps=[uid('02_ruins/0')]
  task={'id':uid(f'{slug}/{i}/task'),'type':'item' if item else 'checkmark'}
  if item: task.update(item=item,count=count)
  else: task['title']='Подтвердить выполненное действие вручную'
  auto={('06_horde',4):'sculkhorde:sculk_horde_start',('08_final',2):'sculkhorde:sculk_horde_defeat'}
  extra_auto={'Разведка узла':'sculkhorde:sculk_tomb_visit','Очищение блока':'sculkhorde:craft_infestation_purifier','Защита поселения':'sculkhorde:craft_infestation_ward_block','Поражение орды':'sculkhorde:sculk_horde_defeat'}
  adv=auto.get((slug,i)) or (extra_auto.get(name) if slug=='32_abyss' else None)
  if slug=='34_wards': adv={3:'ashes:ward/registered',4:'sculkhorde:craft_infestation_ward_block'}.get(i)
  if slug=='40_lore_sites' and i%2==0:
   adv='ashes:lore/'+('silent_hamlet','last_stand','nameless_graves','three_seals_altar','broken_watch','sealed_archive')[i//2]
  if adv:
   task={'id':task['id'],'type':'advancement','advancement':adv}
   if name=='Очищение блока': name='Штатный очиститель'; desc='Изготовь очиститель Sculk Horde. После установки проверь восстановление земли.'
   if name=='Разведка узла': name='Гробница орды'; desc='Посети штатную гробницу Sculk Horde; достижение фиксирует посещение.'
   if name=='Защита поселения': desc='Изготовь штатный защитный блок Sculk Horde. Установи его и проверь границу отдельно.'
  task_icon = icon if not item or item.startswith('#') else item
  q={'id':qid,'title':name,'description':[desc],'icon':task_icon,'x':float(i%4*2),'y':float(i//4*2),'tasks':[task]}
  if slug=='40_lore_sites': q.update(x=float(i%2*3),y=float(i//2*2))
  if slug=='33_finale' and i==4: deps.append(ends['32_abyss'])
  if deps:q['dependencies']=deps
  decorate_quest(q,slug,order,i,rows,uid)
  bind_alternatives(slug,q)
  quests.append(q); prev=qid; total+=1; refs+=deps; allids.add(qid); index.append({'chapter':title,'quest':name,'task':('advancement:'+adv) if adv else item or 'manual','count':count,'id':qid,'dependencies':deps,**({'family':family} if (family:=task_family(task)) else {})})
 ends[slug]=prev
 js(Q/(slug+'.snbt'),{'default_hide_dependency_lines':False,'default_quest_shape':'','filename':slug,'group':'','icon':icon,'id':uid(slug),'order_index':order,'quest_links':links_for(slug,uid),'title':title,'quests':quests})
assert set(refs)<=allids and len(allids)==total
tag_files(DATA, js)
write_coverage(ROOT, chapters)
js(ROOT/'docs'/'quests.json',index)
manifest=json.loads((ROOT/'manifest.json').read_text());manifest['version']='1.0.0-rc5-author-content.5';js(ROOT/'manifest.json',manifest)
assert len({x['projectID'] for x in manifest['files']})==len(manifest['files'])
print(f'{total} quests, {sum(x["task"]=="manual" for x in index)} manual; {len(manifest["files"])} locked projects; {len(items)} items')

from gameplay import generate_gameplay
generate_gameplay(ROOT, K, F, DATA, fn, js, msg)
from skills import generate_skills
generate_skills(DATA, F, fn, js, msg)
generate_artifacts(K, F, put, fn, msg)
from wards import generate_wards
generate_wards(DATA,F,fn,js,msg)

from news import generate_news
generate_news(DATA,F,fn,js)

from structures import generate_structures
from site_supports import DEPTH_SCORE, generate_foundations
generate_structures(ROOT)
generate_foundations(fn, js, DATA/'ashes'/'tags')
with (F/'load.mcfunction').open('a', encoding='utf-8') as f:
 f.write(f'scoreboard objectives add {DEPTH_SCORE} dummy\n')
with (F/'tick.mcfunction').open('a', encoding='utf-8') as f:
 f.write('function ashes:foundation/tick\n')
