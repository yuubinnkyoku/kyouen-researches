#!/usr/bin/env python3
"""WIN8 receipt provenance census: folds 11-25 (15 published receipts).

Read-only, deterministic machine. For each published WIN8 receipt fold
(receipt_ordinal eighteenth..thirty-second) this census fetches, from static
raw URLs pinned to one repository commit:

  (1) the receipt-fold JSON of the fold's own experiment dir,
  (2) the certificate `.n11` named by receipt `certificate_source.certificate_path`,
  (3) the verification JSON in the dir named by `certificate_source.record`
      (the fold's own certificate-extract dir),

classifies `receipts[0].independent_verification.source_record` as 'own'
(pointing at the fold's own certificate-extract dir) or 'stale', materializes
the classification by SHA-256 against the actually published bytes, and
checks the copy hypothesis (stale value == immediately preceding fold's
`independent_verification.source_record` value) across the published
sequence.

The machine performs NO game-tree computation, NO certificate verification,
NO row closure and NO modification of any record. A 'stale' classification is
a provenance report only, never a game-theoretic claim.

Fail-closed: any fetch failure, parse failure or structural gate failure
aborts with a non-zero exit and no output is written.
"""
import hashlib
import json
import re
import sys
import urllib.request

PIN = "32cb492c5b13bdab00f5bdad11de06391fcb1274"
RAW = "https://raw.githubusercontent.com/yuubinnkyoku/kyouen-researches/" + PIN + "/{}"

# (fold tag, receipt-fold experiment dir, receipt JSON file name).
# Universe fixed by the single-owner declaration note
# research/log/2026-11-21-n11-win8-receipt-source-record-census-single-owner-note.md
FOLDS = [
    ("fold11", "n11-residual72-win8-receipt-fold-root8003180-20261120", "win8-root8003180-receipt-fold-20261120.json"),
    ("fold12", "n11-residual68-win8-receipt-fold-root8005021-20261120", "win8-root8005021-receipt-fold-20261120.json"),
    ("fold13", "n11-residual65-win8-receipt-fold-root9840004-20261120", "win8-root9840004-receipt-fold-20261120.json"),
    ("fold14", "n11-residual62-win8-receipt-fold-root9090022-20261120", "win8-root9090022-receipt-fold-20261120.json"),
    ("fold15", "n11-residual58-win8-receipt-fold-root120000038-20261120", "win8-root120000038-receipt-fold-20261120.json"),
    ("fold16", "n11-residual55-win8-receipt-fold-root8890020-20261120", "win8-root8890020-receipt-fold-20261120.json"),
    ("fold17", "n11-residual51-win8-receipt-fold-root22081000-20261120", "win8-root22081000-receipt-fold-20261120.json"),
    ("fold18", "n11-residual48-win8-receipt-fold-root00901010-20261120", "win8-root00901010-receipt-fold-20261120.json"),
    ("fold19", "n11-residual41-win8-receipt-fold-root1009000-20261120", "win8-root1009000-receipt-fold-20261120.json"),
    ("fold20", "n11-residual38-win8-receipt-fold-root08d10000-20261120", "win8-root08d10000-receipt-fold-20261120.json"),
    ("fold21", "n11-residual35-win8-receipt-fold-root80880200-20261120", "win8-root80880200-receipt-fold-20261120.json"),
    ("fold22", "n11-residual32-win8-receipt-fold-root840500-20261120", "win8-root840500-receipt-fold-20261120.json"),
    ("fold23", "n11-residual29-win8-receipt-fold-root208090020004-20261120", "win8-root208090020004-receipt-fold-20261120.json"),
    ("fold24", "n11-residual29-win8-receipt-fold-root438000000818-20261120", "win8-root438000000818-receipt-fold-20261120.json"),
    ("fold25", "n11-residual26-win8-receipt-fold-root200003800200-20261120", "win8-root200003800200-receipt-fold-20261120.json"),
]

EXPECTED_ORDINALS = [
    "eighteenth", "nineteenth", "twentieth", "twenty-first", "twenty-second",
    "twenty-third", "twenty-fourth", "twenty-fifth", "twenty-sixth",
    "twenty-seventh", "twenty-eighth", "twenty-ninth", "thirtieth",
    "thirty-first", "thirty-second",
]

VERIF_NAME = "win8-cert-extract-verification-20261120.json"
REPO_PREFIX = "research/experiments/"

