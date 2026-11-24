"""Architecture of the sites added to Ashes after the first six ruins."""

LANTERN = {'hanging': 'false', 'waterlogged': 'false'}
RAILING = {'waterlogged': 'false'}


def terrace(b, x0, z0, x1, z1, block, y=2):
    b.fill(x0, y, z0, x1, y, z1, block)
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if x in (x0, x1) or z in (z0, z1) or (x % 4 == 0 and z % 4 == 0):
                b.fill(x, 0, z, x, y - 1, z, block)


def arch(b, x, y, z, stone, span=5):
    for edge in (x, x + span - 1):
        b.fill(edge, y, z, edge, y + 3, z, stone)
    b.put(x + 1, y + 3, z, stone)
    b.put(x + span - 2, y + 3, z, stone)
    b.fill(x + 1, y + 4, z, x + span - 2, y + 4, z, stone)


def light(b, x, y, z, soul=False):
    b.put(x, y, z, 'soul_lantern' if soul else 'lantern', LANTERN)


def steps(b, x0, x1, y, z, length, material='stone_brick'):
    # The north end is the lower end. Ascend to the south.
    for distance in range(length):
        rise, row = y + distance, z + distance
        b.fill(x0, rise, row, x1, rise, row, material + '_stairs', {
            'facing': 'south', 'half': 'bottom', 'shape': 'straight', 'waterlogged': 'false'
        })
        b.fill(x0, rise + 1, row, x1, rise + 3, row, 'air')


def fallen_capital(b):
    stone = 'stone_bricks' if b.style == 0 else 'deepslate_bricks'
    terrace(b, 12, 6, 32, 35, stone)
    b.path(19, 1, 25, 42)
    b.path(3, 18, 41, 22)
    for x, z, door in ((4, 9, 8), (34, 9, 37), (4, 26, 7), (34, 26, 38)):
        b.house(x, z, x + 6, z + 7, door, roof=(z == (9 if b.style else 26)))
    for z in (8, 26):
        for x in (13, 26):
            arch(b, x, 3, z, stone)
    for x in (15, 29):
        for z in range(11, 19, 3):
            b.pillar(x, z, b.r.randint(2, 5))
    terrace(b, 16, 27, 28, 36, stone, y=3)
    for x in range(16, 29):
        top = b.r.randint(6, 11)
        b.fill(x, 4, 36, x, top, 36, stone)
        if x % 3 == 0:
            b.put(x, top, 36, 'gilded_blackstone')
    arch(b, 19, 4, 28, 'polished_andesite', 7)
    b.put(22, 4, 33, 'lectern', {'facing': 'north', 'has_book': 'false', 'powered': 'false'})
    b.chest(20, 4, 34, 'fallen_capital')
    b.chest(36, 3, 31, 'fallen_capital', supplies=True)
    for x in (20, 24):
        b.put(x, 3, 22, 'create:copper_casing')
        light(b, x, 4, 22)
    b.fill(21, 2, 25, 23, 2, 25, 'create:industrial_iron_block')


def citadel(b, primary, accent):
    terrace(b, 4, 4, 28, 28, primary)
    b.fill(5, 3, 5, 27, 5, 27, 'air')
    for x in range(4, 29):
        for z in range(4, 29):
            if (x in (4, 28) or z in (4, 28)) and not (z == 4 and 14 <= x <= 18):
                b.fill(x, 3, z, x, b.r.randint(5, 7), z, primary)
                if (x + z) % 6 == 0:
                    b.put(x, 4, z, accent)
    arch(b, 13, 3, 4, primary, 7)
    for x,z in ((5, 5), (25, 5), (5, 25), (25, 25)):
        b.fill(x, 3, z, x + 2, 7 + (x + z) % 3, z + 2, primary)
        b.put(x + 1, 6, z, accent)


