"""World chronicles driven by real vanilla state and mod advancements, no random fake events."""
import json

FUNCTIONS = {
  "news/weather": [
    "scoreboard players set #weather anews 0",
    "execute if predicate ashes:news/rain run scoreboard players set #weather anews 1",
    "execute if predicate ashes:news/thunder run scoreboard players set #weather anews 2",
    "execute unless score #weather_ready anews matches 1 run scoreboard players operation #lastweather anews = #weather anews",
    "scoreboard players set #weather_ready anews 1",
    "execute unless score #weather anews = #lastweather anews if score #weather anews matches 0 run tellraw @a[distance=0..,tag=!ashes_news_muted] {\"text\": \"[Хроники] Небо прояснилось. Путники могут продолжить путь.\", \"color\": \"dark_aqua\"}",
    "execute unless score #weather anews = #lastweather anews if score #weather anews matches 1 run tellraw @a[distance=0..,tag=!ashes_news_muted] {\"text\": \"[Хроники] Над долинами идёт дождь. Укройте припасы и приготовьте факелы.\", \"color\": \"dark_aqua\"}",
    "execute unless score #weather anews = #lastweather anews if score #weather anews matches 2 run tellraw @a[distance=0..,tag=!ashes_news_muted] {\"text\": \"[Хроники] Гроза над рубежом. Вдали гремят раскаты; лучше переждать бурю под крышей.\", \"color\": \"gold\"}",
    "scoreboard players operation #lastweather anews = #weather anews"
  ],
  "news/time": [
    "execute store result score #tod anews run time query daytime",
    "execute store result score #day anews run time query day",
    "scoreboard players set #phase anews 0",
    "execute if score #tod anews matches 12000..23999 run scoreboard players set #phase anews 1",
    "scoreboard players operation #moon anews = #day anews",
    "scoreboard players operation #moon anews %= #eight anews",
    "execute unless score #time_ready anews matches 1 run scoreboard players operation #lastphase anews = #phase anews",
    "scoreboard players set #time_ready anews 1",
    "execute unless score #phase anews = #lastphase anews if score #phase anews matches 0 run tellraw @a[distance=0..,tag=!ashes_news_muted] {\"text\": \"[Хроники] Новый рассвет. В убежищах снова зажигают печи.\", \"color\": \"dark_aqua\"}",
    "execute unless score #phase anews = #lastphase anews if score #phase anews matches 1 unless score #moon anews matches 0 run tellraw @a[distance=0..,tag=!ashes_news_muted] {\"text\": \"[Хроники] Сумерки опускаются на старые дороги. Возвращайтесь к огням поселений.\", \"color\": \"gray\"}",
    "execute unless score #phase anews = #lastphase anews if score #phase anews matches 1 if score #moon anews matches 0 run tellraw @a[distance=0..,tag=!ashes_news_muted] {\"text\": \"[Хроники] Полная луна поднялась над руинами. Дозорные заняли свои посты.\", \"color\": \"gold\"}",
    "scoreboard players operation #lastphase anews = #phase anews"
  ],
  "news/horde": [
    "execute if score #horde_defeated anews matches 0 if entity @a[advancements={sculkhorde:sculk_horde_defeat=true}] run function ashes:news/horde_defeat",
    "execute if score #horde_started anews matches 0 if score #horde_defeated anews matches 0 if entity @a[advancements={sculkhorde:sculk_horde_start=true}] run function ashes:news/horde_start"
  ],
  "news/horde_start": [
    "scoreboard players set #horde_started anews 1",
    "tellraw @a[tag=!ashes_news_muted] {\"text\": \"[Хроники] Глубоко под землёй пробудилось нечто древнее. Скверна пришла в движение. Подготовьте рубежи.\", \"color\": \"dark_red\"}"
  ],
  "news/horde_defeat": [
    "scoreboard players set #horde_started anews 1",
    "scoreboard players set #horde_defeated anews 1",
    "tellraw @a[tag=!ashes_news_muted] {\"text\": \"[Хроники] Победа над ордой подтверждена. Время вернуть долинам жизнь и восстановить города.\", \"color\": \"gold\"}"
  ],
  "news/twilight": [
    "tag @s add ashes_twilight_seen",
    "tellraw @s[tag=!ashes_news_muted] {\"text\": \"[Хроники] Здесь время словно остановилось. Перед тобой Сумеречный архив — забытая тропа древних орденов.\", \"color\": \"dark_purple\"}"
  ],
  "news/nether": [
    "tag @s add ashes_nether_seen",
    "tellraw @s[tag=!ashes_news_muted] {\"text\": \"[Хроники] Жар старых глубин встречает тебя. Держись ближе к порталу, пока не нанесёшь путь на карту.\", \"color\": \"gold\"}"
  ],
  "news/end": [
    "tag @s add ashes_end_seen",
    "tellraw @s[tag=!ashes_news_muted] {\"text\": \"[Хроники] За краем мира не слышно ветра. Только пустота и отзвук древней катастрофы.\", \"color\": \"dark_purple\"}"
  ],
  "news/player": [
    "scoreboard players enable @s ashes_news",
    "execute if score @s ashes_news matches 1 run tag @s remove ashes_news_muted",
    "execute if score @s ashes_news matches 1 run tellraw @s {\"text\": \"[Хроники] Сообщения хроник включены.\", \"color\": \"dark_aqua\"}",
    "execute if score @s ashes_news matches 2 run tag @s add ashes_news_muted",
    "execute if score @s ashes_news matches 2 run tellraw @s {\"text\": \"[Хроники] Сообщения хроник отключены. /trigger ashes_news set 1 — включить.\", \"color\": \"dark_aqua\"}",
    "scoreboard players set @s ashes_news 0",
    "execute if dimension twilightforest:twilight_forest unless entity @s[tag=ashes_twilight_seen] run function ashes:news/twilight",
    "execute if dimension minecraft:the_nether unless entity @s[tag=ashes_nether_seen] run function ashes:news/nether",
    "execute if dimension minecraft:the_end unless entity @s[tag=ashes_end_seen] run function ashes:news/end"
  ]
}
APPEND = {
  "load": [
    "scoreboard objectives add anews dummy",
    "scoreboard objectives add ashes_news trigger",
    "scoreboard players set #eight anews 8",
    "scoreboard players add #horde_started anews 0",
    "scoreboard players add #horde_defeated anews 0"
  ],
  "second": [
    "execute in minecraft:overworld if entity @a[distance=0..] run function ashes:news/weather",
    "execute in minecraft:overworld if entity @a[distance=0..] run function ashes:news/time",
    "execute if entity @a run function ashes:news/horde"
  ],
  "player": [
    "function ashes:news/player"
  ],
  "intro": [
    "tellraw @s {\"text\": \"[Хроники] Хроники мира: /trigger ashes_news set 2 — скрыть сообщения, set 1 — включить.\", \"color\": \"dark_aqua\"}"
  ]
}
PREDICATES = json.loads("{\"rain\":{\"condition\":\"minecraft:weather_check\",\"raining\":true},\"thunder\":{\"condition\":\"minecraft:weather_check\",\"thundering\":true}}")

def generate_news(DATA, F, fn, js):
    for path, lines in FUNCTIONS.items():
        fn(path, lines)
    for path, lines in APPEND.items():
        p = F / (path + '.mcfunction')
        p.write_text(p.read_text(encoding='utf-8') + '\n'.join(lines) + '\n', encoding='utf-8')
    for name, predicate in PREDICATES.items():
        js(DATA / 'ashes' / 'predicates' / 'news' / (name + '.json'), predicate)
