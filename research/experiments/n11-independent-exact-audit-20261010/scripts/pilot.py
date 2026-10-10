"""Small measured independent minimax trials; no unbounded n11 search."""
import gzip
import json
import time
from independent import Board, solve_certificate
from audit import OUT, dump, key

def main():
    proof=json.loads(gzip.decompress((OUT/'raw-rooted-proof.json.gz').read_bytes()))
    results=[]
    board=Board(11)
    for n in (5,6):
        for v in (1,2):
            choices=[r for r in proof['nodes'].values() if int(r['mask']).bit_count()==n
                     and r['verdict']==v and r['kind']=='solver-replay']
            sample=min(choices,key=lambda r:r['evidence']['nodes'])
            start=time.perf_counter()
            attempt=solve_certificate(board,int(sample['mask']),2000)
            seconds=time.perf_counter()-start
            if attempt['verdict'] and attempt['verdict']!=v:
                raise ValueError('independent minimax contradiction')
            name=f'minimax-s{n}-{v}.json.gz'
            if attempt['certificate']:
                dump(name,attempt['certificate'])
            results.append(dict(stones=n,key=key(int(sample['mask'])),solver_verdict=v,
                saved_solver_nodes=sample['evidence']['nodes'],limit_unique_states=2000,
                verdict=attempt['verdict'],visited=attempt['visited'],seconds=seconds,
                certificate=name if attempt['certificate'] else None))
            print(results[-1],flush=True)
    # Fully self-contained small-board certificates and exhaustive safe-state
    # counts. The test suite checks every safe state using a side-to-move DP.
    small=[]
    for n in range(1,5):
        b=Board(n)
        safe=0
        for m in range(b.full+1):
            try: b.legal(m)
            except ValueError: continue
            safe+=1
        attempt=solve_certificate(b,0,100000)
        dump(f'minimax-n{n}-empty.json.gz',attempt['certificate'])
        small.append(dict(n=n,safe_states=safe,verdict=attempt['verdict'],visited=attempt['visited'],
                          certificate_nodes=len(attempt['certificate']['nodes'])))
    # Both terminal parities on n11, constructed independently rather than
    # assumed from a solver. These verify the empty-child base case on n11.
    terminal={}
    for seed in range(100):
        m=0
        while board.legal(m):
            pts=board.points(board.legal(m))
            m|=1<<pts[seed%len(pts)]
        v=1 if m.bit_count()%2 else 2
        terminal[v]=m
        if len(terminal)==2: break
    assert len(terminal)==2
    for v,m in terminal.items():
        attempt=solve_certificate(board,m,1)
        assert attempt['verdict']==v
        dump(f'minimax-n11-terminal-{v}.json.gz',attempt['certificate'])
    dump('minimax-pilot.json',dict(samples=results,small_boards=small,
        n11_terminal=[dict(key=key(m),stones=m.bit_count(),verdict=v) for v,m in terminal.items()],
        caveat='2000 unique-state limit per S5/S6 sample; costs are not extrapolated to 5734 roots'))

if __name__=='__main__': main()
