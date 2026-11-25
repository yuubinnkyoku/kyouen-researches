"""Exhaustive small-n verification of pysat ``CardEnc.equals`` (seqcounter).

Mirrors the encoding used by ``build()`` in ``search_shape_class.py``::

    card_b = CardEnc.equals(lits=both, bound=c, top_id=4*h,    encoding=EncType.seqcounter)
    card_n = CardEnc.equals(lits=none, bound=e, top_id=card_b.nv, encoding=EncType.seqcounter)

i.e. ``equals`` with ``EncType.seqcounter`` and two back-to-back constraints whose
auxiliary variable ranges are chained through ``top_id`` / ``.nv``.

Verification method
-------------------
For each case (n, k) we build the cardinality CNF over main variables 1..n and
enumerate **all** 2^n main-variable assignments.  For each assignment X we ask
whether the CNF restricted to X (auxiliary variables free) is satisfiable, and
compare with the ground truth ``#true(X) == k``.

The extension question is decided by two independent procedures:

  * ``dpll_sat``: a from-scratch unit-propagation + DPLL search written here, over
    the auxiliary variables only.  This does not use any pysat code.
  * ``pysat_sat``: ``pysat.solvers.Cadical195`` with the main variables fixed as
    assumptions.

A case is recorded as a mismatch only if both procedures agree on a value that
disagrees with the ground truth.  Every (n, k, assignment) triple is checked;
the first mismatch per case is stored (the whole space is small, so the first
mismatch is also the smallest in enumeration order and we keep all of them up
to a cap).

Variants
--------
``contiguous``  lits = 1..n, top_id = n  (canonical shape)
``strided``     lits = 4i-3 (i = 1..n), top_id = 4n, matching the BOTH variable
                set of ``build()`` (4*i-4+1)
``chained``     a first ``equals(lits=4i-3, bound=k)`` followed by a second
                ``equals(lits=4i-2, bound=k)`` with top_id = first.nv, then the
                pair of constraints is checked against BOTH counts simultaneously
                (this is exactly the two-constraint chaining of ``build()``).

Usage::

    uv run --locked --with python-sat python cardenc_verify.py --nmax 12
"""
from __future__ import annotations

import argparse
import itertools
import json
import time
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical195

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"


# --------------------------------------------------------------------------- #
# independent checker: unit propagation + DPLL, no pysat
# --------------------------------------------------------------------------- #
def _assign(clauses, assign: dict[int, bool]) -> bool | None:
    """Unit propagation in place.  False on conflict, True if fully satisfied, None otherwise."""
    while True:
        conflict = False
        unit = None
        open_clause = None
        for c in clauses:
            count = 0
            last = None
            sat = False
            for lit in c:
                val = assign.get(abs(lit))
                if val is None:
                    count += 1
                    last = lit
                elif val == (lit > 0):
                    sat = True
                    break
            if sat:
                continue
            if count == 0:
                conflict = True
                break
            if count == 1:
                unit = last
                break
            if open_clause is None:
                open_clause = c
        if conflict:
            return False
        if unit is not None:
            assign[abs(unit)] = unit > 0
            continue
        if open_clause is None:
            return True
        # branch on the first literal of some still-open clause
        lit = None
        for cl in clauses:
            for l in cl:
                if abs(l) not in assign:
                    lit = l
                    break
            if lit is not None:
                break
        for val in (lit > 0, not (lit > 0)):
            branch = dict(assign)
            branch[abs(lit)] = val
            if _assign(clauses, branch):
                return True
        return False


def dpll_sat(clauses: list[list[int]], fixed: dict[int, bool]) -> bool:
    """Satisfiability of ``clauses`` over the free variables with ``fixed`` applied."""
    return bool(_assign(clauses, dict(fixed)))


def pysat_sat(clauses: list[list[int]], fixed: dict[int, bool], solver=None) -> bool:
    def solve(s):
        return s.solve(assumptions=[v if b else -v for v, b in fixed.items()])

    if solver is not None:
        return solve(solver)
    with Cadical195(bootstrap_with=clauses) as s:
        return solve(s)


