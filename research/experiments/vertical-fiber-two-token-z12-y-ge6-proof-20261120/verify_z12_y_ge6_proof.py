#!/usr/bin/env python3
"""Independent audit for the z=12, y>=6 two-token full-Grundy theorem.

The universal claim rests on the y-strong induction, x-outer induction,
and the complete A/B/C signature-band table in report.md. This verifier
separately checks the table against closed-form child transcriptions and
against two direct mex recurrences on finite grids.
"""
from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path

from candidate import (
    H_ordered, H_canonical, clear_engines, value12, k1043_z12_y5,
    k1055_z11, single_token,
)
from bands import band_sig
from band_derive import child_signature, mex_of_signature


class Audit:
    def __init__(self):
        self.counts = {}
        self.failures = []

    def check(self, key, condition, detail=""):
        self.counts[key] = self.counts.get(key, 0) + 1
        if not condition and len(self.failures) < 30:
            self.failures.append(f"{key}: {detail}")


def main():
    audit = Audit()

    # V1: complete parity-band coverage, closed-form child signature,
    # mex formula, and the K0832 parity upper bound on a wide (y,d) grid.
    y_grid = list(range(6, 81)) + [90, 100, 125, 150, 200, 300]
    for y in y_grid:
        dmax = 81 if y <= 80 else 41
        for d in range(dmax):
            S = 2 * y + d
            for R in range(1, S + 13):
                sig = band_sig(y, d, R)
                cl = child_signature(y, d, R)
                audit.check("band_vs_closed_form_children", sig == cl,
                            f"y={y} d={d} R={R}: {sig} != {cl}")
                if sig is None:
                    continue
                m = mex_of_signature(sig)
                audit.check("band_mex_vs_value12",
                            m == value12(y + d, y, R),
                            f"y={y} d={d} R={R}: mex({sig})={m}")
                bound = 2 if R % 2 else 1
                audit.check("theorem_T_parity_bound", m <= bound,
                            f"y={y} d={d} R={R}: mex({sig})={m}>{bound}")

    # V2: two genuinely different direct recurrences vs the proposed formula.
    for y in range(6, 13):
        for d in range(0, 11):
            x = y + d
            S = x + y
            for R in range(0, S + 21):
                ordered = H_ordered(R, (x, y), 12)
                canonical = H_canonical(R, (x, y), 12)
                expected = value12(x, y, R)
                audit.check("ordered_vs_formula", ordered == expected,
                            f"x={x} y={y} R={R}: {ordered}!={expected}")
                audit.check("canonical_vs_formula", canonical == expected,
                            f"x={x} y={y} R={R}: {canonical}!={expected}")
                audit.check("ordered_vs_canonical", ordered == canonical,
                            f"x={x} y={y} R={R}: {ordered}!={canonical}")
            clear_engines()

    # V3: the y=6 B-child is the published K1043 slice.
    for x in range(6, 41):
        for r in range(0, x + 21):
            actual = H_ordered(r, (x, 5), 12)
            expected = k1043_z12_y5(x, r)
            audit.check("K1043_base_anchor", actual == expected,
                        f"x={x} r={r}: {actual}!={expected}")
        clear_engines()

    # V4: every C-child is 1 xor the published K1055 z=11 uniform formula.
    for y in range(6, 13):
        for d in range(0, 13):
            x = y + d
            S = x + y
            for r in range(0, S + 21):
                actual = H_ordered(r, (x, y), 11)
                expected = k1055_z11(x, y, r)
                audit.check("K1055_C_anchor", actual == expected,
                            f"x={x} y={y} r={r}: {actual}!={expected}")
            clear_engines()

    # V5: K0832 height-only reduction for R<=z+1=13.
    for y in range(6, 101):
        for d in range(0, 51):
            x = y + d
            S = x + y
            for R in range(0, 14):
                audit.check("height_only_R_le_13",
                            value12(x, y, R) == single_token(S, 12, R),
                            f"x={x} y={y} R={R}")

    # V6: K0832 general tail R>=S+13.
    for y in range(6, 501):
        for d in (0, 1, 2, 3, 4, 7, 10, 11, 12, 13, 14, 15, 16, 31, 64, 100):
            x = y + d
            S = x + y
            for R in range(S + 13, S + 17):
                audit.check("general_tail_formula",
                            value12(x, y, R) == S % 2,
                            f"x={x} y={y} R={R}")

    # V7: direct engine tail spot checks, separate from formula-only V6.
    for y in range(6, 11):
        for d in range(0, 11):
            x = y + d
            S = x + y
            for R in range(S + 13, S + 18):
                actual = H_ordered(R, (x, y), 12)
                audit.check("general_tail_vs_engine", actual == S % 2,
                            f"x={x} y={y} R={R}: {actual}!={S % 2}")
            clear_engines()

    # V8: fixed-seed direct-engine scatter.
    rng = random.Random(20261120)
    for _ in range(400):
        y = rng.randint(6, 30)
        d = rng.randint(0, 30)
        x = y + d
        S = x + y
        R = rng.randint(0, S + 25)
        actual = H_ordered(R, (x, y), 12)
        expected = value12(x, y, R)
        audit.check("fixed_seed_scatter", actual == expected,
                    f"x={x} y={y} R={R}: {actual}!={expected}")
        clear_engines()

    verifier_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    audit_body = {
        "all_pass": not audit.failures,
        "classification": (
            "universal theorem: y-strong induction, x-outer induction, "
            "and a complete A/B/C signature-band partition"
        ),
        "slice": "two-token residual game z=12, all x>=y>=6, all R>=0",
        "counts": dict(sorted(audit.counts.items())),
        "total_checks": sum(audit.counts.values()),
        "failure_count": len(audit.failures),
        "failures": audit.failures,
        "finite_audit_role": (
            "finite transcription and implementation audit only; universality "
            "rests on the two-level induction and the complete symbolic "
            "signature-band table in report.md"
        ),
        "seeds": {"scatter": 20261120},
        "verifier_sha256": verifier_sha,
    }
    out = Path(__file__).with_name("output")
    out.mkdir(parents=True, exist_ok=True)
    body = json.dumps(audit_body, sort_keys=True, indent=2, ensure_ascii=False)
    (out / "audit.json").write_bytes(body.encode("utf-8"))

    stable = dict(audit_body)
    stable.pop("verifier_sha256", None)
    stable.pop("total_checks", None)
    stable["counts"] = dict(sorted(audit.counts.items()))
    stable_sha = hashlib.sha256(
        json.dumps(stable, sort_keys=True, indent=2,
                   ensure_ascii=False).encode("utf-8")
    ).hexdigest()
    print(json.dumps({
        "all_pass": audit_body["all_pass"],
        "total_checks": audit_body["total_checks"],
        "failure_count": audit_body["failure_count"],
        "verifier_sha256": verifier_sha,
        "audit_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
        "audit_sha256_excluding_self_reference": stable_sha,
        "counts": audit_body["counts"],
    }, sort_keys=True, indent=2, ensure_ascii=False))
    return audit_body["all_pass"]


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
