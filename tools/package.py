"""Produce reproducible CurseForge manifests. Horizon profile replaces shaders with LODs."""
from pathlib import Path
import argparse,csv,html,io,json,zipfile
root=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('output',nargs='?',type=Path);parser.add_argument('--profile',choices=['standard','horizons'],default='standard');args=parser.parse_args()
m=json.loads((root/'manifest.json').read_text());version=m['version']
lockpath='overrides/ashes_docs/mods-lock.tsv'
rows=list(csv.DictReader((root/lockpath).open(encoding='utf-8'),delimiter='\t'))
profile=args.profile
if profile=='horizons':
    drop={'oculus','complementary-unbound'}
    removed={int(r['projectID']) for r in rows if r['slug'] in drop}
    assert len(removed)==2
    rows=[r for r in rows if r['slug'] not in drop]
    dh={'slug':'distant-horizons','projectID':'508933','fileID':'7334195','filename':'DistantHorizons-2.4.1-b-1.20.1-fabric-forge.jar'}
    rows.append(dh)
    m['files']=[f for f in m['files'] if f['projectID'] not in removed]+[{'projectID':int(dh['projectID']),'fileID':int(dh['fileID']),'required':True}]
    m['name']+=' — Horizons';m['version']+='-horizons'
assert len(rows)==len(m['files'])==len({x['projectID'] for x in m['files']})
assert {(int(r['projectID']),int(r['fileID'])) for r in rows}=={(f['projectID'],f['fileID']) for f in m['files']}
output=args.output or root.parent/f'Ashes-{m["version"]}-CurseForge.zip';output.parent.mkdir(parents=True,exist_ok=True)
lock=io.StringIO();w=csv.DictWriter(lock,fieldnames=['slug','projectID','fileID','filename'],delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
links=''.join(f'<li><a href="https://www.curseforge.com/minecraft/{"shaders" if r["filename"].endswith(".zip") else "mc-mods"}/{html.escape(r["slug"])}/files/{r["fileID"]}">{html.escape(r["slug"])}</a> — {html.escape(r["filename"])}</li>' for r in sorted(rows,key=lambda r:r['slug']))
modlist=f'<!doctype html><html><meta charset="utf-8"><title>Ashes {m["version"]}</title><h1>Ashes {m["version"]}</h1><ul>{links}</ul></html>\n'
with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as z:
    z.writestr('manifest.json',json.dumps(m,ensure_ascii=False,indent=2)+'\n');z.writestr('modlist.html',modlist);z.writestr(lockpath,lock.getvalue())
    for p in sorted((root/'overrides').rglob('*')):
        if not p.is_file():continue
        name=p.relative_to(root).as_posix()
        if name==lockpath:continue
        if profile=='horizons' and name in ('overrides/config/oculus.properties','overrides/ashes_docs/graphics/oculus-atmospheric.properties'):continue
        if profile=='horizons' and name=='overrides/ashes_docs/CLIENT_ONLY.txt':
            z.writestr(name,'\n'.join(l for l in p.read_text(encoding='utf-8').splitlines() if not l.startswith(('oculus:','complementary-unbound:')))+'\ndistant-horizons: '+dh['filename']+' (optional client LOD)\n');continue
        if profile=='horizons' and name=='overrides/ASHES_README_RU.txt':
            s=p.read_text(encoding='utf-8').replace('129 проектов','128 проектов').replace('Первый запуск без шейдера; затем выбери Complementary Unbound в меню Oculus.','Профиль Horizons: Distant Horizons 2.4.1-b, без Oculus и шейдера. Начни с 64 чанков LOD, не добавляй шейдеры без отдельного теста.');z.writestr(name,s);continue
        z.write(p,name)
with zipfile.ZipFile(output) as z:
    assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))
    assert all(not name.startswith('/') and '..' not in Path(name).parts for name in z.namelist())
print(f'{output}: {len(rows)} locked projects, {profile}')