def mechanists_keep(b):
    citadel(b, 'polished_andesite' if b.style == 0 else 'deepslate_bricks',
            'create:industrial_iron_block')
    for z in (13, 19, 25):
        arch(b, 9, 3, z, 'create:andesite_casing', span=5)
        arch(b, 19, 3, z, 'create:andesite_casing', span=5)
    for x in (10, 20):
        b.fill(x, 8, 13, x + 2, 8, 25, 'immersiveengineering:treated_wood_horizontal')
    for x in range(9, 24):
        b.put(x, 2, 23, 'create:industrial_iron_block')
        if x % 3 == 0:
            b.put(x, 3, 24, 'immersiveengineering:coil_lv')
    b.fill(15, 3, 25, 17, 9, 28, 'bricks')
    b.fill(16, 7, 25, 16, 12, 26, 'bricks')
    b.put(16, 3, 24, 'blast_furnace', {'facing': 'north', 'lit': 'false'})
    b.chest(16, 3, 20, 'mechanists_keep')
    b.chest(22, 3, 23, 'mechanists_keep', supplies=True)


def keepers_keep(b):
    citadel(b, 'mossy_stone_bricks' if b.style == 0 else 'tuff', 'botania:livingrock')
    for x0,x1 in ((8, 13), (19, 24)):
        b.fill(x0, 2, 10, x1, 2, 20, 'farmersdelight:rich_soil')
        for x in (x0, x1):
            for z in (10, 15, 20):
                b.fill(x, 3, z, x, 6, z, 'botania:livingwood', {'axis': 'y'})
                b.put(x, 7, z, 'azalea_leaves', {'distance': '7', 'persistent': 'true', 'waterlogged': 'false'})
        for z in (11, 14, 17):
            b.put(x0 + 2, 3, z, 'azalea')
            b.put(x1 - 2, 3, z, 'flowering_azalea')
    for x in (11, 19):
        arch(b, x, 3, 23, 'botania:livingrock')
    b.put(16, 3, 23, 'composter', {'level': '0'})
    b.chest(16, 3, 26, 'keepers_keep')
    b.chest(10, 3, 24, 'keepers_keep', supplies=True)


def archmages_keep(b):
    citadel(b, 'polished_blackstone_bricks' if b.style == 0 else 'deepslate_bricks',
            'ars_nouveau:sourcestone')
    for x in (9, 22):
        for z in (12, 22):
            b.fill(x, 3, z, x + 1, 9, z + 1, 'ars_nouveau:sourcestone')
            b.put(x, 10, z, 'ars_nouveau:source_gem_block')
            b.put(x + 1, 10, z + 1, 'amethyst_cluster', {'facing': 'up', 'waterlogged': 'false'})
    for x,z in ((12, 15), (20, 15), (12, 19), (20, 19)):
        b.fill(x, 3, z, x, 5, z, 'bookshelf')
    b.fill(14, 3, 20, 18, 3, 24, 'ars_nouveau:sourcestone')
    b.put(16, 4, 23, 'lectern', {'facing': 'north', 'has_book': 'false', 'powered': 'false'})
    arch(b, 14, 4, 24, 'ars_nouveau:sourcestone')
    b.chest(16, 4, 22, 'archmages_keep')
    b.chest(22, 3, 19, 'archmages_keep', supplies=True)


def underground_room(b, x0, z0, x1, z1, floor, wall, height=5):
    b.fill(x0, floor, z0, x1, floor + height, z1, wall)
    b.fill(x0 + 1, floor + 1, z0 + 1, x1 - 1, floor + height - 1, z1 - 1, 'air')


def buried_entrance(b, x0, x1, bottom, first_row, length, stone):
    z = first_row + length
    top = bottom + length
    b.fill(x0 - 1, top, z, x1 + 1, top, z + 3, stone)
    b.fill(x0, top + 1, z, x1, top + 3, z + 4, 'air')
    arch(b, x0 - 1, top + 1, z + 1, stone, x1 - x0 + 3)
    for x in (x0 - 1, x1 + 1):
        for rise in range(length):
            b.fill(x, bottom + rise, first_row + rise, x,
                   bottom + rise + 2, first_row + rise, stone)
    steps(b, x0, x1, bottom, first_row, length)


def limit_lab(b):
    stone = 'deepslate_tiles' if b.style == 0 else 'polished_deepslate'
    underground_room(b, 4, 3, 26, 18, 2, stone, 7)
    for x in (7, 22):
        for z in (7, 14):
            b.fill(x, 3, z, x + 1, 4, z + 1, 'create:industrial_iron_block')
            b.put(x, 5, z, 'immersiveengineering:coil_lv')
            b.put(x + 1, 5, z + 1, 'create:brass_casing')
    b.fill(13, 3, 7, 17, 3, 11, 'create:andesite_casing')
    for y,block in ((4, 'ars_nouveau:sourcestone'), (5, 'tinted_glass'), (6, 'ars_nouveau:source_gem_block')):
        b.put(15, y, 9, block)
    b.chest(15, 3, 6, 'limit_lab', facing='south')
    b.chest(24, 3, 15, 'limit_lab', supplies=True)
    for x in (11, 19):
        light(b, x, 3, 14)
    buried_entrance(b, 14, 16, 2, 17, 10, 'polished_andesite')