GUARD = ("Interpretation rules: REFUTED-D10 is not a LOSS proof. WIN8-D10 proves "
         "only the game tree of its root. Receipt folding is row-closure bookkeeping "
         "and claims no game-theoretic value for closed rows. pn/dn, node counts and "
         "solved counts are never read as win/loss. A stale source_record is a "
         "provenance recording defect only and does not affect the certificates or "
         "verifications themselves. The standard 11x11 empty board, the two-stone "
         "roots {49,60}/{59,60}, S2 {59,60} and classes 1/2/4 are all UNKNOWN.")

GATES = 0


def fail(msg):
    sys.stderr.write("FAIL-CLOSED: " + msg + "\n")
    sys.exit(1)


def gate(cond, msg):
    global GATES
    GATES += 1
    if not cond:
        fail(msg)


def fetch_bytes(repo_path):
    url = RAW.format(repo_path)
    try:
        with urllib.request.urlopen(url, timeout=120) as resp:
            if resp.status != 200:
                fail("HTTP %s for %s" % (resp.status, repo_path))
            return resp.read()
    except Exception as e:  # fetch failure is fail-closed by design
        fail("fetch error for %s: %r" % (repo_path, e))


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def root_hint(dir_name):
    m = re.search(r"cert-extract-root([0-9a-f]+)", dir_name)
    return m.group(1) if m else None


