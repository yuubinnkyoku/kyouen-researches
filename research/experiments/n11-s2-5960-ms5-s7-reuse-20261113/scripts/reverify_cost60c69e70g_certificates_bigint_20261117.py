#!/usr/bin/env python3
"""Independent bytes re-verification of the published cost-60c / cost-69e /
cost-70g class2-lane WIN7 certificates (2026-11-17).

Follow-up to the head-1452 receipt-certificate coverage census (v3, 775/775
certified, tier R 525): the 58c (33) and warm/multiband (82) records were
already bytes-re-verified; this script upgrades three more receiptcert-only
bands - cost-60c (1 cert), cost-69e (10 certs, bit 116 published as
base64(gzip-9)), cost-70g (8 certs) - by re-checking the published bytes
against the manifest pins and re-running the independent BigInt 3x3-cofactor
verifier (verify_win7_certificate_bigint_independent.mjs, git blob
62b5d9413daafb172f6e10249976ee6808f7b454) on every certificate.

Checks per band (all asserted):
- cost-60c: git blob SHA + whole-file md5/sha256 equality with the manifest
  (class2-lane-cost60c-win7-certificates-20261116.json), verifier PASS with
  rows/sub-roots/terminal/winner/loser equality.
- cost-69e: whole-file md5/sha256 equality with the manifest
  (class2-lane-cost69e-win7-certificates-20261114.json); bit 116 restored via
  base64 -d | gunzip with gz_b64_md5 + uncompressed md5/sha256/bytes/lines
  equality before verification; verifier PASS with rows/sub-roots/mobility
  equality for all 10.
- cost-70g: git blob SHA equality with the per-cert repo_blob_sha pins
  (class2-lane-cost70g-win7-certificates-20261115.json), verifier PASS with
  rows/mobility/sub-roots/terminal/visited/edges equality for all 8.

Determinism: no timestamps, sorted iteration; running twice must produce
byte-identical output.
Interpretation guard: bookkeeping and certificate verification only; the
WIN7-D10 certificates prove first-player wins within depth 10 for the
individual 7-stone roots only; 11x11 empty board, two-stone roots
{49,60}/{59,60}, S2 {59,60} and classes 1/2/4 remain UNKNOWN.
"""
import base64
import concurrent.futures
import gzip
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
VERIFIER = HERE / "scripts" / "verify_win7_certificate_bigint_independent.mjs"
NODE = "node"
SOURCE_COMMIT = "0b81d0d1763a218caae22f867612b1919eec4f38"
VERIFIER_BLOB = "62b5d9413daafb172f6e10249976ee6808f7b454"

