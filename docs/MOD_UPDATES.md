# Обновление модов Minecraft 1.20.1 Forge

Сверка каталога CurseForge от 24 ноября 2026 года после закрепления TerraBlender 3.0.1.10 и Vinery 1.4.41. Повторить её можно командой `python tools/audit_updates.py --include-beta`. Без флага команда ищет только релизы. Учитываются метки файлов. Совместимость внутри сборки проверяется по зависимостям JAR и игровому запуску.


Из 170 проектов найдено 53 модов с более свежим файлом, из них 44 релиза и 9 бета-версий. Для 103 модов более свежий файл с обеими метками не найден. 5 шейдерпаков исключены из этой сверки.

Страницу файлов или метки не удалось подтвердить для `architectury-api`, `spark`, `lootr`, `glitchcore`, `cristel-lib`, `resourceful-lib`, `resourceful-config`, `clumps`, `appleskin`.

## Связанные обновления

- Для MineColonies тестировать вместе Compatibility, Tweaks, Structurize, BlockUI, Multi-Piston и Domum Ornamentum. У ряда компонентов новейший файл — snapshot. Проверить создание нового мира, запуск встроенного сервера и рецепты колонии.
- Для MCA Reborn сверять все пять аддонов. В таблице MCA 7.7 — beta, а текущий Family Life предназначен для 7.6.
- Для обновления Distant Horizons повторить тест и в Horizons, и в профиле с Oculus. Проверить загрузку карты и формирование LOD.
- Simply Swords 1.70.2 добавляет обязательные Fzzy Config и Simply Tooltips. Enhanced Celestials 5.0.3.3 требует Data Anchor. Puzzles Lib из списка требует Puzzles Access API. Эти зависимости видны в Forge-метаданных скачанных кандидатов.
- Проверять парами или группами Iron’s Spells и Iron’s Lib, Supplementaries и Moonlight, а также Sophisticated Core, Backpacks и Storage.

## Файлы для проверки

