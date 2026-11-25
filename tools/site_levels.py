"""Terraced site layouts selected by the world's existing jigsaw pools."""
from dataclasses import dataclass
from itertools import pairwise
from random import Random

from site_terrain import LAND_DEPTH

VARIANTS = 6
FLOOR_RESERVE = 3
EDGE_RESERVE = 6
BURIAL_RESERVE = 5

DIRECTIONS = {
    'north': (0, -1, 'south'),
    'south': (0, 1, 'north'),
    'west': (-1, 0, 'east'),
    'east': (1, 0, 'west'),
}


@dataclass(frozen=True)
class Terrace:
    bounds: tuple
    entrance: tuple
    outward: str = 'north'

    def approach(self, rise):
        x, z = self.entrance
        dx, dz, _ = DIRECTIONS[self.outward]
        return [(x + dx * distance, z + dz * distance) for distance in range(abs(rise) + 2)]

    def columns(self):
        x0, z0, x1, z1 = self.bounds
        return {(x, z) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1)}


def house(x, z, door, width=8, length=8):
    return Terrace((x, z, x + width - 1, z + length - 1), (door, z))


TERRACES = {
    'silent_hamlet': tuple(house(x, z, x + 3) for x, z in ((3, 3), (20, 3), (3, 20), (20, 20))),
    'surviving_hamlet': (house(3, 4, 6), house(19, 4, 22), house(3, 19, 6),
                         Terrace((19, 18, 26, 26), (19, 22), 'west')),
    'infected_hamlet': (house(3, 4, 6), house(17, 5, 20), house(5, 19, 8, 7, 7)),
    'last_stand': tuple(
        Terrace((x, z, x + 6, z + 3), (x + (3 if z == 5 else 2), z + 3 if z == 5 else z), 'south' if z == 5 else 'north')
        for x, z in ((3, 5), (18, 5), (3, 20), (18, 20))
    ),
    'nameless_graves': (Terrace((5, 5, 6, 19), (6, 7), 'east'),
                        Terrace((14, 5, 15, 19), (14, 15), 'west')),
    'three_seals_altar': (Terrace((6, 6, 10, 11), (10, 9), 'east'),),
    'broken_watch': (Terrace((3, 3, 13, 13), (8, 3)),),
    'sealed_archive': (Terrace((2, 2, 18, 18), (10, 2)),),
    'fallen_capital': (house(4, 9, 8, 7), house(34, 9, 37, 7), house(4, 26, 7, 7),
                       house(34, 26, 38, 7), Terrace((16, 27, 28, 36), (22, 27))),
    'mechanists_keep': (Terrace((8, 12, 13, 25), (11, 12)),
                        Terrace((19, 12, 24, 25), (21, 12))),
    'keepers_keep': (Terrace((8, 10, 13, 20), (11, 10)),
                     Terrace((19, 10, 24, 20), (22, 10))),
    'archmages_keep': (Terrace((8, 11, 13, 23), (11, 11)),
                       Terrace((20, 11, 24, 23), (22, 11)),
                       Terrace((14, 20, 18, 24), (16, 20))),
    'abyss_temple': (Terrace((10, 22, 18, 25), (13, 22)),),
    'drowned_city': tuple(
        Terrace((x, z, x + 9, z + 9), (x + 9 if x == 4 else x, z + (4 if x == 4 else 6)),
                'east' if x == 4 else 'west')
        for x, z in ((4, 8), (25, 8), (4, 24), (25, 24))
    ),
    'observatory': (Terrace((2, 2, 20, 20), (11, 2)),),
}


def level_layouts(slug):
    """Distinct reproducible offsets. The game selects a layout using its world RNG."""
    if slug not in TERRACES:
        return [(depth,) for depth in (2, 4, 0, 3, 5, 1)]
    count = len(TERRACES[slug])
    if count == 1:
        return [(rise,) for rise in (3, 5, -2, 6, 4, -3)]

    rng = Random('ashes:terraces:' + slug)
    layouts = []
    while len(layouts) < VARIANTS:
        rises = rng.choices((-3, -2, 2, 3, 4, 5, 6), k=count)
        if min(rises) < 0 < max(rises) and tuple(rises) not in layouts:
            layouts.append(tuple(rises))
    return layouts


