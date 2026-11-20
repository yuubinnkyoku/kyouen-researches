#!/usr/bin/env python3
"""Independent stdlib-only audit of the fold25 receipt and its geometry.
Uses coordinate permutations and a permutation-expanded 4x4 determinant,
not the fold25 machine's determinant/canonicalization helpers.
"""
import csv, hashlib, itertools, json, pathlib, sys

W = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '/tmp/kyouen-fold25/W')
OUT = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else W/'fold25/output/independent-audit.json')
checks=[]
def ok(cond, name):
    if not cond: raise SystemExit('AUDIT FAILED: '+name)
    checks.append(name)
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def blob_sha(path):
    b=path.read_bytes(); return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()

def point(p,t):
    x,y=p%11,p//11
    if t==0: X,Y=x,y
    elif t==1: X,Y=10-y,x
    elif t==2: X,Y=10-x,10-y
    elif t==3: X,Y=y,10-x
    elif t==4: X,Y=10-x,y
    elif t==5: X,Y=x,10-y
    elif t==6: X,Y=y,x
    else: X,Y=10-y,10-x
    return 11*Y+X

def transform(mask,t):
    z=0
    while mask:
        bit=mask & -mask; p=bit.bit_length()-1; mask-=bit
        z |= 1 << point(p,t)
    return z

def canon(mask): return min(transform(mask,t) for t in range(8))
def bits(mask): return [p for p in range(121) if (mask>>p)&1]

def det4(points):
    mat=[]
    for p in points:
        x,y=p%11,p//11
        mat.append([x,y,x*x+y*y,1])
    total=0
    for perm in itertools.permutations(range(4)):
        inv=sum(1 for i in range(4) for j in range(i+1,4) if perm[i]>perm[j])
        term=1
        for i,j in enumerate(perm): term*=mat[i][j]
        total += -term if inv&1 else term
    return total

def row_parents(row_hex, parent_int_to_hex):
    mask=int(row_hex,16); out=set()
    for p in bits(mask):
        c=canon(mask ^ (1<<p))
        if c in parent_int_to_hex: out.add(parent_int_to_hex[c])
    return out

foldp=W/'fold25/output/win8-root200003800200-receipt-fold-20261120.json'
fold24p=W/'fold24/output/win8-root438000000818-receipt-fold-20261120.json'
auditp=W/'k1137/output/win8-cert-extract-verification-20261120.json'
certp=W/'k1137/certs/win8-root-00000000000200003800200008180000-20261120.n11'
sweepp=W/'k1086/output/addtwo-greedy23-d10-sweep-20261120.json'
runnerp=W/'k1137/runner_v17.ts'
k1097p=W/'k1097/output/safe8-refuted50-refsolve-20261120.json'
worklistp=W/'inputs/worklist.csv'; censusp=W/'inputs/census.json'
record=json.loads(foldp.read_text()); prev=json.loads(fold24p.read_text()); audit=json.loads(auditp.read_text()); k1097=json.loads(k1097p.read_text())
root='00000000000200003800200008180000'
receipt=record['receipts'][0]
claim=sorted(receipt['covered_five_parent_target_rows'])
closed=sorted(receipt['covered_s6_rows'])
extra=sorted(receipt['extra_s6_rows_not_in_target'])

