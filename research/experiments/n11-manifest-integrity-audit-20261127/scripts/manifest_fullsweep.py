import json, urllib.request, hashlib, time, os, sys
from concurrent.futures import ThreadPoolExecutor

BASE="https://raw.githubusercontent.com/yuubinnkyoku/kyouen-researches/main/"
tree=json.load(open('tree2.json'))
entries={e['path'] for e in tree['tree'] if e['type']=='blob'}
targets=sorted(p for p in entries if 'MANIFEST' in p and p.endswith('.txt') and '/n11-' in p)
DONE='fs_done.txt'; BAD='fs_bad.txt'
done=set()
if os.path.exists(DONE):
    done=set(open(DONE).read().split())
todo=[t for t in targets if t not in done]
print(f"{len(targets)} manifests, {len(todo)} remaining", flush=True)

def fetch(p):
    try:
        with urllib.request.urlopen(BASE+p, timeout=25) as r:
            return r.read()
    except Exception:
        return None

def resolve(kit, rel):
    rel=rel.strip('./')
    if rel.startswith('research/'): return rel if rel in entries else None
    for c in (kit+'/'+rel, rel, 'research/experiments/'+rel):
        if c in entries: return c
    return None

def handle_manifest(m):
    out=[]
    b=fetch(m)
    if b is None: return [(m,'MANIFEST_FETCH_FAIL','')]
    kit=m.rsplit('/',1)[0]
    for rawline in b.decode(errors='replace').splitlines():
        line=rawline.split('(')[0].strip()
        if not line or line.startswith('#'): continue
        parts=line.replace(',',' ').split()
        if len(parts)>=3 and parts[1].isdigit():
            sha,size,rel=parts[0],int(parts[1]),parts[2]
        elif len(parts)==2:
            sha,size,rel=parts[0],None,parts[1]
        else:
            out.append((m,'UNPARSED',rawline[:100])); continue
        fp=resolve(kit,rel)
        if fp is None:
            out.append((m,'NOT_IN_TREE',rel)); continue
        fb=fetch(fp)
        if fb is None: out.append((m,'FETCH_FAIL',fp)); continue
        h=hashlib.sha256(fb).hexdigest()
        if h!=sha: out.append((m,'SHA_MISMATCH',f"{fp} manifest={sha} actual={h} size={len(fb)}"))
        elif size is not None and size!=len(fb): out.append((m,'SIZE_MISMATCH',f"{fp} manifest={size} actual={len(fb)} sha_ok"))
    return out

with open(DONE,'a') as df, open(BAD,'a') as bf:
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs={ex.submit(handle_manifest, m): m for m in todo}
        for f in futs:
            pass
        import concurrent.futures as cf2
        for f, m in [(f2, futs[f2]) for f2 in cf2.as_completed(futs)]:
            for r in f.result():
                bf.write(' '.join(r)+'\n'); bf.flush()
            df.write(m+'\n'); df.flush()
print("done")