def infected_hamlet(b):
    b.path(11, 2, 15, 27)
    b.path(4, 12, 24, 16)
    b.house(3, 4, 10, 11, 6)
    b.house(17, 5, 24, 12, 20, roof=False)
    b.house(5, 19, 11, 25, 8, roof=(b.style == 0))
    b.footing(12, 12, 17, 16)
    for x,z in ((8, 8), (19, 8), (8, 21), (14, 14)):
        for dx in range(-2, 3):
            for dz in range(-2, 3):
                if abs(dx) + abs(dz) < 4 and b.r.random() < .78:
                    b.put(x + dx, 2, z + dz, 'sculk')
        b.put(x, 3, z, 'sculk')
        if x != 19:
            b.put(x, 4, z, 'sculk_vein', {'down': 'true', 'waterlogged': 'false'})
    b.put(5, 3, 9, 'farmersdelight:cutting_board', {'facing': 'north'})
    b.put(20, 3, 10, 'create:copper_casing')
    b.chest(6, 3, 22, 'infected_hamlet')
    b.chest(23, 3, 9, 'infected_hamlet', supplies=True)
    light(b, 15, 3, 15, soul=True)


def catacombs(b):
    stone = 'mossy_stone_bricks' if b.style == 0 else 'deepslate_bricks'
    for x0,z0,x1,z1 in ((10, 3, 16, 17), (4, 4, 11, 9), (15, 4, 22, 9),
                        (4, 11, 11, 16), (15, 11, 22, 16)):
        underground_room(b, x0, z0, x1, z1, 2, stone)
    b.fill(11, 3, 4, 15, 6, 16, 'air')
    for z in (6, 13):
        b.fill(10, 3, z, 16, 5, z + 1, 'air')
        for x in (7, 19):
            b.fill(x - 1, 3, z + 1, x + 1, 3, z + 2, 'botania:livingrock')
            light(b, x, 4, z + 2, soul=True)
    b.chest(13, 3, 4, 'catacombs', facing='south')
    b.chest(20, 3, 14, 'catacombs', supplies=True)
    buried_entrance(b, 12, 14, 2, 16, 9, stone)


def surviving_hamlet(b):
    for x,z,door in ((3, 4, 6), (19, 4, 22), (3, 19, 6)):
        b.house(x, z, x + 7, z + 7, door, ruined=False)
        for dz,part in ((5, 'head'), (6, 'foot')):
            b.put(x + 3, 3, z + dz, 'brown_bed' if b.style else 'red_bed', {
                'part': part, 'facing': 'north', 'occupied': 'false'
            })
        light(b, x + 4, 3, z + 2)
    b.path(13, 2, 16, 27)
    b.path(4, 13, 26, 16)
    b.footing(11, 10, 17, 12)
    b.put(14, 3, 11, 'bell', {'attachment': 'floor', 'facing': 'north', 'powered': 'false'})
    terrace(b, 19, 18, 26, 26, 'botania:livingrock')
    b.fill(20, 2, 19, 25, 2, 25, 'farmersdelight:rich_soil')
    for x in (20, 23, 25):
        for z in (19, 21, 23, 25):
            b.put(x, 3, z, 'sweet_berry_bush', {'age': '2'})
    b.put(7, 3, 8, 'farmersdelight:cutting_board', {'facing': 'west'})
    b.put(24, 3, 8, 'smoker', {'facing': 'west', 'lit': 'false'})
    b.put(21, 3, 24, 'composter', {'level': '0'})
    b.chest(9, 3, 24, 'surviving_hamlet')
    b.villager(6, 3, 8)
    b.villager(22, 3, 8)
    b.villager(8, 3, 22)