M60C = {
    "bit": 92,
    "name": "bit92-root-00000000100000003800000008008020.cert",
    "root": "00000000100000003800000008008020",
    "blob": "b35128897b07f03e4baa11583423453cb378e18d",
    "md5": "d771ef8275a9889a22974310e5c1e411",
    "sha256": "33fcd4853b874f88d44a7c0e7a2f0d48c9d96dadf12eaad4bf6b27a3eebf31d9",
    "bytes": 996758,
    "rows": 27547,
    "sub_roots": 45,
    "terminal_count": 8543,
    "winner_states": 38090,
    "loser_states": 12028,
}
# bit -> (root, md5, sha256, rows, sub_roots, mobility)
M69E = {
    21: ("00000000000000803202000000208000", "b229fe7c0c96901fe04ddf05763ffb9e", "8c730b8880f9734d5cc156b19a5b9c62484ba4ffea49494eb5913ae3d4d84203", 22261, 45, 45),
    99: ("00000008000000803202000000008000", "69f5fae13d3c712df7b2883ec79d7c2a", "62172344421d73a12dbe71a1efd735dd7899f031d1d3638af30139762ba096dc", 25149, 50, 50),
    87: ("00000000008000803202000000008000", "5f5063233ff919b704e01a105e1fb132", "a5ee200e72bb7b0fa15b128805de9391092d6fb21c9f8a49aaa66418ef23e7bd", 43838, 59, 59),
    84: ("00000000001000803202000000008000", "41adac3c1d684d4b4dde25c416c2ae20", "9540dee4c8b213e9b659e3af6e88e0730a81fd6f56ef09b497e97ea28a137133", 29614, 50, 50),
    76: ("00000000000010803202000000008000", "2358870d7a2625b4d40a0c178f8cba66", "ea9f04da58b67801b5c98cec0bb2150a96dba8e00a5d3fd79876b863233bb4ee", 45665, 57, 57),
    90: ("00000000040000803202000000008000", "b0e6f779b229ef4993c8715691db7ede", "a86f492ec972d5c7458c99dcd6a1ac06758cfd333c26e90d671fbc7f274a5c5c", 46959, 58, 58),
    89: ("00000000020000803202000000008000", "1e2c8db6cd9303fcf0167f59ccb83bae", "0399eb05cf207eb8e40218f344d4707f629bf07f6bd352e89de37f81e95bc47a", 47035, 54, 54),
    94: ("00000000400000803202000000008000", "4dc6076b96edc3a472b4b23f38739451", "9edda222d3b5bb25a94a497043a670a85141cb19f5b09ae9a892aa50ce81ca74", 42538, 52, 52),
    108: ("00001000000000803202000000008000", "74d071466140e1b0a48b67134431a570", "be2fb2ee178b3aca96fabceffaf30ac6b9bc44fbd9d8f3e76f8e2059c29dcadb", 33942, 51, 51),
    116: ("00100000000000803202000000008000", None, None, 74113, 59, 59),
}
M69E_116 = {
    "gz_b64_md5": "9aa8925c2f08857a92be67dc7f4f7ed4",
    "uncompressed_md5": "691140486067132237d8c11d93a12559",
    "uncompressed_sha256": "20c0f5edf05f9f45cd0e5d3331a22ec3a39ac001b28428a51d79eefda4498159",
    "uncompressed_bytes": 2670116,
    "uncompressed_lines": 74115,
}
# bit -> (root, blob, rows, mobility, sub, terminal, visited, edges)
M70G = {
    9: ("00000000000100809002000000000a00", "1877c1c6d07a458b6daa53e56338cffc941c2a5a", 51456, 60, 60, 15885, 102474, 92383),
    20: ("00000000000100809002000000100800", "b2a83239066c35944c281823b9b3ebb77f94815e", 16902, 46, 46, 5695, 38438, 35277),
    29: ("00000000000100809002000020000800", "bab4338b0a17ca93425f4e846d3e0995efa71f99", 44195, 54, 54, 14967, 99654, 91511),
    34: ("00000000000100809002000400000800", "e95fcaf5becc9dadacd9c382c57b1faaf395d8b6", 56345, 63, 63, 17849, 115931, 104901),
    62: ("0000000000010080d002000000000800", "1c023a37bebd87ca3a5a86dc39663e743d1d66fa", 26591, 51, 51, 8166, 56806, 52248),
    70: ("00000000000100c09002000000000800", "d522d9ebcddd30483eaa2ee60f24a1cee8e1273e", 19456, 49, 49, 6618, 45395, 41826),
    76: ("00000000000110809002000000000800", "63a6c8b4667ae8a96086d986607891716a021477", 45917, 55, 55, 14094, 97634, 90276),
    119: ("00800000000100809002000000000800", "b5a4297977595a6f11ef21995135f4b2cbe31b78", 41408, 56, 56, 14119, 89094, 79274),
}


def digests(buf):
    return {
        "md5": hashlib.md5(buf).hexdigest(),
        "sha256": hashlib.sha256(buf).hexdigest(),
        "git_blob_sha": hashlib.sha1(b"blob %d\0" % len(buf) + buf).hexdigest(),
        "bytes": len(buf),
    }