# --------------------------------------------------------------------------- #
# encodings
# --------------------------------------------------------------------------- #
def encode_contiguous(n: int, k: int):
    res = CardEnc.equals(lits=list(range(1, n + 1)), bound=k, top_id=n,
                         encoding=EncType.seqcounter)
    return list(res.clauses), res.nv


def encode_strided(n: int, k: int):
    """Both-variable set of build(): 4i-3 for i = 1..n, top_id = 4n."""
    lits = [4 * i - 3 for i in range(1, n + 1)]
    res = CardEnc.equals(lits=lits, bound=k, top_id=4 * n, encoding=EncType.seqcounter)
    return list(res.clauses), res.nv


def encode_chained(n: int, k: int):
    """Two chained equals constraints, as build() does (BOTH-count and NONE-count)."""
    card_b = CardEnc.equals(lits=[4 * i - 3 for i in range(1, n + 1)], bound=k,
                            top_id=4 * n, encoding=EncType.seqcounter)
    card_n = CardEnc.equals(lits=[4 * i - 2 for i in range(1, n + 1)], bound=k,
                            top_id=card_b.nv, encoding=EncType.seqcounter)
    return list(card_b.clauses) + list(card_n.clauses), max(card_b.nv, card_n.nv)


def encode_chained_distinct(n: int, k: int, e: int):
    """build()'s two constraints with independent bounds c (=k) and e, both fixed.

    ``build()`` calls ``equals(both, c)`` then ``equals(none, e)`` with
    ``top_id=card_b.nv``; here both bounds are pinned, so the ground truth is
    ``#A == k and #B == e``.
    """
    card_b = CardEnc.equals(lits=[4 * i - 3 for i in range(1, n + 1)], bound=k,
                            top_id=4 * n, encoding=EncType.seqcounter)
    card_n = CardEnc.equals(lits=[4 * i - 2 for i in range(1, n + 1)], bound=e,
                            top_id=card_b.nv, encoding=EncType.seqcounter)
    return list(card_b.clauses) + list(card_n.clauses), max(card_b.nv, card_n.nv)


VARIANTS = {
    "contiguous": (encode_contiguous, [lambda i: i]),
    "strided": (encode_strided, [lambda i: 4 * i - 3]),
    "chained": (encode_chained, [lambda i: 4 * i - 3, lambda i: 4 * i - 2]),
}


# --------------------------------------------------------------------------- #
# verification
# --------------------------------------------------------------------------- #
def check_case(name: str, n: int, k: int, encoder, main_lit_fns):
    clauses, nv = encoder(n, k)
    # structural sanity: aux variables live strictly above every main variable
    mainvars = {fn(i) for fn in main_lit_fns for i in range(1, n + 1)}
    top_main = max(mainvars)
    aux_touched = {abs(l) for c in clauses for l in c} - mainvars
    bad_alias = sorted(v for v in aux_touched if v <= top_main)
    over_nv = [l for c in clauses for l in c if abs(l) > nv]

    ok = 0
    mismatches = []
    expected_sat = 0
    with Cadical195(bootstrap_with=clauses) as solver:
        for bits in itertools.product((False, True), repeat=n):
            truth = sum(bits) == k
            fixed = {fn(i + 1): bits[i] for fn in main_lit_fns for i in range(n)}
            got_dpll = dpll_sat(clauses, fixed)
            got_pysat = pysat_sat(clauses, fixed, solver)
            if got_dpll != got_pysat:
                mismatches.append({"bits": list(bits), "truth": truth,
                                   "dpll": got_dpll, "pysat": got_pysat,
                                   "kind": "checker-disagreement"})
            elif got_pysat != truth:
                mismatches.append({"bits": list(bits), "truth": truth,
                                   "cnf_sat": got_pysat, "kind": "encoding-mismatch"})
            else:
                ok += 1
            if truth:
                expected_sat += 1
    return {
        "n": n, "k": k, "vars": nv, "clauses": len(clauses),
        "assignments": 2 ** n, "ok": ok, "mismatches": len(mismatches),
        "expected_sat_assignments": expected_sat,
        "aux_vars": nv - len(mainvars),
        "aux_alias_main": len(bad_alias), "lit_above_nv": len(over_nv),
        "first_mismatch": mismatches[0] if mismatches else None,
        "mismatch_examples": mismatches[:5],
    }