# Exact provenance pins.
ok(sha(fold24p)=='c4ab76d3cb7eba5c1ab8e1830c43d17bf9a771f511b66e7e8573864f3f2402c7','fold24 record SHA-256')
ok(sha(auditp)=='dafa177bf74fd528c34e9a858a83345df4cf8138c17f33ca0102c28840f28c04','K1137 audit SHA-256')
ok(sha(certp)=='7bd64a47bed13c25fe069b0b3563c06081639cd3d2ad09b28a1e6c65a41fa61d','K1137 certificate SHA-256')
ok(sha(sweepp)=='3045e15295af9b85b86578b5e8d55a8b325466eac576ee15b8450f6acb9b9ced','K1086 sweep SHA-256')
ok(blob_sha(runnerp)=='c132cc6425eee3feaeef1d697dd74f968cfedb59','runner v17 Git blob SHA-1')
ok(audit['all_gates_pass'] is True and audit['gate_count']==19 and all(g['passed'] for g in audit['gates']),'K1137 19/19 audit gates')
gates={g['gate']:g for g in audit['gates']}
ok(gates['g01_k1086_master_sha256_pin']['detail']==sha(sweepp),'K1086 pin embedded in K1137 g01')
ok(gates['g02_runner_v17_blob_pin_recorded']['detail']==blob_sha(runnerp)==gates['g03_runner_v17_copy_git_blob']['detail'],'runner v17 pin embedded in K1137 g02/g03')
ok(gates['g19_k1097_footprint_and_fold23_residual_open']['detail']['fold23_sha256']==sha(W/'fold23/output/win8-root208090020004-receipt-fold-20261120.json'),'K1137 g19 fold23 pin')
ok(sorted(gates['g19_k1097_footprint_and_fold23_residual_open']['detail']['residual_open_rows'])==claim,'K1137 g19 residual open rows equal claim (fold23 residual-29 era)')
ok(record['source_blob_pins'].__len__()==12 and record['source_sha256_pins'].__len__()==51,'12 blob pins + 51 SHA-256 pins')
ok(record['schema']=='n11-five-parent-win8-root200003800200-receipt-fold-20261120-v1' and record['status']=='fold-complete','fold25 schema and status')
ok(record['receipt_ordinal']=='thirty-second (fold25, fifteenth WIN8 receipt fold)' and receipt['receipt']=='thirty-second','fold25 receipt ordinal')
ok(receipt['root']==root and receipt['stones']==8 and receipt['verdict']=='WIN8-D10','receipt root identity and scope')
ok(record['frontier_before']==prev['frontier_after'],'fold25 frontier_before equals fold24 frontier_after')

# Certificate structure and K1097 footprint.
cert=certp.read_bytes(); lines=cert.decode().splitlines()
ok(len(cert)==706180 and len(lines)-2==19525,'certificate byte and strategy-row counts')
ok(lines[0]=='n11-terminal-strategy-v1 original_first_WIN8 second_to_move_LOSS' and lines[1]=='root '+root,'certificate header and root')
ok(lines[2:]==sorted(lines[2:]) and len(set(lines[2:]))==19525,'certificate rows sorted and unique')
ok(audit['root']==root and audit['recorded']['certificate']['sha256']==sha(certp),'K1137 audit certificate identity')
foot=k1097['win16_intrinsic_footprints'][root]
ok(foot['intrinsic_equals_claimed'] is True and sorted(foot['claimed'])==claim==sorted(foot['intrinsic']),'K1097 intrinsic footprint equals two receipt claims')
ok(len(k1097['gates'])==27 and all(g['ok'] for g in k1097['gates']),'K1097 27 gates')

# Independent D4 geometry using coordinate maps and a permutation-expanded determinant.
mask=int(root,16); stones=bits(mask)
unsafe=[]
for four in itertools.combinations(stones,4):
    if det4(four)==0: unsafe.append(four)
ok(len(stones)==8 and not unsafe,'root is eight-stone and quadruple-free')
ok(canon(mask)==mask,'root is D4-canonical')
rootA=set()
for t in range(8):
    image=transform(mask,t); sb=bits(image)
    for a,b in itertools.combinations(sb,2): rootA.add(canon(image^(1<<a)^(1<<b)))
rootB=set()
for six in itertools.combinations(stones,6):
    sm=0
    for p in six: sm|=1<<p
    rootB.add(canon(sm))
ok(rootA==rootB and len(rootA)==28,'two independent D4-removal constructions agree on 28 rows')
legal=[]
for p in range(121):
    if (mask>>p)&1: continue
    if all(det4((*triple,p))!=0 for triple in itertools.combinations(stones,3)):
        legal.append(p)
ok(len(legal)==42,'independent integer determinant mobility 42')
ok(set(int(h,16) for h in claim)<=rootA and len(claim)==2,'two claimed rows belong to the 28-row root footprint')
ok(set(int(h,16) for h in extra)<=rootA and len(extra)==1,'the one extra row belongs to the root footprint geometry')
ok(all(h not in foot['intrinsic'] for h in extra),'extra row outside the K1097 win16 intrinsic footprint')
ok(closed==sorted(claim+extra) and len(closed)==3,'covered rows are exactly the two claims plus one extra')

# Independently derive parent incidence and edge cost from worklist + census.
with worklistp.open(newline='') as f: wl={r['s6_canonical_hex']:r for r in csv.DictReader(f)}
census=json.loads(censusp.read_text())
parents=census['open_s5_census']; parent_int_to_hex={int(p['hex'],16):p['hex'] for p in parents}; parent_by_hex={p['hex']:p for p in parents}
parent_counts={}
row_parent_sets={}
for h in closed:
    ok(h in wl,'closed row present in worklist '+h)
    ps=row_parents(h,parent_int_to_hex); row_parent_sets[h]=sorted(ps)
    for p in ps: parent_counts[p]=parent_counts.get(p,0)+1
