#!/usr/bin/env python3
"""Independent re-verification of the 34 published cost-58c class2-lane WIN7
certificates (output/class2-lane-cost58c-certificates/) with the BigInt
3x3-cofactor verifier (scripts/verify_win7_certificate_bigint_independent.mjs),
cross-checked per-bit against class-frontier-cost58c-receipts-recompute-20261116.json.

Run from the repo root of yuubinnkyoku/kyouen-researches at main
(or any checkout whose certificate bytes match the pinned git blob SHAs):
    python3 research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/reverify_cost58c_certificates_bigint_20261117.py

Steps (all asserted):
 1. glob the 34 .cert files; assert the exact file-name set;
 2. recompute each file's git blob SHA-1 (sha1("blob <size>\\0" + bytes)) and
    assert byte-exact match with the pinned blob SHAs published at main
    commit 0c486e53bb84c4418c9a6c89073cdc067a4172e8;
 3. run the BigInt independent verifier (node) on each file (4 workers);
 4. for the 33 folded bits assert verifier PASS and rows / full-file md5 /
    sub_roots_pass equality with the receipts-recompute per-bit records;
 5. for bit 76 assert verifier FAIL with the documented 13..17 terminal-range
    guard (the fold excluded bit 76 for exactly this reason);
 6. write the deterministic re-verification JSON to the output path.

Determinism: no timestamps, no wall times, sorted iteration; running twice
must produce byte-identical output.
11x11 empty board remains UNKNOWN; WIN7 certificates prove only individual
7-stone roots within depth 10.
"""
import concurrent.futures, glob, hashlib, json, os, subprocess, sys

EXP = "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113"
CERT_DIR = f"{EXP}/output/class2-lane-cost58c-certificates"
VERIFIER = f"{EXP}/scripts/verify_win7_certificate_bigint_independent.mjs"
RECOMP = f"{EXP}/output/class-frontier-cost58c-receipts-recompute-20261116.json"
OUT = f"{EXP}/output/class2-lane-cost58c-certificates-bigint-independent-reverification-20261117.json"
SOURCE_COMMIT = "0c486e53bb84c4418c9a6c89073cdc067a4172e8"
NODE = "node"

BLOB_SHAS = {
"bit1-root-00000000000000801206000040000002.cert":"48f9a81fa9e202b64df15bbcaf395af0df339b4f",
"bit102-root-00000040000000801206000040000000.cert":"6f708e96a46f99b44b709a2bceb79cc72850e457",
"bit103-root-00000080000000801206000040000000.cert":"9ec50a6ef84cdb89e9545f031afae54e9a6e1ead",
"bit105-root-00000200000000801206000040000000.cert":"0dc5876b076046e9016cd333936d7b269360dee1",
"bit109-root-00002000000000801206000040000000.cert":"3be2bcc8e8030c1132c7f16618ab7db394cc2b50",
"bit114-root-00040000000000801206000040000000.cert":"5e85b3c9329bf4f592633c54fe6853626b9b9720",
"bit116-root-00100000000000801206000040000000.cert":"db0dff0eafbedf8b9cf269560168a3720730fb51",
"bit117-root-00200000000000801206000040000000.cert":"91b2f28b6e05dc85070ca8b09bbdb62e3c40be76",
"bit118-root-00400000000000801206000040000000.cert":"c0adb1b6c70cde164340f005bb878f1d6c562e95",
"bit120-root-01000000000000801206000040000000.cert":"d9750cfacb76b96e86baa19702c213b5c637a5fb",
"bit18-root-00000000000000801206000040040000.cert":"1574f8ee29a7fab3829576427fbfa9124f4ee9b7",
"bit22-root-00000000000000801206000040400000.cert":"4a147c05d46c24899d51ffc0709eb52a250fe316",
"bit24-root-00000000000000801206000041000000.cert":"3351615260aad5a5ce1a2af9ed0f70fec73416ec",
"bit3-root-00000000000000801206000040000008.cert":"52ea10376ce7d460b2f19ad5f62c5b9ad8f8d947",
"bit32-root-00000000000000801206000140000000.cert":"addc09bfdf100d6ac81172b1e9bfffda84dfd17b",
"bit35-root-00000000000000801206000840000000.cert":"62a4f0bc057f2df60c1a2bb030f5743cacd06cc8",
"bit42-root-00000000000000801206040040000000.cert":"0c74492a5b3ee7df66addc2a573a9265e19de275",
"bit43-root-00000000000000801206080040000000.cert":"ca939085af52071e47ec31b2e23def154c347f32",
"bit44-root-00000000000000801206100040000000.cert":"1d053c0b6ddc7900d6c99688b7267b09839488b5",
"bit56-root-00000000000000801306000040000000.cert":"8e8f16c6aaa1bb7245d4ddf6aff0816ffb4837fc",
"bit6-root-00000000000000801206000040000040.cert":"97d3e87bcef47c2ae3192e6e9eef5d58cceabf1f",
"bit66-root-00000000000000841206000040000000.cert":"4eb42319eb0507e83e7ae672e240c45687fbc3c8",
"bit67-root-00000000000000881206000040000000.cert":"2df7c83b9423542247d691fe1ab938589103f835",
"bit73-root-00000000000002801206000040000000.cert":"3345347d351563115651976aabafddc40cdaa9a0",
"bit75-root-00000000000008801206000040000000.cert":"2a5046db7fc483565bf03e1790a76396ef130221",
"bit76-root-00000000000010801206000040000000.cert":"56af7a8f513bc3d2d0bef5521a808756c169ebfe",
"bit78-root-00000000000040801206000040000000.cert":"eda44f1ebc619a3138a74f1349f0342c61a427d9",
"bit79-root-00000000000080801206000040000000.cert":"b80df86f5da752402177e725ec64bf1eb25228f4",
"bit86-root-00000000004000801206000040000000.cert":"e55e2837ea21028d1439f8def2fd7948e233c867",
"bit88-root-00000000010000801206000040000000.cert":"31d1f4af18ba90b35ca0b3132e7842b7d0fa3c1c",
"bit89-root-00000000020000801206000040000000.cert":"c92a2cf9c90ead145c0524de6958b148d8ac7f33",
"bit91-root-00000000080000801206000040000000.cert":"f9a18a97242a0d99845516f6a8683bb469d32d1c",
"bit92-root-00000000100000801206000040000000.cert":"0f8e4d07e7a6ab13a82dc5953df06993de75282f",
"bit99-root-00000008000000801206000040000000.cert":"b529d78846f899541211dcafb9319be7e9824b46",
}
EXPECTED_BITS = [1,3,6,18,22,24,32,35,42,43,44,56,66,67,73,75,78,79,86,88,89,91,92,99,102,103,105,109,114,116,117,118,120]
FOLDED_TOTAL_ROWS = 1156691

