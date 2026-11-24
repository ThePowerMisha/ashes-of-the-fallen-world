# Проверка состава и совместимости

Состав сверяется с docs/mod-plan.json. Сохранены 129 прежних проектов, импортированы 27 из Once upon an year: 156 в основном профиле и 153 в резервном Horizons. Oculus + DH включены в основной профиль; точная совместимость требует запуска. См. ONCE_IMPORT.md. Sound Filters исключён как дублирование.

Проверено на уровне опубликованных метаданных и текущего lock:
- [Steam 'n' Rails 1.7.2 C6](https://www.curseforge.com/minecraft/mc-mods/create-steam-n-rails/files/7758640) для Create 6; три компонента Mekanism имеют одинаковую версию.
- [MineColonies](https://www.curseforge.com/minecraft/mc-mods/minecolonies/files/9624306) требует Structurize ≥1.0.825, установлен 1.0.826; присутствуют BlockUI, Domum Ornamentum, Multi-Piston и TownTalk.
- [Sculk Horde](https://www.curseforge.com/minecraft/mc-mods/sculk-horde/relations/dependencies) с GeckoLib; [Iron's Spells](https://www.curseforge.com/minecraft/mc-mods/irons-spells-n-spellbooks/relations/dependencies) с Curios, GeckoLib, Iron's Lib и playerAnimator.
- [IDAS](https://www.curseforge.com/minecraft/mc-mods/idas/relations/dependencies) с Create, Integrated API, Quark, Supplementaries; [Bons Voyage](https://www.curseforge.com/minecraft/mc-mods/bons-voyage/relations/dependencies) с Balm, Lithostitched, Waystones 14.1.21; [Relics](https://www.curseforge.com/minecraft/mc-mods/relics-mod/relations/dependencies) с Curios и OctoLib.
- [Terralith](https://www.curseforge.com/minecraft/mc-mods/terralith) совместим с модовой версией Tectonic; конкретная генерация вместе с другими структурами не запускалась.
- [FTB Quests 2001.4.22](https://www.curseforge.com/minecraft/mc-mods/ftb-quests-forge/files/8078538) является Forge 1.20.1, несмотря на название проекта; Item Filters не обязательный.

Проверки: `python tools/audit_mods.py` — локальная сверка манифеста, lock, запланированных модов и известных зависимостей; пройдена. `CF_API_KEY=... python tools/audit_mods.py --curseforge` проверяет все точные файлы, версии, загрузчик и обязательные/несовместимые зависимости через официальный API. Ключ не хранить в репозитории. `python tools/audit_mods.py --instance /path/to/instance` читает реально скачанные JAR и вложенные Jar-in-Jar; проверяет наличие mod ID, не разрешает Maven ranges, не запускает mixin. Оба расширенных режима пока не выполнены: нет ключа API, локальных JAR и сетевого доступа в среде сборки. Отсутствие конфликтов в игре не подтверждено.

## RC4 — исправление запуска
Forge сообщил об отсутствующих обязательных mod ID `guideme`, `villagertradingplus`, `fusion`. Добавлены три точных Forge-файла 1.20.1: GuideME 20.1.15, VillagersTradingPlus 1.1.0, Fusion 1.3.16. Все прежние 156 projectID/fileID сохранены. Проверка манифеста и известного графа не заменяет проверку фактических JAR; страница зависимостей AE2 15.4.10 не перечисляла GuideME, хотя Forge требует его. Источник: сообщение Forge от пользователя; обновлённый вручную профиль, по его словам, запускается, точные версии этого профиля неизвестны. RC4 ещё не проверен в игре.

## Эксперимент companions
Четыре точных Forge-файла 1.20.1 добавлены без изменения старых 159 пар projectID/fileID. TLM 1.5.3 необходим для Maid Action Expansion; Patchouli уже установлен. Источники и ограничения в COMPANIONS.md. Страницы метаданных не заменяют официальный API и проверку JAR. Monster Girl предупреждает о несовместимости сохранения после удаления; только отдельный мир до тестов.

## MCA
Шесть Forge 1.20.1 проектов; сохранены прежние 163 пары. Architectury уже в lock; добавлены связи зависимости от MCA. Источники, ограничения метаданных и отсутствующие проверки в MCA.md. Colony Integration исключён (1.21.1 NeoForge).

## Сбой при создании мира в MineColonies

Строка `minecolonies.FoodUtilsMixin ... hasBestOptionInInv2 ... (0/1) succeeded` указывает на сбой в MineColonies Tweaks 2.104 при работе с MineColonies 1.1.1318. MineColonies Compatibility 2.128 требует Tweaks через `META-INF/mods.toml`. В сборке закреплён [Tweaks 2.107 для Forge 1.20.1](https://www.curseforge.com/minecraft/mc-mods/minecolonies-tweaks/files/8600075). В этом JAR отсутствует проблемный миксин, что также подтверждено в [обсуждении ошибки у автора](https://github.com/gisellevonbingen-Minecraft/MineColonies_Tweaks/issues/96).

Для существующего экземпляра закройте игру и замените `MineColonies_Tweaks-1.20.1-2.104-all.jar` в папке `mods` на `MineColonies_Tweaks-1.20.1-2.107-all.jar`. В папке должен остаться один JAR Tweaks. Для первого запуска после обновления используйте новый тестовый мир.

Проверены метаданные и содержимое точных JAR-файлов зависимостей. Полный запуск Forge с обновлённым профилем требует игрового теста.
