"""Sparse perimeter slopes, foundations and decoration for authored structure templates."""
from collections import defaultdict
from math import cos, sin

from site_supplies import SITE_FIXTURES

LAND_DEPTH = 5
HOUSE_SITES = {'silent_hamlet', 'surviving_hamlet', 'infected_hamlet'}
CASTLES = {'fallen_capital', 'mechanists_keep', 'keepers_keep', 'archmages_keep'}
DECOR = {
    'farm': ('potted_fern', 'composter', 'hay_block', 'lantern'),
    'fortress': ('flower_pot', 'chiseled_stone_bricks', 'lantern', 'bookshelf'),
    'ruin': ('cobbled_deepslate_slab', 'lantern', 'potted_dead_bush', 'moss_carpet'),
    'cavern': ('candle', 'deepslate_brick_slab', 'chiseled_deepslate', 'soul_lantern'),
    'water': ('prismarine_slab', 'sea_pickle', 'prismarine_wall', 'sea_lantern'),
}
DECO_PROPERTIES = {
    'candle': {'candles': '2', 'lit': 'false', 'waterlogged': 'false'},
    'sea_pickle': {'pickles': '2', 'waterlogged': 'true'},
    'prismarine_slab': {'type': 'bottom', 'waterlogged': 'true'},
    'prismarine_wall': {'waterlogged': 'true'},
}


def enhance_site(build, site):
    """Return the additional vertical offset needed for terrain-aligned placement."""
    sea = site.biomes == 'deep_ocean'
    outdoor = site.surface == 2 and not sea
    decor_kind = ('water' if sea else 'cavern' if not outdoor else
                  'farm' if site.slug in HOUSE_SITES else
                  'fortress' if site.slug in CASTLES else 'ruin')
    protected = {(x,z) for (x,_,z),(_,tag) in build.blocks.items() if tag}
    protected.update((e['blockPos'][0], e['blockPos'][2]) for e in build.entities)
    decorate(build, decor_kind, protected, SITE_FIXTURES[site.slug][0])
    if outdoor:
        add_terrain(build, site.biomes)
        return LAND_DEPTH
    return 0


def decorate(build, kind, protected, fixtures):
    width, height, length = build.size
    columns = defaultdict(list)
    for (x,y,z),(state,_) in build.blocks.items():
        if state['Name'] != 'minecraft:air':
            columns[x,z].append(y)
    candidates, open_floor = [], []
    for (x,z), levels in columns.items():
        if x<=0 or z<=0 or x>=width-1 or z>=length-1:
            continue
        if any(abs(x-a)+abs(z-b)<=2 for a,b in protected):
            continue
        for y in sorted(levels):
            if y<2 or y+2>=height or (kind in ('farm','fortress','ruin') and y>3):
                continue
            ground=build.blocks[x,y,z][0]['Name']
            if ground in ('minecraft:gravel','minecraft:coarse_dirt','minecraft:cobblestone','minecraft:mossy_cobblestone'):
                continue
            if ground.endswith(('_stairs','_slab','_fence','_wall','_leaves','_lantern')):
                continue
            if not all(pos not in build.blocks or build.blocks[pos][0]['Name']=='minecraft:air'
                       for pos in ((x,y+1,z),(x,y+2,z))):
                continue
            adjacent = ((x+1,y+1,z), (x-1,y+1,z), (x,y+1,z+1), (x,y+1,z-1))
            near_wall = any(pos in build.blocks and build.blocks[pos][0]['Name']!='minecraft:air'
                            for pos in adjacent)
            # Put most props against actual walls and keep passages and open courts clear.
            if near_wall or kind=='water':
                candidates.append((x,y+1,z))
            else:
                open_floor.append((x,y+1,z))
            break
    build.r.shuffle(candidates)
    build.r.shuffle(open_floor)
    wall_or_water=set(candidates)
    chosen=[]
    limit=max(3, min(18, width*length//80))
    for x,y,z in candidates + open_floor:
        index=len(chosen)
        if index >= limit or (index >= len(fixtures) and (x,y,z) not in wall_or_water):
            break
        separation=2 if index < len(fixtures) else 4
        if any(abs(x-a)+abs(z-c) < separation for a,_,c in chosen):
            continue
        chosen.append((x,y,z))
        block=fixtures[index] if index < len(fixtures) else DECOR[kind][(index+build.style)%len(DECOR[kind])]
        build.put(x,y,z,block,DECO_PROPERTIES.get(block))
    assert len(chosen) >= len(fixtures), (kind, build.size, fixtures)


def add_terrain(build, biome):
    width, height, length = build.size
    original=build.blocks
    footprint={(x,z) for x,y,z in original if y<=2}
    all_columns={(x,z) for x,_,z in original}
    build.size=(width,height+LAND_DEPTH,length)
    build.blocks={(x,y+LAND_DEPTH,z):entry for (x,y,z),entry in original.items()}
    for entity in build.entities:
        entity['pos'][1]+=LAND_DEPTH
        entity['blockPos'][1]+=LAND_DEPTH

    # Foundations descend in stepped fingers while most existing terrain remains untouched.
    for x,z in sorted(footprint):
        edge=any((x+dx,z+dz) not in footprint for dx,dz in ((-1,0),(1,0),(0,-1),(0,1)))
        if not edge and (x%3 or z%3):
            continue
        depth=2+int((sin(x*.38)+cos(z*.42)+2)*.82)
        for y in range(LAND_DEPTH-depth,LAND_DEPTH):
            build.put(x,y,z,'stone' if y<LAND_DEPTH-2 else 'tuff')

    # Broken banks in open perimeter quadrants. Use different contours for the two templates.
    for x in range(1,width-1):
        for z in range(1,length-1):
            if (x,z) in all_columns:
                continue
            near=min(x,z,width-1-x,length-1-z)
            if near>5 or abs(x-width//2)<3 or abs(z-length//2)<3:
                continue
            contour=sin(x*.31+build.style*1.8)+cos(z*.34-build.style*.7)
            if contour<.40 or not any((x+dx,z+dz) in footprint for dx in range(-2,3) for dz in range(-2,3)):
                continue
            rise=int((contour-.3)*2)
            y=LAND_DEPTH+1+rise
            top='gravel' if biome=='highland' and rise>1 else 'grass_block'
            for layer in range(y-2,y):
                build.put(x,layer,z,'stone' if layer<LAND_DEPTH else 'coarse_dirt')
            build.put(x,y,z,top)
            if top=='grass_block' and build.r.random()<.1:
                build.put(x,y+1,z,build.r.choice(('grass','fern','dandelion')))
