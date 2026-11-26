"""Map every locked project to a playable route, a guide, or its role in the pack."""
import csv

ROUTE_PROJECTS = {
    '01_survival': 'waystones ftb-ultimine-forge',
    '04_magic': 'patchouli',
    '05_colony': 'ftb-teams-forge ftb-chunks-forge minecolonies',
    '13_create': 'create',
    '14_mekanism': 'mekanism mekanism-generators',
    '15_immersive': 'immersive-engineering industrial-foregoing',
    '16_storage': 'applied-energistics-2 sophisticated-backpacks sophisticated-storage functional-storage pipez',
    '17_power': 'powah-rearchitected flux-networks',
    '18_ars': 'ars-nouveau',
    '19_spells': 'irons-spells-n-spellbooks goety',
    '20_botania': 'botania',
    '22_bosses': 'born-in-chaos mowzies-mobs lendercataclysm the-graveyard-forge',
    '23_city': 'towntalk domum-ornamentum',
    '24_food': 'farmers-delight serene-seasons',
    '25_paladin': 'better-combat-by-daedelus',
    '27_engineer': 'mekanism-tools',
    '31_forge': 'artifacts relics-mod simply-swords apotheosis curios',
    '32_abyss': 'sculk-horde',
    '35_parkour': 'parcool',
    '36_colony_styles': 'stylecolonies smallcolonies smallcolonies-me minecolonies-tweaks minecolonies-compatibility colony-curios',
    '37_twilight': 'the-twilight-forest',
    '38_aircraft': 'immersive-aircraft',
    '39_field_manual': 'lootr jade guideme ftb-quests-forge villagerstradingplus corpse',
    '41_people': 'minecraft-comes-alive-reborn mca-quests mca-conversations mca-reputation mca-mob-compat mca-family-life '
                 'dwarfs-tyranny touhou-little-maid maid-action-expansion monster-girl custom-player-models',
    '42_workshops': 'chipped rechiseled framedblocks macaws-bridges macaws-roofs macaws-doors macaws-trapdoors '
                    'macaws-windows handcrafted decorative-blocks supplementaries amendments quark',
    '43_survey': 'tectonic terralith natures-compass explorers-compass xaeros-minimap xaeros-world-map '
                 'when-dungeons-arise towns-and-towers idas bons-voyage yungs-better-dungeons '
                 'yungs-better-mineshafts-forge yungs-better-strongholds '
                 'yungs-better-ocean-monuments yungs-better-nether-fortresses yungs-better-jungle-temples '
                 'yungs-better-end-island naturalist alexs-mobs enhanced-celestials from-the-fog',
    '44_homestead': 'lets-do-vinery appleskin',
    '45_networks': 'create-steam-n-rails',
}
GUIDES = {
    'Классы и характеристики, главы 11 и 39': 'puffish-skills puffish-attributes apothic-attributes',
    'Рецепты и интерфейс, глава 39': 'jei jei-integration just-enough-resources-jer just-enough-professions-jep '
                                    'just-enough-mekanism-multiblocks polymorph almost-unified mouse-tweaks',
    'Графика, справка GRAPHICS.md': 'oculus complementary-unbound bliss-shader complementary-reimagined solas-shader '
                                    'bsl-shaders distant-horizons turbo-for-distant-horizons ambientsounds sound-physics-remastered dynamiclights-reforged magnesium-extras',
    'Серверная диагностика, справка SERVER.md': 'spark',
}
INFRASTRUCTURE = {
    'Библиотеки и совместимость': 'playeranimator geckolib sophisticated-core selene rhino architectury-api balm '
        'creativecore glitchcore placebo lionfishapi lithostitched ftb-library-forge irons-lib citadel cloth-config '
        'titanium corgilib supermartijn642s-core-lib supermartijn642s-config-lib structurize blockui multi-piston '
        'cristel-lib yungs-api athena resourceful-lib kotlin-for-forge puzzles-lib caelus resourceful-config '
        'shatterbyte-lib terrablender integrated-api zeta sodium-options-api do-api fusion-connected-textures '
        'ftb-filter-system ftb-xmod-compat',
    'Производительность': 'modernfix embeddium ferritecore entityculling immediatelyfast clumps',
    'Сценарии, предметы и таблицы добычи сборки': 'kubejs lootjs',
    'Исправление подсчёта предметов FTB Quests 2001.4.22': 'dreadhollow-quest-count-fix',
}


def write_coverage(root, chapters):
    titles = {slug: title for slug, title, *_ in chapters}
    rows = {}
    for groups, kind in ((ROUTE_PROJECTS, 'Игровая цепочка'),
                         (GUIDES, 'Справка'), (INFRASTRUCTURE, 'Служебная роль')):
        for destination, projects in groups.items():
            for slug in projects.split():
                assert slug not in rows, slug
                rows[slug] = (kind, titles.get(destination, destination))
    with (root / 'overrides/ashes_docs/mods-lock.tsv').open(encoding='utf-8') as data:
        locked = {row['slug'] for row in csv.DictReader(data, delimiter='\t')}
    assert rows.keys() == locked, (sorted(locked - rows.keys()), sorted(rows.keys() - locked))
    report = ['# Покрытие модов в книге заданий', '',
              'Цепочки объединяют совместимые механики. Служебные библиотеки и оптимизации указаны по их роли.',
              '', '| Проект | Где искать | Глава или связанная справка |', '| --- | --- | --- |']
    report.extend(f'| `{slug}` | {kind} | {dest} |' for slug, (kind, dest) in sorted(rows.items()))
    content = '\n'.join(report) + '\n'
    for folder in ('docs', 'overrides/ashes_docs'):
        (root / folder / 'QUEST_COVERAGE.md').write_text(content, encoding='utf-8')
