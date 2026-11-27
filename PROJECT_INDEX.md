# Индекс проекта
| Теги | Файл/путь | Назначение |
|---|---|---|
| #context #lore | PROJECT_CONTEXT.md | Цели, история, ограничения |
| #release #mods #lock | manifest.json, modlist.html, overrides/ashes_docs/mods-lock.tsv | Фиксированные версии и ссылки |
| #builder #source | tools/build.py | Генератор квестов, предметов, рецептов, классов и функций |
| #quests #progression | docs/quests.json, overrides/config/ftbquests/quests/chapters/ | 40 глав, зависимости и задания |
| #items #kubejs | overrides/kubejs/startup_scripts/ashes_items.js | 30 предметов |
| #recipes #balance | overrides/kubejs/server_scripts/ashes_recipes.js | 32 рецепта, существующие рецепты модов не заменяются |
| #classes #multiplayer | overrides/kubejs/data/ashes/functions/ | Выбор классов, атрибуты, 3 ранга, очищение игрока |
| #config #server | overrides/ashes_docs/server.properties.example, docs/SERVER.md | Шаблон и рекомендации по настройке |
| #testing #compatibility | docs/TESTING.md, overrides/ashes_docs/compatibility.txt | Проверки и ограничения |
| #roadmap | docs/ROADMAP.md, CHANGELOG.md | Незавершённые функции, версии |

Сначала изменять tools/build.py, затем запускать его из исходников. Он генерирует перечисленные файлы; ручные правки в них будут перезаписаны. Для релиза запустить tools/package.py. Не менять идентификаторы существующих квестов: они вычисляются из имени главы и индекса; новые квесты дописывать в конец или перейти на стабильные явные ключи до перестановок.

## GitHub
- `.github/workflows/build.yml`: статическая проверка воспроизводимости и упаковка ZIP.
- `.gitignore`: исключает скачанные моды, миры, логи, секреты и локальную среду.

## 0.3.0-alpha
- #agents AGENTS.md — правила разработки.
- #lore docs/LORE.md — канон, герои, архивы, история глав.
- #tooltip overrides/kubejs/client_scripts/ashes_lore.js — подсказки досье и артефактов.
- #test tools/validate.py — статическая проверка замков, графа квестов, предметов, скриптов.
- #story главы 09–12 — архивы, снабжение, классовые испытания, восстановление.

## 1.0.0-rc1
- #campaign tools/campaign.txt — 21 дополнительная глава.
- #items #recipes tools/extension.py — новые предметы и межмодовые рецепты.
- #talents #ritual tools/gameplay.py — активные навыки, образцы, gamerules.
- #loot overrides/kubejs/server_scripts/ashes_archives.js — дополнительные документы в сундуках.
- #horde overrides/config/sculkhorde_config.toml — параметры заражения для нового мира.
- #graphics docs/GRAPHICS.md, overrides/config/oculus.properties, overrides/options.txt.
- #balance docs/BALANCE.md; #release docs/RELEASE_STATUS.md — реализованные функции и ограничения.

- #audit #dependencies `tools/audit_mods.py`, `docs/mod-plan.json`, `docs/MOD_AUDIT.md` — сверка запланированного состава, официальный API по ключу и анализ скачанных JAR.

- #skills #visual `tools/skills.py`, `docs/SKILLS.md`, `overrides/kubejs/data/ashes/puffish_skills/` — дерево мастерства, очки и меню классов.
- `tools/wards.py` / `docs/WARDS.md`: регистрация обелисков, защита жителей, тревоги, тег бойцов орды и достижение установки.
- `docs/MOD_CONFIGS.md` / `overrides/config/sculkhorde_config.toml` / `overrides/defaultconfigs/ftb*`: проверенные имена параметров орды, приватов и добычи.
- `tools/package.py --profile horizons` — архив с привычным названием. Состав проектов совпадает со стандартным архивом. `docs/RELEASE_STATUS.md` — точное состояние финального кандидата.

- #assets #textures `docs/ASSETS.md`, `overrides/kubejs/assets/kubejs/textures/item/` — исходные PNG, привязка в `tools/build.py` и проверка в `tools/validate.py`.

- #animation `*.png.mcmeta` рядом с текстурами — 8 анимированных артефактов; список в `docs/ASSETS.md`.

- #release 1.0.0-rc2 — визуальное обновление; список модов и игровые ID не изменены.

- #once #mod-import `docs/ONCE_IMPORT.md` — аудит второй сборки.

- #client `sodiumdynamiclights-client.toml`, `sodiumextras-client.toml`, `parcool-client.toml` — клиентский профиль (в overrides/config).

- #worldgen #ores `docs/WORLDGEN.md`, `overrides/config/tectonic.json`, `overrides/config/Mekanism/world.toml`, `overrides/kubejs/data/minecraft/worldgen/configured_feature/` — генерация и параметры жил.

