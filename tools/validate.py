from pathlib import Path
import json, csv, re, subprocess, shutil, tomllib
root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
assert manifest['minecraft']['version']=='1.20.1'
assert len(manifest['files'])==129
ids={(i['projectID'],i['fileID']) for i in manifest['files']}
assert len(ids)==129 and len({p for p,f in ids})==129
with (root/'overrides/ashes_docs/mods-lock.tsv').open(encoding='utf-8') as f:
    locked=list(csv.DictReader(f,delimiter='\t'))
assert {(int(r['projectID']),int(r['fileID'])) for r in locked}==ids
quests=[]; chapter_ids=set(); task_ids=set(); reward_ids=set()
for p in sorted((root/'overrides/config/ftbquests/quests/chapters').glob('*.snbt')):
    c=json.loads(p.read_text(encoding='utf-8'))
    assert c['filename']==p.stem and c['id'] not in chapter_ids
    chapter_ids.add(c['id'])
    for q in c['quests']:
        quests.append(q)
        for t in q['tasks']:
            assert t['id'] not in task_ids; task_ids.add(t['id'])
            assert t['type'] in ('item','checkmark','advancement')
            if t['type']=='advancement': assert ':' in t['advancement']
            if t['type']=='item': assert ':' in t['item'] and t['count']>0
        for r in q.get('rewards',[]):
            assert r['id'] not in reward_ids; reward_ids.add(r['id'])
byid={q['id']:q for q in quests}
assert len(byid)==len(quests)==423
assert len(chapter_ids)==33
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
base=root/'overrides/kubejs'
items=set(re.findall(r"event.create\('([^']+)'\)",(base/'startup_scripts/ashes_items.js').read_text(encoding='utf-8')))
recipes=(base/'server_scripts/ashes_recipes.js').read_text(encoding='utf-8')
refs=set(re.findall(r'kubejs:([a-z_]+)',recipes))
refs|={t['item'].split(':')[1] for q in quests for t in q['tasks'] if t.get('item','').startswith('kubejs:')}
assert refs<=items and len(items)==30
rids=re.findall(r"\.id\('([^']+)'\)",recipes);assert len(set(rids))==len(rids)==32
functions=base/'data/ashes/functions'
for p in functions.rglob('*.mcfunction'):
    for name in re.findall(r'\bfunction ashes:([a-z0-9_/]+)',p.read_text(encoding='utf-8')):
        assert (functions/(name+'.mcfunction')).is_file(),(p,name)
for p in base.rglob('*.json'):json.loads(p.read_text(encoding='utf-8'))
if shutil.which('node'):
    for p in base.rglob('*.js'):subprocess.run(['node','--check',str(p)],check=True)
for p in (root/'overrides').rglob('*.toml'): tomllib.loads(p.read_text(encoding='utf-8'))
print(f'PASS: {len(ids)} projects, {len(quests)} quests, {len(chapter_ids)} chapters, {len(items)} items, {len(rids)} recipes; dependency DAG and references. Game runtime NOT tested.')
