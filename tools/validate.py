from pathlib import Path
import json, csv, re, subprocess, shutil, tomllib
root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
assert manifest['minecraft']['version']=='1.20.1'
assert len(manifest['files'])==171
ids={(i['projectID'],i['fileID']) for i in manifest['files']}
assert len(ids)==171 and len({p for p,f in ids})==171
assert {(896746,8657397),(1733245,9553070)} <= ids
shader_config=(root/'overrides/config/oculus.properties').read_text(encoding='utf-8')
assert 'enableShaders=true' in shader_config
assert 'shaderPack=ComplementaryUnbound_r5.6.1.zip' in shader_config
preset=(root/'overrides/shaderpacks/ComplementaryUnbound_r5.6.1.zip.txt').read_text(encoding='utf-8')
assert 'TM_EXPOSURE=0.90' in preset and 'T_SATURATION=0.85' in preset
with (root/'overrides/ashes_docs/mods-lock.tsv').open(encoding='utf-8') as f:
    locked=list(csv.DictReader(f,delimiter='\t'))
assert {(int(r['projectID']),int(r['fileID'])) for r in locked}==ids
quests=[]; chapter_ids=set(); task_ids=set(); reward_ids=set(); illustrated=0; quest_art=set()
for p in sorted((root/'overrides/config/ftbquests/quests/chapters').glob('*.snbt')):
    c=json.loads(p.read_text(encoding='utf-8'))
    assert c['filename']==p.stem and c['id'] not in chapter_ids
    chapter_ids.add(c['id'])
    for q in c['quests']:
        quests.append(q)
        assert q['description'] and q['description'][0].strip()
        assert q['rewards']
        for description in q['description']:
            if description.startswith('{image:'):
                art=re.fullmatch(r'\{image:kubejs:(textures/quest/[a-z_]+\.png) width:150 height:84 align:1\}',description)
                assert art,(q['id'],description)
                texture=root/'overrides/kubejs/assets/kubejs'/art[1]
                assert texture.read_bytes().startswith(b'\x89PNG\r\n\x1a\n')
                quest_art.add(texture)
                illustrated+=1
        for t in q['tasks']:
            assert t['id'] not in task_ids; task_ids.add(t['id'])
            assert t['type'] in ('item','checkmark','advancement')
            if t['type']=='advancement': assert ':' in t['advancement']
            if t['type']=='item': assert ':' in t['item'] and t['count']>0
        for r in q.get('rewards',[]):
            assert r['id'] not in reward_ids; reward_ids.add(r['id'])
byid={q['id']:q for q in quests}
assert len(byid)==len(quests)==495
assert len(chapter_ids)==40
assert len(chapter_ids|set(byid)|task_ids|reward_ids)==len(chapter_ids)+len(byid)+len(task_ids)+len(reward_ids)
seen=set(); visiting=set()
def visit(qid):
    assert qid in byid and qid not in visiting
    if qid in seen:return
    visiting.add(qid)
    for d in byid[qid].get('dependencies',[]):visit(d)
    visiting.remove(qid);seen.add(qid)
for qid in byid:visit(qid)
assert {q['id'] for q in json.loads((root/'docs/quests.json').read_text(encoding='utf-8'))}==set(byid)
assert illustrated==40 and len(quest_art)==3
base=root/'overrides/kubejs'
items=set(re.findall(r"event.create\('([^']+)'\)",(base/'startup_scripts/ashes_items.js').read_text(encoding='utf-8')))
recipes=(base/'server_scripts/ashes_recipes.js').read_text(encoding='utf-8')
refs=set(re.findall(r'kubejs:([a-z_]+)',recipes))
refs|={t['item'].split(':')[1] for q in quests for t in q['tasks']+q['rewards'] if t.get('item','').startswith('kubejs:')}
assert refs<=items and len(items)==30
rids=re.findall(r"\.id\('([^']+)'\)",recipes);assert len(set(rids))==len(rids)==38
functions=base/'data/ashes/functions'
for p in functions.rglob('*.mcfunction'):
    for name in re.findall(r'\bfunction ashes:([a-z0-9_/]+)',p.read_text(encoding='utf-8')):
        assert (functions/(name+'.mcfunction')).is_file(),(p,name)
for p in base.rglob('*.json'):json.loads(p.read_text(encoding='utf-8'))
if shutil.which('node'):
    for p in base.rglob('*.js'):subprocess.run(['node','--check',str(p)],check=True)
for p in (root/'overrides').rglob('*.toml'): tomllib.loads(p.read_text(encoding='utf-8'))
print(f'PASS: {len(ids)} projects, {len(quests)} quests, {len(chapter_ids)} chapters, {len(items)} items, {len(rids)} recipes; dependency DAG and references. Game runtime NOT tested.')

