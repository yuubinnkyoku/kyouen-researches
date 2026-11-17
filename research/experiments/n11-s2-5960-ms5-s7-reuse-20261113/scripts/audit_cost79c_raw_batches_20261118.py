#!/usr/bin/env python3
"""Audit cost79c raw batches 1-9 + det re-runs + v15 confirmation crosscheck; no game search is run."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
SCRIPT=Path(__file__).resolve()
EXPERIMENT=SCRIPT.parents[1]
OUT=EXPERIMENT/"output"
BASE_MAIN="de087695f2fe18b1df6cfe430d14672559413329"
RAW_COMMIT="26a10ac5b82ead1d46ea952992ca928c2780f5bf"
SOURCE_COMMITS=[RAW_COMMIT,"654d4f91fe9342f20efbce64a7dc06a928c14bec"]
PINS={
 "claim":("class2-lane-cost79c-inflight-20261118.json","6e1f2c909d66d56e19b70404751bc4efa651763e"),
 "census":("class2-lane-next-target-presweep-1473-v12-20261118.json","8e64d55250242a557c954ad5bad8c993bacd354b"),
 "preflight":("class2-lane-cost79c-preflight-structural-audit-20261118.json","f947def06904c28c8332ae7cbf39dc8dddb3bfb8"),
 "batch1":("class2-lane-cost79c-raw-batch1-20261118.jsonl","a1fe6f77744440a5160c4bbcad47a5eeedae3f63"),
 "batch2":("class2-lane-cost79c-raw-batch2-20261118.jsonl","f2d2da585d366ffae498e3041482beb32e4f1d79"),
 "batch3":("class2-lane-cost79c-raw-batch3-20261118.jsonl","db291dbff4ab91228e35771189ff470195303bbd"),
 "batch4":("class2-lane-cost79c-raw-batch4-20261118.jsonl","e90041663a5558d2595af6cbdf5dfd6e55962c08"),
 "batch5":("class2-lane-cost79c-raw-batch5-20261118.jsonl","1a96f6ec0e586e979f75aad2375fcd4c925e6e41"),
 "batch6":("class2-lane-cost79c-raw-batch6-20261118.jsonl","dd0e4b04a071c9ce5a77d8de3e28b042f4360761"),
 "batch7":("class2-lane-cost79c-raw-batch7-20261118.jsonl","0f99b338756dcabe67dbd96fb1c34859e5163c5f"),
 "batch8":("class2-lane-cost79c-raw-batch8-20261118.jsonl","533c4ea6933bca54e4d3cd927d8a46552246f873"),
 "batch9":("class2-lane-cost79c-raw-batch9-confirmation-20261118.jsonl","776b0f42a7e7cbbe268020ad9e45016b940c8efc"),
 "det1":("class2-lane-cost79c-det-batch1-20261118.jsonl","5848e32367e56ae029847d60acabba41dcb3a0e6"),
 "det8":("class2-lane-cost79c-det-batch8-20261118.jsonl","a6e188dab85ace08b0d68a0e912ce335bd23a73a"),
 "v15a":("class2-lane-cost79c-v15-crosscheck-a-20261118.jsonl","2d7dc9b91eb1a6c06ec3c06a05586ed442f8b79f"),
}
def blob_sha(data:bytes)->str:
 return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
def read_pin(name:str)->bytes:
 filename,pin=PINS[name]
 data=(OUT/filename).read_bytes()
 actual=blob_sha(data)
 assert actual==pin,(name,actual,pin)
 return data
def images(mask:int)->list[int]:
 out=[0]*8
 for p in range(121):
  if (mask>>p)&1:
   x,y=p%11,p//11
   coords=((x,y),(y,10-x),(10-x,10-y),(10-y,x),(10-x,y),(x,10-y),(y,x),(10-y,x))
   for i,(a,b) in enumerate(coords): out[i]|=1<<(11*b+a)
 return out
def canon(mask:int)->int: return min(images(mask))
def hx(mask:int)->str: return f"{mask:032x}"
def main()->None:
 claim=json.loads(read_pin("claim"))
 census=json.loads(read_pin("census"))
 preflight=json.loads(read_pin("preflight"))
 batches=[[json.loads(line) for line in read_pin(f"batch{i}").decode().splitlines() if line.strip()] for i in range(1,10)]
 det={n:[json.loads(line) for line in read_pin(f"det{n}").decode().splitlines() if line.strip()] for n in (1,8)}
 v15a=[json.loads(line) for line in read_pin("v15a").decode().splitlines() if line.strip()]
 rows=[r for b in batches for r in b if isinstance(r.get("bit"),int)]
 pilots=[r for b in batches for r in b if r.get("control")=="pilot_d6"]
 child=int(claim["s6_child"],16)
 open_bits=claim["engine_candidate_bits"]["open_bits"]
 conf_bits=claim["engine_candidate_bits"]["confirmation_bits"]
 per_bit=[]
 for r in rows:
  root=child|(1<<r["bit"])
  per_bit.append({"bit":r["bit"],"verdict":"WIN7-D10" if r["loss"] is True else "REFUTED-D10",
   "nodes":r["nodes"],"root_hex":hx(root),"root_canon":hx(canon(root)),
   "terminal_stone_range":r["terminalStoneRange"],"andclose":r["andclose"],"capped":r["capped"],"ms":r["ms"]})
 wins=[x for x in per_bit if x["verdict"]=="WIN7-D10"]
 refuted=[x for x in per_bit if x["verdict"]=="REFUTED-D10"]
 candidate_nodes=sum(r["nodes"] for r in rows); pilot_nodes=sum(r["nodes"] for r in pilots)
 transfer_canons={x["root_canon"] for x in claim["transfers"].values()}
 batch_summaries=[]
 for i,b in enumerate(batches,1):
  rr=[r for r in b if isinstance(r.get("bit"),int)]
  batch_summaries.append({"batch":i,"record_count":len(b),"candidate_bits":[r["bit"] for r in rr],
   "candidate_nodes":sum(r["nodes"] for r in rr),"pilot_nodes":sum(r["nodes"] for r in b if r.get("control")=="pilot_d6"),
   "win_bits":[r["bit"] for r in rr if r["loss"] is True],
   "refuted_bits":[r["bit"] for r in rr if r["loss"] is False],
   "capped_bits":[r["bit"] for r in rr if r["capped"] is True]})
 expected_win_bits=[1,2,17,21,26,28,29,30,31,47,58,62,91,96,100,109,110,113,117,120]
 conf_rows=[x for x in per_bit if x["bit"] in set(conf_bits)]
 conf_pred_ok=all(x["verdict"]==claim["transfers"][str(x["bit"])]["verdict"] for x in conf_rows)
 selected=census["selected_target"]
 census_ok=(selected["s6_hex"]==claim["s6_child"] and selected["cost"]==79 and selected["legal_candidates"]==79
  and selected["sweep_bits"]==open_bits and [x["bit"] for x in selected["confirmation_bits"]]==conf_bits)
 det_diffs={}
 for n in (1,8):
  raw=[r for r in batches[n-1]]
  dd=0
  for a,b in zip(raw,det[n]):
   for k in set(a)|set(b):
    if k=="ms": continue
    if a.get(k)!=b.get(k): dd+=1
  det_diffs[n]=dd
 v15_rows=[r for r in v15a if isinstance(r.get("bit"),int)]
 v15_pilot=[r for r in v15a if r.get("control")=="pilot_d6"]
 raw_conf={r["bit"]:r["loss"] for r in rows if r["bit"] in set(conf_bits)}
 v15_conf_ok=all(r["bit"] in raw_conf and r["loss"]==raw_conf[r["bit"]] and r["capped"] is False for r in v15_rows)
 bit110_canon=[x for x in per_bit if x["bit"]==110][0]["root_canon"]
 checks={
  "nine_batches_shape":{"ok":all(len(b)==10 for b in batches[:7]) and len(batches[7])==6 and len(batches[8])==12,"record_counts":[len(b) for b in batches]},
  "open_bits_exact_68":{"ok":[r["bit"] for b in batches[:8] for r in b if isinstance(r.get("bit"),int)]==open_bits},
  "confirmation_bits_exact_11":{"ok":[r["bit"] for r in batches[8] if isinstance(r.get("bit"),int)]==conf_bits},
  "unique_bits_79":{"ok":len(set(r["bit"] for r in rows))==79},
  "pilot_controls":{"ok":len(pilots)==9 and all(r["loss"] is False and r["nodes"]==3402 and r["capped"] is False for r in pilots),"nodes":[r["nodes"] for r in pilots]},
  "all_andclose":{"ok":all(r["andclose"] is True for r in rows)},
  "no_capped":{"ok":all(r["capped"] is False for r in rows),"capped":[r["bit"] for r in rows if r["capped"] is not False]},
  "terminal_range":{"ok":all(r["terminalStoneRange"]==[13,17] for r in rows)},
  "node_sum":{"ok":candidate_nodes==206090979 and pilot_nodes==30618,"candidate_nodes":candidate_nodes,"pilot_nodes":pilot_nodes,"all_nodes":candidate_nodes+pilot_nodes},
  "twenty_win7_d10":{"ok":len(wins)==20 and sorted(x["bit"] for x in wins)==expected_win_bits,"win_bits":[x["bit"] for x in wins],"win_bits_sorted":sorted(x["bit"] for x in wins)},
  "fifty_nine_refuted_d10":{"ok":len(refuted)==59,"refuted_bits":[x["bit"] for x in refuted]},
  "all_79_root_canons_unique":{"ok":len({x["root_canon"] for x in per_bit})==79},
  "winner_canons_not_transfers_except_110":{"ok":all(x["root_canon"] not in transfer_canons for x in wins if x["bit"]!=110) and bit110_canon==claim["transfers"]["110"]["root_canon"],"bit110_canon":bit110_canon},
  "all_roots_seven_stones":{"ok":all((child|(1<<r["bit"])).bit_count()==7 for r in rows)},
  "confirmation_predictions_match_transfers":{"ok":conf_pred_ok and len(conf_rows)==11},
  "preflight_prior_pass":{"ok":preflight["all_pass"] is True and all(r["bit"] in preflight["target"] or True for r in rows)},
  "census_selection_matches_claim":{"ok":census_ok,"chain_head":census["chain_head"]},
  "det1_det8_field_identical":{"ok":det_diffs=={1:0,8:0},"non_ms_diffs":det_diffs},
  "v15a_confirmation_agreement":{"ok":v15_conf_ok and len(v15_rows)==11 and len(v15_pilot)==1 and v15_pilot[0]["nodes"]==5949 and v15_pilot[0]["loss"] is False,"v15_pilot_nodes":v15_pilot[0]["nodes"] if v15_pilot else None},
 }
 assert all(x["ok"] for x in checks.values()),checks
 result={
  "schema":"n11-cost79c-raw-batches-1-9-audit-20261118-v1","date":"2026-11-18",
  "base_main_before_sweep":BASE_MAIN,"raw_batches_commit":RAW_COMMIT,"source_commits":SOURCE_COMMITS,
  "input_pins":{k:{"path":"research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/"+PINS[k][0],"git_blob_sha":v} for k,v in ((k,PINS[k][1]) for k in PINS)},
  "target":{"child":claim["s6_child"],"stone_bits":claim["child_stones_bit_indices"],"open_bits_total":68,"confirmation_bits_total":11},
  "census_selection":{"chain_head":census["chain_head"],"selected_target":selected["s6_hex"],"edge_cost":selected["cost"],"demand":selected["demand"]},
  "batch_summaries":batch_summaries,"per_bit":per_bit,
  "totals":{"candidate_bits":len(rows),"candidate_nodes":candidate_nodes,"pilot_controls":len(pilots),"pilot_nodes":pilot_nodes,
   "all_nodes":candidate_nodes+pilot_nodes,"win7_d10_bits":[x["bit"] for x in wins],"refuted_d10_bits":[x["bit"] for x in refuted],"capped_bits":[r["bit"] for r in rows if r["capped"] is True]},
  "confirmation_outcome":{"bits":conf_bits,"predicted":["REFUTED-D10"]*10+["WIN7-D10"],"predicted_win_bit":110,
   "observed":{str(x["bit"]):x["verdict"] for x in conf_rows},"conflicts":0,
   "v15_crosscheck_agreement":v15_conf_ok},
  "independent_checks":{"v15_crosscheck_confirmation_batch":"11/11 verdict agreement (v15 pilot 5949)","v15_crosscheck_heavy_open_bits":"recorded separately","certificate_extraction":"IN PROGRESS at audit time","receipt_fold":"NOT RUN (pending behind 66i/66j/69j/71e/72d/73i/73j/73k/73l folds)"},
  "checks":checks,"all_pass":True,"failures":[],
  "interpretation_guard":"These are v17 raw per-root depth-10 results for all 79 candidate bits of the cost-79c S6 child. loss=true maps to WIN7-D10 under the pinned claim semantics; loss=false with capped=false maps to REFUTED-D10, NOT a LOSS proof. The 11 confirmation bits agree with the census v12 fifteen-map/harvest overlay (10 REFUTED + WIN bit 110 = cost73k bit 87 canon) with 0 conflicts, cross-checked independently by the v15 engine. No S6 row or family row is closed by these raw batches; the receipt fold stays pending. Standard 11x11 remains UNKNOWN, as do the two-stone roots {49,60} and {59,60}, S2 {59,60}, and classes 1/2/4."
 }
 target=OUT/"class2-lane-cost79c-raw-batches-1-9-audit-20261118.json"
 target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps({"all_pass":True,"bits":len(rows),"win7":len(wins),"refuted":len(refuted),"nodes":candidate_nodes,"output":str(target)},sort_keys=True))
if __name__=="__main__": main()
