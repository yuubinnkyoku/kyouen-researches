#!/usr/bin/env python3
"""Cross-lane agreement check: the presweep census v12 (published at
56d81b077362e71a2cb0ec232470b25c4fd06ca9, marking the cost-78c row swept as
its 15th verdict map and selecting the cost-79 runner-up as the next target)
versus the cost-78c sweep claim v5 (blob 1850832186ba9c8715624094f05d67aa4eb10f0b),
the in-band manifest (blob b7fe519e923c6170e836f71e3f084f73219319d5), and the
BigInt independent re-verification batch output published at
2d447098547c74d89b7d8147eeefe7c77fd4e4e7 (blob
7d97599186e6c76b8566d5f5703d71915224a129).

The census v12 was published BEFORE the BigInt batch (it cannot reference
it); this check closes that direction: every 78c fact the census relies on
(win/refuted bits, manifest totals, certificates-published statements) is
cross-agreed here against the BigInt-reverified bytes population. Follows
the check_cost73j/k cross-lane agreement pattern.

Determinism: no timestamps, fixed order, byte-identical on rerun.
11x11 empty board remains UNKNOWN; no row is closed by this check.
"""
import hashlib, json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
CENSUS = os.path.join(ROOT, "census12",
                      "class2-lane-next-target-presweep-1473-v12-20261118.json")
CENSUS_BLOB_SHA = "8e64d55250242a557c954ad5bad8c993bacd354b"
CLAIM = os.path.join(ROOT, "claim78c",
                     "class2-lane-cost78c-inflight-20261117.json")
CLAIM_BLOB_SHA = "1850832186ba9c8715624094f05d67aa4eb10f0b"
MINE = os.path.join(ROOT, "myoutput",
                    "class2-lane-cost78c-certificates-bigint-"
                    "independent-reverification-20261117.json")
MINE_BLOB_SHA = "7d97599186e6c76b8566d5f5703d71915224a129"
MANIFEST = os.path.join(ROOT, "certs78c",
                        "class2-lane-cost78c-win7-certificates-20261117.json")
MANIFEST_BLOB_SHA = "b7fe519e923c6170e836f71e3f084f73219319d5"
CHILD = "00000000000000403800000008000008"
PARENT = "00000000000000403800000008000000"
EXPECTED_BITS = [1, 4, 9, 30, 49, 69, 75, 79, 100, 114, 116]
OUT = os.path.join(ROOT, "class2-lane-cost78c-census-v12-cross-lane-"
                    "agreement-20261118.json")


def git_blob_sha(b):
    return hashlib.sha1(b"blob %d\x00" % len(b) + b).hexdigest()


def root_of_bit(bit):
    return f"{int(CHILD, 16) | (1 << bit):032x}"


def load(path, sha):
    b = open(path, "rb").read()
    assert git_blob_sha(b) == sha, ("blob sha mismatch", path)
    return json.loads(b)