def check_joint_case(n: int, c: int, e: int):
    """build()'s literal shape: equals(BOTH,c) chained with equals(NONE,e).

    Main variables: BOTH_i = 4i-3, NONE_i = 4i-2.  Enumerates all 4^n joint
    assignments (the two variable sets are independent in the CNF, so this is the
    full main-variable space) and compares auxiliary satisfiability with
    ``#BOTH == c and #NONE == e``.
    """
    clauses, nv = encode_chained_distinct(n, c, e)
    A = [4 * i - 3 for i in range(1, n + 1)]
    B = [4 * i - 2 for i in range(1, n + 1)]
    mainvars = set(A) | set(B)
    top_main = max(mainvars)
    bad_alias = sorted(v for v in {abs(l) for cl in clauses for l in cl} - mainvars
                       if v <= top_main)
    over_nv = [l for cl in clauses for l in cl if abs(l) > nv]

    ok = 0
    mismatches = []
    expected_sat = 0
    with Cadical195(bootstrap_with=clauses) as solver:
        for ma in itertools.product((False, True), repeat=n):
            for mb in itertools.product((False, True), repeat=n):
                truth = sum(ma) == c and sum(mb) == e
                fixed = {v: b for v, b in zip(A, ma)}
                fixed.update({v: b for v, b in zip(B, mb)})
                got_dpll = dpll_sat(clauses, fixed)
                got_pysat = pysat_sat(clauses, fixed, solver)
                if got_dpll != got_pysat:
                    mismatches.append({"both": list(ma), "none": list(mb), "truth": truth,
                                       "dpll": got_dpll, "pysat": got_pysat,
                                       "kind": "checker-disagreement"})
                elif got_pysat != truth:
                    mismatches.append({"both": list(ma), "none": list(mb), "truth": truth,
                                       "cnf_sat": got_pysat, "kind": "encoding-mismatch"})
                else:
                    ok += 1
                if truth:
                    expected_sat += 1
    return {
        "n": n, "c": c, "e": e, "vars": nv, "clauses": len(clauses),
        "assignments": 4 ** n, "ok": ok, "mismatches": len(mismatches),
        "expected_sat_assignments": expected_sat,
        "aux_vars": nv - len(mainvars),
        "aux_alias_main": len(bad_alias), "lit_above_nv": len(over_nv),
        "first_mismatch": mismatches[0] if mismatches else None,
        "mismatch_examples": mismatches[:5],
    }


