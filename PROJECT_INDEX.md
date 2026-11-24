# Индекс проекта
| Теги | Файл/путь | Назначение |
|---|---|---|
| #context #lore | PROJECT_CONTEXT.md | Цели, история, ограничения |
| #release #mods #lock | manifest.json, modlist.html, overrides/ashes_docs/mods-lock.tsv | Фиксированные версии и ссылки |
| #builder #source | tools/build.py | Генератор квестов, предметов, рецептов, классов и функций |
| #quests #progression | docs/quests.json, overrides/config/ftbquests/quests/chapters/ | 34 главы, зависимости и задания |
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
- `tools/package.py --profile horizons` — отдельный CurseForge ZIP с Distant Horizons вместо Oculus и Complementary. `docs/RELEASE_STATUS.md` — точное состояние финального кандидата.

- #assets #textures `docs/ASSETS.md`, `overrides/kubejs/assets/kubejs/textures/item/` — исходные PNG, привязка в `tools/build.py` и проверка в `tools/validate.py`.

- #animation `*.png.mcmeta` рядом с текстурами — 8 анимированных артефактов; список в `docs/ASSETS.md`.