def main():
    census = load(CENSUS, CENSUS_BLOB_SHA)
    claim = load(CLAIM, CLAIM_BLOB_SHA)
    mine = load(MINE, MINE_BLOB_SHA)
    manifest = load(MANIFEST, MANIFEST_BLOB_SHA)

    assert census["schema"] == ("n11-class2-lane-next-target-"
                               "presweep-1473-v12-20261118-v1")
    assert census["chain_head"] == claim["basis_head"].split(" ")[0], \
        census["chain_head"]
    assert census["chain_head"] == "1473/174/6375/504596/4648/368510"

    maps = census["new_verdict_maps"]
    assert len(maps) == 15, len(maps)
    assert list(maps)[-1] == "cost78c", list(maps)[-1]
    m78 = maps["cost78c"]
    assert m78["child"] == CHILD
    assert m78["bits"] == 78
    cw = sorted(m78["win7_d10_bits"])
    assert cw == sorted(EXPECTED_BITS), cw
    assert cw == sorted(claim["actual_execution"]["win7_d10_bits"])
    my_bits = sorted(e["bit"] for e in mine["entries"])
    assert my_bits == cw, my_bits
    cr = m78["refuted_d10_bits"]
    assert sorted(cr) == sorted(claim["actual_execution"]["refuted_d10_bits"])
    assert m78["capped"] == 0 == len(claim["actual_execution"]["capped_bits"])
    legal = claim["legal_candidates"]
    assert len(legal) == 78
    ws, rs, lg = set(cw), set(cr), set(legal)
    assert ws <= lg and rs <= lg and not (ws & rs) and ws | rs == lg
    # every BigInt-re-verified root is child | (1 << bit) of a census WIN bit
    for e in mine["entries"]:
        assert e["root_hex"] == root_of_bit(e["bit"]), ("root", e["bit"])
    assert len(mine["entries"]) == 11
    assert all(e["verifier_status"] == "PASS" for e in mine["entries"])
    assert all(e["manifest_record_agreement"] for e in mine["entries"])

    # totals: census cross_checks == manifest totals == claim v5 == my batch
    ct = census["cross_checks"]["78c_manifest_totals"]
    mt = manifest["totals"]
    kt = claim["certificates"]["totals"]
    assert ct["rows"] == mt["rows"] == kt["rows"] == 614003
    assert ct["extraction_nodes"] == mt["extraction_nodes"] == \
        kt["extraction_nodes"] == 77967826
    assert ct["published_bytes"] == mt["published_bytes"] == \
        kt["published_bytes"] == 22223603
    assert ct["fbt_drops_total"] == mt["fbt_drops_total"] == 0
    assert ct["capped_per_move_total"] == mt["capped_per_move_total"] == 0
    ms = mine["summary"]
    assert ms["total_rows_independently_verified"] == 614003
    assert ms["total_certificate_bytes_rehashed"] == 22223603
    assert ms["total_extraction_nodes_manifest_agreed"] == 77967826
    assert ms["records"] == 11 and ms["verifier_pass"] == 11
    assert census["cross_checks"]["78c_manifest_roots_are_child_or_bit"] is True
    assert census["cross_checks"]["78c_win_bits_claim_audit_manifest_agreement"] \
        == "11/11"
    assert census["cross_checks"]["78c_certificates"].startswith(
        "11/11 published (manifest git blob b7fe519e")
    assert census["cross_checks"]["78c_receipt_fold"].startswith(
        "pending behind the 66i/66j/69j/71e/72d/73i/73j/73k/73l folds")

    # next target: the census v11 runner-up selected for sweeping
    sel = census["selected_target"]
    assert sel["cost"] == 79
    assert sel["parent"] == PARENT
    assert sel["legal_candidates"] == 79
    assert len(sel["sweep_bits"]) + len(sel["confirmation_bits"]) == 79
    assert sel["runner_up"]["cost"] == 79
    assert "UNKNOWN" in census["interpretation_guard"]

    doc = {
        "schema": ("n11-class2-lane-cost78c-census-v12-cross-lane-"
                   "agreement-20261118-v1"),
        "date": "2026-11-18",
        "pins": {
            "census_v12": {
                "file": ("research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/"
                         "output/class2-lane-next-target-presweep-1473-v12-20261118.json"),
                "git_blob_sha": CENSUS_BLOB_SHA,
                "published_at": "56d81b077362e71a2cb0ec232470b25c4fd06ca9",
            },
            "claim_v5": {
                "file": ("research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/"
                         "output/class2-lane-cost78c-inflight-20261117.json"),
                "git_blob_sha": CLAIM_BLOB_SHA,
            },
            "bigint_batch": {
                "file": ("research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/"
                         "output/class2-lane-cost78c-certificates-bigint-"
                         "independent-reverification-20261117.json"),
                "git_blob_sha": MINE_BLOB_SHA,
                "published_at": "2d447098547c74d89b7d8147eeefe7c77fd4e4e7",
            },
            "manifest": {
                "file": ("research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/"
                         "output/class2-lane-cost78c-certificates/"
                         "class2-lane-cost78c-win7-certificates-20261117.json"),
                "git_blob_sha": MANIFEST_BLOB_SHA,
            },
        },
        "checks": {
            "chain_head": "census v12 chain_head == claim v5 basis_head == "
                          "1473/174/6375/504596/4648/368510",
            "verdict_map_position": "cost78c is the 15th (last) of the 15 "
                                    "new_verdict_maps",
            "win_bits_agreement": "census 78c win7_d10_bits == claim v5 "
                                  "win7_d10_bits == BigInt batch entry bits == "
                                  "[1,4,9,30,49,69,75,79,100,114,116]",
            "refuted_bits_agreement": "census 78c refuted_d10_bits == claim v5 "
                                      "refuted_d10_bits (67 bits), capped 0, "
                                      "win/refuted disjoint, union == the 78 "
                                      "legal_candidates",
            "totals_agreement": "census cross_checks 78c_manifest_totals == "
                                "manifest totals == claim v5 certificates."
                                "totals == BigInt batch summary "
                                "(rows 614003, extraction_nodes 77967826, "
                                "published_bytes 22223603, fbt_drops 0, "
                                "capped 0)",
            "bigint_roots_agreement": "all 11 BigInt-re-verified roots are "
                                      "child | (1 << win_bit), each "
                                      "verifier_status PASS and "
                                      "manifest_record_agreement True",
            "next_target": "selected_target cost 79 (the census v11 "
                           "runner-up), parent == the cost-78c s5 parent, "
                           "sweep_bits + confirmation_bits == legal_candidates "
                           "== 79",
        },
        "agreement": "PASS",
        "interpretation_guard": [
            "this check closes the agreement direction the census v12 could "
            "not reference (it was published before the BigInt batch); it "
            "creates no verdict, closes no row and changes no frontier "
            "number",
            "the census 78c verdict map carries REFUTED-D10 for 67 bits, "
            "which are NOT LOSS proofs of those roots",
            "11x11 empty board: UNKNOWN. Two-stone roots {49,60} and "
            "{59,60}: UNKNOWN. S2 {59,60}: UNKNOWN. Classes 1, 2 and 4: "
            "UNKNOWN",
        ],
    }
    with open(OUT, "w") as fh:
        json.dump(doc, fh, indent=1, sort_keys=False)
        fh.write("\n")
    print(json.dumps({"agreement": doc["agreement"],
                      "checks": len(doc["checks"])}))


if __name__ == "__main__":
    main()
