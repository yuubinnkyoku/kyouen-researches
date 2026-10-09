"""Summarize measured costs and materialize the next unproved boundary."""
import gzip
import json
from collections import Counter
from study import ROOT, EXP, s5cache, sha, dump, legal_points, pts

def main():
    out=EXP/'output'
    cache=s5cache(out/'current-exact-s5.cache')
    profile=json.loads((out/'historical-cost-profile.json').read_text())['profile']
    geo=json.loads(gzip.decompress((out/'geometry.json.gz').read_bytes()))
    hist={(h['stones'],*h['key']):h for h in json.loads((out/'history.json').read_text())}
    runs=[json.loads(f.read_text()) for f in sorted(out.glob('*/summary.json'))]
    for run in runs:
        for r in run['results']:
            if r.get('verdict') is None:
                continue
            k=(r['stones'],*r['key'])
            h=hist.setdefault(k,dict(verdict=0,max_unknown_budget=0))
            if r['verdict']:
                h['verdict']=r['verdict']
            else:
                h['max_unknown_budget']=max(h['max_unknown_budget'],r['budget'])
    ranking=[]
    for g in geo:
        if not {100,108}.intersection(g['coverage']):
            continue
        ch={tuple(c) for c in g['children']}
        if any(cache.get(c)==1 for c in ch) or all(cache.get(c)==2 for c in ch):
            continue
        unknown=sorted(ch-cache.keys())
        legals={k:len(legal_points(pts(k))) for k in unknown}
        estimated=sum(profile.get(str(l//10*10),{'mean_truncated_nodes':15_000_000})['mean_truncated_nodes'] for l in legals.values())
        held=[k for k in unknown if hist.get((5,*k),{}).get('max_unknown_budget',0)>=15_000_000]
        ranking.append(dict(key=g['key'],coverage=g['coverage'],unknown=len(unknown),known_loss=len(ch)-len(unknown),
                            children=len(ch),full_remaining_coverage={100,108}.issubset(g['coverage']),
                            capped_cost_proxy=estimated,held_same_15m=held,unknown_keys=unknown))
    ranking.sort(key=lambda r:(not r['full_remaining_coverage'],r['capped_cost_proxy'],r['key']))
    next_row=ranking[0]
    ready=[k for k in next_row['unknown_keys'] if k not in next_row['held_same_15m']]
    ready.sort(key=lambda k:(len(legal_points(pts(k))),k))
    dump(out/'next-boundary.json',dict(ranking=ranking,next_class=next_row,
         next_probe_keys=ready[:8],budget=15_000_000,dispatch=False,
         prerequisite='refresh origin/main, exact cache, raw history, quarantine registry and saved S6/S7 intersections'))
    measurements={}
    for arm in ('A','B','C','C_shared','B_next','B_completion'):
        rr=[r for run in runs for r in run['results'] if r.get('arm')==arm and r.get('verdict') is not None]
        measurements[arm]=dict(rows=len(rr),nodes=sum(r['nodes'] for r in rr),
             wall_seconds=sum(r['wall_seconds'] for r in rr),peak_rss_bytes=max((r['peak_rss_bytes'] for r in rr),default=0),
             verdicts=dict(Counter(r['verdict'] for r in rr)))
    dump(out/'strategy-comparison.json',dict(measurements=measurements,
        same_condition_pilot=dict(budget=2_000_000,workers=1,memo=22,order='count',
           hardware='AMD Ryzen 7 5800HS, 8 cores / 16 threads, Windows',
           A_nodes=290045,B_nodes=7289601,
           caveat='four deliberately selected low-branching leaves per arm; not random, no uncensored cost bound'),
        A=dict(initial_s5_unknown=2,initial_s6_unknown=6,initial_s7_unknown=512,
               minimum_complete_loss_pair_s7=175,S7_incidences=521,shared_s7=9,
               decisive_refutation_s6_nodes=2214318,
               final='WIN: this S4 cannot supply a LOSS certificate'),
        B=dict(initial_candidates=115,initial_excluded_WIN=44,initial_eligible_UNKNOWN=71,
               first_alternative=[1297036692700528640,0],initial_s5_unknown=98,
               estimated_capped_completion_nodes=534944346.6166041,
               direct_probe_refutation_nodes=7541821,
               final_remaining_candidate_count=len(ranking),
               final='first alternative is WIN; all eight escalation siblings stopped after one replay'),
        C=dict(choice='polarity-aware direct S6 escalation, exact LOSS reverse propagation, shared S5 rejection probes',
               S6_escalation_nodes=20056308,shared_S5_nodes=44544197,
               new_exact_S5_from_direct_replays=sum(r.get('verdict') in (1,2) and r['stones']==5 for run in runs for r in run['results']),new_exact_S5_from_sound_propagation=6,
               caveat='no calibrated probabilities; no independent recursive minimax leaf certificate'),
        next_class={k:v for k,v in next_row.items() if k!='unknown_keys'},
        rigorous_bounds=dict(minimum_additional_class=1,rational_dual='1',
               finite_node_dispatch_caps={'pilot':16000000,'direct_S6':90000000,'B_escalation':120000000,'shared':120000000,'next_pilot':120000000,'next_completion':1365000000},
               no_completion_upper_bound=True),
        total_nodes=sum(run['total_nodes'] for run in runs),
        compiler=dict(command='g++ -O3 -std=c++20 -DNDEBUG cpp/solvers/kyouen_dfpn_root.cpp -o .local/n11/strategy-20261010/dfpn.exe',
                      version='g++ 15.2.0 (MSYS2 Rev8)',solver_source_sha256=sha(ROOT/'cpp/solvers/kyouen_dfpn_root.cpp'))))
    print('next', {k:v for k,v in next_row.items() if k!='unknown_keys'}, 'live candidates',len(ranking))
    print('measurements',measurements)

if __name__=='__main__':
    main()
