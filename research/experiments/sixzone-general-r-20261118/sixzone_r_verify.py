#!/usr/bin/env python3
"""K0968 verifier: gamma_r (r>=4) SIX-ZONE_r / P2-LOWER_r / BAND_r / Y-CAP_r
on published kodd>=5 rows (K0965 modeb_rows_k5p + K0963 band), kodd=4
reproduction (K0966 inputs), and A-POS (kap even <=> a>=1) machine anchor
on all published row files including kodd=3 deep band.

Deterministic, stdlib only. Cold-rerun byte-identical requirement.
Inputs are pinned by sha256 (asserted).
"""
import json, hashlib, sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent

INPUTS = {
    "k5p":  EXP / "remo-kodd4-sqrt-band-20261118/output/modeb_rows_k5p.jsonl",
    "band": EXP / "remo-kodd5-cap-20261118/output/kodd5_band_k5rows.json",
    "k4d":  EXP / "remo-kodd4-sqrt-band-20261118/output/modeb_rows_k4_deep.jsonl",
    "k4k":  EXP / "remo-kodd4-sqrt-band-20261118/output/modeb_rows_k4_kap0.jsonl",
    "k3d":  EXP / "remo-kodd4-sqrt-band-20261118/output/modeb_rows_k3_t300plus.jsonl",
}
PIN_SHA256 = {
    "k5p":  "25a0a3346cc0cb08f3c97aa3fa7251bd3e992aa555c0bab9e9df861479351bb1",
    "band": "782736fdfc0c2a340f6ece0eb28b2b727d866ea9cc21b05bb6e0a9b4e2f57664",
    "k4d":  "38e578327a2a9ded86b3925b1c86d45f37b823b9596a156132766f0f53c44bc7",
    "k4k":  "be6bff78910d1df2a5ca16a05496e825814f552704106ca4f6433ffa92000b2d",
    "k3d":  "e45f02934f905c86cb4d00164658a8295d5b9d8e426f6b3bf7e73207c83e88dc",
}

def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def is_prime(n):
    if n < 2: return False
    if n % 2 == 0: return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0: return False
        d += 2
    return True

def v2(n):
    a = 0
    while n % 2 == 0:
        n //= 2; a += 1
    return a

def divisors_from_odd(odd):
    """All divisors of prod(odd) (odd part)."""
    divs = [1]
    for p in odd:
        divs = divs + [d * p for d in divs]
    return divs

def row_violations(r):
    """Identity / regime / smooth / window / A-POS checks. Returns list of codes."""
    v = []
    M, t, kap, Y, N, a, k0, odd = (r["M"], r["t"], r["kap"], r["Y"],
                                   r["N"], r["a"], r["k0"], r["odd"])
    if N != M * Y - 1: v.append("N=MY-1")
    if N != (2 ** a) * __import__("math").prod(odd): v.append("N=2^a*odd")
    if k0 != M * t + kap - 1: v.append("k0")
    if Y != (M + 1) * t + kap + 1: v.append("Y")
    if Y - k0 != t + 2: v.append("Y-k0=t+2")
    if N != (M + 1) * k0 + 2 * M - kap: v.append("core-id")
    if not is_prime(M): v.append("M-prime")
    if not (M >= 5): v.append("M>=5")
    if not (0 <= kap <= M - 2): v.append("regime-kap")
    if (t, kap) == (1, 0): v.append("regime-(t,kap)")
    if a != v2(N): v.append("a=v2(N)")
    if sorted(odd) != odd: v.append("odd-sorted")
    for p in odd:
        if p % 2 == 0 or not is_prime(p): v.append("odd-prime"); break
    if odd and max(odd) > M - 1: v.append("smooth")
    # window empty: no divisor 2^j * d in [M, k0]
    bad = 0
    for d in divisors_from_odd(odd):
        for j in range(a + 1):
            q = (2 ** j) * d
            if M <= q <= k0:
                bad += 1
                break
        if bad: break
    if bad: v.append("window")
    # A-POS machine anchor: kap even <=> Y odd <=> N even <=> a>=1
    if kap % 2 != 0: v.append("APOS-kap-even")
    if a < 1: v.append("APOS-a>=1")
    return v

def gamma_state(r):
    odd = r["odd"]; M = r["M"]; rr = len(odd)
    if rr < 4:
        return None, None
    gprod = 1
    for x in odd[1:rr-1]:
        gprod *= x
    return (gprod >= M), gprod