def negative_control(nmax: int = 6) -> dict:
    """Sanity check of the harness itself: an intentionally wrong bound must be caught.

    For each (n,k) the CNF encodes ``equals(..., bound=k+1)`` while the ground truth
    used for comparison is ``#true == k``; the checker must report mismatches.
    """
    total = detected = 0
    for n in range(1, nmax + 1):
        for k in range(0, n + 1):
            if k == n:
                continue  # bound k+1 == n makes the encoding correct by accident; skip
            res = CardEnc.equals(lits=list(range(1, n + 1)), bound=k + 1, top_id=n,
                                 encoding=EncType.seqcounter)
            for bits in itertools.product((False, True), repeat=n):
                fixed = {i + 1: bits[i] for i in range(n)}
                total += 1
                if dpll_sat(list(res.clauses), fixed) != (sum(bits) == k):
                    detected += 1
    return {"assignments": total, "detected_mismatches": detected,
            "expect": "detected_mismatches > 0"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--nmax", type=int, default=12)
    ap.add_argument("--nmin", type=int, default=1)
    ap.add_argument("--joint-nmax", type=int, default=8)
    ap.add_argument("--time-limit", type=float, default=600.0)
    args = ap.parse_args()

    OUT.mkdir(exist_ok=True)
    t_start = time.time()
    records = {}
    total_cases = total_assignments = total_mismatches = 0
    incomplete = []
    for name, (encoder, main_lit_fns) in VARIANTS.items():
        recs = []
        for n in range(args.nmin, args.nmax + 1):
            for k in range(0, n + 1):
                if time.time() - t_start > args.time_limit:
                    incomplete.append([name, n, k])
                    break
                rec = check_case(name, n, k, encoder, main_lit_fns)
                recs.append(rec)
                total_cases += 1
                total_assignments += rec["assignments"]
                total_mismatches += rec["mismatches"]
                if rec["mismatches"] or rec["aux_alias_main"] or rec["lit_above_nv"]:
                    print(f"[FAIL] {name} n={n} k={k}: {rec['first_mismatch']} "
                          f"alias={rec['aux_alias_main']} above_nv={rec['lit_above_nv']}",
                          flush=True)
            else:
                continue
            break
        records[name] = recs
        ns = sorted({r["n"] for r in recs})
        print(f"{name}: {len(recs)} cases, n in {ns[0] if ns else '-'}..{ns[-1] if ns else '-'}, "
              f"mismatches={sum(r['mismatches'] for r in recs)}", flush=True)

    # joint variant: build()'s two chained constraints with independent bounds c, e
    joint = []
    joint_done = True
    for n in range(args.nmin, args.joint_nmax + 1):
        for c in range(0, n + 1):
            for e in range(0, n + 1):
                if time.time() - t_start > args.time_limit:
                    joint_done = False
                    break
                rec = check_joint_case(n, c, e)
                joint.append(rec)
                total_cases += 1
                total_assignments += rec["assignments"]
                total_mismatches += rec["mismatches"]
                if rec["mismatches"] or rec["aux_alias_main"] or rec["lit_above_nv"]:
                    print(f"[FAIL] joint n={n} c={c} e={e}: {rec['first_mismatch']} "
                          f"alias={rec['aux_alias_main']} above_nv={rec['lit_above_nv']}",
                          flush=True)
            if not joint_done:
                break
        if not joint_done:
            incomplete.append(["joint", n, None])
            break
    records["joint"] = joint
    print(f"joint: {len(joint)} cases, n<={args.joint_nmax if joint_done else 'partial'}, "
          f"mismatches={sum(r['mismatches'] for r in joint)}", flush=True)

    neg = negative_control(min(args.joint_nmax, 6))
    print(f"negative control: {neg['detected_mismatches']}/{neg['assignments']} "
          f"mutations detected", flush=True)

    report = {
        "script": "cardenc_verify.py",
        "pysat_encoding": "pysat.card.CardEnc.equals(..., encoding=EncType.seqcounter)",
        "verified_encoder": "search_shape_class.py::build (lines 50-53)",
        "method": {
            "extension_check": "for each main-variable assignment, decide auxiliary "
                               "satisfiability (a) by an independent unit-propagation+DPLL "
                               "implemented in this script and (b) by Cadical195 with the main "
                               "variables fixed as assumptions; a case counts as a mismatch "
                               "only when both agree against the ground truth",
            "ground_truth": "single-set variants: exactly k of the n main literals true; "
                            "joint variant: #BOTH == c and #NONE == e",
            "single_variants": "2^n assignments per (n,k)",
            "joint_variant": "4^n assignments per (n,c,e) for the chained "
                             "equals(BOTH,c)/equals(NONE,e) pair of build()",
        },
        "nmax": args.nmax,
        "joint_nmax": args.joint_nmax,
        "joint_complete": joint_done,
        "variants": list(VARIANTS) + ["joint"],
        "scope_note": "per-case range is stated in records; joint capped at n<=joint_nmax",
        "negative_control": neg,
        "total_cases": total_cases,
        "total_assignments": total_assignments,
        "total_mismatches": total_mismatches,
        "incomplete": incomplete,
        "seconds": round(time.time() - t_start, 2),
        "records": records,
    }
    path = OUT / "w15-cardenc-verify.json"
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"cases={total_cases} assignments={total_assignments} "
          f"mismatches={total_mismatches} seconds={report['seconds']} -> {path}")
    return 0 if total_mismatches == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
