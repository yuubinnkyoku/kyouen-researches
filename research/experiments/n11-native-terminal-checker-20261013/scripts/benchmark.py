"""Run the standalone checker and record independently matched prior receipts."""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import subprocess
import time

EXP = Path(__file__).resolve().parents[1]
ROOT = EXP.parents[2]


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("index", type=int)
    parser.add_argument("--trace", type=Path)
    parser.add_argument("--prior", type=Path)
    parser.add_argument("--manifest", type=Path, help="bind a solved row, root and trace hash to its source manifest")
    parser.add_argument("--root")
    parser.add_argument("--verdict", type=int, choices=[1, 2])
    parser.add_argument("--no-json-dag", action="store_true")
    args = parser.parse_args()
    if args.manifest:
        args.manifest = args.manifest.resolve()
    if args.prior:
        args.prior = args.prior.resolve()
    trace = args.trace or ROOT / f"build/n11-proof-traces/budget10m-{args.index}-proof.csv"
    prior_path = args.prior or ROOT / f"research/experiments/n11-s5-s6-quotient-20261013/output/pilot-{args.index}-terminal-verification.json"
    prior = json.loads(prior_path.read_text()) if prior_path.exists() else None
    root = args.root or (prior["root_mask"] if prior else None)
    verdict = args.verdict or (prior["verdict"] if prior else None)
    manifest = None
    row = None
    if args.manifest:
        manifest = json.loads(args.manifest.read_text())
        row = next(r for r in manifest["rows"] if r["s5_index"] == args.index)
        assert row["verdict"] in (1, 2) and row["status"] == "SOLVED", "only completed traces carry propositions"
        source = ROOT / manifest["source"]
        assert digest(source) == manifest["source_sha256"], "manifest source hash mismatch"
        source_row = next(r for r in json.loads(source.read_text())["rows"] if r["s5_index"] == args.index)
        assert source_row["mask"] == row["mask"], "manifest root differs from frozen source"
        trace = args.trace or ROOT / row["trace_path"]
        root = str(row["mask"][0] | row["mask"][1] << 64)
        verdict = row["verdict"]
        assert digest(trace) == row["trace_sha256"], "manifest trace hash mismatch"
    output = EXP / "output"
    output.mkdir(exist_ok=True)
    pruned = output / f"pilot-{args.index}-pruned.csv.gz"
    dag = output / f"pilot-{args.index}-terminal-dag.json.gz"
    cmd = [str(output / "check_trace"), str(trace), "--pruned", str(pruned)]
    if not args.no_json_dag:
        cmd.extend(["--json-dag", str(dag)])
    if root:
        cmd.extend(["--expect-root", root])
    if verdict:
        cmd.extend(["--expect-verdict", str(verdict)])
    started = time.monotonic()
    result = subprocess.run(cmd, text=True, capture_output=True, check=True)
    receipt = json.loads(result.stdout)
    receipt["wall_seconds"] = time.monotonic() - started
    receipt["peak_rss_kib"] = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    receipt["trace_sha256"] = digest(trace)
    receipt["pruned_sha256"] = digest(pruned)
    receipt["trace_bytes"] = trace.stat().st_size
    receipt["pruned_bytes"] = pruned.stat().st_size
    replay_cmd = [str(output / "check_trace"), str(pruned), "--expect-root", receipt["root_mask"],
                  "--expect-verdict", str(receipt["verdict"])]
    replay = json.loads(subprocess.run(replay_cmd, text=True, capture_output=True, check=True).stdout)
    assert all(replay[k] == receipt[k] for k in ("root_mask", "verdict", "nodes", "edges", "terminal_nodes", "trusted_leaves"))
    assert replay["orphan_nodes"] == 0
    receipt["pruned_roundtrip_verified"] = True
    receipt["pruned_roundtrip_seconds"] = replay["total_seconds"]
    if not args.no_json_dag:
        receipt["certificate_sha256"] = digest(dag)
        receipt["certificate_bytes"] = dag.stat().st_size
    receipt["checker_source_sha256"] = digest(EXP / "scripts" / "check_trace.cpp")
    if manifest:
        receipt["manifest"] = str(args.manifest.relative_to(ROOT))
        receipt["manifest_sha256"] = digest(args.manifest)
        receipt["manifest_source_sha256"] = manifest["source_sha256"]
        receipt["manifest_trace_sha256_match"] = receipt["trace_sha256"] == row["trace_sha256"]
        receipt["s5_index"] = args.index
    if prior:
        fields = ("root_mask", "verdict", "nodes", "edges", "terminal_nodes", "trusted_leaves", "trace_sha256")
        if any(receipt[key] != prior[key] for key in fields):
            raise AssertionError({key: (receipt[key], prior[key]) for key in fields if receipt[key] != prior[key]})
        for key in ("trace_nodes", "trace_edges", "orphan_nodes"):
            assert receipt[key] == prior["stats"][key], key
        receipt["prior_python_receipt_match"] = True
        receipt["prior_python_receipt"] = str(prior_path.relative_to(ROOT))
    (output / f"pilot-{args.index}-receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
