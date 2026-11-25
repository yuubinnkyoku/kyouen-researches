import json,tempfile,copy
from pathlib import Path
from verify_gap6_terminal import verify
base=json.loads((Path(__file__).parent/'gap6-terminal-cert.json').read_text())
changes=[]
a=copy.deepcopy(base);a['s8_win_roots'][0]['s9_witness']=a['s8_win_roots'][0]['root'];changes.append(('illegal_s9_witness',a))
a=copy.deepcopy(base);a['s8_win_roots'][0]['s10_win_children'].pop();changes.append(('missing_s10_child',a))
a=copy.deepcopy(base);a['s8_loss_s10_leaves'].pop();changes.append(('missing_s10_loss_leaf',a))
a=copy.deepcopy(base);a['s8_loss_dual_weights_halves'][0]+=2;changes.append(('dual_weight_corruption',a))
for name,data in changes:
 with tempfile.TemporaryDirectory() as d:
  path=Path(d)/'mutated.json';path.write_text(json.dumps(data))
  try:verify(path,False)
  except ValueError as e:print('PASS rejected',name,':',str(e)[:90])
  else:raise AssertionError('ACCEPTED invalid certificate: '+name)
