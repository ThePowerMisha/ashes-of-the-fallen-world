from pathlib import Path
import zipfile,json,sys
root=Path(__file__).resolve().parents[1]
m=json.loads((root/'manifest.json').read_text())
output=Path(sys.argv[1]) if len(sys.argv)>1 else root.parent/f'Ashes_of_the_Fallen_World-{m["version"]}-CurseForge.zip'
with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as z:
 for name in ['manifest.json','modlist.html']:z.write(root/name,name)
 for p in sorted((root/'overrides').rglob('*')):
  if p.is_file():z.write(p,p.relative_to(root).as_posix())
with zipfile.ZipFile(output) as z:assert z.testzip() is None
print(output)
