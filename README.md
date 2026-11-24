# Пепел ушедшего мира / Ashes of the Fallen World

Кооперативная RPG-сборка Minecraft в мрачном мире после катастрофы: изучение руин, развитие поселений, магия, промышленность и борьба со Скверной.

**1.0.0-rc2** — Minecraft 1.20.1 · Forge 47.4.28 · Java 17 · 129 зафиксированных проектов CurseForge, включая шейдер. 431 квеста (161 с ручным подтверждением), 34 главы, 30 авторских предметов, 32 дополнительных рецепта, шесть индивидуальных классов с тремя рангами и альтернативными активными талантами. 18 визуальных узлов мастерства, защитные обелиски и глава рубежей. Сборка не проверена запуском Minecraft.

## Установка

В разделе Actions скачайте артефакт `Ashes-CurseForge`, распакуйте внешний архив артефакта и импортируйте находящийся внутри `Ashes-CurseForge.zip` в CurseForge. Для локальной сборки используйте Python 3.11+:

```sh
python tools/build.py
python tools/validate.py
mkdir -p dist
python tools/package.py dist/Ashes-CurseForge.zip
```

Не импортируйте архив исходников как модпак. Клиент: Java 17, начальные 8–10 ГБ ОЗУ, первый запуск без шейдеров. Сервер: [руководство](docs/SERVER.md). Не храните скачанные JAR в репозитории.

## Разработка

- [AGENTS.md](AGENTS.md) — правила работы и ограничения.
- [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) — краткий контекст.
- [PROJECT_INDEX.md](PROJECT_INDEX.md) — карта файлов и тегов.
- [docs/LORE.md](docs/LORE.md) — канон и сюжет.
- [docs/CLASSES.md](docs/CLASSES.md) — классы и ранги.
- [docs/TESTING.md](docs/TESTING.md) — план проверок.
- [docs/ROADMAP.md](docs/ROADMAP.md) — оставшиеся задачи.
- [CHANGELOG.md](CHANGELOG.md) — версии.

[Статус кандидата](docs/RELEASE_STATUS.md) · [Графика](docs/GRAPHICS.md) · [Баланс](docs/BALANCE.md).

`tools/build.py`, `tools/campaign.txt`, `tools/extension.py` и `tools/gameplay.py` — первичные источники квестов, предметов, рецептов и функций; генерируемые файлы коммитятся вместе с ним. Не менять существующие идентификаторы квестов. `main` — интеграционная ветка; сложные изменения вести в feature-ветках. CI проверяет структуру и упаковывает ZIP, но не запускает Forge.

Графический профиль Horizons (не содержит Oculus и шейдер): `python tools/package.py --profile horizons dist/Ashes-Horizons.zip`. Не смешивать два профиля. [Навыки](docs/SKILLS.md) · [Рубежи](docs/WARDS.md) · [Конфигурации](docs/MOD_CONFIGS.md) · [Аудит](docs/MOD_AUDIT.md).

[Авторские текстуры и анимации](docs/ASSETS.md): 30 уникальных текстур, восемь анимированных артефактов.