def ancient_mine(b):
    stone = 'cobblestone' if b.style == 0 else 'cobbled_deepslate'
    underground_room(b, 9, 2, 17, 20, 2, stone)
    underground_room(b, 3, 5, 23, 12, 2, stone)
    b.fill(10, 3, 3, 16, 6, 19, 'air')
    for z in (5, 8, 11, 14, 17):
        for x in (10, 16):
            b.fill(x, 3, z, x, 5, z, 'immersiveengineering:treated_wood_horizontal')
        b.fill(10, 6, z, 16, 6, z, 'immersiveengineering:treated_wood_horizontal')
    for z in range(4, 18):
        if z not in (7, 13):
            b.put(13, 3, z, 'rail', {'shape': 'north_south', 'waterlogged': 'false'})
    for x,z,ore in ((5, 7, 'copper_ore'), (20, 8, 'create:zinc_ore'), (21, 10, 'iron_ore')):
        b.put(x, 3, z, ore)
    light(b, 11, 3, 6)
    light(b, 15, 3, 16)
    b.chest(5, 3, 9, 'ancient_mine', facing='east')
    b.chest(21, 3, 8, 'ancient_mine', supplies=True)
    buried_entrance(b, 12, 14, 2, 18, 8, stone)


def abyss_temple(b):
    stone = 'polished_blackstone_bricks' if b.style == 0 else 'deepslate_tiles'
    terrace(b, 5, 3, 23, 25, stone)
    b.fill(6, 3, 4, 22, 6, 24, 'air')
    for z in (5, 10, 15, 20):
        arch(b, 7, 3, z, stone, 5)
        arch(b, 17, 3, z, stone, 5)
    for z in range(8, 23):
        for x in (12, 16):
            b.put(x, 2, z, 'sculk' if z % 3 else 'crying_obsidian')
    b.fill(11, 3, 22, 17, 3, 24, stone)
    b.fill(12, 4, 23, 16, 4, 23, 'ars_nouveau:sourcestone')
    b.put(14, 5, 23, 'tinted_glass')
    light(b, 11, 4, 23, soul=True)
    light(b, 17, 4, 23, soul=True)
    b.chest(14, 4, 22, 'abyss_temple')


def drowned_city(b):
    stone = 'prismarine_bricks' if b.style == 0 else 'dark_prismarine'
    terrace(b, 14, 5, 24, 34, stone)
    for x,z in ((4, 8), (25, 8), (4, 24), (25, 24)):
        terrace(b, x, z, x + 9, z + 9, 'prismarine')
        for dx in (0, 8):
            for dz in (0, 8):
                b.pillar(x + dx, z + dz, b.r.randint(3, 5))
        for dx in range(10):
            if b.r.random() > .25:
                b.put(x + dx, 5, z + 8, stone)
        arch(b, x + 2, 3, z, stone, 6)
    for z in (8, 19, 31):
        for x in (15, 23):
            b.put(x, 3, z, stone)
            b.put(x, 4, z, 'sea_lantern')
    b.fill(16, 3, 24, 22, 3, 27, 'cut_copper')
    b.fill(18, 4, 25, 20, 4, 26, 'create:copper_casing')
    b.chest(19, 4, 24, 'drowned_city', submerged=True)
    b.chest(8, 3, 29, 'drowned_city', supplies=True, submerged=True)


def observatory(b):
    stone = 'polished_andesite' if b.style == 0 else 'deepslate_bricks'
    for x in range(2, 21):
        for z in range(2, 21):
            distance = (x - 11)**2 + (z - 11)**2
            if distance <= 81:
                b.fill(x, 0, z, x, 2, z, stone)
            if 42 <= distance <= 81 and (z > 5 or not 9 <= x <= 13):
                b.fill(x, 3, z, x, b.r.randint(4, 6), z, stone)
    for x,z in ((6, 8), (16, 8), (6, 14), (16, 14)):
        b.fill(x, 3, z, x, 8, z, stone)
        b.put(x, 9, z, 'create:copper_casing')
    for dx in range(-5, 6):
        height = 12 - abs(dx) // 2
        for z in (9, 13):
            b.put(11 + dx, height, z, 'cut_copper')
    for rise in range(7):
        b.put(11, 4 + rise, 11 - rise // 2, 'create:andesite_casing')
    b.fill(10, 10, 6, 12, 11, 8, 'create:copper_casing')
    b.put(11, 11, 5, 'tinted_glass')
    b.put(12, 3, 15, 'cartography_table')
    b.chest(10, 3, 16, 'observatory', facing='north')