| Мод | Закреплённый файл | Более свежий файл | Тип |
|---|---|---|---|
| apotheosis | `Apotheosis-1.20.1-7.4.2.jar` | [`Apotheosis-1.20.1-7.4.8.jar`](https://www.curseforge.com/minecraft/mc-mods/apotheosis/files/6461960) | релиз |
| applied-energistics-2 | `appliedenergistics2-forge-15.4.10.jar` | [`appliedenergistics2-forge-15.4.12.jar`](https://www.curseforge.com/minecraft/mc-mods/applied-energistics-2/files/9357405) | релиз |
| artifacts | `artifacts-forge-9.5.19.jar` | [`artifacts-forge-9.5.20.jar`](https://www.curseforge.com/minecraft/mc-mods/artifacts/files/9773756) | релиз |
| blockui | `blockui-1.20.1-1.0.193.jar` | [`blockui-1.20.1-1.0.194-snapshot.jar`](https://www.curseforge.com/minecraft/mc-mods/blockui/files/7606230) | beta |
| botania | `Botania-1.20.1-450-FORGE.jar` | [`Botania-1.20.1-456-FORGE.jar`](https://www.curseforge.com/minecraft/mc-mods/botania/files/8901969) | релиз |
| chipped | `Chipped-forge-1.20.1-3.0.6.jar` | [`chipped-forge-1.20.1-3.0.7.jar`](https://www.curseforge.com/minecraft/mc-mods/chipped/files/5813138) | релиз |
| corgilib | `Corgilib-Forge-1.20.1-4.0.3.0.jar` | [`Corgilib-Forge-1.20.1-4.0.3.6.jar`](https://www.curseforge.com/minecraft/mc-mods/corgilib/files/9113598) | релиз |
| create-steam-n-rails | `Steam_Rails-1.7.2+forge-mc1.20.1.jar` | [`Steam_Rails-1.7.3+forge-mc1.20.1.jar`](https://www.curseforge.com/minecraft/mc-mods/create-steam-n-rails/files/8745475) | релиз |
| creativecore | `CreativeCore_FORGE_v2.12.40_mc1.20.1.jar` | [`CreativeCore_FORGE_v2.12.42_mc1.20.1.jar`](https://www.curseforge.com/minecraft/mc-mods/creativecore/files/9542632) | релиз |
| decorative-blocks | `decorative_blocks-forge-1.20.1-4.1.1.jar` | [`decorative_blocks-forge-1.20.1-4.1.3.jar`](https://www.curseforge.com/minecraft/mc-mods/decorative-blocks/files/5089406) | релиз |
| distant-horizons | `DistantHorizons-3.1.2-b-1.20.1-fabric-forge.jar` | [`DistantHorizons-3.3.3-1.20.1-fabric-forge.jar`](https://www.curseforge.com/minecraft/mc-mods/distant-horizons/files/9004753) | релиз |
| domum-ornamentum | `domum_ornamentum-1.20.1-1.0.296-universal.jar` | [`domum_ornamentum-1.20.1-1.0.304-snapshot-universal.jar`](https://www.curseforge.com/minecraft/mc-mods/domum-ornamentum/files/8765962) | beta |
| enhanced-celestials | `Enhanced_Celestials-forge-1.20.1-5.0.0.4.jar` | [`Enhanced-Celestials-forge-1.20.1-5.0.3.3.jar`](https://www.curseforge.com/minecraft/mc-mods/enhanced-celestials/files/8592325) | релиз |
| entityculling | `entityculling-forge-1.11.3-mc1.20.1.jar` | [`entityculling-forge-1.12.2-mc1.20.1.jar`](https://www.curseforge.com/minecraft/mc-mods/entityculling/files/9752253) | релиз |
| farmers-delight | `FarmersDelight-1.20.1-1.3.1.jar` | [`FarmersDelight-1.20.1-1.3.4.jar`](https://www.curseforge.com/minecraft/mc-mods/farmers-delight/files/8765179) | релиз |
| ftb-chunks-forge | `ftb-chunks-forge-2001.3.1.jar` | [`ftb-chunks-forge-2001.3.8.jar`](https://www.curseforge.com/minecraft/mc-mods/ftb-chunks-forge/files/8216874) | релиз |
| ftb-ultimine-forge | `ftb-ultimine-forge-2001.1.5.jar` | [`ftb-ultimine-forge-2001.1.8.jar`](https://www.curseforge.com/minecraft/mc-mods/ftb-ultimine-forge/files/7880472) | релиз |
| functional-storage | `functionalstorage-1.20.1-1.2.13.jar` | [`functionalstorage-1.20.1-1.2.14.jar`](https://www.curseforge.com/minecraft/mc-mods/functional-storage/files/8412552) | beta |
| geckolib | `geckolib-forge-1.20.1-4.8.4.jar` | [`geckolib-forge-1.20.1-4.8.5.jar`](https://www.curseforge.com/minecraft/mc-mods/geckolib/files/9730442) | релиз |
| goety | `goety-2.5.53.1.jar` | [`goety-2.5.60.6.jar`](https://www.curseforge.com/minecraft/mc-mods/goety/files/9474033) | релиз |
| immediatelyfast | `ImmediatelyFast-1.2.4+1.20.1.jar` | [`ImmediatelyFast-Forge-1.5.5+1.20.4.jar`](https://www.curseforge.com/minecraft/mc-mods/immediatelyfast/files/8348481) | релиз |
| immersive-aircraft | `immersive_aircraft-1.4.1+1.20.1-forge.jar` | [`immersive_aircraft-1.5.0+1.20.1-forge.jar`](https://www.curseforge.com/minecraft/mc-mods/immersive-aircraft/files/8865821) | релиз |
| industrial-foregoing | `industrial-foregoing-1.20.1-3.5.19.jar` | [`industrial-foregoing-1.20.1-3.5.28.jar`](https://www.curseforge.com/minecraft/mc-mods/industrial-foregoing/files/9664707) | beta |
| integrated-api | `integrated_api-forge-1.20.1-1.9.1.jar` | [`integrated_api-forge-1.20.1-1.9.2.jar`](https://www.curseforge.com/minecraft/mc-mods/integrated-api/files/9552187) | релиз |
| irons-lib | `irons_lib-1.20.1-1.1.0.jar` | [`irons_lib-1.20.1-2.4.0.jar`](https://www.curseforge.com/minecraft/mc-mods/irons-lib/files/9687937) | релиз |
| irons-spells-n-spellbooks | `irons_spellbooks-1.20.1-3.16.1.jar` | [`irons_spellbooks-1.20.1-3.16.4.jar`](https://www.curseforge.com/minecraft/mc-mods/irons-spells-n-spellbooks/files/9702213) | релиз |
| jade | `Jade-1.20.1-Forge-11.13.2.jar` | [`Jade-1.20.1-Forge-11.13.3.jar`](https://www.curseforge.com/minecraft/mc-mods/jade/files/8479276) | релиз |
| jei | `jei-1.20.1-forge-15.74.0.234.jar` | [`jei-1.20.1-forge-15.75.0.242.jar`](https://www.curseforge.com/minecraft/mc-mods/jei/files/9749863) | beta |
| just-enough-mekanism-multiblocks | `JustEnoughMekanismMultiblocks-1.20.1-4.18.jar` | [`JustEnoughMekanismMultiblocks-1.20.1-4.27.jar`](https://www.curseforge.com/minecraft/mc-mods/just-enough-mekanism-multiblocks/files/9068209) | релиз |
| kotlin-for-forge | `kotlinforforge-4.12.0-all.jar` | [`kotlinforforge-4.13.0-all.jar`](https://www.curseforge.com/minecraft/mc-mods/kotlin-for-forge/files/9695363) | релиз |
| lithostitched | `lithostitched-forge-1.20.1-1.4.11.jar` | [`lithostitched-forge-1.20.1-1.4.12.jar`](https://www.curseforge.com/minecraft/mc-mods/lithostitched/files/9486341) | релиз |
| macaws-bridges | `mcw-bridges-3.0.0-mc1.20.1forge.jar` | [`mcw-bridges-3.1.2-mc1.20.1forge.jar`](https://www.curseforge.com/minecraft/mc-mods/macaws-bridges/files/7627954) | релиз |
| macaws-roofs | `mcw-roofs-2.3.1-mc1.20.1forge.jar` | [`mcw-roofs-2.3.2-mc1.20.1forge.jar`](https://www.curseforge.com/minecraft/mc-mods/macaws-roofs/files/6494466) | релиз |
| mca-family-life | `mcafamilylife-0.3.0+1.20.1-mca7.6.jar` | [`mcafamilylife-0.3.0-1.20.1.jar`](https://www.curseforge.com/minecraft/mc-mods/mca-family-life/files/9495197) | релиз |
| minecolonies | `minecolonies-1.20.1-1.1.1318.jar` | [`minecolonies-1.20.1-1.1.1323-snapshot.jar`](https://www.curseforge.com/minecraft/mc-mods/minecolonies/files/9770027) | beta |
| minecolonies-compatibility | `MineColonies_Compatibility-1.20.1-2.128.jar` | [`MineColonies_Compatibility-1.20.1-2.143.jar`](https://www.curseforge.com/minecraft/mc-mods/minecolonies-compatibility/files/9454731) | beta |
| minecraft-comes-alive-reborn | `minecraft-comes-alive-7.6.26+1.20.1-universal.jar` | [`minecraft-comes-alive-7.7.1-beta.6-1.20.1-universal.jar`](https://www.curseforge.com/minecraft/mc-mods/minecraft-comes-alive-reborn/files/9616432) | beta |
| modernfix | `modernfix-forge-5.27.91+mc1.20.1.jar` | [`modernfix-forge-5.28.8-mc1.20.1.jar`](https://www.curseforge.com/minecraft/mc-mods/modernfix/files/9791665) | релиз |
| multi-piston | `multipiston-1.20-1.2.43-RELEASE.jar` | [`multipiston-1.20-0.0.47-snapshot.jar`](https://www.curseforge.com/minecraft/mc-mods/multi-piston/files/7097889) | beta |
| parcool | `ParCool-1.20.1-3.4.3.3.jar` | [`ParCool-1.20.1-4.0.2.0.jar`](https://www.curseforge.com/minecraft/mc-mods/parcool/files/9415747) | релиз |
| puffish-attributes | `puffish_attributes-0.8.2-1.20-forge.jar` | [`puffish_attributes-0.8.4-1.20-forge.jar`](https://www.curseforge.com/minecraft/mc-mods/puffish-attributes/files/9780067) | релиз |
| puzzles-lib | `PuzzlesLib-v8.1.33-1.20.1-Forge.jar` | [`PuzzlesLib-v8.1.36-1.20.1-Forge.jar`](https://www.curseforge.com/minecraft/mc-mods/puzzles-lib/files/9130247) | релиз |
| rechiseled | `rechiseled-1.1.6-forge-mc1.20.jar` | [`rechiseled-1.2.6-forge-mc1.20.1.jar`](https://www.curseforge.com/minecraft/mc-mods/rechiseled/files/8875661) | релиз |
| selene | `moonlight-1.20-2.16.34-forge.jar` | [`moonlight-1.20-2.16.39-forge.jar`](https://www.curseforge.com/minecraft/mc-mods/selene/files/9493250) | релиз |
| simply-swords | `simplyswords-forge-1.56.0-1.20.1.jar` | [`simplyswords-forge-neoforge-1.70.2-1.20.1.jar`](https://www.curseforge.com/minecraft/mc-mods/simply-swords/files/8746028) | релиз |
| sophisticated-backpacks | `sophisticatedbackpacks-1.20.1-3.24.35.1675.jar` | [`sophisticatedbackpacks-1.20.1-3.26.22.2264.jar`](https://www.curseforge.com/minecraft/mc-mods/sophisticated-backpacks/files/9758729) | релиз |
| sophisticated-core | `sophisticatedcore-1.20.1-1.3.21.1676.jar` | [`sophisticatedcore-1.20.1-1.5.40.2493.jar`](https://www.curseforge.com/minecraft/mc-mods/sophisticated-core/files/9758584) | релиз |
| sophisticated-storage | `sophisticatedstorage-1.20.1-1.4.39.1666.jar` | [`sophisticatedstorage-1.20.1-1.5.19.2243.jar`](https://www.curseforge.com/minecraft/mc-mods/sophisticated-storage/files/9692993) | релиз |
| stylecolonies | `stylecolonies-1.20.1-1.15.63.jar` | [`stylecolonies-1.20.1-1.15.91.jar`](https://www.curseforge.com/minecraft/mc-mods/stylecolonies/files/9447135) | релиз |
| supplementaries | `supplementaries-1.20-3.1.43-forge.jar` | [`supplementaries-1.20-3.1.45-forge.jar`](https://www.curseforge.com/minecraft/mc-mods/supplementaries/files/9635391) | релиз |
| titanium | `titanium-1.20.1-3.8.32.jar` | [`titanium-1.20.1-3.8.37.jar`](https://www.curseforge.com/minecraft/mc-mods/titanium/files/9441193) | релиз |
| villagerstradingplus | `villagertradingplus-forge-mc1.20.1-1.1.0.jar` | [`villagertradingplus-forge-mc1.20.1-1.1.1.jar`](https://www.curseforge.com/minecraft/mc-mods/villagerstradingplus/files/9346742) | релиз |
| when-dungeons-arise | `DungeonsArise-1.20.1-2.1.57-release.jar` | [`DungeonsArise-1.20.x-2.1.58-release.jar`](https://www.curseforge.com/minecraft/mc-mods/when-dungeons-arise/files/4983862) | релиз |

## Тестовая ветка rc5-mod-updates.1

Обновлены 36 релизов из каталога. Состав и номера файлов этой ветки перечислены в `overrides/ashes_docs/mods-lock.tsv`. В списке выше колонка «Закреплённый файл» относится к `main` на момент сверки. Для новой версии создайте отдельный профиль и тестовый мир.

Ветка включает обновления следующих проектов.

`apotheosis`, `applied-energistics-2`, `artifacts`, `botania`, `chipped`, `corgilib`, `create-steam-n-rails`, `creativecore`, `decorative-blocks`, `entityculling`, `farmers-delight`, `ftb-chunks-forge`, `ftb-ultimine-forge`, `geckolib`, `goety`, `immersive-aircraft`, `integrated-api`, `irons-lib`, `irons-spells-n-spellbooks`, `jade`, `just-enough-mekanism-multiblocks`, `lithostitched`, `macaws-bridges`, `macaws-roofs`, `modernfix`, `puffish-attributes`, `rechiseled`, `selene`, `sophisticated-backpacks`, `sophisticated-core`, `sophisticated-storage`, `stylecolonies`, `supplementaries`, `titanium`, `villagerstradingplus`, `when-dungeons-arise`.
