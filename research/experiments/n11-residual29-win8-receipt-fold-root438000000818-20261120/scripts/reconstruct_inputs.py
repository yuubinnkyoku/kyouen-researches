#!/usr/bin/env python3
"""Reconstruct the pinned fold24 W tree from GitHub at an immutable commit."""
import ast, hashlib, json, pathlib, re, sys, urllib.request
REPO='yuubinnkyoku/kyouen-researches'
HEAD=sys.argv[2] if len(sys.argv)>2 else 'b91e85a99f0480f084835bdff51533d0cf5feaa8'
ROOT=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else '/tmp/kyouen-fold24/W-reconstructed')
RAW=f'https://raw.githubusercontent.com/{REPO}/{HEAD}/'
API=f'https://api.github.com/repos/{REPO}/git/trees/'
ROOT.mkdir(parents=True,exist_ok=True)
def get(url): return urllib.request.urlopen(url,timeout=90).read()
# The published fold23 machine carries the 12 Git-blob pins and 46 SHA-256 pins.
source=get(RAW+'research/experiments/n11-residual29-win8-receipt-fold-root208090020004-20261120/scripts/fold_win8_root208090020004.py').decode()
def literal_dict(name):
 m=re.search(rf'{name} = (\{{.*?\n\}})',source,re.S)
 return ast.literal_eval(m.group(0).split('=',1)[1])
PINS=literal_dict('PINS'); PIN256=literal_dict('PIN256')
# Exact Git tree paths are found by blob SHA for the legacy Git-blob pins.
root_tree=json.loads(get(API+HEAD))['tree']
research=next(x for x in root_tree if x['path']=='research')
research_tree=json.loads(get(API+research['sha']))['tree']
experiments=next(x for x in research_tree if x['path']=='experiments')
exp_tree=json.loads(get(API+experiments['sha']+'?recursive=1'))['tree']
by_sha={x['sha']:x['path'] for x in exp_tree if x['type']=='blob'}

def write_checked(rel,data,kind,expected):
 if kind=='sha256': actual=hashlib.sha256(data).hexdigest()
 elif kind=='blob': actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
 else: raise ValueError(kind)
 if actual!=expected: raise SystemExit(f'{kind} mismatch {rel}: {actual} != {expected}')
 out=ROOT/rel; out.parent.mkdir(parents=True,exist_ok=True); out.write_bytes(data)
 print(kind,rel,len(data),actual)

for rel,sha in PINS.items():
 p=by_sha.get(sha)
 if not p: raise SystemExit(f'no tree path for pinned blob {rel} {sha}')
 write_checked(rel,get(RAW+'research/experiments/'+p),'blob',sha)

folders={
'foldv2':'n11-117pool-d10-sweep-7th8th-win7-certs-20261119/foldv2',
'resolve6':'n11-residual78-cache-join-resolve6-20261120',
'fs13':'n11-residual78-windfall4-receipt-fold-20261120',
'sv17pub':'n11-residual78-seventeenth-win7-cert-extract-20261120',
'fold10':'n11-seventeenth-win7-receipt-fold-20261120/fold',
'k1096':'n11-residual72-win8-cert-extract-root8003180-20261120',
'k1097':'n11-residual72-safe8-refuted50-refsolve-20261120',
'fold11':'n11-residual72-win8-receipt-fold-root8003180-20261120',
'k1106':'n11-residual72-win8-cert-extract-root8005021-20261120',
'fold12':'n11-residual68-win8-receipt-fold-root8005021-20261120',
'k1108':'n11-residual65-win8-cert-extract-root9840004-20261120',
'fold13':'n11-residual65-win8-receipt-fold-root9840004-20261120',
'k1109':'n11-residual65-win8-cert-extract-root9090022-20261120',
'fold14':'n11-residual62-win8-receipt-fold-root9090022-20261120',
'k1114':'n11-residual58-win8-cert-extract-root120000038-20261120',
'fold15':'n11-residual58-win8-receipt-fold-root120000038-20261120',
'k1113':'n11-residual58-win8-cert-extract-root8890020-20261120',
'fold16':'n11-residual55-win8-receipt-fold-root8890020-20261120',
'k1117':'n11-residual55-win8-cert-extract-root22081000-20261120',
'fold17':'n11-residual51-win8-receipt-fold-root22081000-20261120',
'k1120':'n11-residual48-win8-cert-extract-root00901010-20261120',
'fold18':'n11-residual48-win8-receipt-fold-root00901010-20261120',
'k1119':'n11-residual51-win8-cert-extract-root1009000-20261120',
'fold19':'n11-residual41-win8-receipt-fold-root1009000-20261120',
'k1121':'n11-residual48-win8-cert-extract-root08d10000-20261120',
'fold20':'n11-residual38-win8-receipt-fold-root08d10000-20261120',
'k1124':'n11-residual45-win8-cert-extract-root80880200-20261120',
'fold21':'n11-residual35-win8-receipt-fold-root80880200-20261120',
'k1125':'n11-residual45-win8-cert-extract-root840500-20261120',
'fold22':'n11-residual32-win8-receipt-fold-root840500-20261120',
'k1123':'n11-residual48-win8-cert-extract-root208090020004-20261120',
'fold23':'n11-residual29-win8-receipt-fold-root208090020004-20261120',
'k1136':'n11-residual29-win8-cert-extract-root438000000818-20261120',
}
# New fold24 chain pins: fold23 record + K1136 audit + K1136 certificate.
extra_pin256={
'fold23/output/win8-root208090020004-receipt-fold-20261120.json':'04f334ff0f6aa995375283e94afc0e83ced6bebfeefea47359a5090a338fad59',
'k1136/output/win8-cert-extract-verification-20261120.json':'d065383428621e03cfda87c9b20834f3e425c8c0e58f30823ee36d20828aa90c',
'k1136/certs/win8-root-00000000000000043800000008180010-20261120.n11':'dbcb0bae71b9e00570f66db601790380362c65aaad2e46911cd2b80119337004',
}
all_pin256={**PIN256,**extra_pin256}
for rel,expected in all_pin256.items():
 alias,sub=rel.split('/',1)
 if alias not in folders: raise SystemExit('unmapped alias '+alias)
 prefix=folders[alias]+'/'
 wanted=prefix+sub
 paths=[x['path'] for x in exp_tree if x['type']=='blob' and x['path']==wanted]
 if not paths:
  paths=[x['path'] for x in exp_tree if x['type']=='blob' and x['path'].startswith(prefix) and x['path'].split('/')[-1]==sub.split('/')[-1]]
 if len(paths)!=1: raise SystemExit(f'cannot uniquely resolve {rel}: {paths}')
 write_checked(rel,get(RAW+'research/experiments/'+paths[0]),'sha256',expected)

