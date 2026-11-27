# check_golay.py — independent Python cross-check of stage-1 outputs.
# Re-derives the Golay code, dodecads, d11 and re-verifies the 13-cap list
# and the nond11 mask file.  Standard library only.
#
# Usage (from repo root, with -I):
#   python -I check_golay.py BOARD GOLAY_TXT CAPS_TXT D11_TXT NOND11_BIN HASHES_TXT OUT_JSON
import sys, json, hashlib, struct
from bisect import bisect_left

def main():
    board, golay_txt, caps_txt, d11_txt, nond_bin, hashes_txt, out_json = sys.argv[1:8]

    # ---- board ----
    toks = open(board).read().split()
    it = iter(toks)
    n = int(next(it)); nb = int(next(it))
    octs = []
    for _ in range(nb):
        k = int(next(it))
        m = 0
        for _ in range(k):
            m |= 1 << int(next(it))
        octs.append(m)
    assert n == 24 and nb == 759

    def popcount(x):
        return bin(x).count("1")

    # ---- Golay span (F2 doubling over pivot basis) ----
    piv = {}
    for o in octs:
        x = o
        while x:
            hb = x.bit_length() - 1
            if hb in piv:
                x ^= piv[hb]
            else:
                piv[hb] = x
                break
    basis = [piv[k] for k in sorted(piv)]
    span = [0]
    for b in basis:
        span += [w ^ b for w in span]
    wh = {}
    for w in span:
        c = popcount(w)
        wh[c] = wh.get(c, 0) + 1
    exp_wh = {0: 1, 8: 759, 12: 2576, 16: 759, 24: 1}
    weights_ok = wh == exp_wh and len(span) == 4096
    dodecads = [w for w in span if popcount(w) == 12]
    dodecads_ok = len(dodecads) == 2576

    # ---- d11 regeneration ----
    d11_set = set()
    for d in dodecads:
        for p in range(24):
            if d >> p & 1:
                d11_set.add(d ^ (1 << p))
    d11_reg_ok = len(d11_set) == 30912

    # ---- golay_weights.txt compare ----
    got = {}
    for line in open(golay_txt):
        parts = line.split()
        got[int(parts[1])] = int(parts[3])
    golay_file_ok = got == exp_wh

    # ---- d11.txt compare ----
    d11_file = [int(l) for l in open(d11_txt)]
    d11_sorted = sorted(d11_file)
    d11_file_ok = (len(d11_file) == 30912 and d11_sorted == d11_file
                   and set(d11_file) == d11_set)

    # ---- caps13.txt verify ----
    caps = [int(l) for l in open(caps_txt)]
    caps_sorted_strict = all(caps[i] < caps[i + 1] for i in range(len(caps) - 1))
    caps_pc_ok = all(popcount(c) == 13 for c in caps)
    unsafe = 0
    for c in caps:
        for o in octs:
            if c & o == o:
                unsafe += 1
                break
    caps_count_ok = len(caps) == 30912 and unsafe == 0

    # ---- maximality sample (every 309th cap + first/last) ----
    sample = sorted(set(list(range(0, 30912, 309)) + [0, 30911]))
    pnt_blocks = [[] for _ in range(24)]
    for o in octs:
        for p in range(24):
            if o >> p & 1:
                pnt_blocks[p].append(o)
    nonmax = 0
    for ci in sample:
        c = caps[ci]
        for p in range(24):
            if c >> p & 1:
                continue
            if all(popcount(c & o) <= 6 for o in pnt_blocks[p]):
                nonmax += 1
                break
    max_sample_ok = nonmax == 0

    # ---- nond11 bin integrity ----
    raw = open(nond_bin, "rb").read()
    bin_len_ok = len(raw) == 4 * 2040192
    nond = list(struct.unpack("<%dI" % (len(raw) // 4), raw)) if bin_len_ok else []
    nond_sorted_strict = all(nond[i] < nond[i + 1] for i in range(len(nond) - 1)) if bin_len_ok else False
    disjoint = not any(m in d11_set for m in nond) if bin_len_ok else False
    sha = hashlib.sha256(raw).hexdigest()

    hashes_ok = False
    for line in open(hashes_txt):
        parts = line.split()
        if len(parts) == 2 and parts[1].endswith("nond11_masks.bin"):
            hashes_ok = parts[0] == sha

    # ---- incidence + split sample: exactly one dodecad, 12/66 split ----
    inc_bad = split_bad = 0
    sample2 = sorted(set(list(range(0, 30912, 51)) + [0, 30911]))
    for ci in sample2:
        c = caps[ci]
        indd = [d for d in dodecads if c & d == d]
        if len(indd) != 1:
            inc_bad += 1
            continue
        D = indd[0]
        pts = [p for p in range(24) if c >> p & 1]
        din = dnond = 0
        for a in range(13):
            for b in range(a + 1, 13):
                sub = c & ~((1 << pts[a]) | (1 << pts[b]))
                if sub in d11_set:
                    din += 1
                    if sub & D != sub:
                        split_bad += 1
                else:
                    dnond += 1
                    i = bisect_left(nond, sub)
                    if not (i < len(nond) and nond[i] == sub):
                        split_bad += 1
        if din != 12 or dnond != 66:
            split_bad += 1
    inc_sample_ok = inc_bad == 0 and split_bad == 0

    all_ok = all([weights_ok, dodecads_ok, d11_reg_ok, golay_file_ok, d11_file_ok,
                  caps_sorted_strict, caps_pc_ok, caps_count_ok, max_sample_ok,
                  bin_len_ok, nond_sorted_strict, disjoint, hashes_ok, inc_sample_ok])

    res = {
        "weights_ok": weights_ok, "span4096": len(span) == 4096,
        "dodecads_ok": dodecads_ok, "d11_reg_ok": d11_reg_ok,
        "golay_file_ok": golay_file_ok, "d11_file_ok": d11_file_ok,
        "caps_sorted_strict": caps_sorted_strict, "caps_popcount_ok": caps_pc_ok,
        "caps_all_safe": unsafe == 0, "caps_count_ok": caps_count_ok,
        "maximality_sample_size": len(sample), "maximality_sample_ok": max_sample_ok,
        "nond11_bin_len_ok": bin_len_ok, "nond11_sorted_strict": nond_sorted_strict,
        "nond11_disjoint_d11": disjoint, "sha256_nond11": sha, "hashes_match": hashes_ok,
        "incidence_split_sample_size": len(sample2),
        "incidence_split_sample_ok": inc_sample_ok,
        "all_ok": all_ok,
    }
    with open(out_json, "w") as f:
        json.dump(res, f, indent=2)
    print("crosscheck:", "PASS" if all_ok else "FAIL", json.dumps(res))
    sys.exit(0 if all_ok else 1)

main()