def gamma_predicates(r):
    """For gamma_r rows: GZ/EX/SIX-ZONE/P2-LOWER/BAND/Y-CAP (+CONG as identity).
    Returns dict bool + margins dict."""
    odd = r["odd"]; M, t, kap, k0 = r["M"], r["t"], r["kap"], r["k0"]
    a = r["a"]; rr = len(odd); c = (2 ** a) * odd[0]
    B = (M - 1) // c
    gprod = 1
    for x in odd[1:rr-1]:
        gprod *= x
    ex_vals = [odd[0] * odd[i] for i in range(rr)]
    six_vals = [c * odd[i] for i in range(rr)]
    lhs = t * c ** (rr - 2) * M * (M + 1)
    rhs = (M - 1) ** (rr - 1) + c ** (rr - 2)
    cong = (c * __import__("math").prod(odd[1:])) % M == (M - 1) % M
    res = {
        "GZ": gprod >= k0 + 1,
        "EX": max(ex_vals) <= k0,
        "SIXZONE": max(six_vals) <= M - 1,
        "P2LOWER": odd[1] * B ** (rr - 3) >= k0 + 1,
        "BAND": M * t + kap <= B ** (rr - 2),
        "YCAP": lhs < rhs,
        "CONG": cong,
    }
    margins = {
        "gz_minus_k0": gprod - k0,
        "ex_margin": k0 - max(ex_vals),
        "sixzone_margin": M - 1 - max(six_vals),
        "p2lower_ratio": (odd[1] * B ** (rr - 3)) / (k0 + 1),
        "band_margin": B ** (rr - 2) - (M * t + kap),
        "ycap_ratio": rhs / lhs,
    }
    return res, margins

def nongamma_sixzone(r):
    odd = r["odd"]; M = r["M"]; a = r["a"]
    c = (2 ** a) * odd[0]
    fails = [i for i in range(len(odd)) if c * odd[i] > M - 1]
    return fails

def load_jsonl(p):
    return [json.loads(l) for l in Path(p).read_text().splitlines() if l.strip()]

