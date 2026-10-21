#!/usr/bin/env python3
"""Independent subset oracle: no kernel transitions, normalization or compression."""
import functools,hashlib,json,pathlib
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[2]
SOURCE=ROOT/'research/experiments/n11-reduction-followup-20261005/output/n11-snapshots.json'

def evaluate(s):
    labels={v:i for i,v in enumerate(s['legal'])}
    edges=[sum(1<<labels[v] for v in e) for e in s['minimal_residual_edges']]
    full=(1<<len(labels))-1
    @functools.lru_cache(None)
    def g(selected):
        seen=set();moves=full^selected
        while moves:
            bit=moves&-moves;moves-=bit;child=selected|bit
            if not any(child&edge==edge for edge in edges):seen.add(g(child))
        value=0
        while value in seen:value+=1
        return value
    return dict(g=g(0),states=g.cache_info().currsize)

def main():
    snapshots=json.loads(SOURCE.read_text())['snapshots'];assert len(snapshots)==826
    result=[]
    for i,s in enumerate(snapshots):result.append(dict(id=i,**evaluate(s)))
    output=dict(source=str(SOURCE.relative_to(ROOT)),sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        total_states=sum(r['states'] for r in result),rows=result)
    (HERE/'oracle.json').write_text(json.dumps(output,indent=2)+'\n')
    print(f'VERIFIED independent roots={len(result)} states={output["total_states"]}')
if __name__=='__main__':main()
