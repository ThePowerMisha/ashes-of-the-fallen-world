# Графика и атмосфера
Основной профиль: Tectonic, Terralith, YUNG's, IDAS, Bons Voyage, Dungeons Arise, Towns and Towers. Клиент: Embeddium, Oculus, Entity Culling, ImmediatelyFast, ModernFix, FerriteCore. Звук: AmbientSounds и Sound Physics Remastered. From The Fog — отдельный источник хоррора, не замена Sculk Horde.

- `overrides/options.txt`: русский, 16 чанков, симуляция 8, лимит 120 FPS, гамма 0.45, частицы включены, облака Minecraft выключены, баланс громкости.
- `overrides/config/oculus.properties`: шейдер по умолчанию выбран, но выключен для надёжного первого старта. В меню Shader Packs включить Complementary Unbound r5.6.1, если он скачан CurseForge. Альтернативный файл `ashes_docs/graphics/oculus-atmospheric.properties` включает его. Для 3440×1440 и RX 7900 XT начать со среднего/высокого пресета, снижать тени и объёмное освещение при необходимости. Фактический FPS не измерен.
- Профиль Horizons — отдельный ZIP, Distant Horizons 2.4.1-b (https://www.curseforge.com/minecraft/mc-mods/distant-horizons/files/7334195), без Oculus и Complementary. Начать с 64–96 LOD-чанков, среднее качество; фактический FPS и совместимость не проверены. Не смешивать профили.
- Не добавлять OptiFine или второй движок рендера. Для проблем с рендером сначала отключить шейдер, затем локализовать причину по логу.