def main():
    records = []
    prev_iv_raw = None
    prev_own_dir = None
    own_dirs = []

    for (tag, rdir, rjson), ordinal in zip(FOLDS, EXPECTED_ORDINALS):
        receipt_path = REPO_PREFIX + rdir + "/output/" + rjson
        rb = fetch_bytes(receipt_path)
        receipt_sha = sha256(rb)
        try:
            d = json.loads(rb.decode("utf-8"))
        except Exception as e:
            fail("parse %s: %r" % (receipt_path, e))

        gate(d.get("receipt_ordinal", "").startswith(ordinal + " (fold"),
             "ordinal mismatch for %s: %r" % (tag, d.get("receipt_ordinal")))
        recs = d.get("receipts")
        gate(isinstance(recs, list) and len(recs) == 1,
             "receipts array not singleton for %s" % tag)
        r = recs[0]
        gate(r.get("verdict") == "WIN8-D10", "verdict not WIN8-D10 for %s" % tag)
        gate(r.get("stones") == 8, "stones != 8 for %s" % tag)
        root = r.get("root")
        gate(isinstance(root, str) and len(root) > 0
             and all(c in "0123456789abcdef" for c in root),
             "bad root for %s" % tag)
        gate(root == r.get("raw_root_hex"), "root/raw_root_hex mismatch for %s" % tag)

        cs = d.get("certificate_source")
        gate(isinstance(cs, dict), "certificate_source missing for %s" % tag)
        own_dir = cs.get("record", "").split(" ")[0]
        gate(own_dir.startswith(REPO_PREFIX),
             "certificate_source.record not a repo path for %s" % tag)
        own_dir_name = own_dir[len(REPO_PREFIX):]

        # material check (1): own-dir certificate bytes == receipt-pinned SHA-256
        cert_path = cs.get("certificate_path", "")
        gate(cert_path.startswith(REPO_PREFIX),
             "certificate_path not a repo path for %s" % tag)
        cb = fetch_bytes(cert_path)
        cert_sha = sha256(cb)
        cert_sha_match = (cert_sha == cs.get("certificate_sha256"))
        gate(cert_sha_match, "own-dir certificate SHA-256 mismatch for %s" % tag)

        # material check (2): own-dir verification JSON SHA-256
        verif_path = REPO_PREFIX + own_dir_name + "/output/" + VERIF_NAME
        vb = fetch_bytes(verif_path)
        verif_sha = sha256(vb)
        verif_sha_match = (verif_sha == cs.get("verification_sha256"))
        gate(verif_sha_match, "own-dir verification SHA-256 mismatch for %s" % tag)

        # provenance classification of IV.source_record
        iv_raw = r.get("independent_verification", {}).get("source_record", "")
        gate(iv_raw.startswith(REPO_PREFIX),
             "IV.source_record not a repo path for %s" % tag)
        iv_dir = iv_raw[len(REPO_PREFIX):] if iv_raw.startswith(REPO_PREFIX) else iv_raw
        iv_class = "own" if iv_dir == own_dir_name else "stale"

        records.append({
            "fold": tag,
            "receipt_ordinal": d.get("receipt_ordinal"),
            "root": root,
            "receipt_path": receipt_path,
            "receipt_sha256": receipt_sha,
            "covered_s6_rows_count": len(r.get("covered_s6_rows") or []),
            "covered_five_parent_target_rows_count": len(r.get("covered_five_parent_target_rows") or []),
            "extra_s6_rows_not_in_target_count": len(r.get("extra_s6_rows_not_in_target") or []),
            "certificate_bytes_receipt": r.get("certificate_bytes"),
            "certificate_block_sha256": r.get("certificate_sha256"),
            "own_dir": own_dir_name,
            "own_dir_root_hint": root_hint(own_dir_name),
            "own_dir_root_hint_matches_receipt_root_suffix":
                (root_hint(own_dir_name) is not None and root.endswith(root_hint(own_dir_name))),
            "own_dir_certificate_path": cert_path,
            "own_dir_certificate_bytes_fetched": len(cb),
            "own_dir_certificate_sha256": cert_sha,
            "own_dir_certificate_sha256_match": cert_sha_match,
            "own_dir_verification_path": verif_path,
            "own_dir_verification_sha256": verif_sha,
            "own_dir_verification_sha256_match": verif_sha_match,
            "iv_source_record_raw": iv_raw,
            "iv_dir": iv_dir,
            "iv_class": iv_class,
            "iv_dir_root_hint": root_hint(iv_dir),
            "iv_dir_root_hint_matches_receipt_root_suffix":
                (root_hint(iv_dir) is not None and root.endswith(root_hint(iv_dir))),
            "iv_equals_previous_fold_iv":
                (None if prev_iv_raw is None else (prev_iv_raw == iv_raw)),
            "iv_dir_equals_previous_fold_own_dir":
                (None if prev_own_dir is None else (iv_dir == prev_own_dir)),
        })
        own_dirs.append(own_dir_name)
        prev_iv_raw = iv_raw
        prev_own_dir = own_dir_name

    # cross-fold pass: universe membership of every referenced dir
    universe_dirs = sorted(set(own_dirs))
    for rec in records:
        rec["iv_dir_in_universe"] = rec["iv_dir"] in universe_dirs
        rec["own_dir_is_current_fold_receipt_dir"] = False  # by construction differs (receipt dir vs cert-extract dir)

    stale = [rec for rec in records if rec["iv_class"] == "stale"]
    summary = {
        "receipts_total": len(records),
        "iv_own_count": len(records) - len(stale),
        "iv_stale_count": len(stale),
        "iv_stale_folds": [rec["fold"] for rec in stale],
        "stale_all_equal_previous_fold_iv":
            all(rec["iv_equals_previous_fold_iv"] is True for rec in stale),
        "stale_all_dir_equals_previous_fold_own_dir":
            all(rec["iv_dir_equals_previous_fold_own_dir"] is True for rec in stale),
        "iv_dirs_all_in_universe":
            all(rec["iv_dir_in_universe"] for rec in records),
        "own_dir_certificate_sha256_match_count":
            sum(1 for rec in records if rec["own_dir_certificate_sha256_match"]),
        "own_dir_verification_sha256_match_count":
            sum(1 for rec in records if rec["own_dir_verification_sha256_match"]),
        "certificate_source_blocks_correct_count":
            sum(1 for rec in records if rec["own_dir_certificate_sha256_match"]
                and rec["own_dir_verification_sha256_match"]),
        "own_dir_certificate_bytes_match_certificate_bytes_receipt_count":
            sum(1 for rec in records
                if rec["own_dir_certificate_bytes_fetched"] == rec["certificate_bytes_receipt"]),
        "own_dir_root_hint_suffix_match_count":
            sum(1 for rec in records if rec["own_dir_root_hint_matches_receipt_root_suffix"]),
        "iv_dir_root_hint_suffix_match_count":
            sum(1 for rec in records if rec["iv_dir_root_hint_matches_receipt_root_suffix"]),
        "structural_gates_passed": GATES,
    }

    census = {
        "census": "n11-win8-receipt-source-record-census-20261121",
        "machine": "win8_receipt_source_record_census.py",
        "repo_head_pin": PIN,
        "single_owner_note": "research/log/2026-11-21-n11-win8-receipt-source-record-census-single-owner-note.md",
        "mode": ("read-only provenance census (no game-tree computation, no "
                 "certificate verification, no row closure, no record modification)"),
        "universe": {
            "receipt_experiment_dirs": {f[0]: f[1] for f in FOLDS},
            "own_certificate_extract_dirs": {rec["fold"]: rec["own_dir"] for rec in records},
        },
        "receipts": records,
        "summary": summary,
        "interpretation_guard": GUARD,
    }

    out = json.dumps(census, indent=2, ensure_ascii=False) + "\n"
    with open("output/census.json", "w", encoding="utf-8") as f:
        f.write(out)
    print("census written: %d receipts, %d gates, stale folds: %s"
          % (len(records), GATES, summary["iv_stale_folds"]))


if __name__ == "__main__":
    main()
