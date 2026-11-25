#!/usr/bin/env python3
import hashlib, json, re, sys
from pathlib import Path

HERE=Path(__file__).resolve().parents[1]
OUT=HERE/"output"
CD=OUT/"class2-lane-cost76c-certificates"
S=HERE/"scripts"
ROOT="0000000001000080b002000001000000"
CHILD="00000000010000809002000001000000"
BIT=61
LEGAL=[0,1,2,4,6,7,9,10,14,15,18,21,26,28,29,30,32,34,36,41,43,45,46,48,54,66,67,69,70,76,77,78,81,85,86,87,89,91,94,95,98,99,103,106,108,109,110,111,113,114,116,117,118,119,120]
HK=("solved_s6_in_manifest","remaining_s5_orbits","unique_remaining_s6","sum_remaining_cost","s6_needed_by_open_classes","cost_needed_by_open_classes")
PINS={
 "claim_v7_snapshot":("class2-lane-cost76c-inflight-20261116-v7-snapshot.json","215115c61896117af774128428c4738ad8dda925"),
 "v17_audit":("class2-lane-cost76c-v17-sweep-and-fbt-saturation-audit-20261117.json","235f964365a7ab33e33986c915fc7f6861e4d686"),
 "marginals":("class2-lane-cost76c-v17-corrected-candidate-manifest-marginals-20261117.json","3469cf3649ae3ab859edb33bf944ff0f13f229b0"),
 "head1472":("class2-lane-next-target-presweep-1472-20261117.json","3ee5703c8cabf738eaecefb17a759c78c4a34e61"),
 "fold64h":("class-frontier-cost64h-receipts-recompute-20261117.json","1633be292f6f1862c895009eac29d398d0be7738"),
 "audit64h":("class2-lane-cost64h-fold-audit-20261117.json","7edbfbf3a3d245ca21f03913e01e816bb0d9c868")}
SPINS={
 "driver":("cert_driver76c.ts","3aae6b6ce133b2a3fb13796ad303e2a57823f05a"),
 "extractor":("class4_child1_cert_extractor_exact_v16.ts","5518d375fc6b4a7a14c22a1a65586f0c1c5731c0"),
 "legal_candidates":("legal_candidates.py","8e97082c42838c7a4a4b6d2dd235276c8d43ab9a"),
 "bareiss_verifier":("verify_bit7_win7_cert.ts","2960afabdf7c1a7012d223974b65f1423e6890da"),
 "bigint_verifier":("verify_win7_certificate_bigint_independent.mjs","62b5d9413daafb172f6e10249976ee6808f7b454")}

def blob(b): return hashlib.sha1(b"blob %d\0"%len(b)+b).hexdigest()
def writej(p,x):
 b=(json.dumps(x,ensure_ascii=False,indent=2,sort_keys=True)+"\n").encode(); p.write_bytes(b); return b
def ck(c,k,v):
 c[k]=bool(v)
 if not v: raise AssertionError(k)
def readpin(n,h):
 b=(OUT/n).read_bytes(); g=blob(b)
 if g!=h: raise AssertionError((n,g,h))
 return json.loads(b),g
def d4(mask,t):
 out=0
 for p in range(121):
  if mask>>p&1:
   x,y=p%11,p//11
   xy=((x,y),(y,10-x),(10-x,10-y),(10-y,x),(10-x,y),(x,10-y),(y,x),(10-y,10-x))[t]
   out|=1<<(11*xy[1]+xy[0])
 return out
def canon(mask): return f"{min(d4(mask,t) for t in range(8)):032x}"
def summary(p):
 for line in p.read_text().splitlines():
  if line.startswith("{"): return json.loads(line)
 raise AssertionError("missing JSON "+str(p))

