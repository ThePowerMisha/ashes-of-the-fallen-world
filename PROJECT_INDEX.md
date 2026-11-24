# Индекс проекта
| Теги | Файл/путь | Назначение |
|---|---|---|
| #context #lore | PROJECT_CONTEXT.md | Цели, история, ограничения |
| #release #mods #lock | manifest.json, modlist.html, overrides/ashes_docs/mods-lock.tsv | Фиксированные версии и ссылки |
| #builder #source | tools/build.py | Генератор квестов, предметов, рецептов, классов и функций |
| #quests #progression | docs/quests.json, overrides/config/ftbquests/quests/chapters/ | 12 глав, зависимости и задания |
| #items #kubejs | overrides/kubejs/startup_scripts/ashes_items.js | 14 предметов |
| #recipes #balance | overrides/kubejs/server_scripts/ashes_recipes.js | 17 рецептов, существующие рецепты модов не заменяются |
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
