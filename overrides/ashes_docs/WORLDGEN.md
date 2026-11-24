# Мир и геология RC3

Tectonic 3.0.17 + Terralith остаются единственной основной системой рельефа. В config/tectonic.json: continental scale 0.10 вместо 0.13, erosion 0.17 вместо 0.25, ridge 0.19 вместо 0.25, temperature 0.17 и vegetation 0.16 вместо 0.25. Меньший масштаб шума означает более протяжённые климатические зоны и горные формы; vertical_scale 1.18, elevation_boost 0.1, flat_terrain_skew 0.18 для мест строительства. Границы Y не изменены, ultrasmooth отключён. Смещение ванильного монумента отключено, потому что установлен YUNG's Better Ocean Monuments. Сочетание с Terralith и конкретные размеры биомов требуют проверки на нескольких сидах.

## Ванильные жилы

| Configured feature | Было | Стало |
|---|---:|---:|
| ore_coal | 17 | 24 |
| ore_coal_buried | 17 | 24 |
| ore_iron | 9 | 15 |
| ore_iron_small | 4 | 7 |
| ore_gold | 9 | 12 |
| ore_gold_buried | 9 | 12 |
| ore_copper_small | 10 | 15 |
| ore_copper_large | 20 | 28 |
| ore_lapis | 7 | 10 |
| ore_lapis_buried | 7 | 10 |
| ore_redstone | 8 | 12 |
| ore_diamond_small | 4 | 6 |
| ore_diamond_large | 12 | 16 |
| ore_diamond_buried | 8 | 11 |
| ore_emerald | 3 | 4 |

Переопределены только configured features Minecraft 1.20.1 (сверены с misode/mcmeta 1.20.1-data), сохранены целевые теги пород и вероятность отбрасывания открытой руды. Частота размещения и высоты не изменены; size — максимальный параметр кластера, не гарантированное число блоков. Если Terralith использует собственные configured features, они не изменяются. Не добавляем вторую независимую генерацию тех же руд.

## Mekanism

| Vein | Было | Стало |
|---|---:|---:|
| tin.small | 4 | 6 |
| tin.large | 9 | 14 |
| osmium.upper | 7 | 10 |
| osmium.middle | 9 | 14 |
| osmium.small | 4 | 6 |
| uranium.small | 4 | 5 |
| uranium.buried | 9 | 12 |
| fluorite.normal | 5 | 7 |
| fluorite.buried | 13 | 18 |
| lead.normal | 9 | 14 |

Путь config/Mekanism/world.toml подтверждён исходным кодом 1.20.x (MekanismModConfig, WorldConfig, OreType). Остальные параметры сохраняют значения мода, retrogen отключён. Руды других модов не переписаны без подтверждения схем.

Только новые чанки; для чистых границ рекомендуется новый мир. Перед запуском сервера проверить datapack registry, генерацию на нескольких сидах, наличие сооружений и выход руд. Изменения не проверены в игре.