def main():
 checks={}; src={}; inp={}
 for k,(n,h) in PINS.items(): inp[k],src[k]=readpin(n,h)
 for k,(n,h) in SPINS.items():
  got=blob((S/n).read_bytes()); ck(checks,"script_"+k,got==h); src[k]=got
 claim=inp["claim_v7_snapshot"]; v17=inp["v17_audit"]; marg=inp["marginals"]
 pres=inp["head1472"]; f64=inp["fold64h"]; a64=inp["audit64h"]
 ck(checks,"claim_v7",claim["schema"]=="n11-class2-lane-cost76c-sweep-complete-20261117-v7")
 ck(checks,"win_bits",claim["actual_execution"]["win7_d10_bits"]==[61,99])
 ck(checks,"bit113_refuted",claim["actual_execution"]["refuted_bit113"] is True)
 ck(checks,"v17_win_bits",v17["v17_full_resweep"]["win_bits_corrected"]==[61,99])
 ck(checks,"v17_bit113_refuted",v17["v17_full_resweep"]["per_bit"]["113"]["v17_loss"] is False)
 ck(checks,"head1472",pres["chain_head"]=="1472/174/6376/504672/4649/368586")
 before=f64["frontier_after_cost64h"]; nums=[before[k] for k in HK]
 ck(checks,"fold64h_head",nums==[1472,174,6376,504672,4649,368586])
 ck(checks,"fold64h_audit",a64["all_checks_pass"] is True and a64["check_count"]==145)
 ck(checks,"cross_conflicts_zero",a64["cross_lane"]["cost66i_conflict_scan"]["conflicts"]==0)
 ck(checks,"root_overlap_zero",a64["cross_lane"]["d4_overlap_with_cost76c"]==[])

 cp=CD/f"n11_s7_{ROOT}.cert"; cert=cp.read_bytes(); lines=cert.decode("ascii").splitlines(); rows=lines[2:]
 cblob=blob(cert); cmd5=hashlib.md5(cert).hexdigest(); csha=hashlib.sha256(cert).hexdigest()
 ck(checks,"header",lines[0]=="n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS")
 ck(checks,"root",lines[1]=="root "+ROOT)
 keys=[r.split()[0] for r in rows]
 ck(checks,"rows",len(rows)==30042)
 ck(checks,"sorted_unique",keys==sorted(set(keys)))
 ck(checks,"row_syntax",all(re.fullmatch(r"[0-9a-f]{32} [0-9]{1,3}",r) for r in rows))
 ck(checks,"whole_file",len(cert)==1083833 and len(cert)<1200000)
 ck(checks,"hashes",(cmd5,csha,cblob)==("6a38f91cb3ec26e5bb7dd4fa937c5e42","91c69354d5f300a367756ca2dd430bc2f093dea8c0a188e7ee5d8b0b749c0f06","374e27eb9a23475b84ec0ca5937d9d98e35a6a71"))

 ex=summary(CD/"bit61-extraction.stderr"); rr=summary(CD/"bit61-rerun.stderr")
 ck(checks,"legal_defenses",ex["moves"]==55 and ex["defenseListExact"] is True and ex["expectedMoves"]==LEGAL)
 ck(checks,"all_per_moves",ex["perMoveComplete"] and ex["perMoveKeysExact"] and len(ex["perMove"])==55 and all(x["ok"] and not x["capped"] for x in ex["perMove"].values()))
 ck(checks,"rows_fbt",ex["nRows"]==30042 and ex["rowsAvailable"] and ex["rowCountMatches"] and ex["rowsUnique"] and ex["fbt_drops"]==0 and ex.get("fatal") in (None,"undefined"))
 ck(checks,"extraction_nodes",ex["sum"]==1325278)
 ck(checks,"rerun_per_move",rr["perMove"]==ex["perMove"] and rr["sum"]==ex["sum"] and rr["nRows"]==ex["nRows"])
 cmp=json.loads((CD/"bit61-rerun-byte-comparison.json").read_text())
 ck(checks,"rerun_bytes",cmp["byte_identical"] is True and cmp["bytes"]==len(cert) and cmp["md5"]==cmd5 and cmp["sha256"]==csha and cmp["git_blob_sha"]==cblob)

 sys.path.insert(0,str(S))
 from legal_candidates import legal_candidates
 _,legal=legal_candidates(ROOT)
 ck(checks,"independent_legal",legal==LEGAL and len(legal)==55)
 bi=json.loads((CD/"bit61-bigint-verification.json").read_text())
 ck(checks,"bigint_pass",bi["verdict"]=="WIN7 certificate independently verified" and bi["root_safe"] is True)
 ck(checks,"bigint_root",bi["root_hex"]==ROOT and bi["root_stones"]==7 and bi["root_mobility"]==55)
 ck(checks,"bigint_union",bi["subroots_passed"]==55 and bi["strategy_rows"]==30042 and bi["consumed_winner_rows"]==30042 and bi["union_missing"]==0 and bi["union_extra"]==0)
 ck(checks,"bigint_range",bi["terminal_range"]==[13,17])

 bl=(CD/"bit61-bareiss-verification.raw.jsonl").read_text().splitlines()
 br=json.loads(bl[0]); st=json.loads(bl[1])["stats"]
 ck(checks,"bareiss_root",br=={"stones":7,"loserMobility":55})
 ck(checks,"bareiss_subroots",len(st)==55)
 seen=sum(x["seen"] for x in st.values()); terms=sum(x["terminals"] for x in st.values()); edges=sum(x["opponentEdges"] for x in st.values())
 cons=CD/"bit61-bareiss-consumed.txt"; bs=CD/"bit61-bareiss-verification.json"
 if cons.exists():
  c=cons.read_text().splitlines(); u=set(c)
  bsum={"method":"verify_bit7_win7_cert.ts; exact Bareiss 4x4; engine-free","root_check":br,"rows":30042,"subroots":55,"consumed_entries":len(c),"consumed_unique":len(u),"union_missing":len(set(keys)-u),"union_extra":len(u-set(keys)),"sum_seen":seen,"sum_terminals":terms,"sum_opponent_edges":edges,"terminal_range":[13,17]}
  writej(bs,bsum)
 else: bsum=json.loads(bs.read_text())
 ck(checks,"bareiss_union",bsum["consumed_unique"]==30042 and bsum["union_missing"]==0 and bsum["union_extra"]==0)
 ck(checks,"seen_agreement",seen==bi["visited_states_across_subroots"]==67865)
 ck(checks,"terminal_agreement",terms==bi["terminal_count"]==10187)
 ck(checks,"edge_agreement",edges==bi["loser_reply_edges"]==62162)
 ck(checks,"ranges",all(13<=x["range"][0]<=x["range"][1]<=17 for x in st.values()))

 mask=int(ROOT,16); pts=[p for p in range(121) if mask>>p&1]
 subsets=sorted({canon(mask^(1<<p)) for p in pts})
 proj=next(x for x in marg["single_candidate_projections"] if x["bit"]==BIT)
 new=sorted(proj["marginal_hexes"])
 ck(checks,"seven_subset_canons",len(subsets)==7)
 ck(checks,"five_marginals",len(new)==5 and all(x in subsets for x in new))
 ck(checks,"two_precovered",len(set(subsets)-set(new))==2)
 open_rows=marg["candidate_cover_union"]["currently_open_manifest_hexes"]
 closed=set(pres["cross_checks"]["landed_64h_closed_rows"])
 ck(checks,"one_open_manifest",open_rows==[CHILD])
 ck(checks,"row_still_open",CHILD not in closed)
 ck(checks,"five_new_not_closed",not(set(new)&closed))
 fam=pres["families_v3"]["00000000000000801202000040000000"]
 target=next(x for x in fam if x["s6_hex"]==CHILD)
 ck(checks,"pending_bit61",target["open_after_census"]>0 and target["pending_close_76c_fold_by_bit"]==BIT)
 ck(checks,"root_canonical",canon(mask)==ROOT)

 parents={}
 for k,old in marg["combined_projection"]["affected_parents_after_bit61"].items():
  prev=f64["parents_after"].get(k)
  rb=prev["rows_after"] if prev else old["rows_before"]
  cb=prev["edge_cost_after"] if prev else old["edge_cost_before"]
  lr=old["rows_before"]-old["rows_after"]; lc=old["lost_edge_cost"]
  ra=rb-lr; ca=cb-lc
  ck(checks,"parent_open_"+k,ra>0)
  parents[k]={"s5_hex":old["s5_hex"],"classes":old["classes"],"rows_before":rb,"rows_after":ra,"edge_cost_before":cb,"edge_cost_after":ca,"lost_rows":lr,"lost_edge_cost":lc,"lost_rows_hexes":old["lost_rows_hexes"],"cost64h_preapplied":prev is not None}
 incid=sum(x["lost_rows"] for x in parents.values()); edelta=sum(x["lost_edge_cost"] for x in parents.values())
 ck(checks,"parent_incidences",incid==6); ck(checks,"parent_edge_delta",edelta==458)
 after=[nums[0]+1,nums[1],nums[2]-1,nums[3]-76,nums[4]-1,nums[5]-76]
 ck(checks,"head_after",after==[1473,174,6375,504596,4648,368510])

 (CD/"bit61-rootcheck.json").write_text('{"stones":7,"loserMobility":55}\n{"rows":30042,"stats":{}}\n')
 records=sorted(st.items(),key=lambda z:int(z[0][1:]))
 groups=[{"rows":30042,"stats":{m:{"seen":v["seen"],"terminals":v["terminals"],"opponentEdges":v["opponentEdges"],"range":v["range"]} for m,v in records[i:i+8]}} for i in range(0,len(records),8)]
 (CD/"bit61-subroots.jsonl").write_text("".join(json.dumps(x,separators=(",",":"))+"\n" for x in groups))
 (CD/"bit61-legal-defenses.json").write_text(json.dumps({"root":ROOT,"legal_defenses":LEGAL},indent=2)+"\n")
 (CD/"bit61-extraction-summary.json").write_text(json.dumps(ex,indent=2)+"\n")
 (CD/"bit61-rerun-summary.json").write_text(json.dumps(rr,indent=2)+"\n")
 src["fold_script"]=blob(Path(__file__).read_bytes())
 mpath=CD/"class2-lane-cost76c-win7-certificates-20261117.json"
 manifest={"schema":"n11-class2-lane-cost76c-win7-certificates-20261117-v1","date":"2026-11-17","s5_parent_hex":"00000000000000801202000040000000","s6_child_hex":CHILD,"s6_s7_edge_cost":76,
  "method":"Fail-closed cert_driver76c.ts; exact raw-root legal-defense list; 55 uncapped subroots; FBT drops 0; engine-free Bareiss and independent BigInt verifiers pass; fresh-process byte-identical rerun.",
  "totals":{"certificates":1,"rows":30042,"extraction_nodes":1325278,"published_bytes":len(cert),"fbt_drops_total":0,"capped_per_move_total":0},
  "basis":"cost76c v17 sweep: 76 candidates, WIN7-D10 bits 61/99, bit113 REFUTED-D10; bit61 is the first manifest-closing candidate.",
  "certificates":[{"bit":61,"root":ROOT,"verdict":"WIN7","depth":10,"rows":30042,"extraction_nodes":1325278,"fbt_drops":0,"fatal":None,"subroots":55,"subroots_pass":55,"union_missing":0,"union_extra":0,"terminal_stone_range":[13,17],"loser_mobility":55,"file":cp.name,"bytes":len(cert),"md5":cmd5,"sha256":csha,"git_blob_sha":cblob,"d4_canon_root":canon(mask),"raw_is_canon":True,"certificate_split":"1083833 bytes below the 1200000-byte whole-file threshold; published whole","split_cut_byte":None,"storage":"whole file"}],
  "verification":{"bigint":bi,"bareiss":bsum,"cross_agreement":{"seen":seen==bi["visited_states_across_subroots"],"terminals":terms==bi["terminal_count"],"opponent_edges":edges==bi["loser_reply_edges"]},"fresh_process":{"byte_identical":True,"md5":cmd5,"sha256":csha,"git_blob_sha":cblob}},
  "source_blob_pins":src,"unknown_status":"11x11 empty board UNKNOWN; this proves only the individual seven-stone root. REFUTED-D10 is not a LOSS proof; two-stone roots, S2, and classes 1/2/4 remain UNKNOWN."}
 mb=writej(mpath,manifest); msha=blob(mb)
 before={k:before[k] for k in HK}; afterdict=dict(zip(HK,after))
 certrel="class2-lane-cost76c-certificates/"+cp.name
 fold={"schema":"n11-class2-lane-cost76c-receipts-recompute-20261117-v1","date":"2026-11-17","status":"fold-complete","basis_head":1472,"baseline_record":{"frontier_before":before},"frontier_after_cost76c":afterdict,
  "receipts":[{"bit":61,"root_hex":ROOT,"d4_canon_root":canon(mask),"certificate":{"path":certrel,"git_blob_sha":cblob,"bytes":len(cert),"md5":cmd5,"sha256":csha,"strategy_rows":30042,"subroots_passed":55,"root_mobility":55,"terminal_count":10187,"terminal_range":[13,17],"visited_states":67865,"loser_reply_edges":62162,"union_missing":0,"union_extra":0},"marginal_d4_s6_orbits":5,"marginal_manifest_rows":1,"marginal_manifest_hexes":new,"extraction_nodes":1325278,"fbt_drops":0,"fatal":None}],
  "totals":{"receipts":1,"total_certificate_bytes":len(cert),"total_strategy_rows":30042,"total_extraction_nodes":1325278,"total_visited_states":67865,"total_loser_reply_edges":62162,"total_terminals":10187,"marginal_d4_s6_orbits":5,"marginal_manifest_rows":1},
  "parents_after":parents,"parent_row_incidences":incid,"parent_edge_cost_delta":edelta,"parent_count_fully_closed":0,
  "conflict_census":{"verdict_conflicts":0,"d4_root_overlap_with_cost64h":0,"marginal_row_overlap_with_cost64h_closed_rows":0,"cost64h_cross_source_conflicts":0},
  "source_blob_pins":src,"certificate_manifest":{"path":"class2-lane-cost76c-certificates/class2-lane-cost76c-win7-certificates-20261117.json","git_blob_sha":msha},
  "interpretation_guard":"Bookkeeping fold over one independently verified WIN7-D10 receipt. It closes one S6 manifest row and reduces open frontier demand; it creates no new engine verdict and closes no S5 parent. The 11x11 empty board and all requested smaller roots/classes remain UNKNOWN."}
 fpath=OUT/"class-frontier-cost76c-receipts-recompute-20261117.json"; fb=writej(fpath,fold); fsha=blob(fb)
 audit={"schema":"n11-class2-lane-cost76c-fold-audit-20261117-v1","date":"2026-11-17","status":"PASS","all_checks_pass":all(checks.values()),"check_count":len(checks),"checks":checks,
  "certificate_count":1,"certificate_bytes":len(cert),"strategy_rows":30042,"visited_states":67865,"loser_reply_edges":62162,"terminal_count":10187,"terminal_range":[13,17],"fbt_drops":0,"capped_per_move":0,
  "fold":{"basis_head":1472,"projected_head":after,"closed_manifest_rows":1,"marginal_d4_s6_orbits":5,"affected_parents":4,"parent_row_incidences":incid,"parent_edge_cost_delta":edelta,"fully_closed_s5_parents":0},
  "certificate_manifest_blob_sha":msha,"fold_blob_sha":fsha,"source_blob_pins":src}
 apath=OUT/"class2-lane-cost76c-fold-audit-20261117.json"; ab=writej(apath,audit); asha=blob(ab)
 claimpath=OUT/"class2-lane-cost76c-inflight-20261116.json"
 current=json.loads(claimpath.read_text())
 if current["schema"] not in ("n11-class2-lane-cost76c-sweep-complete-20261117-v7","n11-class2-lane-cost76c-sweep-certificate-fold-20261117-v8"): raise AssertionError("unexpected current claim schema")
 current["schema"]="n11-class2-lane-cost76c-sweep-certificate-fold-20261117-v8"
 current["previous_version"]={"path":"class2-lane-cost76c-inflight-20261116-v7-snapshot.json","git_blob_sha":src["claim_v7_snapshot"]}
 current["status"]="v17-corrected; bit61 WIN7-D10 certificate extracted, independently verified by Bareiss and BigInt, fresh-process byte-identical; receipt fold complete at head1473; bit99 remains unused backup; bit113 REFUTED-D10 excluded"
 ce=current["certificate_extraction"]; ce["status"]="complete; bit61 certificate published and independently verified; bit99 remains fallback only"
 ce["independent_verification"]="PASS: Bareiss and BigInt, 55/55 sub-roots, exact union 0/0, terminal range [13,17], fresh-process byte-identical"
 ce["manifest_path"]="class2-lane-cost76c-certificates/class2-lane-cost76c-win7-certificates-20261117.json"; ce["manifest_blob_sha"]=msha
 ce["actual_extraction"]={"bit":61,"root_hex":ROOT,"legal_defenses":55,"nodes":1325278,"rows":30042,"fbt_drops":0,"fatal":None,"elapsed_ms":9592,"bytes":len(cert),"md5":cmd5,"sha256":csha,"git_blob_sha":cblob,"fresh_process_byte_identical":True}
 current["receipt_fold"]={"status":"fold-complete","basis_head":nums,"frontier_after":after,"fold_json":"class-frontier-cost76c-receipts-recompute-20261117.json","fold_blob_sha":fsha,"fold_audit":"class2-lane-cost76c-fold-audit-20261117.json","fold_audit_blob_sha":asha,"marginal_d4_s6_orbits":5,"marginal_manifest_rows":1,"closed_manifest_rows":1,"affected_parents":4,"parent_row_incidences":incid,"parent_edge_cost_delta":edelta,"fully_closed_s5_parents":0}
 current["latest_canonical_head_after_cost76c_fold"]=after
 current["next_action"]="Rebase cost66i's nine already verified receipts against head1473, recompute its marginal and conflicts, then fold; do not reuse its head1452 projection."
 current["last_updated"]="2026-11-17"
 cb=writej(claimpath,current); csha_claim=blob(cb)
 audit["checks"]["manifest_fold_audit_claim_generated"]=True; audit["check_count"]=len(audit["checks"]); audit["all_checks_pass"]=all(audit["checks"].values())
 ab=writej(apath,audit); asha=blob(ab)
 current["receipt_fold"]["fold_audit_blob_sha"]=asha
 cb=writej(claimpath,current); csha_claim=blob(cb)
 readme=("cost76c bit61 WIN7-D10 certificate\n\n"
  f"S6 child {CHILD}; bit {BIT}; seven-stone root {ROOT}.\n"
  "55 legal replies; 1,325,278 extraction nodes; 30,042 strategy rows; zero FBT drops.\n"
  f"Certificate bytes {len(cert)}; MD5 {cmd5}; SHA-256 {csha}.\n"
  "Bareiss and BigInt verifiers pass all 55 sub-roots; exact union 0 missing / 0 extra.\n"
  "Fresh-process re-extraction is byte-identical. The certificate is stored whole.\n\n"
  "Reproduction from this directory, Node v22.16.0 or later:\n"
  f"ROOT={ROOT}\nCHILD={CHILD}\n"
  "MOVES=$(python3 ../../scripts/legal_candidates.py \"$ROOT\" | tail -1)\n"
  "printf '%s\\n' \"$MOVES\" | node --experimental-strip-types ../../scripts/cert_driver76c.ts \"$CHILD\" 61 /tmp/bit61.cert\n"
  "node ../../scripts/verify_win7_certificate_bigint_independent.mjs /tmp/bit61.cert 55\n"
  "node --experimental-strip-types ../../scripts/verify_bit7_win7_cert.ts --cert /tmp/bit61.cert --root \"$ROOT\" --root-check --subroots \"$MOVES\" --consumed-out /tmp/bit61-consumed.txt\n\n"
  "This receipt fold closes one S6 manifest row only. The standard 11x11 empty board and all smaller target roots/classes remain UNKNOWN.\n")
 (CD/"README.md").write_text(readme)
 print(json.dumps({"status":"PASS","checks":len(checks),"passed":sum(checks.values()),"certificate_bytes":len(cert),"certificate_sha256":csha,"certificate_blob_sha":cblob,"rows":len(rows),"extraction_nodes":1325278,"root_mobility":55,"subroots":55,"head_before":nums,"head_after":after,"closed_manifest_rows":1,"parent_row_incidences":incid,"parent_edge_cost_delta":edelta,"fully_closed_s5_parents":0,"manifest_blob_sha":msha,"fold_blob_sha":fsha,"audit_blob_sha":asha,"claim_blob_sha":csha_claim},indent=2,sort_keys=True))

if __name__=="__main__": main()