cost=sum(int(wl[h]['own_candidates_s6_s7_edge_cost']) for h in closed)
expected_parent_deltas=[]
for p in sorted(parent_counts):
    expected_parent_deltas.append({'parent_hex':p,'classes':parent_by_hex[p]['classes'],'rows_closed':parent_counts[p]})
actual=receipt['parent_deltas']
actual_projection=[{'parent_hex':p['parent_hex'],'classes':p['classes'],'rows_closed':p['rows_closed']} for p in actual]
ok(actual_projection==expected_parent_deltas,'parent delta map independently rederived from 3 rows and census')
ok(sum(parent_counts.values())==6 and len(parent_counts)==4,'three rows touch six parent incidences across four parents')
ok(all(parent_by_hex[p]['classes']==2 for p in parent_counts),'all four affected parents are class 2')
ok(all(p['rows_after']==p['rows_before']-p['rows_closed'] for p in actual),'per-parent before/after arithmetic')
ok(cost==216 and receipt['closed_edge_cost']==216,'closed edge cost independently sums to 216')
ok(receipt['affected_parents']==4 and len(actual)==4,'four affected parent rows')

# Frontier arithmetic and target ledger.
before=record['frontier_before']; after=record['frontier_after']
ok(before['unique_remaining_s6']==6123 and after['unique_remaining_s6']==6120,'S6 frontier 6123 -> 6120')
ok(before['sum_remaining_cost']==485213 and after['sum_remaining_cost']==484997,'remaining cost 485213 -> 484997')
ok(before['solved_s6_in_manifest']==1725 and after['solved_s6_in_manifest']==1728,'manifest bookkeeping 1725 -> 1728')
ok(before['parent_row_incidence']==11660 and after['parent_row_incidence']==11654 and before['parent_row_incidence']-after['parent_row_incidence']==sum(parent_counts.values()),'parent incidence 11660 -> 11654, decrement 6')
ok(before['s6_needed_by_open_classes']==4431 and after['s6_needed_by_open_classes']==4428,'needed S6 4431 -> 4428')
ok(before['cost_needed_by_open_classes']==351661 and after['cost_needed_by_open_classes']==351445,'needed cost 351661 -> 351445')
ok(before['remaining_s5_orbits']==after['remaining_s5_orbits']==173,'remaining S5 orbits unchanged')
ok(receipt['covered_s6_rows']==closed and receipt['covered_five_parent_target_rows']==claim and receipt['extra_s6_rows_not_in_target']==extra,'covered rows split into two claims plus one extra')
ok(record['five_parent_target_after']['closed_target_rows_total']==88 and record['five_parent_target_after']['residual_target_rows']==24,'target ledger 88 closed / 24 residual')
ok(record['win_candidate_plan_impact']['win16_candidates_remaining']==1 and record['win_candidate_plan_impact']['win16_claimed_rows_remaining']==1,'K1097 plan leaves one candidate / one claimed row')
ok(record['controls'] and all(record['controls'].values()),'all 93 fold controls true')

result={
 'schema':'n11-fold25-independent-audit-v1','status':'PASS','checks':checks,'check_count':len(checks),
 'receipt_sha256':sha(foldp),'certificate_sha256':sha(certp),'K1137_audit_sha256':sha(auditp),
 'root':root,'claimed_rows':claim,'extra_rows':extra,'row_parent_sets':row_parent_sets,'parent_counts':parent_counts,
 'closed_edge_cost':cost,'parent_incidence_before':before['parent_row_incidence'],
 'parent_incidence_after':after['parent_row_incidence'],'parent_incidence_decrement':sum(parent_counts.values()),
 'frontier_before':before,'frontier_after':after,
 'geometry':{'stones':len(stones),'unsafe_quads':len(unsafe),'legal_moves':len(legal),'canonical_rows_method_A':len(rootA),'canonical_rows_method_B':len(rootB),'methods_equal':rootA==rootB},
 'scope_guard':'This audit verifies a certificate-backed WIN8-D10 root and receipt bookkeeping only; it does not solve the empty 11x11 board or any two-stone root.'
}
OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':result['status'],'check_count':len(checks),'receipt_sha256':result['receipt_sha256'],'audit_sha256':sha(OUT),'parent_incidence':f"{before['parent_row_incidence']}->{after['parent_row_incidence']}",'parent_delta':sum(parent_counts.values()),'affected_parents':len(parent_counts),'cost':cost,'rows':closed},indent=2))
