# Внутренняя база знаний Ashes
Единая навигация: PROJECT_INDEX.md (поиск по тегам), PROJECT_CONTEXT.md (контекст и ограничения), AGENTS.md (обязательные правила), DEVELOPMENT_RULES.md (инструменты). Не дублировать канон и актуальные числовые данные вручную.

| Тема | Источник истины |
|---|---|
| #mods #versions #compatibility | manifest.json, overrides/ashes_docs/mods-lock.tsv, MOD_AUDIT.md, MOD_CONFIGS.md, mod-plan.json |
| #lore #canon | LORE.md, WORLD_NEWS.md, tools/news.py |
| #structures #loot #worldgen | STRUCTURES.md, WORLDGEN.md, lore-structures.json, tools/structures.py, tools/structure_sites.py |
| #quests #progression | tools/build.py, tools/campaign.txt, quests.json, сгенерированные главы FTB Quests |
| #items #recipes #balance | tools/build.py, tools/extension.py, BALANCE.md, ASSETS.md |
| #classes #skills #wards | CLASSES.md, SKILLS.md, WARDS.md, tools/gameplay.py, tools/skills.py, tools/wards.py |
| #graphics #performance | GRAPHICS.md, конфиги в overrides/config |
| #server #testing #release | SERVER.md, TESTING.md, RELEASE_STATUS.md, CHANGELOG.md |
| #roadmap #decisions | ROADMAP.md, PROJECT_CONTEXT.md, AGENTS.md |

## Машиночитаемая часть
python tools/devtools.py snapshot -o .local/knowledge.json — актуальные версии, состав, авторские предметы, требуемые ID, структуры и палитры, квестовые метрики, рецепты, настройки генерации и карта файлов. Не требуется повторно читать все сгенерированные главы при поиске сводки. Для отдельного раздела доступны команды refs, structures, balance, worldgen.
- Уровень доказательности: source = присутствует в исходниках; asset candidate = обнаружен ресурс в JAR; runtime = зарегистрирован в фактически запущенной сборке; playtest = проверена механика в игре. Не смешивать уровни.
- Фактические реестры блоков, предметов и сущностей всей сборки пока не получены. Хранить дампы конкретного экземпляра локально; проверять через registry-check. Список JAR-кандидатов генерируется только при наличии mods.
- Не записывать пароль, токен, персональные пути или содержимое логов в базу.

## Открытые проверки
RC5: игровые тесты клиента/сервера, фактические реестры, генерация на нескольких сидах, Lootr, взаимодействие модовых структур, производительность. См. TESTING.md. Изменение инструментов не означает прохождение этих проверок.

Для мест памяти `devtools.py structures` проверяет палитры, количество блоков, координаты шаблонных жителей и ссылки на добычу. `devtools.py worldgen` показывает сетки размещения и команды поиска. Результаты отдельного запуска Minecraft 1.20.1 и ограничения проверки приведены в TESTING.md.

## Эксперимент companions
#companions #skins #touhou #succubus — COMPANIONS.md и его копия в overrides/ashes_docs/COMPANIONS.md, LORE.md, mod-plan.json. Данные версий подтверждены публичными страницами файлов; реестры, механики и совместимость в игре не проверены. snapshot автоматически читает актуальный lock.

## MCA / живые поселения
#mca #villagers #npcquests #reputation — MCA.md (справка, источники, ограничения), mod-plan.json (группа living_villages), LORE.md. Сводка devtools snapshot читает lock автоматически. Валидация и упаковщик обновлены под 169 проектов. Нужны реальные реестры и приёмка, в частности типы жителей и обелиски.

- #minecolonies #mixin #launch Сигнатура `FoodUtilsMixin` при создании мира, связь Tweaks с Compatibility, зафиксированная версия и процедура проверки описаны в [MOD_AUDIT.md](MOD_AUDIT.md).

- #botania #patchouli Для сообщения `Currently, patchouli is not installed` см. [проверку папки профиля и версию JAR](MOD_AUDIT.md#forge-сообщает-об-отсутствии-patchouli).

- #forge #mixin #rechiseled Если запуск останавливается на `GameDataMixin.postRegisterEvents`, см. [проверенную пару Forge и Core Lib](MOD_AUDIT.md#сбой-core-lib-при-запуске-forge-47428). В отчёте `devtools.py crash` поле `line_numbers.critical_injections` указывает строки с фатальным сбоем внедрения.

- #corelib [Парная проверка старой и новой версии на выделенном сервере](TESTING.md#проверка-запуска-с-rechiseled-на-forge-47428).

- #terrablender #vinery #launch [Два сбоя запуска](MOD_AUDIT.md#два-сбоя-запуска-с-terrablender-и-vinery), точные версии и сигнатуры ошибок.

- #mods #updates `python tools/audit_updates.py --include-beta` ищет более новые файлы по меткам Minecraft 1.20.1 и Forge. [Снимок и приоритеты](MOD_UPDATES.md).

- #mods #update [Профиль тестовой ветки обновлений](MOD_UPDATES.md#тестовая-ветка-rc5-mod-updates1), список версий и требования совместимости.
