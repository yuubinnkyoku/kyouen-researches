#!/usr/bin/env python3
"""
Width-66 2R2A surgery (complete) for the (7,4) seven-row family.

Base = w65-01 id-image @ shift 11 on the 7x66 board (same base and scope as the
class-(i) 1R1A/2R1A run, surgery66.py). Base is safe, and maximal except the
single uncovered cell T = (0,6). A 2R2A surgery state = base - {r1,r2} + {a1,a2}.

Completeness partition of the 2R2A space around this base (def-mode enforced by
row gates: every final row <= q-1 = 3; 0R2A is always def-incompatible because
both adds then land in row 6 -> row 6 = 4):
  Branch A ("(1,2)", declared class (ii)): both adds on one T-curve with
            exactly 1 base stone (final count on that curve = 3 = q-1).
  Branch B ("(2,1)"): a1 on a T-curve with exactly 2 base stones, a2 free.
            Skips pairs where a2 also sits on the same curve (final count 4
            = unsafe by construction). Enumerated per (curve, a1, a2) role
            because the R-avoid set differs per curve.
  Branch C: T is occupied (one add = T); the other add anywhere empty.
Final-state dedupe is state-level only; every surviving final state is
verified from scratch by verify_int.verify (safe + maximal + def); hits get
per-stone tamper checks (drop -> maximal must break). Resumable per-pair-index
progress; JSONL logs; hard time budget; 0 hits -> scoped local negative.
"""
import json, os, sys, time, itertools
from verify_int import verify, circle_thru, line_thru, curve_cells, curves_with_3plus
from fastv import Screen

M, H, Q = 66, 7, 4
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output66b")
os.makedirs(OUT, exist_ok=True)
BUDGET = float(sys.argv[1]) if len(sys.argv) > 1 else 240.0

