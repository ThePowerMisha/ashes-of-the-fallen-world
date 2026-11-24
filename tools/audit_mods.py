"""Check lock, planned features, CurseForge metadata (optional), and installed Forge jars.
No silent resolution: all failures must be fixed in the lock, not at install time.
"""
import argparse,csv,io,json,os,sys,tomllib,urllib.request,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
LOCK=ROOT/'overrides/ashes_docs/mods-lock.tsv'
PLANNED=ROOT/'docs/mod-plan.json'

def read_lock():
    return list(csv.DictReader(LOCK.open(encoding='utf-8'),delimiter='\t'))

def check_profile_dependencies(rows, files, dependencies):
    included = {row['slug'] for row in rows}
    required_ids = {entry['projectID'] for entry in files if entry.get('required') is True}
    required = {row['slug'] for row in rows if int(row['projectID']) in required_ids}
    for parent, deps in dependencies.items():
        if parent in included:
            missing = set(deps) - required
            if missing:
                raise ValueError(f"{parent} requires these projects in the profile: {', '.join(sorted(missing))}")

def static(rows):
    m=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
    assert m['minecraft']['version']=='1.20.1' and m['minecraft']['modLoaders'][0]['id'].startswith('forge-47.')
    names={r['slug']:r for r in rows}; ids={int(r['projectID']):r for r in rows}
    assert len(names)==len(ids)==len(rows)==len(m['files'])
    assert {(int(r['projectID']),int(r['fileID'])) for r in rows}=={(r['projectID'],r['fileID']) for r in m['files']}
    plan=json.loads(PLANNED.read_text(encoding='utf-8'))
    for group,slugs in plan['required'].items():
        missing=set(slugs)-names.keys()
        assert not missing,(group,missing)
    dependencies = plan['reviewed_dependencies']
    assert dependencies.keys() <= names.keys(), dependencies.keys() - names.keys()
    check_profile_dependencies(rows, m['files'], dependencies)
    assert not set(plan['excluded'])&names.keys()
    assert not {'optifine','rubidium','sodium','epic-fight-mod'}&names.keys()
    mekanism=[names[s]['filename'].split('10.4.')[-1] for s in ['mekanism','mekanism-tools','mekanism-generators']]
    assert len(set(mekanism))==1
    assert '6.0.' in names['create']['filename'] and names['create-steam-n-rails']['filename'].startswith('Steam_Rails-1.7.3+forge-')
    print(f'Static lock: {len(rows)} unique projects; all {sum(map(len,plan["required"].values()))} planned main-profile entries present.')

def cf_audit(rows,key):
    ids={int(r['projectID']):r for r in rows}; files={int(r['fileID']):r for r in rows}
    data=[]
    for start in range(0,len(files),50):
        req=urllib.request.Request('https://api.curseforge.com/v1/mods/files',data=json.dumps({'fileIds':list(files)[start:start+50]}).encode(),headers={'x-api-key':key,'Content-Type':'application/json','Accept':'application/json'},method='POST')
        with urllib.request.urlopen(req,timeout=45) as response: data.extend(json.load(response)['data'])
    errors=[]; warnings=[]
    for f in data:
        r=files[f['id']]; name=r['slug']; versions=set(f.get('gameVersions',[]))
        if f['modId']!=int(r['projectID']) or f['fileName']!=r['filename']: errors.append(f'{name}: project or file name mismatch')
        if '1.20.1' not in versions and '1.20' not in versions: errors.append(f'{name}: no 1.20/1.20.1 tag: {sorted(versions)}')
        if r['filename'].endswith('.jar') and 'Forge' not in versions:
            if versions & {'Fabric','NeoForge','Quilt'}: errors.append(f'{name}: no Forge tag: {sorted(versions)}')
            else: warnings.append(f'{name}: no explicit loader tag; verify JAR')
        if f.get('isAvailable') is False: errors.append(f'{name}: unavailable')
        for d in f.get('dependencies',[]):
            dep=d['modId']; rel=d['relationType']
            if rel==3 and dep not in ids: errors.append(f'{name}: missing required project {dep}')
            if rel==5 and dep in ids: errors.append(f'{name}: incompatible project {dep} present')
    for missing in set(files)-{f['id'] for f in data}: errors.append(f'Missing API file {missing}')
    for w in warnings: print('WARNING:',w)
    for e in errors: print('FAIL:',e)
    print(f'CurseForge metadata: {len(data)}/{len(files)}; {len(errors)} errors, {len(warnings)} warnings')
    return not errors

def jar_audit(rows,instance):
    """Read actual mods.toml and nested Jar-in-Jar archives. This checks mod IDs, not Maven version ranges or mixins."""
    mods=instance/'mods'; required=[]; modids={'minecraft','forge','java'}; errors=[]; top={}; seen=set()
    def read(z,label,depth=0):
        if depth>5: raise ValueError('Unexpected nested JAR depth')
        names=set(z.namelist())
        if 'META-INF/mods.toml' in names:
            t=tomllib.loads(z.read('META-INF/mods.toml').decode('utf-8-sig'))
            for m in t.get('mods',[]):
                mid=m['modId']
                if depth==0 and mid in top: errors.append(f'Duplicate mod ID {mid}: {top[mid]}, {label}')
                if depth==0: top[mid]=label
                modids.add(mid)
            for owner,deps in t.get('dependencies',{}).items():
                for d in deps:
                    if d.get('mandatory'):
                        required.append((owner,d['modId'],d.get('versionRange',''),d.get('side','BOTH')))
        for n in names:
            if n.startswith('META-INF/jarjar/') and n.endswith('.jar'):
                with zipfile.ZipFile(io.BytesIO(z.read(n))) as inner: read(inner,label+'!'+n,depth+1)
    for r in rows:
        path=instance/('shaderpacks' if r['filename'].endswith('.zip') else 'mods')/r['filename']
        if not path.is_file(): errors.append(f'Missing locked file {path.name}')
    for p in mods.glob('*.jar'):
        try:
            with zipfile.ZipFile(p) as z: read(z,p.name)
        except (zipfile.BadZipFile,ValueError,KeyError) as e: errors.append(f'{p.name}: {e}')
    for owner,dep,rng,side in required:
        if dep not in modids: errors.append(f'{owner}: missing {dep} {rng} ({side})')
    for e in errors: print('FAIL:',e)
    print(f'Installed files: {len(top)} top-level mod IDs; {len(errors)} errors; version ranges and runtime NOT tested.')
    return not errors

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--curseforge',action='store_true');parser.add_argument('--instance',type=Path);a=parser.parse_args();rows=read_lock();static(rows);ok=True
    if a.curseforge:
        key=os.environ.get('CF_API_KEY');
        if not key: parser.error('CF_API_KEY is required for official API verification')
        ok=cf_audit(rows,key) and ok
    if a.instance: ok=jar_audit(rows,a.instance) and ok
    if not a.curseforge and not a.instance: print('Official API and installed JAR checks NOT run.')
    return 0 if ok else 1
if __name__=='__main__': sys.exit(main())
