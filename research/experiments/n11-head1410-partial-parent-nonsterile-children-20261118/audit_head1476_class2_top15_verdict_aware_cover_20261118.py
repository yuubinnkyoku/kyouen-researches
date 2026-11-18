#!/usr/bin/env python3
"""Pinned verdict-aware cover audit for the head-1476 class-2 parent."""
import hashlib, itertools, json, os, sys
HERE=os.path.dirname(os.path.abspath(__file__))
ROOT=os.path.abspath(os.path.join(HERE,"..","..",".."))
OUT=os.path.join(HERE,"output","head1476-class2-top15-verdict-aware-cover-audit-20261118.json")
MAIN_COMMIT="e3efa46aa9ae36e3c8d06a1fae3a4a25936c53b8"
INPUTS={
 "membership":("research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/minimum-cover-root-membership-20261118.json","ab1e655f4a89a677e57515cdbacfe56894323013"),
 "cost69j":("research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost69j-inflight-20261117.json","a87dcb727a2d29a34be244d2713cb21f36f85442"),
 "cost79c":("research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost79c-inflight-20261118.json","ca517b73ffe287def7bf2c215fa4c38a6d15838a"),
 "cost73j":("research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost73j-inflight-20261117.json","74fc3417391e30cf4cff9c2ffce059dce529ed86"),
 "cost78c":("research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost78c-inflight-20261117.json","1850832186ba9c8715624094f05d67aa4eb10f0b"),
 "cost73l":("research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost73l-inflight-20261117.json","39cf0f9b31a28ad6358f157e2433477ab0659243"),
 "cost72d":("research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost72d-inflight-20261117.json","c64e28fdc91ba9ffaa3518dfbc9d764ec5663b05"),
 "cost73i":("research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost73i-inflight-20261117.json","4a6a17e66fc1a1bfe8efb7dc6fb2400b9af6aa1d"),
 "win66j":("research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost66j-win7-certificates-20261117.json","b0af082044f669cdc7d5e633544069173938f7cb"),
 "win73i":("research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost73i-certificates/class2-lane-cost73i-win7-certificates-20261118.json","8a766a4225c418cb5eae297404de71d7f402c103"),
 "audit66j":("research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-66j69j-certificates-bigint-independent-reverification-20261117.json","c24224eaa3f48b0e5d1fbe90f4daccf284e6c968"),
 "audit73i":("research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost73i-certificates-third-independent-audit-20261118.json","f98b2c54c612339ad06b97306b32d04e701beb18"),
}
REFUTED=[
 (2,"00000000000000c29002000000001000","cost69j","108"),
 (4,"00000000000000c09002000200001000","cost79c","12"),
 (5,"00000000020001003800040008000000","cost73j","97"),
 (7,"00000000000021801202000000080000","cost78c","97"),
 (9,"00000000000000c29002000000400000","cost73l","65"),
 (10,"00000000000041801202000000100000","cost72d","108"),
 (11,"00000000000000c09002000200400000","cost79c","22"),
 (12,"00000000100001801202000000100000","cost73i","108"),
 (13,"00000000200040003801000000100000","cost73j","108"),
 (14,"00000000000021801202000000100000","cost78c","108"),
]
WINS=[
 (6,"00000000020001003810000008000000","win73i","audit73i",97),
 (15,"00000000000000c09002000000001200","win66j","audit66j",9),
]
def blob_sha(b): return hashlib.sha1(b"blob %d\\0"%len(b)+b).hexdigest()
def load():
 d={}
 for n,(p,pin) in INPUTS.items():
  b=open(os.path.join(ROOT,p),"rb").read()
  if blob_sha(b)!=pin: raise SystemExit(n+" blob SHA mismatch")
  d[n]=json.loads(b.decode("utf-8"))
 return d
def det3(a,b,c):
 x1,y1=a%11,a//11; x2,y2=b%11,b//11; x3,y3=c%11,c//11
 A,B,C=x1*x1+y1*y1,x1,y1
 D,E,F=x2*x2+y2*y2,x2,y2
 G,H,I=x3*x3+y3*y3,x3,y3
 return A*(E*I-F*H)-B*(D*I-F*G)+C*(D*H-E*G)
