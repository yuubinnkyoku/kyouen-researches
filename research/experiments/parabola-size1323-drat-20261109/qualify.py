"""Bind selected certificates to the repaired encoding before any geometric claim."""
from __future__ import annotations
import argparse
import gzip
import hashlib
import json
from pathlib import Path
from corrected import encode, dimacs, SHAPES

HERE = Path(__file__).resolve().parent


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    if args.output.exists():
        raise FileExistsError("preserve prior qualification snapshots")
    source = HERE.parent/"parabola-hplus1-drat-20261109/input/verified_edges.txt.gz"
    edge_raw = gzip.decompress(source.read_bytes())
    edge_rows = edge_raw.decode("ascii").splitlines()
    assert list(map(int, edge_rows[0].split())) == [2647, 53886]
    edges = [tuple(map(int, line.split())) for line in edge_rows[1:]]
    records = []
    for key in SHAPES:
        location = HERE/"output"/("fixed" if key in ("000", "101") else "")/f"shape-{key}"
        record = {"class": key, "location": location.relative_to(HERE).as_posix(), "verified": False}
        if not (location/"init.json").exists():
            record["status"] = "NOT_STARTED"
            records.append(record)
            continue
        init = json.loads((location/"init.json").read_text())
        cnf = gzip.decompress((location/"input.cnf.gz").read_bytes())
        clauses, nv, base, _ = encode(2647, key, edges)
        assert dimacs(clauses, nv) == cnf, f"not the repaired class CNF: {key}"
        assert init["input_sha256"] == sha(cnf) and init["edge_input_sha256"] == sha(edge_raw)
        assert init["target_size"] == 1323 and init["origin_both_none"] == list(SHAPES[key])
        record.update(input_matches_repaired_encoder=True, input_sha256=sha(cnf), variables=nv, clauses=len(clauses))
        if not (location/"solver.json").exists():
            record["status"] = "GENERATION_PENDING_OR_INTERRUPTED"
            records.append(record)
            continue
        solver = json.loads((location/"solver.json").read_text())
        record["solver_status"] = solver["solver_status"]
        if solver["solver_status"] != "SOLVER_UNSAT" or not (location/"proof.drat.gz").exists():
            record["status"] = "PROOF_LOCAL_ONLY" if (location/"proof-manifest.json").exists() else "NO_UNSAT_PROOF"
            records.append(record)
            continue
        digest, lines = hashlib.sha256(), 0
        with gzip.open(location/"proof.drat.gz", "rb") as stream:
            for block in iter(lambda: stream.read(8*1024*1024), b""):
                digest.update(block)
                lines += block.count(b"\n")
        proof_sha = digest.hexdigest()
        assert proof_sha == solver["proof_sha256"] and lines == solver["proof_lines"]
        record.update(proof_sha256=proof_sha, proof_lines=solver["proof_lines"], status="AWAITING_CHECK")
        receipts = ([location/"audit.json"] if (location/"audit.json").exists() else [])
        receipts += sorted((HERE/"output").glob(f"recheck-{key}-*.json"))
        for receipt_path in receipts:
            audit = json.loads(receipt_path.read_text())
            assert audit["input_sha256"] == sha(cnf) and audit["proof_sha256"] == proof_sha
            assert audit["checker_source_sha256"] == "34249932790a9e9d924e9403b75563a2ff051277923301e34ace33e2a5a3650b"
            good = audit["verified"] is True and audit["returncode"] == 0 and audit["stdout"].splitlines()[-1:] == ["VERIFIED"]
            if good:
                record.update(verified=True, status="VERIFIED", accepted_receipt=receipt_path.relative_to(HERE).as_posix())
                break
            record["status"] = "CHECK_TIMEOUT" if audit.get("timed_out") else "CHECK_REJECTED"
        records.append(record)
    complete = all(r["verified"] for r in records)
    result = {"p": 2647, "excluded_size": 1323, "all_four_verified": complete,
              "independent_upper_bound": 1322 if complete else None, "records": records,
              "legacy_000_101": "INADMISSIBLE: selector/counter/point variable aliasing; not used above",
              "legacy_011_112": "May reuse only after byte equality with the repaired encoder, enforced above.",
              "scope": "Hash/encoding qualification of existing proof receipts, not a DRAT replay."}
    args.output.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