def main():
    out = {"schema": "k0968-sixzone-general-r-v1", "input_sha256": {}, "files": {}}
    for k, p in INPUTS.items():
        h = sha256(p)
        out["input_sha256"][k] = h
        if PIN_SHA256[k] is not None and h != PIN_SHA256[k]:
            out["files"][k] = {"pin_mismatch": True, "actual": h}
    all_ok = all("pin_mismatch" not in v for v in out["files"].values())

    def audit(name, rows, do_gamma=True, deep=False):
        st = {"rows": len(rows), "identity_violations": 0,
              "identity_codes": Counter(), "unique_rows": 0,
              "kodd_dist": Counter(), "a_dist": Counter(),
              "kap0": 0, "gamma": Counter(), "nongamma": Counter(),
              "gamma_pred_fail": Counter(), "margins_min": {},
              "nongamma_sixzone_fail": 0, "nongamma_sixzone_pass": 0,
              "nongamma_fail_index": Counter(), "args": {},
              "gamma_wall_rows": []}
        seen = {}
        marg_acc = {}
        for r in rows:
            iv = row_violations(r)
            if iv:
                st["identity_violations"] += 1
                st["identity_codes"].update(iv)
            key = (r["M"], r["t"], r["kap"])
            if key in seen:
                if json.dumps(seen[key], sort_keys=True) != json.dumps(r, sort_keys=True):
                    st["identity_codes"].update(["dup-mismatch"])
            else:
                seen[key] = r
            st["unique_rows"] = len(seen)
            st["kodd_dist"][len(r["odd"])] += 1
            st["a_dist"][r["a"]] += 1
            if r["kap"] == 0: st["kap0"] += 1
            if not do_gamma:
                continue
            rr = len(r["odd"])
            g, gprod = gamma_state(r)
            if g is None:
                st["nongamma"]["r<4"] += 1
                continue
            if g:
                st["gamma"][rr] += 1
                res, margins = gamma_predicates(r)
                for kk, ok in res.items():
                    if not ok:
                        st["gamma_pred_fail"][f"r{rr}:{kk}"] += 1
                for kk, val in margins.items():
                    keym = f"r{rr}:{kk}"
                    if keym not in marg_acc or val < marg_acc[keym]:
                        marg_acc[keym] = val
                if margins["sixzone_margin"] <= 15:
                    st["gamma_wall_rows"].append(
                        {"M": r["M"], "t": r["t"], "kap": r["kap"], "a": r["a"],
                         "odd": r["odd"], "sixzone_margin": margins["sixzone_margin"]})
            else:
                st["nongamma"][rr] += 1
                fails = nongamma_sixzone(r)
                if fails:
                    st["nongamma_sixzone_fail"] += 1
                    st["nongamma_fail_index"][tuple(fails)] += 1
                else:
                    st["nongamma_sixzone_pass"] += 1
        st["margins_min"] = marg_acc
        st["identity_codes"] = dict(st["identity_codes"])
        st["kodd_dist"] = {str(k): v for k, v in sorted(st["kodd_dist"].items())}
        st["a_dist"] = {str(k): v for k, v in sorted(st["a_dist"].items())}
        st["gamma"] = {str(k): v for k, v in sorted(st["gamma"].items())}
        st["nongamma"] = {str(k): v for k, v in sorted(st["nongamma"].items())}
        st["nongamma_fail_index"] = {str(k): v for k, v in sorted(st["nongamma_fail_index"].items())}
        st["gamma_pred_fail"] = dict(st["gamma_pred_fail"])
        st["gamma_wall_rows"] = sorted(st["gamma_wall_rows"],
                                       key=lambda w: (w["sixzone_margin"], w["M"]))
        ok = (st["identity_violations"] == 0
              and not st["gamma_pred_fail"]
              and st["nongamma_sixzone_pass"] == 0)
        return st, ok

    k5p = load_jsonl(INPUTS["k5p"])
    band = json.loads(INPUTS["band"].read_text())
    k4d = load_jsonl(INPUTS["k4d"])
    k4k = load_jsonl(INPUTS["k4k"])
    k3d = load_jsonl(INPUTS["k3d"])

    st, ok = audit("k5p", k5p)
    out["files"]["k5p"] = st; all_ok &= ok
    st, ok = audit("band", band)
    out["files"]["band"] = st; all_ok &= ok
    st, ok = audit("k4d+k4k", k4d + k4k)
    out["files"]["k4d+k4k"] = st; all_ok &= ok
    st, ok = audit("k3d", k3d, do_gamma=False)
    out["files"]["k3d"] = st
    all_ok &= (st["identity_violations"] == 0)

    # overlap between k5p and band on (M,t,kap): common fields must agree
    k5map = {(r["M"], r["t"], r["kap"]): r for r in k5p}
    ov = 0; ov_ok = True
    for b in band:
        key = (b["M"], b["t"], b["kap"])
        if key in k5map:
            ov += 1
            r = k5map[key]
            for f in ("M", "t", "kap", "Y", "N", "a", "k0", "odd"):
                if r[f] != b[f]:
                    ov_ok = False
    out["k5p_band_overlap"] = {"count": ov, "common_fields_agree": ov_ok}
    all_ok &= ov_ok

    # band config x gamma cross-tab + Y_prime / cap_holds recheck
    ct = Counter(); yp_bad = 0; ch_bad = 0
    for b in band:
        g, _ = gamma_state(b)
        ct[(b["config"], "gamma" if g else "nongamma")] += 1
        if b["Y_prime"] != is_prime(b["Y"]): yp_bad += 1
        if not b["cap_holds"]: ch_bad += 1
    out["band_config_x_gamma"] = {f"{c}/{g}": n for (c, g), n in sorted(ct.items())}
    out["band_yprime_recheck_bad"] = yp_bad
    out["band_capholds_bad"] = ch_bad
    all_ok &= (yp_bad == 0 and ch_bad == 0)

    # gamma<=>sixzone equivalence census (unique rows, kodd>=4 files)
    eq = {"gamma_pass": 0, "nongamma_fail": 0, "exceptions": 0}
    uniq = {}
    for r in k5p + band + k4d + k4k:
        uniq[(r["M"], r["t"], r["kap"])] = r
    for r in uniq.values():
        g, _ = gamma_state(r)
        if g is None: continue
        if g:
            res, _ = gamma_predicates(r)
            eq["gamma_pass" if res["SIXZONE"] else "exceptions"] += 1
        else:
            eq["nongamma_fail" if nongamma_sixzone(r) else "exceptions"] += 1
    out["gamma_iff_sixzone_census"] = eq
    all_ok &= (eq["exceptions"] == 0)

    out["all_ok"] = bool(all_ok)
    dest = HERE / "output" / "sixzone_r_audit.json"
    dest.write_text(json.dumps(out, indent=1, sort_keys=True, ensure_ascii=False) + "\n",
                    encoding="utf-8")
    print("all_ok =", all_ok)
    print(json.dumps({k: v for k, v in out.items()
                      if k in ("k5p_band_overlap", "band_config_x_gamma",
                               "gamma_iff_sixzone_census")}, ensure_ascii=False))
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