# Additional inputs are checked by the K1136 audit's own g01/g02/g03 pins.
write_checked('k1091/output/replace15-d10-sweep-20261120.json',
 get(RAW+'research/experiments/n11-residual72-replace15-d10-sweep-20261120/output/replace15-d10-sweep-20261120.json'),
 'sha256','edd7ac84f47268adcc8a3364a5ff687499cb2a76ded0c0fa379506af02f40b25')
runner=get(RAW+'research/experiments/n11-residual29-win8-cert-extract-root438000000818-20261120/runner_v17.ts')
write_checked('k1136/runner_v17.ts',runner,'blob','c132cc6425eee3feaeef1d697dd74f968cfedb59')

# Published predecessor machines needed by the nested pristine rerun chain.
machines={
'fold_win8_root840500.py':('n11-residual32-win8-receipt-fold-root840500-20261120/scripts/fold_win8_root840500.py','d5721408e7fb41e794175f3f3bb8b9d43fae13d18c244a831b81532aa9f1db1d'),
'fold_win8_root80880200.py':('n11-residual35-win8-receipt-fold-root80880200-20261120/scripts/fold_win8_root80880200.py','44399cc59ef088ad25e90411f4404dbd0bad8ff14bc7c8a50be1a91bcc04102b'),
'fold_win8_root08d10000.py':('n11-residual38-win8-receipt-fold-root08d10000-20261120/scripts/fold_win8_root08d10000.py','9e141d4a721025fd55a5bda68266a5f1b43cbcb65112f438839b0db351a06f72'),
'fold_win8_root1009000.py':('n11-residual41-win8-receipt-fold-root1009000-20261120/scripts/fold_win8_root1009000.py','51442d96341fcffc17d9cb72e36946cb68cd97100abaa6939b27e0d6a20949e8'),
'fold_win8_root00901010.py':('n11-residual48-win8-receipt-fold-root00901010-20261120/scripts/fold_win8_root00901010.py','dcdfbf92d62409cc3a92f9f16f319e1328180622660b39751921b5de72800091'),
'fold_win8_root00901010_preverified.py':('n11-residual41-win8-receipt-fold-root1009000-20261120/scripts/fold_win8_root00901010_preverified.py','d342f1f883d2e22ecca25903ec14ed24f16c77a0895e3ed022ab8832736e7f9e'),
'fold_win8_root208090020004.py':('n11-residual29-win8-receipt-fold-root208090020004-20261120/scripts/fold_win8_root208090020004.py','c908f6c02842a305d642dcbb6157d3dfd832350afcc59452b0c917b0277d0a8e'),
}
for rel,(path,expected) in machines.items(): write_checked(rel,get(RAW+'research/experiments/'+path),'sha256',expected)
print('RECONSTRUCTED',ROOT,'PINS',len(PINS),'PIN256',len(all_pin256),'machine_files',len(machines))