def run_verifier(path):
    p = subprocess.run([NODE, str(VERIFIER), str(path)], capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def main():
    checks = []
    ok = True

    def check(name, cond, detail=None):
        nonlocal ok
        checks.append({"check": name, "pass": bool(cond),
                       "detail": detail if detail else ("" if cond else "FAILED")})
        if not cond:
            ok = False

    check("verifier_blob_sha_matches_pinned_62b5d941",
          digests(VERIFIER.read_bytes())["git_blob_sha"] == VERIFIER_BLOB)

    entries = []  # (band, bit, path, expected dict)

    # ---- cost-60c ----
    d60 = OUT / "class2-lane-cost60c-certificates"
    p = d60 / M60C["name"]
    buf = p.read_bytes()
    g = digests(buf)
    check("60c_bit92_blob_sha_matches_manifest", g["git_blob_sha"] == M60C["blob"])
    check("60c_bit92_md5_matches_manifest", g["md5"] == M60C["md5"])
    check("60c_bit92_sha256_matches_manifest", g["sha256"] == M60C["sha256"])
    check("60c_bit92_bytes_match_manifest", g["bytes"] == M60C["bytes"])
    entries.append(("cost60c", 92, p, {
        "root": M60C["root"], "rows": M60C["rows"], "sub_roots": M60C["sub_roots"],
        "terminal_count": M60C["terminal_count"], "winner_states": M60C["winner_states"],
        "loser_states": M60C["loser_states"], "storage": "plain text single file",
        "published": {"git_blob_sha": g["git_blob_sha"], "md5": g["md5"],
                       "sha256": g["sha256"], "bytes": g["bytes"]}}))

    # ---- cost-69e ----
    d69 = OUT / "class2-lane-cost69e-certificates"
    for bit in sorted(M69E):
        root, md5, sha, rows, sub, mob = M69E[bit]
        if bit == 116:
            pgz = d69 / f"bit116-root-{root}.cert.gz.b64"
            gzbuf = pgz.read_bytes()
            ggz = digests(gzbuf)
            check("69e_bit116_gzb64_md5_matches_manifest",
                  ggz["md5"] == M69E_116["gz_b64_md5"])
            raw = gzip.decompress(base64.b64decode(gzbuf))
            graw = digests(raw)
            check("69e_bit116_uncompressed_md5_matches_manifest",
                  graw["md5"] == M69E_116["uncompressed_md5"])
            check("69e_bit116_uncompressed_sha256_matches_manifest",
                  graw["sha256"] == M69E_116["uncompressed_sha256"])
            check("69e_bit116_uncompressed_bytes_match_manifest",
                  graw["bytes"] == M69E_116["uncompressed_bytes"])
            lines = raw.decode().splitlines()
            check("69e_bit116_uncompressed_lines_match_manifest",
                  len(lines) == M69E_116["uncompressed_lines"])
            tmp = d69 / f".tmp-bit116-root-{root}.cert"
            tmp.write_bytes(raw)
            entries.append(("cost69e", 116, tmp, {
                "root": root, "rows": rows, "sub_roots": sub, "mobility": mob,
                "storage": "base64(gzip -9) published; restored in-memory for verification",
                "published": {"gz_b64_md5": ggz["md5"], "gz_b64_bytes": ggz["bytes"],
                              "uncompressed_md5": graw["md5"],
                              "uncompressed_sha256": graw["sha256"],
                              "uncompressed_bytes": graw["bytes"],
                              "uncompressed_lines": len(lines)}}))
        else:
            p = d69 / f"bit{bit}-root-{root}.cert"
            buf = p.read_bytes()
            g = digests(buf)
            check(f"69e_bit{bit}_md5_matches_manifest", g["md5"] == md5)
            check(f"69e_bit{bit}_sha256_matches_manifest", g["sha256"] == sha)
            entries.append(("cost69e", bit, p, {
                "root": root, "rows": rows, "sub_roots": sub, "mobility": mob,
                "storage": "plain text single file",
                "published": {"git_blob_sha": g["git_blob_sha"], "md5": g["md5"],
                               "sha256": g["sha256"], "bytes": g["bytes"]}}))

    # ---- cost-70g ----
    d70 = OUT / "class2-lane-cost70g-certificates"
    for bit in sorted(M70G):
        root, blob, rows, mob, sub, term, visited, edges = M70G[bit]
        p = d70 / f"bit{bit}-root-{root}.cert"
        g = digests(p.read_bytes())
        check(f"70g_bit{bit}_blob_sha_matches_manifest", g["git_blob_sha"] == blob)
        entries.append(("cost70g", bit, p, {
            "root": root, "rows": rows, "mobility": mob, "sub_roots": sub,
            "terminal_count": term, "visited_states": visited,
            "loser_reply_edges": edges, "storage": "plain text single file",
            "published": {"git_blob_sha": g["git_blob_sha"], "md5": g["md5"],
                          "sha256": g["sha256"], "bytes": g["bytes"]}}))

    # ---- run the BigInt verifier on all certificates (4 workers) ----
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        results = list(ex.map(run_verifier, [e[2] for e in entries]))

    per_cert = []
    for (band, bit, path, exp), (rc, stdout, stderr) in zip(entries, results):
        rec = {"band": band, "bit": bit, "root_hex": exp["root"],
               "expected_rows": exp["rows"], "storage": exp["storage"],
               "published": exp["published"]}
        if rc != 0:
            rec["verifier_status"] = "FAIL"
            rec["error"] = (stderr or stdout).strip()[:400]
            check(f"{band}_bit{bit}_verifier_pass", False, rec["error"])
            per_cert.append(rec)
            continue
        v = json.loads(stdout)
        fields_ok = (
            v["verdict"] == "WIN7 certificate independently verified"
            and v["root_hex"] == exp["root"]
            and v["root_stones"] == 7
            and v["root_safe"] is True
            and v["rows_sorted_unique"] is True
            and v["union_missing"] == 0
            and v["union_extra"] == 0
            and v["strategy_rows"] == exp["rows"]
            and v["subroots_passed"] == exp["sub_roots"]
            and v["terminal_range"] == [13, 17]
            and (exp.get("mobility") is None or v["root_mobility"] == exp["mobility"])
            and (exp.get("terminal_count") is None or v["terminal_count"] == exp["terminal_count"])
            and (exp.get("winner_states") is None or v["winner_states"] == exp["winner_states"])
            and (exp.get("loser_states") is None or v["loser_states"] == exp["loser_states"])
            and (exp.get("visited_states") is None or v["visited_states_across_subroots"] == exp["visited_states"])
            and (exp.get("loser_reply_edges") is None or v["loser_reply_edges"] == exp["loser_reply_edges"])
        )
        check(f"{band}_bit{bit}_verifier_pass_with_manifest_stats", fields_ok)
        rec.update({
            "verifier_status": "PASS" if fields_ok else "STATS_MISMATCH",
            "verifier": {k: v[k] for k in (
                "root_mobility", "strategy_rows", "subroots_passed",
                "union_missing", "union_extra", "winner_states", "loser_states",
                "loser_reply_edges", "terminal_count", "terminal_range",
                "visited_states_across_subroots")},
        })
        per_cert.append(rec)

    # clean up the temporary restored 69e bit116 file
    tmp116 = OUT / "class2-lane-cost69e-certificates" / f".tmp-bit116-root-{M69E[116][0]}.cert"
    if tmp116.exists():
        tmp116.unlink()

    total_rows = sum(r["expected_rows"] for r in per_cert)
    n_pass = sum(1 for r in per_cert if r["verifier_status"] == "PASS")
    result = {
        "schema": "n11-class2-lane-cost60c69e70g-certificates-bigint-reverification-20261117-v1",
        "date": "2026-11-17",
        "source_commit": SOURCE_COMMIT,
        "method": ("published certificate bytes re-checked against the band manifest pins "
                   "(git blob SHA / md5 / sha256; bit 116 restored from base64(gzip-9) with "
                   "in-memory round-trip digest equality) and every certificate re-run "
                   "through verify_win7_certificate_bigint_independent.mjs (BigInt 3x3 "
                   "cofactor expansion, no solver/verdict-cache import); 4 workers"),
        "verifier_blob_sha": VERIFIER_BLOB,
        "bands": {
            "cost60c": {"certificates": 1, "manifest": "class2-lane-cost60c-win7-certificates-20261116.json"},
            "cost69e": {"certificates": 10, "manifest": "class2-lane-cost69e-win7-certificates-20261114.json"},
            "cost70g": {"certificates": 8, "manifest": "class2-lane-cost70g-win7-certificates-20261115.json"},
        },
        "certificates_checked": len(per_cert),
        "verifier_pass": n_pass,
        "total_strategy_rows": total_rows,
        "per_certificate": per_cert,
        "checks": checks,
        "all_checks_pass": ok,
        "interpretation_guard": ("bytes and verifier re-check of published WIN7-D10 "
            "certificates only; they prove first-player wins within depth 10 for the "
            "individual 7-stone roots only; REFUTED-D10 is not a LOSS proof; 11x11 empty "
            "board, two-stone roots {49,60}/{59,60}, S2 {59,60} and classes 1/2/4 remain "
            "UNKNOWN"),
    }
    dest = OUT / "class2-lane-cost60c69e70g-certificates-bigint-reverification-20261117.json"
    with open(dest, "w") as f:
        json.dump(result, f, indent=1, sort_keys=True)
        f.write("\n")
    print("checks:", len(checks), "all pass:", ok)
    print("certs", len(per_cert), "pass", n_pass, "rows", total_rows)
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