- #expeditions #twilight #aircraft #parkour `tools/campaign.txt` (главы 35–39) — новые побочные линии.

- #news #immersion `tools/news.py`, `docs/WORLD_NEWS.md`, `overrides/kubejs/data/ashes/functions/news/` — события и отключение сообщений.

- #rc3 Основной профиль 159 проектов, резервный 153; 483 задания в 39 главах. Источники: tools/news.py, tools/campaign.txt, docs/ONCE_IMPORT.md, WORLDGEN.md, WORLD_NEWS.md.

- #rc4 #launch-dependencies `docs/mod-plan.json` — три обязательные библиотеки, подтверждённые ошибками Forge; `docs/MOD_AUDIT.md`.

- #structures #lore #worldgen `tools/structures.py`, `docs/STRUCTURES.md`, `docs/lore-structures.json`, `overrides/kubejs/data/ashes/structures/lore/` — шаблоны, генерация, добыча и открытия.

- #lore-quests Глава 40 `40_lore_sites.snbt`, источники `tools/campaign.txt` и `tools/build.py`; шесть параллельных ветвей и реальные достижения.

- #rc5 Места памяти; 495 квестов / 40 глав; 159 проектов, состав не изменён.

## Инструменты и база знаний
- #devtools #knowledge docs/KNOWLEDGE_BASE.md, docs/DEVELOPMENT_RULES.md — карта знаний, регламент, команды и ограничения.
- #registry #nbt #balance #worldgen #logs tools/devtools.py — snapshot, refs, scan-jars, registry-check, structures, balance, worldgen, crash, loot-preview; JSON-отчёты в .local/.
- #tests tools/test_devtools.py — тесты парсера, JAR-кандидатов, логов и лута; вызываются из tools/validate.py (существующий CI).

## Расширение мест памяти
- #lore #structures #worldgen `tools/structures.py`, `tools/structure_sites.py`, `docs/STRUCTURES.md` — архитектура 18 локаций, 36 шаблонов, тематические находки и события обнаружения.

- #companions #skins #touhou #succubus docs/COMPANIONS.md, overrides/ashes_docs/COMPANIONS.md — справка и тесты; docs/LORE.md — экспериментальный канон; manifest и mods-lock — 163 проекта в этой ветке. Квесты и игровые ID не изменены.

- #mca #villagers #reputation #family #npcquests docs/MCA.md, overrides/ashes_docs/MCA.md — справка, версии, лор, зависимости, сценарии тестов; 169 проектов в каждом профиле. MCA-квесты не входят в число авторских FTB Quests.

- #minecolonies #launch #crash `docs/MOD_AUDIT.md`, `docs/mod-plan.json` — краш `FoodUtilsMixin` и обязательная версия Tweaks.

- #botania #patchouli [Диагностика установки](docs/MOD_AUDIT.md#forge-сообщает-об-отсутствии-patchouli). Связи Botania с Patchouli и Curios заданы в `docs/mod-plan.json` и проверяются упаковщиком каждого профиля.

- #corelib #forge #crash [Диагностика GameDataMixin](docs/MOD_AUDIT.md#сбой-core-lib-при-запуске-forge-47428) и `tools/devtools.py crash` — поиск фатальной ошибки среди предупреждений Mixin.

- #corelib #testing [Результаты запуска с Rechiseled](docs/TESTING.md#проверка-запуска-с-rechiseled-на-forge-47428).

- #terrablender #vinery #launch [Конфликт с Cristel Lib и отсутствующий класс рецептов Vinery](docs/MOD_AUDIT.md#два-сбоя-запуска-с-terrablender-и-vinery).

- #mods #updates `tools/audit_updates.py` и [сводка по обновлениям](docs/MOD_UPDATES.md).

- #chunky #pregen [Предгенерация чанков](docs/SERVER.md#предгенерация-чанков) и состав обоих профилей в `docs/mod-plan.json`.

- #mca [Файлы MCA Reborn 7.7.1-beta.6 и пяти аддонов](docs/MCA.md#версии-и-источники).

## DH Turbo
Эксперимент DH Turbo для одиночной игры: Distant Horizons 3.3.3 и Turbo 1.6.0, без Chunky и YUNG’s Better Caves. Начальные настройки: восемь потоков Turbo, точное фоновое уточнение выключено, дальность обычных чанков 8, симуляция 6, ограничение 60 FPS. Игровые замеры предстоят.

- #controls Начальные назначения клавиш для импорта CurseForge хранятся в `overrides/options.txt`.

- #mods Amendments 2.2.6 и зависимость Moonlight Lib закреплены в списке модов.

- Кампания FTB Quests из author-content: 532 заданий в 45 главах, новые награды, маршруты и иллюстрации.

#quests #balance Правила выдачи наград находятся в tools/quest_rewards.py, сводка в docs/BALANCE.md.

- #mods Ore Excavation включён в оба профиля CurseForge.