def git_blob_sha(path):
    buf = open(path, "rb").read()
    h = hashlib.sha1()
    h.update(b"blob %d\0" % len(buf)); h.update(buf)
    return h.hexdigest(), len(buf), hashlib.md5(buf).hexdigest()

def run_verifier(path):
    p = subprocess.run([NODE, VERIFIER, path], capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr

def main():
    files = sorted(glob.glob(f"{CERT_DIR}/bit*.cert"))
    names = [os.path.basename(p) for p in files]
    assert names == sorted(BLOB_SHAS), f"cert set mismatch: {len(names)} files"
    recomp = json.load(open(RECOMP))
    add = {e["bit"]: e for e in recomp["cost58c_addition"]}
    assert sorted(add) == EXPECTED_BITS, "recompute addition bits mismatch"
    assert recomp["totals"]["receipts"] == 34

    blob_ok = 0
    entries = []
    for p in files:
        name = os.path.basename(p)
        bsha, nbytes, md5 = git_blob_sha(p)
        assert bsha == BLOB_SHAS[name], f"blob sha mismatch for {name}"
        blob_ok += 1
        bit = int(name.split("-")[0][3:])
        entries.append({"bit": bit, "path": p, "name": name,
                        "file_bytes": nbytes, "md5_full_file": md5})
    assert blob_ok == 34

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        results = list(ex.map(run_verifier, [e["path"] for e in entries]))
    for e, (rc, out, err) in zip(entries, results):
        if rc == 0:
            v = json.loads(out)
            assert v["verdict"] == "WIN7 certificate independently verified"
            assert v["root_stones"] == 7 and v["root_safe"] is True
            assert v["rows_sorted_unique"] is True
            assert v["union_missing"] == 0 and v["union_extra"] == 0
            assert v["root_hex"] in e["name"]
            e.update({
                "verifier_status": "PASS",
                "verifier_rows": v["strategy_rows"],
                "verifier_subroots_passed": v["subroots_passed"],
                "verifier_root_mobility": v["root_mobility"],
                "verifier_terminal_range": v["terminal_range"],
                "verifier_union_missing": v["union_missing"],
                "verifier_union_extra": v["union_extra"],
            })
        else:
            assert 'throw new Error("terminal range outside 13..17")' in err
            e.update({"verifier_status": "FAIL",
                      "verifier_error": "terminal range outside 13..17"})

    for e in entries:
        rec = add.get(e["bit"])
        if rec is not None:
            assert e["verifier_status"] == "PASS", f"bit {e['bit']} unexpectedly failed"
            assert e["verifier_rows"] == rec["rows"], f"rows mismatch bit {e['bit']}"
            assert e["md5_full_file"] == rec["md5"], f"md5 mismatch bit {e['bit']}"
            assert e["verifier_subroots_passed"] == rec["sub_roots_pass"], f"subroots mismatch bit {e['bit']}"
            e.update({"record_rows": rec["rows"], "record_md5": rec["md5"],
                      "record_sub_roots_pass": rec["sub_roots_pass"],
                      "rows_match": True, "md5_match": True, "sub_roots_match": True})
        else:
            assert e["bit"] == 76 and e["verifier_status"] == "FAIL", "unexpected unrecorded bit"
            e.update({"record_present_in_recompute": False,
                      "documented_exclusion": "class2-lane-cost58c-inflight-20261116.json fold: "
                      "bit76 excluded (certificate terminal range 11..17, rejected by the "
                      "BigInt verifier 13..17 guard); independently reproduced here"})

    passed = [e for e in entries if e["verifier_status"] == "PASS"]
    failed = [e for e in entries if e["verifier_status"] == "FAIL"]
    assert len(passed) == 33 and len(failed) == 1 and failed[0]["bit"] == 76
    total_rows = sum(e["verifier_rows"] for e in passed)
    assert total_rows == FOLDED_TOTAL_ROWS == recomp["totals"]["certificate_rows"]

    pub_entries = []
    for e in sorted(entries, key=lambda x: x["bit"]):
        pub_entries.append({k: e[k] for k in (
            "bit", "name", "root_hex_from_name", "file_bytes", "md5_full_file",
            "verifier_status", "verifier_rows", "verifier_subroots_passed",
            "verifier_root_mobility", "verifier_terminal_range",
            "verifier_union_missing", "verifier_union_extra",
            "record_rows", "record_md5", "record_sub_roots_pass",
            "rows_match", "md5_match", "sub_roots_match",
            "record_present_in_recompute", "documented_exclusion") if k in e})
        pub_entries[-1]["root_hex_from_name"] = e["name"][9:-5]

    doc = {
        "schema": "n11-class2-lane-cost58c-certificates-bigint-independent-reverification-20261117-v1",
        "date": "2026-11-17",
        "source_main_commit": SOURCE_COMMIT,
        "method": ("all 34 published cost-58c certificate files byte-checked against their pinned "
                   "git blob SHAs (sha1(\"blob <size>\\0\"+bytes)) at main commit " + SOURCE_COMMIT +
                   ", then independently verified with the published BigInt 3x3-cofactor verifier "
                   "(verify_win7_certificate_bigint_independent.mjs, no engine, no floating point); "
                   "the 33 folded bits cross-checked per-bit (strategy rows, full-file md5, "
                   "sub_roots_pass) against class-frontier-cost58c-receipts-recompute-20261116.json"),
        "certificates": {
            "dir": "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost58c-certificates",
            "files": 34, "total_bytes": sum(e["file_bytes"] for e in entries),
            "blob_sha_matches": 34,
        },
        "summary": {
            "verifier_pass": 33, "verifier_fail": 1,
            "fail_bit": 76, "fail_reason": "terminal range outside 13..17 guard (documented fold exclusion, independently reproduced)",
            "folded_bits_with_recompute_record": 33,
            "recompute_record_mismatch": 0,
            "total_rows_independently_verified": total_rows,
            "total_sub_roots_independently_verified": sum(e["verifier_subroots_passed"] for e in passed),
        },
        "bit76_note": ("bit 76 (root 00000000000010801206000040000000) is published in the "
                       "certificate folder but its certificate carries terminals at ply 11, "
                       "outside the WIN7-D10 window guard 13..17; the cost-58c fold already "
                       "excluded it from the 33 folded receipts for exactly this reason "
                       "(class2-lane-cost58c-inflight-20261116.json). Its exclusion is "
                       "independently reproduced here; no folded bookkeeping ever counted it."),
        "entries": pub_entries,
        "interpretation_guard": ("bookkeeping over published certificates; solved counts measure "
                                 "manifest coverage, not the game-theoretic value of any position; "
                                 "WIN7 certificates prove only individual 7-stone roots within depth 10"),
        "unknown_status": "11x11 empty board: UNKNOWN",
    }
    with open(OUT, "w") as f:
        json.dump(doc, f, indent=1)
        f.write("\n")
    print(f"wrote {OUT}: pass=33 fail=1(bit76, documented guard) rows={total_rows} mismatch=0")

if __name__ == "__main__":
    main()
