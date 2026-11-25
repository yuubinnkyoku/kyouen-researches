from pathlib import Path
import shutil
from verify_loss6_global import run
B=Path(__file__).resolve().parent
run(full=False)
# Negative tests are performed on temporary copies, never original files.
a=(B/'loss6_dual.tsv').read_text().splitlines()
for name,lines in [('dual_zero', [a[0].split('\t')[0]+'\t-1']+a[1:]),('dual_inflate',[a[0].split('\t')[0]+'\t10']+a[1:]),('dual_missing',a[:-1])]:
 path=B/(name+'.tmp')
 try:
  path.write_text('\n'.join(lines)+'\n')
  try:run(dual=path.name,full=False)
  except ValueError:pass
  else:raise AssertionError('accepted invalid dual '+name)
 finally:path.unlink(missing_ok=True)
selected=(B/'loss6_all_cover_selected.txt').read_text().splitlines()
path=B/'selected_missing.tmp'
try:
 path.write_text('\n'.join(selected[:-1])+'\n')
 try:run(selection=path.name,full=False)
 except ValueError:pass
 else:raise AssertionError('accepted incomplete selected cover')
finally:path.unlink(missing_ok=True)
print('PASS 4 mutation rejections')
