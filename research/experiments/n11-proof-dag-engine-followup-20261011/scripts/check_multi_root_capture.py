"""Small end-to-end check for proof capture across shared replay roots."""
import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[2] / "n11-proof-dag-engine-20261011" / "scripts"
sys.path.insert(0, str(SCRIPTS))
from dag_verifier import verify_certificate  # noqa: E402
from trace_to_certificate import trace_to_certificate  # noqa: E402
from verify_shared_bundle import verify_trace  # noqa: E402


def read_replays(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return [row for row in csv.reader(stream) if row and row[0] == "replay"]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--solver", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    solver, out = args.solver.resolve(), args.out.resolve()
    if not solver.is_file() or out.exists():
        ap.error("solver must exist and output directory must be new")
    out.mkdir(parents=True)
    replay_input = out / "duplicate-s0.csv"
    replay_input.write_text(
        "first,0,0,0,0,16,0,1,0,0,0\n"
        "second,1,0,0,0,16,0,1,0,0,0\n", encoding="utf-8")
    trace_dir = out / "shared-traces"
    raw = out / "shared-raw.csv"
    command = [str(solver), "--n=4", "--memo=16",
               f"--exact-replay={replay_input}", "--only=0",
               "--exact-order=count", "--exact-replay-budget=100000",
               "--exact-replay-share-tt", f"--proof-dag-dir={trace_dir}",
               f"--csv={raw}"]
    subprocess.run(command, check=True, capture_output=True, text=True)
    rows = read_replays(raw)
    if len(rows) != 2 or any(len(row) != 11 or int(row[6]) != 2 for row in rows):
        raise AssertionError(f"small shared replay did not prove both LOSS roots: {rows}")
    if int(rows[1][7]) != 0:
        raise AssertionError(f"duplicate second root missed the shared TT: {rows[1]}")
    trace = trace_dir / "proof-bundle.csv"
    if not trace.is_file():
        raise AssertionError("shared roots did not produce one proof-bundle trace")
    cert, receipt = verify_trace(trace)
    if len(receipt["roots"]) != 2 or receipt["trusted_leaves"] != 0:
        raise AssertionError(f"independent bundle verifier rejected shared trace: {receipt}")
    # Cross-check the small fixture root-by-root with the established verifier.
    receipts = []
    for root in cert["roots"]:
        reachable, pending = set(), [root["root"]]
        while pending:
            ident = pending.pop()
            if ident in reachable:
                continue
            reachable.add(ident)
            pending.extend(edge["child"] for edge in cert["nodes"][ident]["edges"])
        single = {"schema": "kyouen-proof-dag-edge-v1", "board_size": 4,
                  "proposition": "original_first_player_wins", "root": root["root"],
                  "nodes": {ident: cert["nodes"][ident] for ident in reachable}}
        single_receipt = verify_certificate(single)
        if single_receipt["verdict"] != 2 or single_receipt["trusted_leaves"] != 0:
            raise AssertionError(f"existing verifier disagreed on shared root: {single_receipt}")
        receipts.append(single_receipt)

    # Preserve the original single-root --proof-dag wire format and path.
    single_input = out / "single-s0.csv"
    single_input.write_text("single,0,0,0,0,16,0,1,0,0,0\n", encoding="utf-8")
    single_trace = out / "single-proof.csv"
    single_raw = out / "single-raw.csv"
    single_command = [str(solver), "--n=4", "--memo=16",
                      f"--exact-replay={single_input}", "--only=0",
                      "--exact-order=count", "--exact-replay-budget=100000",
                      f"--proof-dag={single_trace}", f"--csv={single_raw}"]
    subprocess.run(single_command, check=True, capture_output=True, text=True)
    single_rows = read_replays(single_raw)
    single_certificate, _ = trace_to_certificate(single_trace, 4, 0, 2)
    single_receipt = verify_certificate(single_certificate)
    if len(single_rows) != 1 or int(single_rows[0][6]) != 2 or single_receipt["trusted_leaves"] != 0:
        raise AssertionError("legacy single-root proof capture regressed")

    # A one-node budget must produce UNKNOWN and no certificate file.
    cutoff_input = out / "cutoff-s0.csv"
    cutoff_input.write_text("cutoff,0,0,0,0,16,0,1,0,0,0\n", encoding="utf-8")
    cutoff_dir, cutoff_raw = out / "cutoff-traces", out / "cutoff-raw.csv"
    cutoff_command = [str(solver), "--n=4", "--memo=16",
                      f"--exact-replay={cutoff_input}", "--only=0",
                      "--exact-replay-budget=1", "--exact-replay-share-tt",
                      f"--proof-dag-dir={cutoff_dir}", f"--csv={cutoff_raw}"]
    subprocess.run(cutoff_command, check=True, capture_output=True, text=True)
    cutoff_rows = read_replays(cutoff_raw)
    if len(cutoff_rows) != 1 or int(cutoff_rows[0][6]) != 0:
        raise AssertionError(f"budget cutoff did not remain UNKNOWN: {cutoff_rows}")
    if (cutoff_dir / "proof-bundle.csv").exists():
        raise AssertionError("UNKNOWN replay emitted a proof trace")

    result = {"schema": "n11-multi-root-capture-small-check-v1",
              "board_size": 4, "duplicate_root": "0", "solved_rows": len(rows),
              "second_row_nodes": int(rows[1][7]), "certificates": receipts,
              "shared_bundle": receipt,
              "single_root_compatibility": single_receipt,
              "cutoff_verdict": int(cutoff_rows[0][6]),
              "cutoff_trace_count": int((cutoff_dir / "proof-bundle.csv").exists()),
              "all_trusted_leaves": 0}
    (out / "result.json").write_text(
        json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