# Validate authored skill-tree references and constrained progression.
mastery=base/'data/ashes/puffish_skills/categories/mastery'
read=lambda name:json.loads((mastery/(name+'.json')).read_text(encoding='utf-8'))
skills,defs,edges,cat=read('skills'),read('definitions'),read('connections'),read('category')
assert len(skills)==len(defs)==54 and cat['spent_points_limit']==9
assert sum(x['root'] for x in skills.values())==6
assert {x['definition'] for x in skills.values()}==set(defs)
assert len(edges['normal']['unidirectional'])==48
for a,b in edges['normal']['unidirectional']:assert a in skills and b in skills and a!=b
assert all(d['cost']==1 for d in defs.values())
assert (base/'data/ashes/advancements/ward/registered.json').exists()
assert any(t.get('advancement')=='ashes:ward/registered' for q in quests for t in q['tasks'])
sculk=tomllib.loads((root/'overrides/config/sculkhorde_config.toml').read_text())
assert sculk['General Variables']['isHordeActiveWithNoPlayers'] is False
assert sculk['Trigger Automatically Variables']['trigger_ancient_node_automatically'] is False
assert not (root/'overrides/defaultconfigs/sculkhorde-server.toml').exists()
assert len({r['data']['attribute'] for d in defs.values() for r in d['rewards']})>=12
assert all((functions/'skills'/f'role_{i}.mcfunction').is_file() for i in range(1,7))
assert 'ashes:mastery 9 ashes:rank' in (functions/'skills/grant.mcfunction').read_text(encoding='utf-8')
from artifacts import CONSUMABLES, INTERACTIONS
assert all(name in items for name in (*CONSUMABLES,*INTERACTIONS))
assert all((functions/'kit'/f'{name}_used.mcfunction').is_file() for name in CONSUMABLES)
print('PASS: class menus, mastery, artifacts, ward advancement and Sculk configuration.')

