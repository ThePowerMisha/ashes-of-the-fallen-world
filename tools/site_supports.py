"""Columns that receive a foundation when their structure appears in the world."""
from collections import defaultdict

SUPPORT_JOB = 'ashes_foundation'
PIER_JOB = 'ashes_pier'
WET_JOB = 'ashes_wet'
DEPTH_SCORE = 'ashes_gap'
BANK_LIMIT = 5
SCAN_LIMIT = 384
JOBS_PER_TICK = 8
REPLACEABLE = (
    'air', 'cave_air', 'void_air', 'water', 'grass', 'tall_grass', 'fern', 'large_fern',
    'dead_bush', 'snow', 'seagrass', 'tall_seagrass',
)
VOID = {'minecraft:' + name for name in REPLACEABLE}


def foundation_jobs(build):
    """Anchor below the deck and close any gaps inside its authored foundation."""
    tracks = {}
    for (x, y, z), pier in build.walkways.items():
        existing = tracks.get((x, z))
        if existing is None or y < existing[0]:
            tracks[x, z] = (y, pier)
        elif y == existing[0]:
            tracks[x, z] = (y, pier or existing[1])

    levels = defaultdict(list)
    for (x, y, z), (state, _) in build.blocks.items():
        if (x, z) in tracks and y <= tracks[x, z][0] and state['Name'] not in VOID:
            levels[x, z].append(y)

    count = 0
    for (x, z), (deck, pier) in sorted(tracks.items()):
        if deck not in levels[x, z]:
            continue
        bottom = min(levels[x, z])
        for y in range(bottom, deck):
            if (x, y, z) not in build.blocks or build.blocks[x, y, z][0]['Name'] in VOID:
                build.put(x, y, z, 'cobblestone')
        tags = [SUPPORT_JOB, PIER_JOB] if pier else [SUPPORT_JOB]
        build.entities.append({
            'pos': [x + 0.5, bottom + 0.5, z + 0.5],
            'blockPos': [x, bottom, z],
            'nbt': {'id': 'minecraft:marker', 'Tags': tags},
        })
        count += 1
    return count


def generate_foundations(fn, js, tags):
    js(tags / 'blocks' / 'foundation_replaceable.json', {
        'replace': False, 'values': ['minecraft:' + name for name in REPLACEABLE],
    })
    fn('foundation/tick', [
        f'execute in minecraft:overworld as @e[type=minecraft:marker,tag={SUPPORT_JOB},distance=0..,limit={JOBS_PER_TICK}] at @s run function ashes:foundation/start',
    ])
    fn('foundation/start', [
        f'scoreboard players set @s {DEPTH_SCORE} 0',
        f'tag @s remove {WET_JOB}',
        'execute unless block ~ ~ ~ #ashes:foundation_replaceable positioned ~ ~-1 ~ run function ashes:foundation/probe',
        f'execute if score @s {DEPTH_SCORE} matches 1..{BANK_LIMIT} unless entity @s[tag={WET_JOB}] positioned ~ ~-1 ~ run function ashes:foundation/bank',
        f'execute if score @s {DEPTH_SCORE} matches 1..{BANK_LIMIT} if entity @s[tag={WET_JOB},tag={PIER_JOB}] positioned ~ ~-1 ~ run function ashes:foundation/pier',
        f'execute if score @s {DEPTH_SCORE} matches {BANK_LIMIT + 1}..{SCAN_LIMIT - 1} if entity @s[tag={PIER_JOB}] positioned ~ ~-1 ~ run function ashes:foundation/pier',
        f'scoreboard players reset @s {DEPTH_SCORE}',
        'kill @s',
    ])
    fn('foundation/probe', [
        'execute if block ~ ~ ~ #ashes:foundation_replaceable run function ashes:foundation/count',
    ])
    fn('foundation/count', [
        f'execute if block ~ ~ ~ minecraft:water run tag @s add {WET_JOB}',
        f'scoreboard players add @s {DEPTH_SCORE} 1',
        f'execute if score @s {DEPTH_SCORE} matches ..{BANK_LIMIT} unless entity @s[tag={PIER_JOB}] positioned ~ ~-1 ~ run function ashes:foundation/probe',
        f'execute if score @s {DEPTH_SCORE} matches ..{SCAN_LIMIT - 1} if entity @s[tag={PIER_JOB}] positioned ~ ~-1 ~ run function ashes:foundation/probe',
    ])
    for name, material in [('bank', 'tuff'), ('pier', 'stone_bricks')]:
        fn('foundation/' + name, [
            f'execute if block ~ ~ ~ #ashes:foundation_replaceable run setblock ~ ~ ~ minecraft:{material}',
            f'scoreboard players remove @s {DEPTH_SCORE} 1',
            f'execute if score @s {DEPTH_SCORE} matches 1.. positioned ~ ~-1 ~ run function ashes:foundation/{name}',
        ])