def shift_vertically(build, offset):
    build.blocks = {(x, y + offset, z): block for (x, y, z), block in build.blocks.items()}
    for entity in build.entities:
        entity['pos'][1] += offset
        entity['blockPos'][1] += offset


def terraform_levels(build, site, rises):
    sea = site.biomes == 'deep_ocean'
    original_floor = 2 + (0 if sea else LAND_DEPTH)
    floor = original_floor + FLOOR_RESERVE
    sections = TERRACES[site.slug]
    columns = {}
    for section, rise in zip(sections, rises, strict=True):
        assert not (columns.keys() & section.columns()), site.slug
        columns.update(dict.fromkeys(section.columns(), rise))

    width, height, length = build.size
    build.size = (width + 2 * EDGE_RESERVE, height + FLOOR_RESERVE + max(0, *rises),
                  length + 2 * EDGE_RESERVE)
    original = build.blocks
    build.blocks = {
        (x + EDGE_RESERVE, y + FLOOR_RESERVE + columns.get((x, z), 0), z + EDGE_RESERVE): block
        for (x, y, z), block in original.items()
    }
    for entity in build.entities:
        x, _, z = entity['blockPos']
        offsets = (EDGE_RESERVE, FLOOR_RESERVE + columns.get((x, z), 0), EDGE_RESERVE)
        for key in ('pos', 'blockPos'):
            entity[key] = [value + offset for value, offset in zip(entity[key], offsets, strict=True)]

    masonry = 'prismarine_bricks' if sea else 'deepslate_bricks' if build.style else 'stone_bricks'
    stairs = {'prismarine_bricks': 'prismarine_brick_stairs',
              'deepslate_bricks': 'deepslate_brick_stairs', 'stone_bricks': 'stone_brick_stairs'}[masonry]
    empty = 'water' if sea else 'air'
    for (x, z), rise in sorted(columns.items()):
        if (x, original_floor, z) not in original:
            continue
        bx, bz = x + EDGE_RESERVE, z + EDGE_RESERVE
        if rise > 0:
            # Extend retaining foundations down to the original floor.
            for y in range(floor - 2, floor + rise):
                if (bx, y, bz) not in build.blocks:
                    build.put(bx, y, bz, masonry)
        else:
            for y in range(floor + rise + 1, floor + 2):
                if (bx, y, bz) not in build.blocks:
                    build.put(bx, y, bz, empty)

    routes = []
    for section, rise in zip(sections, rises, strict=True):
        route = join_terrace(build, section, rise, floor, masonry, stairs, empty, columns, site.slug)
        routes.append(route)
    return routes


def join_terrace(build, section, rise, floor, masonry, stairs, empty, columns, slug):
    _, _, inward = DIRECTIONS[section.outward]
    # Top half of each stair faces uphill. The landing is level with the main site.
    route = []
    for distance, col in enumerate(section.approach(rise)):
        bx, bz = (value + EDGE_RESERVE for value in col)
        if distance == 0:
            y = floor + rise
            assert build.blocks[bx, y, bz][0]['Name'] not in ('minecraft:air', 'minecraft:water'), (slug, col)
            for layer in (y + 1, y + 2):
                assert not build.blocks.get((bx, layer, bz), (None, None))[1], (slug, col)
                build.put(bx, layer, bz, empty)
            route.append((bx, y, bz))
            continue
        assert col not in columns, (slug, section, col)
        is_stair = distance <= abs(rise)
        y = floor + (max(rise - distance + 1, 0) if rise > 0 else min(rise + distance, 0))
        route.append((bx, y, bz))
        for layer in range(min(floor - 2, y - 1), y):
            if (bx, layer, bz) not in build.blocks or build.blocks[bx, layer, bz][0]['Name'] == 'minecraft:air':
                build.put(bx, layer, bz, masonry)
        assert all(not build.blocks.get((bx, layer, bz), (None, None))[1]
                   for layer in range(y, y + 4)), (slug, bx, y, bz)
        if is_stair:
            build.put(bx, y, bz, stairs, {
                'facing': inward if rise > 0 else section.outward,
                'half': 'bottom', 'shape': 'straight', 'waterlogged': str(empty == 'water').lower(),
            })
        else:
            build.put(bx, y, bz, masonry)
        for layer in range(y + 1, y + 4):
            build.put(bx, layer, bz, empty)
    assert all(abs(first[1] - second[1]) <= 1 for first, second in pairwise(route)), (slug, route)
    return route
