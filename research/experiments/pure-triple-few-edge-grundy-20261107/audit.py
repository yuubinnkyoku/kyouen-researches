#!/usr/bin/env python3
"""All pure-three-point clutters with <=5 edges, any number of vertices."""
from collections import Counter
from functools import lru_cache
from itertools import permutations
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


def mex(values):
    g=0
    while g in values:g+=1
    return g


def patterns(h):
    masks=sorted([m for m in range(1,1<<h) if m.bit_count()>=2],key=lambda m:(-m.bit_count(),m))
    found=set()
    def visit(j,remaining,counts):
        if j==len(masks):
            full=[0]*((1<<h)-1)
            for mask,count in counts:full[mask-1]=count
            for e,count in enumerate(remaining):full[(1<<e)-1]=count
            signatures=[m for m,count in enumerate(full,1) for _ in range(count)]
            edges=[sum(1<<v for v,s in enumerate(signatures) if s>>e&1) for e in range(h)]
            if len(set(edges))==h:found.add(tuple(full))
            return
        m=masks[j]
        for count in range(min(remaining[e] for e in range(h) if m>>e&1)+1):
            visit(j+1,tuple(r-count if m>>e&1 else r for e,r in enumerate(remaining)),counts+[(m,count)])
    visit(0,(3,)*h,[])
    return found


def quotient_grundy(signature):
    h=(len(signature)+1).bit_length()-1
    cells=[(mask,count) for mask,count in enumerate(signature,1) if count]
    @lru_cache(None)
    def game(chosen):
        usage=[sum(chosen[i] for i,(mask,count) in enumerate(cells) if mask>>e&1) for e in range(h)]
        options=set()
        for i,(mask,count) in enumerate(cells):
            if chosen[i]==count or any(usage[e]==2 for e in range(h) if mask>>e&1):continue
            child=list(chosen);child[i]+=1
            options.add(game(tuple(child)))
        return mex(options)
    value=game((0,)*len(cells))
    return value,game.cache_info().currsize


def representatives(h):
    pending=patterns(h)
    labeled=len(pending)
    maps=[]
    for permutation in permutations(range(h)):
        maps.append([sum(1<<permutation[e] for e in range(h) if mask>>e&1) for mask in range(1,1<<h)])
    records=[]
    while pending:
        representative=min(pending)
        orbit=set()
        for mapping in maps:
            image=[0]*len(representative)
            for old,count in enumerate(representative):image[mapping[old]-1]=count
            orbit.add(tuple(image))
        assert orbit<=pending
        pending-=orbit
        value,states=quotient_grundy(representative)
        memberships=[mask for mask,count in enumerate(representative,1) for _ in range(count)]
        edges=[sum(1<<v for v,m in enumerate(memberships) if m>>e&1) for e in range(h)]
        assert all(edge.bit_count()==3 for edge in edges) and len(set(edges))==h
        records.append(dict(h=h,n=len(memberships),signature=representative,edges=edges,
                            grundy=value,one_free_grundy=value^1,quotient_states=states,
                            edge_label_orbit_size=len(orbit)))
    return labeled,records


@lru_cache(None)
def canonical_signature(signature):
    h=(len(signature)+1).bit_length()-1
    cells=[(mask,count) for mask,count in enumerate(signature,1) if count]
    best=None
    for permutation in permutations(range(h)):
        image=[0]*len(signature)
        for mask,count in cells:
            new=sum(1<<permutation[e] for e in range(h) if mask>>e&1)
            image[new-1]=count
        image=tuple(image)
        if best is None or image<best:best=image
    return best


def independent_edge_extensions(previous,h):
    # A different complete generator: remove/add the last three-point edge.
    # Vertices private to the new edge are exactly the new singleton cell.
    output=set();new_bit=1<<(h-1)
    for old in previous:
        cells=[(mask,count) for mask,count in enumerate(old,1) if count]
        def choose(index,left,amounts):
            if index<len(cells):
                for k in range(min(left,cells[index][1])+1):
                    choose(index+1,left-k,amounts+[k])
                return
            counts=[0]*((1<<h)-1)
            for (mask,count),k in zip(cells,amounts):
                counts[mask-1]+=count-k
                counts[(mask|new_bit)-1]+=k
            counts[new_bit-1]+=left
            memberships=[mask for mask,count in enumerate(counts,1) for _ in range(count)]
            edges=[sum(1<<v for v,m in enumerate(memberships) if m>>e&1) for e in range(h)]
            if len(set(edges))==h:output.add(canonical_signature(tuple(counts)))
        choose(0,3,[])
    return output


def main():
    directory=Path(__file__).resolve().parent
    all_records=[];summary=[];previous={()}
    for h in range(1,6):
        labeled,records=representatives(h)
        all_records+=records
        separate=independent_edge_extensions(previous,h)
        expected={tuple(row['signature']) for row in records}
        assert separate==expected
        previous=separate
        summary.append(dict(edges=h,labeled_signatures=labeled,unlabeled_types=len(records),
            core_histogram=dict(sorted(Counter(row['grundy'] for row in records).items())),
            core_max=max(row['grundy'] for row in records),
            with_free_max=max(max(row['grundy'],row['one_free_grundy']) for row in records)))
        print(summary[-1],flush=True)
    compiler=shutil.which('g++')
    if compiler is None:raise SystemExit('g++ is required for the independent subset audit')
    with tempfile.TemporaryDirectory(prefix='kyouen-pure3-edges-') as scratch:
        temp=Path(scratch).resolve()
        assert temp.parent==Path(tempfile.gettempdir()).resolve()
        data=temp/'cases.txt';binary=temp/'native.exe';values=temp/'values.bin'
        data.write_text(str(len(all_records))+'\n'+'\n'.join(
            ' '.join(map(str,[row['n'],row['h'],*row['edges']])) for row in all_records)+'\n',encoding='ascii')
        subprocess.run([compiler,'-std=c++17','-O2',str(directory/'independent.cpp'),'-o',str(binary)],check=True)
        native=json.loads(subprocess.check_output([str(binary),str(data),str(values)],text=True))
        assert values.read_bytes()==bytes(row['grundy'] for row in all_records)
    output=dict(audit='PASS',summary=summary,types_compared=len(all_records),
                independent_generation='all edge-extension types equal all Venn-row types for h=1..5',
                cpp_safe_subset_states=native['safe_states'],records=all_records)
    target=directory/'output/audit.json';target.parent.mkdir(exist_ok=True)
    head={key:value for key,value in output.items() if key!='records'}
    text=json.dumps(head,indent=2)
    text=text[:-2]+',\n  "records": [\n'+',\n'.join('    '+json.dumps(row,separators=(',',':')) for row in all_records)+'\n  ]\n}\n'
    json.loads(text);target.write_text(text,encoding='utf-8')
    print(json.dumps(head,indent=2),flush=True)


if __name__=='__main__':main()
