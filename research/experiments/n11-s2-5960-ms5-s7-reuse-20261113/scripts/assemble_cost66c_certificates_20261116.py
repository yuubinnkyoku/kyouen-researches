#!/usr/bin/env python3
"""Assemble, verify and manifest the seven cost-66c WIN7-D10
certificates (bits 73, 75, 79, 87, 96, 97, 112, child
00000000000000003800000008002008, 2026-11-16).
Same protocol as assemble_cost65n_certificates_20261116.py, with the
publication split generalized from 2 parts to N parts (bit 112 whole
cert is ~2.77 MB, so three parts are needed to keep every published
part under the publication split threshold).

Per bit, from the blind extraction chunk written by scripts/cert_driver65j.ts
(published generic single-root blind extraction driver, repo-verbatim
class4_child1_cert_extractor_exact_v16.ts, empty kill table):
  - sort -u the raw rows (exact byte order, Python sorted(set(...))),
  - prepend the n11-terminal-strategy-v1 header and root lines,
  - verify with the published independent verifiers:
      verify_bit7_win7_cert.ts --cert ... --root-check --subroots ...
      verify_win7_certificate_bigint_independent.mjs ... n_moves
  - split every cert over the publication split threshold (1,200,000
    bytes) at line boundaries into N parts (N = ceil(bytes/threshold),
    minimum 2) with a receipt,
  - write the published-schema bigint-verify.json / bareiss-verify.json
    wrappers (verifier stdout, no reinterpretation of the pass criteria:
    the verifiers exit non-zero on any failure),
  - emit the certificates manifest.

Bookkeeping and proof artifacts for individual 7-stone roots only; the
11x11 empty board remains UNKNOWN.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
CERTS = OUT / "class2-lane-cost66c-certificates"
SCRIPTS = HERE / "scripts"
CHILD = "00000000000000003800000008002008"
CHILD_V = int(CHILD, 16)
PARENT_ANCHOR = "00000000000000003800000008002000"
SH_PARENT = "00000000000000003800000008002000"
DIRECT_S5_PARENTS = [
    {"s5_hex": "00000000000000003800000008002000",
     "classes_mask": 2, "remaining_s6_orbits_head1441": 29,
     "remaining_s7_edge_cost_head1441": 2017},
]
BITS = [73, 75, 79, 87, 96, 97, 112]
SPLIT_LIMIT = 1200000  # publication split threshold (bytes):
               # keeps every published part safely below the
               # 1.75 MiB repo per-file convention AND the
               # ~1.2 MB practical single-push transport
               # limit of the publication tooling
HEADER = ("n11-terminal-strategy-v1 original_first_WIN7 "
          "second_to_move_LOSS")


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def d4_canon(hexstr: str) -> str:
    v = int(hexstr, 16)
    st = [i for i in range(121) if (v >> i) & 1]
    best = None
    for swap in (0, 1):
        for fx in (0, 1):
            for fy in (0, 1):
                t = []
                for c in st:
                    x, y = c % 11, c // 11
                    a, b = (y, x) if swap else (x, y)
                    if fx:
                        a = 10 - a
                    if fy:
                        b = 10 - b
                    t.append(a + 11 * b)
                w = 0
                for i in t:
                    w |= 1 << i
                h = format(w, "032x")
                if best is None or h < best:
                    best = h
    return best


def split_parts(whole: bytes, n: int, name_prefix: str):
    """Split whole into n parts at line boundaries, roughly equal."""
    cuts = []
    for i in range(1, n):
        target = len(whole) * i // n
        cut = whole.find(b"\n", target)
        assert cut != -1
        cuts.append(cut + 1)
    bounds = [0] + cuts + [len(whole)]
    parts = [whole[bounds[i]:bounds[i + 1]] for i in range(n)]
    for i, part in enumerate(parts, 1):
        assert part.endswith(b"\n")
        (CERTS / f"{name_prefix}part{i}of{n}").write_bytes(part)
    return parts


def main():
    sys.path.insert(0, str(SCRIPTS))
    from legal_candidates import legal_candidates
    certificates = []
    totals = {"published_certificates": 0, "rows": 0, "extraction_nodes": 0,
               "sub_roots": 0, "winner_states": 0, "loser_states": 0,
               "terminal_count": 0, "cert_bytes": 0}
    for bit in BITS:
        root = f"{CHILD_V | (1 << bit):032x}"
        raw = CERTS / f"bit{bit}-root-{root}.cert.part1of1"
        summary = json.loads((CERTS /
                             f"bit{bit}-root-{root}.cert.part1of1"
                             ".summary.json").read_text())
        assert summary["child"] == CHILD and summary["bit"] == bit
        assert summary.get("fatal") is None and summary["fbt_drops"] == 0
        assert summary["nMoves"] == len(summary["moves"]) > 0
        assert all(v["ok"] is True and v["capped"] is False
                   for v in summary["perMove"].values())
        st, moves = legal_candidates(root)
        assert len(st) == 7
        assert sorted(summary["moves"]) == sorted(moves), \
            "driver moves == legal_candidates(root) mobility"
        rows = raw.read_text().splitlines()
        rows = sorted(set(rows))
        assert len(rows) == summary["nRows"], \
            "raw rows are unique and match the driver count"
        whole = (HEADER + "\n" + f"root {root}\n" +
                 "\n".join(rows) + "\n").encode()
        whole_path = CERTS / f"bit{bit}-root-{root}.cert"
        whole_path.write_bytes(whole)
        # independent verifiers (both exit non-zero on any failure)
        ts = subprocess.run(
            ["node", "--experimental-strip-types",
             str(SCRIPTS / "verify_bit7_win7_cert.ts"),
             "--cert", str(whole_path), "--root", root, "--root-check",
             "--subroots", ",".join(map(str, summary["moves"]))],
            check=True, capture_output=True, text=True)
        ts_lines = [json.loads(x) for x in ts.stdout.splitlines() if x.strip()]
        rc = ts_lines[0]
        stats = ts_lines[1]
        assert rc == {"stones": 7, "loserMobility": len(moves)}, rc
        assert int(stats["rows"]) == len(rows)
        stats_keys = sorted(int(k[1:]) for k in stats["stats"])
        assert stats_keys == sorted(summary["moves"])
        seen = sum(v["seen"] for v in stats["stats"].values())
        terminals = sum(v["terminals"] for v in stats["stats"].values())
        ranges = [v["range"] for v in stats["stats"].values()]
        term_range = [min(r[0] for r in ranges), max(r[1] for r in ranges)]
        assert term_range == [13, 17], term_range
        bj = subprocess.run(
            ["node", str(SCRIPTS /
                         "verify_win7_certificate_bigint_independent.mjs"),
             str(whole_path), str(len(moves))],
            check=True, capture_output=True, text=True)
        bigint = json.loads(bj.stdout)
        assert bigint["verdict"] == "WIN7 certificate independently verified"
        assert bigint["union_missing"] == 0 and bigint["union_extra"] == 0
        assert bigint["subroots_passed"] == len(moves)
        assert bigint["root_hex"] == root
        assert bigint["root_stones"] == 7 and bigint["root_safe"] is True
        assert bigint["root_mobility"] == len(moves)
        assert bigint["strategy_rows"] == len(rows)
        assert bigint["rows_sorted_unique"] is True
        assert bigint["terminal_range"] == [13, 17]
        assert bigint["consumed_winner_rows"] == len(rows)
        # published-schema verify wrappers
        (CERTS / f"bit{bit}-root-{root}.bigint-verify.json").write_text(
            json.dumps({
                "schema": "n11-class2-lane-cost66c-bigint-verify-"
                          "20261116-v1",
                "bit_label": f"bit{bit}-root-{root}",
                "verifier": "verify_win7_certificate_bigint_independent.mjs "
                            "(BigInt 3x3 cofactor expansion; no solver/"
                            "verdict cache/repo import)",
                "bigint_record": bigint,
            }, indent=1) + "\n")
        bare = {
            "schema": "n11-class2-lane-cost66c-bareiss-verify-20261116-v1",
            "bit_label": f"bit{bit}-root-{root}",
            "verifier": "verify_bit7_win7_cert.ts --cert --root-check "
                        "--subroots (exact integer Bareiss 4x4 "
                        "determinants; independent of the BigInt verifier)",
            "root_check": rc,
            "subroots_verified": len(moves),
            "subroot_moves": summary["moves"],
            "rows": len(rows),
            "all_subroots_pass": True,
            "winner_states_seen_across_subroots": seen,
            "terminal_count": terminals,
            "terminal_range": term_range,
        }
        (CERTS / f"bit{bit}-root-{root}-bareiss-verify.json").write_text(
            json.dumps(bare, indent=1) + "\n")
        # split into N parts if over the publication split limit
        published = {
            "note": None, "bytes": len(whole),
            "md5": hashlib.md5(whole).hexdigest(),
            "sha256": hashlib.sha256(whole).hexdigest(),
            "git_blob_sha": git_blob_sha(whole),
            "path": "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/"
                    f"output/class2-lane-cost66c-certificates/"
                    f"bit{bit}-root-{root}.cert",
        }
        if len(whole) > SPLIT_LIMIT:
            n = -(-len(whole) // SPLIT_LIMIT)
            assert n >= 2
            name_prefix = f"bit{bit}-root-{root}.cert."
            parts = split_parts(whole, n, name_prefix)
            whole_path.unlink()
            receipt = {
                "schema": "n11-class2-lane-cost66c-cert-split-receipt-"
                          "20261116-v1",
                "cert": str(whole_path),
                "whole_bytes": len(whole),
                "whole_md5": hashlib.md5(whole).hexdigest(),
                "whole_sha256": hashlib.sha256(whole).hexdigest(),
                "whole_git_blob_sha": git_blob_sha(whole),
                "parts": [
                    {"path": "research/experiments/"
                             "n11-s2-5960-ms5-s7-reuse-20261113/output/"
                             "class2-lane-cost66c-certificates/"
                             f"bit{bit}-root-{root}.cert.part{i}of{n}",
                     "bytes": len(part),
                     "git_blob_sha": git_blob_sha(part),
                     "md5": hashlib.md5(part).hexdigest()}
                    for i, part in enumerate(parts, 1)
                ],
                "joined_equals_whole": True,
            }
            (CERTS / f"bit{bit}-root-{root}.cert-receipt.json").write_text(
                json.dumps(receipt, indent=1) + "\n")
            published = {
                "note": ("split at line boundaries into "
                         f"{n} parts (part1of{n}..part{n}of{n}) "
                         "(whole exceeds the 1,200,000-byte publication "
                         "split threshold: the 1.75 MiB repo per-file "
                         "convention and the ~1.2 MB practical single-push "
                         "transport limit of the publication tooling); "
                         "cat of the parts in order reproduces the whole "
                         "byte-exactly (see bit"
                         f"{bit}-root-{root}.cert-receipt.json)"),
                "whole_bytes": len(whole),
                "whole_md5": hashlib.md5(whole).hexdigest(),
                "whole_sha256": hashlib.sha256(whole).hexdigest(),
                "whole_git_blob_sha": git_blob_sha(whole),
                "parts": [
                    {"path": "research/experiments/"
                             "n11-s2-5960-ms5-s7-reuse-20261113/output/"
                             "class2-lane-cost66c-certificates/"
                             f"bit{bit}-root-{root}.cert.part{i}of{n}",
                     "bytes": len(part),
                     "git_blob_sha": git_blob_sha(part)}
                    for i, part in enumerate(parts, 1)
                ],
                "path": None,
            }
        else:
            published["note"] = ("single whole cert (under the 1.75 MiB "
                                 "repo per-file limit)")
        certificates.append({
            "bit": bit,
            "child_hex": CHILD,
            "root_hex": root,
            "d4_canonical_hex": d4_canon(root),
            "verdict": "WIN7",
            "sub_roots": len(moves),
            "root_mobility_matches_legal_candidates_py": True,
            "rows": len(rows),
            "extraction_nodes": summary["sum"],
            "fbt_drops": summary["fbt_drops"],
            "fatal": summary.get("fatal"),
            "terminal_range": term_range,
            "terminal_count": terminals,
            "winner_states": bigint["winner_states"],
            "loser_states": bigint["loser_states"],
            "published_cert": published,
            "bigint_verify": {
                "union_missing": bigint["union_missing"],
                "union_extra": bigint["union_extra"],
                "subroots_passed": bigint["subroots_passed"],
                "winner_states": bigint["winner_states"],
                "loser_states": bigint["loser_states"],
                "terminal_count": bigint["terminal_count"],
            },
            "bareiss_verify": {
                "subroots_verified": len(moves),
                "all_subroots_pass": True,
                "winner_states_seen_across_subroots": seen,
                "terminal_count": terminals,
            },
        })
        totals["published_certificates"] += 1
        totals["rows"] += len(rows)
        totals["extraction_nodes"] += summary["sum"]
        totals["sub_roots"] += len(moves)
        totals["winner_states"] += bigint["winner_states"]
        totals["loser_states"] += bigint["loser_states"]
        totals["terminal_count"] += terminals
        totals["cert_bytes"] += len(whole)
        print(f"bit{bit}: {len(rows)} rows / {summary['sum']} extraction "
              f"nodes / {len(moves)} sub-roots; BigInt union 0/0 + Bareiss "
              f"{len(moves)}/{len(moves)} PASS; "
              f"{'split parts' if len(whole) > SPLIT_LIMIT else 'whole cert'}"
              f" ({len(whole)} bytes)", flush=True)
    manifest = {
        "schema": "n11-class2-lane-cost66c-win7-certificates-20261116-v1",
        "date": "2026-11-16",
        "target": {
            "s6_child_hex": CHILD,
            "s5_parent": SH_PARENT,
            "protocol_anchor_s5_parent": PARENT_ANCHOR,
            "s5_parent_role": ("protocol parent containing the selected S6 "
                               "row (the single class-2 direct parent; the "
                               "other five one-stone-deletion parents are "
                               "closed orbits at head 1441)"),
            "direct_s5_parents": DIRECT_S5_PARENTS,
            "s6_s7_edge_cost": 66,
            "win7_d10_bits_certified_66c": BITS,
            "note": ("the seven cost-66c v16 WIN7-D10 receipts (bits 73, "
                     "75, 79, 87, 96, 97, 112 of the 59-bit sweep published "
                     "in class2-lane-cost66c-raw-batch1..8-20261116.jsonl; "
                     "bit 112 exceeded the 10000000-node protocol cap in "
                     "raw batch 7 and was resolved at the raised cap "
                     "80000000 as WIN7-D10 with 12574920 nodes, "
                     "determinism rerun node-exact; v15 crosscheck anchors "
                     "73 and 96 WIN and 30/83 REFUTED all agree) now have "
                     "published certificates; the 52 swept REFUTED-D10 "
                     "candidates and the 7 pre-sweep REFUTED-D10 transfers "
                     "have no certificate here (REFUTED is not a LOSS "
                     "proof). The row is NOT sterile; the fold of these "
                     "receipts follows the chain-reproduction protocol on "
                     "the then-current head after the in-flight cost-65n "
                     "fold lands, with a conflict census against the "
                     "folded-root corpus (and the cost-65o sweep corpus "
                     "once it lands) before the next ranking. Cross-row "
                     "watch item: 66c bit 83 REFUTED-D10 root canon "
                     "00000000000000a09002080080000000 is D4-identical to "
                     "the in-flight cost-65o claim's open bit 43 "
                     "candidate, so the cost-65o completion must record it "
                     "as a transfer or a WIN/LOSS conflict investigation"),
        },
        "extraction": {
            "engine": ("repo-verbatim class4_child1_cert_extractor_exact_"
                       "v16.ts driven by scripts/cert_driver65j.ts "
                       "(published generic single-root blind extraction "
                       "driver), empty kill table (blind extraction), "
                       "single chunk part1of1 per bit"),
            "chunking": ("rows sorted-unique (exact byte order); header and "
                         "root lines prepended; whole certs over the "
                         "1,200,000-byte publication split threshold are "
                         "split at line boundaries into N parts (N = "
                         "ceil(bytes/threshold), minimum 2) with a "
                         "receipt"),
        },
        "certificates": certificates,
        "totals": totals,
        "process_notes": [
            ("bit 97 re-extraction: the first extraction invocation of this "
             "session passed a moves list derived from a mis-transcribed "
             "root hex (the bit-85 root's 50-move mobility) while the "
             "repo-verbatim extractor derived the correct bit-97 root "
             "internally from (child, bit); the wrong-scope chunk and its "
             "summary were discarded before any publication and bit 97 was "
             "re-extracted with the correct 45-move mobility (the published "
             "summary and certificate are the re-extraction only; 31,205 "
             "rows / 1,364,577 nodes vs the discarded 41,636 / 3,295,492 "
             "wrong-scope figures)"),
            ("all hex values in this manifest are regenerated with "
             "format(..., '032x') and cross-checked against the published "
             "census bit table, never hand-copied"),
        ],
        "interpretation_guard": ("WIN7 certificates prove a first-player "
                                 "win within depth 10 from the individual "
                                 "7-stone roots only; 11x11 empty board / "
                                 "two-stone roots {49,60} and {59,60} / "
                                 "S2 {59,60} / class 1 / class 2 / "
                                 "class 4 remain UNKNOWN"),
    }
    (OUT / "class2-lane-cost66c-win7-certificates-20261116.json").write_text(
        json.dumps(manifest, indent=1) + "\n")
    print("written class2-lane-cost66c-win7-certificates-20261116.json")
    print("totals:", json.dumps(totals))


if __name__ == "__main__":
    main()