def det4(a,b,c,d): return det3(a,b,c)-det3(a,b,d)+det3(a,c,d)-det3(b,c,d)
def canon(mask):
 ts=(lambda x,y:(x,y),lambda x,y:(y,10-x),lambda x,y:(10-x,10-y),lambda x,y:(10-y,x),
     lambda x,y:(10-x,y),lambda x,y:(x,10-y),lambda x,y:(y,x),lambda x,y:(10-y,10-x))
 out=[]
 for t in ts:
  m=0
  for i in range(121):
   if (mask>>i)&1:
    x,y=t(i%11,i//11); m|=1<<(y*11+x)
  out.append(m)
 return min(out)
def geom(h):
 m=int(h,16); s=[i for i in range(121) if (m>>i)&1]
 safe=all(det4(*q)!=0 for q in itertools.combinations(s,4))
 legal=sum(1 for d in range(121) if d not in s and all(det4(a,b,c,d)!=0 for a,b,c in itertools.combinations(s,3)))
 return {"stones":len(s),"safe":safe,"canonical":canon(m)==m,"legal_replies":legal}
def count(allowed,masks,full,forced=()):
 allowed=set(allowed); forced=tuple(dict.fromkeys(forced))
 if len(forced)>6 or any(r not in allowed for r in forced): return 0
 init=0
 for r in forced: init|=masks[r]
 need=6-len(forced); dp=[[0]*(full+1) for _ in range(need+1)]; dp[0][init]=1
 fs=set(forced)
 for r in sorted(allowed-fs):
  rm=masks[r]
  for k in range(need-1,-1,-1):
   for mask,v in enumerate(dp[k]):
    if v: dp[k+1][mask|rm]+=v
 return dp[need][full]
def main():
 d=load(); ent=d["membership"]["derived"]["all_root_memberships"]
 roots=[x["root"] for x in ent]; top=d["membership"]["derived"]["top50_roots_by_membership"][:15]
 rows=sorted({h for x in ent for h in x["cover_rows"]}); ri={h:i for i,h in enumerate(rows)}
 masks={x["root"]:sum(1<<ri[h] for h in x["cover_rows"]) for x in ent}; full=(1<<11)-1
 status={}
 for rank,root,claim,key in REFUTED:
  assert top[rank-1]["root"]==root
  tr=d[claim]["transfers"][key]; assert tr["root_canon"]==root and tr["verdict"]=="REFUTED-D10"
  status[root]={"status":"REFUTED-D10","evidence":{"claim":claim,"path":INPUTS[claim][0],"blob_sha1":INPUTS[claim][1],"transfer_key":key,"source":tr.get("source"),"kind":tr.get("kind")}}
 for rank,root,mname,aname,bit in WINS:
  assert top[rank-1]["root"]==root
  cert=next(x for x in d[mname]["certificates"] if x.get("bit")==bit and x.get("d4_canon_root")==root)
  if aname=="audit66j":
   a=next(x for x in d[aname]["entries"] if x.get("band")=="66j" and x.get("bit")==bit)
   assert a["verifier_status"]=="PASS" and a["verifier_union_missing"]==a["verifier_union_extra"]==0 and a["manifest_md5_match"] and a["manifest_sha256_match"]
   mob=a["verifier_root_mobility"]; missing=a["verifier_union_missing"]; extra=a["verifier_union_extra"]
  else:
   assert d[aname]["all_pass"]
   a=next(x for x in d[aname]["certificates"] if x.get("bit")==bit)
   assert a["rootCanon"]==root and a["union"]["missing"]==a["union"]["extra"]==0 and a["terminal_range"]==[13,17]
   mob=a["rootMobility"]; missing=a["union"]["missing"]; extra=a["union"]["extra"]
  status[root]={"status":"WIN7-D10","evidence":{"manifest":mname,"manifest_path":INPUTS[mname][0],"manifest_blob_sha1":INPUTS[mname][1],"bit":bit,"raw_root":cert.get("root"),"d4_canon_root":root,"file":cert.get("file"),"md5":cert.get("md5"),"sha256":cert.get("sha256"),"raw_is_canon":cert.get("raw_is_canon"),"audit":aname,"audit_path":INPUTS[aname][0],"audit_blob_sha1":INPUTS[aname][1],"verifier_status":"PASS","root_mobility":mob,"union_missing":missing,"union_extra":extra}}
 ref={r for r,v in status.items() if v["status"]=="REFUTED-D10"}; wins={r for r,v in status.items() if v["status"]=="WIN7-D10"}
 unknown=[x["root"] for x in top if x["root"] not in status]; tset={x["root"] for x in top}
 base=count(roots,masks,full); no_top=count(set(roots)-tset,masks,full)
 after=count(set(roots)-ref,masks,full); no_win=count(set(roots)-ref-wins,masks,full); with_win=after-no_win
 win_inc={r:count(set(roots)-ref,masks,full,[r]) for r in wins}; both=count(set(roots)-ref,masks,full,list(wins))
 uforce={r:count(set(roots)-ref-wins,masks,full,[r]) for r in unknown}
 upairs=[{"a":a,"b":b,"covers":count(set(roots)-ref-wins,masks,full,[a,b])} for a,b in itertools.combinations(unknown,2)]
 utriple=count(set(roots)-ref-wins,masks,full,unknown)
 geometry=[{"rank":i+1,"root":x["root"],**geom(x["root"])} for i,x in enumerate(top)]
 gm={x["root"]:x for x in geometry}; probe=min((gm[r] for r in unknown),key=lambda x:(x["legal_replies"],x["rank"]))
 checks=[
  {"name":"membership.roots_757","pass":len(roots)==757},
  {"name":"membership.rows_11","pass":len(rows)==11},
  {"name":"membership.total_359610","pass":base==359610},
  {"name":"top15.hitting_set","pass":no_top==0},
  {"name":"status.refuted_10","pass":len(ref)==10},
  {"name":"status.win_2","pass":len(wins)==2},
  {"name":"status.unclassified_3","pass":len(unknown)==3},
  {"name":"cover.after_refuted_38265","pass":after==38265},
  {"name":"cover.with_known_win_24990","pass":with_win==24990},
  {"name":"cover.without_known_win_13275","pass":no_win==13275},
  {"name":"cover.win_inclusion_identity","pass":sum(win_inc.values())-both==with_win},
  {"name":"cover.unknown_equal_4425","pass":all(v==4425 for v in uforce.values())},
  {"name":"cover.unknown_pairwise_disjoint","pass":all(x["covers"]==0 for x in upairs)},
  {"name":"cover.unknown_partition","pass":sum(uforce.values())-sum(x["covers"] for x in upairs)+utriple==no_win},
  {"name":"geometry.top15_safe_canonical","pass":all(x["stones"]==7 and x["safe"] and x["canonical"] for x in geometry)},
  {"name":"geometry.win_mobility_matches","pass":gm[WINS[0][1]]["legal_replies"]==57 and gm[WINS[1][1]]["legal_replies"]==60},
  {"name":"geometry.rank3_min_unclassified","pass":probe["rank"]==3 and probe["legal_replies"]==57},
 ]
 if not all(x["pass"] for x in checks): raise SystemExit("check failed: "+json.dumps(checks))
 topout=[]
 for i,x in enumerate(top):
  r=x["root"]; topout.append({"rank":i+1,"root":r,"membership":x["membership"],"cover_rows":x["cover_rows"],"status":status.get(r,{}).get("status","NOT_CLASSIFIED_BY_PINNED_STATUS_SOURCES"),"legal_replies":gm[r]["legal_replies"],"evidence":status.get(r,{}).get("evidence")})
 out={"schema":"n11-head1476-class2-top15-verdict-aware-cover-audit-20261118-v1","date":"2026-11-18","source_main_commit":MAIN_COMMIT,"target_parent":"00000000000000403800000008000000","inputs":{k:{"path":v[0],"git_blob_sha1":v[1]} for k,v in INPUTS.items()},"derived":{"candidate_universe":{"target_rows":11,"candidate_roots":757,"minimum_root_count":6,"minimum_covers":base},"top15_hitting_set":{"roots":15,"covers_avoiding_all_top15":no_top},"top15_status_counts":{"refuted_d10":len(ref),"win7_d10":len(wins),"not_classified_in_pinned_sources":len(unknown)},"top15":topout,"verdict_aware_plan_counts":{"excluded_known_refuted_top15_roots":len(ref),"covers_avoiding_those_refuted_roots":after,"covers_with_at_least_one_known_win7_root":with_win,"covers_with_no_known_win7_root":no_win,"known_win_root_inclusion_counts":win_inc,"covers_containing_both_known_win_roots":both,"no_win_residual_partition_by_unclassified_root":[{"rank":next(i+1 for i,x in enumerate(top) if x["root"]==r),"root":r,"covers":uforce[r],"legal_replies":gm[r]["legal_replies"]} for r in unknown],"no_win_residual_pairwise_intersections":upairs,"no_win_residual_triple_intersection":utriple},"next_probe_candidate":{"rank":probe["rank"],"root":probe["root"],"legal_replies":probe["legal_replies"]},"unjoined_candidate_roots_outside_top15":742},"checks":checks,"check_count":len(checks),"all_pass":True,"interpretation_guard":["REFUTED-D10 is not a LOSS proof.","WIN7-D10 certificates prove the individual 7-stone root only; no S5 parent closure or S6 receipt fold follows automatically.","The 38,265 plans exclude only 10 known REFUTED roots among the top 15; verdicts of the other 742 roots were not joined, so this is an upper bound, not a proven-viable plan count.","The three unclassified roots are not declared globally UNKNOWN; they were not matched in the pinned sources used here."],"unknown_status":"Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN."}
 path=sys.argv[1] if len(sys.argv)>1 else OUT
 with open(path,"w",encoding="utf-8") as f: json.dump(out,f,ensure_ascii=False,indent=2); f.write("\\n")
 print(json.dumps({"all_pass":True,"checks":len(checks),"baseline":base,"after_refuted":after,"with_win":with_win,"without_win":no_win,"unknown_partition":uforce,"probe":probe},ensure_ascii=False,indent=2))
if __name__=="__main__": main()
