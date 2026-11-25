#!/usr/bin/env python3
"""knowledge.yml audit-step byte-pin health scan.

Single-owner lane: research/log/2026-11-20-repo-pkg-bytepin-healthscan-single-owner-note.md.
Published-records-only: fetches the pinned knowledge.yml, every (verifier, audit.json)
pair registered as an audit step, and recomputes sha256(verifier) vs the audit's
self-referential verifier_sha256 field. No verifier re-runs, no math checks: this scan
detects CI-reproducibility breakage (the K1076/K1079 and K1078 failure mode), not
mathematical validity.

Usage:  python3 pkg_bytepin_healthscan_20261120.py <commit_sha> [out.json]
Output is a pure function of the pinned commit; two runs at the same pin
(including different cwd) must be byte-identical.
"""
import hashlib, json, re, sys, urllib.request

RAW = "https://raw.githubusercontent.com/yuubinnkyoku/kyouen-researches/{sha}/{path}"

def fetch(sha, path):
    url = RAW.format(sha=sha, path=path)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return r.read()
        except Exception:
            if attempt == 2:
                raise
    raise RuntimeError("unreachable")

def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: pkg_bytepin_healthscan_20261120.py <commit_sha> [out.json]")
    sha = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else "pkg-bytepin-healthscan-20261120.json"
    yml = fetch(sha, ".github/workflows/knowledge.yml").decode("utf-8")
    lines = yml.splitlines()
    pairs = []
    for i, ln in enumerate(lines):
        m = re.search(r"git diff --exit-code -- (\S+/output/audit\.json)", ln)
        if not m:
            continue
        audit_path = m.group(1)
        v = None
        # search backwards for the verifier invocation line of this step block
        for j in range(i - 1, max(i - 8, -1), -1):
            mv = re.search(r"python (\S+)\.py", lines[j])
            if mv:
                if "uv run" in lines[j] or "python3" in lines[j]:
                    v = mv.group(1) + ".py"
                    break
        pairs.append({"verifier": v, "audit": audit_path})
    results = []
    status_counts = {"match": 0, "mismatch": 0, "no-selfhash-field": 0, "fetch-error": 0, "unparsed-step": 0}
    for p in pairs:
        rec = dict(p)
        if not p["verifier"]:
            rec["status"] = "unparsed-step"
            status_counts[rec["status"]] += 1
            results.append(rec)
            continue
        try:
            vbytes = fetch(sha, p["verifier"])
            abytes = fetch(sha, p["audit"])
        except Exception as e:
            rec["status"] = "fetch-error"
            rec["error"] = repr(e)[:200]
            status_counts[rec["status"]] += 1
            results.append(rec)
            continue
        vsha = hashlib.sha256(vbytes).hexdigest()
        try:
            audit = json.loads(abytes.decode("utf-8"))
        except Exception as e:
            rec["status"] = "audit-parse-error"
            rec["error"] = repr(e)[:200]
            results.append(rec)
            continue
        claimed = None
        if isinstance(audit, dict):
            claimed = audit.get("verifier_sha256") or audit.get("verifier_sha")
        if claimed is None:
            rec["status"] = "no-selfhash-field"
            rec["verifier_sha256_actual"] = vsha
        elif claimed == vsha:
            rec["status"] = "match"
            rec["verifier_sha256"] = vsha
        else:
            rec["status"] = "mismatch"
            rec["verifier_sha256_actual"] = vsha
            rec["verifier_sha256_claimed"] = claimed
        status_counts[rec["status"]] = status_counts.get(rec["status"], 0) + 1
        results.append(rec)
    mismatches = [r for r in results if r["status"] == "mismatch"]
    out = {
        "schema": "repo-pkg-bytepin-healthscan-20261120-v1",
        "date": "2026-11-20",
        "scanned_commit": sha,
        "single_owner_note": "research/log/2026-11-20-repo-pkg-bytepin-healthscan-single-owner-note.md",
        "summary": {
            "audit_steps": len(pairs),
            "status_counts": status_counts,
            "mismatched_packages": [r["verifier"] for r in mismatches],
            "verdict": "byte-pin HEALTHSCAN: %d/%d packages consistent at this pin" % (
                status_counts["match"], len(pairs)),
        },
        "results": results,
        "interpretation_guard": [
            "A mismatch breaks the CI git-diff reproduction of that audit step; it does not by itself invalidate the mathematics of the published audit.",
            "Pin fixes belong to each package's owner lane. This scan performs no fixes.",
            "The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.",
        ],
    }
    blob = json.dumps(out, indent=1, sort_keys=True) + "\n"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(blob)
    print(json.dumps(out["summary"], ensure_ascii=False, indent=1))
    print("sha256:", hashlib.sha256(blob.encode()).hexdigest())

if __name__ == "__main__":
    main()
