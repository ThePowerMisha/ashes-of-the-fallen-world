# Пепел ушедшего мира / Ashes of the Fallen World

Кооперативная RPG-сборка Minecraft в мрачном мире после катастрофы: изучение руин, развитие поселений, магия, промышленность и борьба со Скверной.

**1.0.0-rc4** — Minecraft 1.20.1 · Forge 47.4.28 · Java 17 · 159 зафиксированных проектов CurseForge, включая пять шейдеров. 483 квеста (178 с ручным подтверждением), 39 глав, 30 авторских предметов, 32 дополнительных рецепта, шесть индивидуальных классов с тремя рангами и альтернативными активными талантами. 18 визуальных узлов мастерства, защитные обелиски и глава рубежей. Сборка не проверена запуском Minecraft.

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

## RC3
Основной профиль: Oculus + Distant Horizons; резервный Horizons — 153 проектов без Oculus и пяти шейдеров. Добавлены ParCool, Twilight Forest, Immersive Aircraft, стили MineColonies, дополнения JEI, укрупнённые жилы и хроники мира. Новый мир рекомендуется. `/trigger ashes_news set 2` отключает хроники, `set 1` включает.
[Импорт Once upon an year](docs/ONCE_IMPORT.md) · [Генерация мира](docs/WORLDGEN.md) · [Хроники](docs/WORLD_NEWS.md).

## RC4 — исправление запуска
Forge сообщил об отсутствующих обязательных mod ID `guideme`, `villagertradingplus`, `fusion`. Добавлены три точных Forge-файла 1.20.1: GuideME 20.1.15, VillagersTradingPlus 1.1.0, Fusion 1.3.16. Все прежние 156 projectID/fileID сохранены. Проверка манифеста и известного графа не заменяет проверку фактических JAR; страница зависимостей AE2 15.4.10 не перечисляла GuideME, хотя Forge требует его. Источник: сообщение Forge от пользователя; обновлённый вручную профиль, по его словам, запускается, точные версии этого профиля неизвестны. RC4 ещё не проверен в игре.