# Authored textures: inspect PNG header and animation metadata with stdlib only.
import struct
textures=base/'assets/kubejs/textures/item'
assert {p.stem for p in textures.glob('*.png')}==items
registry=(base/'startup_scripts/ashes_items.js').read_text(encoding='utf-8')
assert set(re.findall(r"texture\('kubejs:item/([a-z_]+)'\)",registry))==items
assert len({p.read_bytes() for p in textures.glob('*.png')})==len(items)
for p in textures.glob('*.png'):
    data=p.read_bytes()
    assert data[:8]==b'\x89PNG\r\n\x1a\n' and data[12:16]==b'IHDR',p
    w,h=struct.unpack('>II',data[16:24])
    assert w in (32,64) and h%w==0,p
    meta=p.with_suffix('.png.mcmeta')
    if meta.exists():
        a=json.loads(meta.read_text(encoding='utf-8'))['animation']
        assert h>w and a['frametime']>0,p
        assert all(0<=f<h//w for f in a.get('frames',range(h//w))),p
    else: assert h==w,p
assert all(p.with_suffix('').exists() for p in textures.glob('*.png.mcmeta'))
print('PASS: custom item textures and animation dimensions.')

assert {p.name.removesuffix('.png.mcmeta') for p in textures.glob('*.png.mcmeta')}=={"abyssal_seal","cleansing_charge","concord_core","final_testament","nature_seal","purifier_matrix","renewal_heart","ward_charm"}
for meta in textures.glob('*.png.mcmeta'):
    assert struct.unpack('>II',meta.with_suffix('').read_bytes()[16:24])==(64,512)
print('PASS: eight animated artifacts, eight frames each.')

# World chronicles: verify referenced predicates and player toggle.
for p in (functions/'news').glob('*.mcfunction'):
    for name in re.findall(r'\bpredicate ashes:([a-z0-9_/]+)',p.read_text(encoding='utf-8')):
        assert (base/'data/ashes/predicates'/(name+'.json')).is_file(),name
assert 'function ashes:news/player' in (functions/'player.mcfunction').read_text(encoding='utf-8')
assert 'scoreboard objectives add ashes_news trigger' in (functions/'load.mcfunction').read_text(encoding='utf-8')
assert 'tag=!ashes_news_seen,tag=!ashes_news_muted' in (functions/'news/player.mcfunction').read_text(encoding='utf-8')
assert 'run function ashes:news/welcome' in (functions/'news/player.mcfunction').read_text(encoding='utf-8')
print('PASS: chronicles are enabled for new players and retain per-player mute.')

# Lore structures: real templates, data registries, loot, and discovery.
import gzip
from structures import PLACEMENT, SITES
from site_supplies import SITE_FIXTURES
from devtools import NBT

lorebase=base/'data/ashes'
site_set_dir=lorebase/'worldgen/structure_set'
site_sets={region:json.loads((site_set_dir/(region+'.json')).read_text(encoding='utf-8'))
           for region in PLACEMENT}
site_entries=[]
for site_set in site_sets.values():
    assert site_set['placement']['spacing']>site_set['placement']['separation']>=2
    site_entries.extend(site_set['structures'])
assert len(site_entries)==len(SITES)
assert {entry['structure'] for entry in site_entries}=={'ashes:'+site.slug for site in SITES}
from itertools import pairwise

from site_levels import TERRACES, VARIANTS
from site_supports import PIER_JOB, SUPPORT_JOB, VOID

inventory = {row['template']: row for row in json.loads(
    (root/'docs/lore-structures.json').read_text(encoding='utf-8'))}
seen_templates=set()
for entry in site_entries:
    site=entry['structure'].split(':')[1]
    blocks, supplies=SITE_FIXTURES[site]
    conf=json.loads((lorebase/'worldgen/structure'/(site+'.json')).read_text(encoding='utf-8'))
    assert conf['type']=='minecraft:jigsaw' and conf['size'] > 0
    pool=conf['start_pool'].split(':')[1]
    assert (lorebase/'tags/worldgen/biome'/(conf['biomes'].split(':')[1]+'.json')).is_file()
    template_pool=json.loads((lorebase/'worldgen/template_pool'/(pool+'.json')).read_text(encoding='utf-8'))
    assert len(template_pool['elements'])==VARIANTS
    profiles = set()
    for el in template_pool['elements']:
        name=el['element']['location'].split(':')[1]
        assert name not in seen_templates
        seen_templates.add(name)
        p=lorebase/'structures'/(name+'.nbt')
        nbt=gzip.decompress(p.read_bytes())
        assert nbt.startswith(b'\x0a\x00\x00') and b'DataVersion' in nbt
        assert ('ashes:lore/'+site).encode() in nbt
        template=NBT(nbt).parse()
        assert set(blocks) <= {state['Name'] for state in template['palette']},name
        row = inventory[name]
        profile = tuple(row['levels'])
        assert profile not in profiles and el['weight'] == 1, name
        profiles.add(profile)
        assert len(row['routes']) == len(TERRACES.get(site, (None,))), name
        positions = {tuple(block['pos']): template['palette'][block['state']]
                     for block in template['blocks']}
        jobs = [e for e in template['entities'] if e['nbt']['id'] == 'minecraft:marker']
        anchors = {tuple(e['blockPos']) for e in jobs}
        assert len(anchors) == len(jobs) == row['foundations'], name
        assert bool(jobs) == (site in TERRACES), name
        assert all(SUPPORT_JOB in e['nbt']['Tags'] for e in jobs), name
        assert not jobs or any(PIER_JOB in e['nbt']['Tags'] for e in jobs), name
        assert all(positions[pos]['Name'] not in VOID for pos in anchors), name
        anchor_columns = {(x, z) for x, _, z in anchors}
        clear = 'minecraft:water' if site == 'drowned_city' else 'minecraft:air'
        for route in row['routes']:
            if site in TERRACES:
                assert all((x, z) in anchor_columns for x, _, z in route), name
                x,y,z = route[0]
                assert all(positions[x,y+h,z]['Name'] == clear for h in (1,2)), name
            assert all(abs(x-a) + abs(z-c) == 1 and abs(y-b) <= 1
                       for (x,y,z),(a,b,c) in pairwise(route)), name
            stairs = 0
            for x,y,z in route[1:-1]:
                stair = positions[x,y,z]
                assert stair['Name'].endswith('_stairs'), (name, (x,y,z))
                assert stair['Properties']['waterlogged'] == str(clear == 'minecraft:water').lower(), name
                assert all(positions[x,y+h,z]['Name'] == clear for h in (1,2)), name
                stairs += 1
            assert stairs >= 2, name
        if 'start_jigsaw_name' in conf:
            assert conf['start_jigsaw_name'].encode() in nbt
    loot=json.loads((lorebase/'loot_tables/lore'/(site+'.json')).read_text(encoding='utf-8'))
    assert loot['type']=='minecraft:chest'
    assert loot['pools'][-1]['rolls']==1
    assert {e['name'] for e in loot['pools'][-1]['entries']}==set(supplies)
    for pool in loot['pools']:
        for e in pool['entries']:
            if e['name'].startswith('kubejs:'): assert e['name'].split(':')[1] in items
    adv=json.loads((lorebase/'advancements/lore'/(site+'.json')).read_text(encoding='utf-8'))
    assert adv['criteria']['visit']['conditions']['player'][0]['predicate']['location']['structure']==entry['structure']
    assert (functions/(adv['rewards']['function'].split(':')[1]+'.mcfunction')).is_file()
assert len(seen_templates)==VARIANTS*len(SITES)
assert len(inventory)==(2+VARIANTS)*len(SITES)+VARIANTS*len(TERRACES)
print('PASS: foundation anchors and pier positions in the 90 surface and coastal layouts.')
print(f'PASS: {len(SITES)} lore structures, {len(seen_templates)} gzip NBT templates, loot and discovery references.')

assert {t['advancement'] for q in quests for t in q['tasks'] if t.get('advancement','').startswith('ashes:lore/')}=={'ashes:lore/'+e['structure'].split(':')[1] for e in site_sets['lore_sites']['structures']}
print('PASS: lore discovery quest coverage.')

# Development tooling: geometry and source references, plus isolated utility tests.
from devtools import check as check_devtools
check_devtools(root)
import sys
subprocess.run([sys.executable, str(root/'tools/test_devtools.py')], check=True)