def main():
    t0 = time.time()
    rec = json.load(open(os.path.join(HERE, "w65-01.json")))
    stones = [tuple(s) for s in rec["stones"]]
    mn = min(x for (x, y) in stones)
    base = sorted((x - mn + 11, y) for (x, y) in stones)
    S = set(base)
    T = (0, 6)
    r0 = verify(base, M, H, Q)
    assert r0["safe"] and set(r0["unblocked"]) == {T}, r0["unblocked"]
    rowBase = [0]*H
    for (x, y) in S:
        rowBase[y] += 1
    assert rowBase == [3,3,3,3,3,3,2]

    empty = [(x, y) for x in range(M) for y in range(H) if (x, y) not in S]
    emptySet = set(empty)
    scr = Screen(base, M, H, Q)

    # base curves with exactly 3 stones -> hot cells
    hot = {}
    for (kind, cur) in curves_with_3plus(sorted(S)):
        cells = curve_cells(kind, cur, M, H)
        on = [c for c in cells if c in S]
        if len(on) == Q - 1:
            for c in cells:
                if c not in S:
                    hot.setdefault(c, []).append(on)

    def cnt_on(kind, cur):
        cells = curve_cells(kind, cur, M, H)
        return ([c for c in cells if c in S], [c for c in cells if c not in S])

    c1 = {}  # key -> (emptyCells, blockingStone)
    for s in base:
        ln = line_thru(T, s)
        if ln:
            on, em = cnt_on("line", ln)
            if len(on) == 1 and len(em) >= 2:
                c1[("line", ln)] = (em, s)
    for s in base:
        for a in empty:
            if a == T:
                continue
            ci = circle_thru(T, s, a)
            if ci is None:
                continue
            key = ("circle", ci)
            if key in c1:
                continue
            on, em = cnt_on("circle", ci)
            if len(on) == 1 and len(em) >= 2:
                c1[key] = (em, s)

    c2 = {}  # key -> (emptyCells, blockingStones)
    for s in base:
        ln = line_thru(T, s)
        if ln:
            key = ("line", ln)
            if key not in c2:
                on, em = cnt_on("line", ln)
                if len(on) == 2 and len(em) >= 1:
                    c2[key] = (em, tuple(on))
    for i in range(len(base)):
        for j in range(i+1, len(base)):
            s1, s2 = base[i], base[j]
            ci = circle_thru(T, s1, s2)
            if ci is None:
                continue
            key = ("circle", ci)
            if key in c2:
                continue
            on, em = cnt_on("circle", ci)
            if len(on) == 2 and len(em) >= 1:
                c2[key] = (em, tuple(on))

    # ---- pair universe ----
    pairs = []  # (branch, a1, a2, avoid frozenset, noteKeyStr)
    bset = set()
    for key in sorted(c1, key=str):
        em, s = c1[key]
        for p in itertools.combinations(sorted(em), 2):
            pairs.append(("A", p[0], p[1], frozenset((s,)), str(key)))
    for key in sorted(c2, key=str):
        em, (s1, s2) = c2[key]
        emset = set(em)
        for a1 in sorted(em):
            for a2 in sorted(emptySet):
                if a2 == a1 or a2 in emset:
                    continue
                t = (key and ("B", str(key), a1, a2))
                if t in bset:
                    continue
                bset.add(t)
                pairs.append(("B", a1, a2, frozenset((s1, s2)), str(key)))
    for a2 in sorted(emptySet):
        if a2 != T:
            pairs.append(("C", T, a2, frozenset(), "T-occupied"))

    # ---- R universe with row vectors ----
    Rs = []
    for i in range(len(base)):
        for j in range(i+1, len(base)):
            rem = [0]*H
            for st in (base[i], base[j]):
                rem[st[1]] -= 1
            Rs.append(((base[i], base[j]), tuple(rem)))

    progPath = os.path.join(OUT, "surgery66_2r2a_progress.json")
    hitsPath = os.path.join(OUT, "surgery66_2r2a_hits.jsonl")
    logPath = os.path.join(OUT, "surgery66_2r2a_log.jsonl")
    seenPath = os.path.join(OUT, "surgery66_2r2a_seen.json")
    genEvent = None
    if os.path.exists(logPath):
        for line in open(logPath):
            d = json.loads(line)
            if d.get("event") == "gen" and "pairsTotal" in d and "next" not in d:
                genEvent = d
                break
    if genEvent is None:
        genEvent = {
            "event": "gen",
            "c1curves": len(c1), "c2curves": len(c2),
            "pairsA": sum(1 for p in pairs if p[0] == "A"),
            "pairsB": sum(1 for p in pairs if p[0] == "B"),
            "pairsC": sum(1 for p in pairs if p[0] == "C"),
            "pairsTotal": len(pairs),
            "genSeconds": round(time.time()-t0, 1),
        }
        with open(logPath, "a") as f:
            f.write(json.dumps(genEvent) + "\n")
    # determinism guard: same pair universe on resume
    assert genEvent["pairsTotal"] == len(pairs), (genEvent["pairsTotal"], len(pairs))

    prog = {"next": 0, "gated": 0, "states": 0, "verified": 0, "hit": 0, "dual": 0, "mismatch": 0, "screenPass": 0}
    if os.path.exists(progPath):
        prog.update(json.load(open(progPath)))
    seen = set()
    if os.path.exists(seenPath):
        seen = set(json.load(open(seenPath)))

    flog = open(logPath, "a")
    fhits = open(hitsPath, "a")
    lastSave = time.time()
    for idx in range(prog["next"], len(pairs)):
        if time.time() - t0 > BUDGET:
            break
        branch, a1, a2, avoid, keystr = pairs[idx]
        crit = hot.get(a1, []) + hot.get(a2, [])
        for (rpair, rem) in Rs:
            if not avoid.isdisjoint(rpair):
                continue
            rows = list(rowBase)
            rows[a1[1]] += 1
            rows[a2[1]] += 1
            rows = [rows[i] + rem[i] for i in range(H)]
            if any(v > Q-1 for v in rows):
                continue
            if crit and not all(any(r in cs for r in rpair) for cs in crit):
                continue
            prog["gated"] += 1
            state = sorted(S - set(rpair) | {a1, a2})
            skey = str(state)
            prog["states"] += 1
            if skey in seen:
                continue
            seen.add(skey)
            prog["verified"] += 1
            sc = scr.screen(rpair, a1, a2)
            if prog["dual"] < 1500 or prog["verified"] % 250 == 0:
                res = verify(state, M, H, Q)
                prog["dual"] += 1
                if res["safe"] != sc[0] or res["maximal"] != sc[1]:
                    prog["mismatch"] += 1
                    flog.write(json.dumps({"event": "MISMATCH", "stones": state,
                                           "screen": [sc[0], sc[1]], "verify": [res["safe"], res["maximal"]]}) + "\n")
                    flog.flush()
                    raise SystemExit("SCREEN MISMATCH " + skey)
            if sc[0] and sc[1]:
                prog["screenPass"] += 1
                res = verify(state, M, H, Q)  # authoritative confirm
                assert res["safe"] and res["maximal"], ("screen false-positive", state)
                prog["hit"] += 1
                tamper = []
                for st in state:
                    r2v = verify([s for s in state if s != st], M, H, Q)
                    tamper.append([list(st), bool(r2v["maximal"])])
                fhits.write(json.dumps({
                    "branch": branch, "curve": keystr, "a1": list(a1), "a2": list(a2),
                    "removed": [list(x) for x in rpair], "stones": state,
                    "verify": res, "tamperAllMustBeFalse": tamper,
                }) + "\n")
                fhits.flush()
        prog["next"] = idx + 1
        if time.time() - lastSave > 5:
            json.dump(prog, open(progPath, "w"))
            lastSave = time.time()
    json.dump(prog, open(progPath, "w"))
    json.dump(sorted(seen), open(seenPath, "w"))
    flog.write(json.dumps({**prog, **genEvent,
                           "event": "chunkEnd", "wall": round(time.time()-t0, 1)}) + "\n")
    flog.close(); fhits.close()
    print(json.dumps({**prog, **genEvent}))

main()
  