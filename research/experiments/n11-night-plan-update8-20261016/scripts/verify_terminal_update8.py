"""Terminal-only independent verification of the update8 probe trace 150871.

Same criteria as the focus-verified set (n11-native-terminal-checker-20261013):
byte-identical check_trace source, root/verdict/trace SHA256 bound to the frozen
update8 probe manifest row, full closure to geometric terminals, pruned
roundtrip, trusted_leaves forced to 0.  The raw solver label stays
solver-trusted; only this receipt upgrades the row to independent evidence.
UNKNOWN is never upgraded, so 144774 stays UNKNOWN.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("index", type=int, default=150871, nargs="?")
    p.add_argument("--manifest", type=Path, default=EXP / "output/update8probe10m-manifest.json")
    p.add_argument("--checker", type=Path,
                   default=ROOT / "research/experiments/n11-adaptive-verify-20261013/output/check_trace")
    p.add_argument("--rerun-python", action="store_true")
    args = p.parse_args()
    manifest_path = args.manifest.resolve()
    manifest = json.loads(manifest_path.read_text())
    row = next(r for r in manifest["rows"] if r["s5_index"] == args.index)
    assert row["status"] == "SOLVED" and row["verdict"] in (1, 2), "only completed traces carry propositions"
    trace = (ROOT / row["trace_path"]).resolve()
    assert digest(trace) == row["trace_sha256"], "trace hash differs from the probe manifest"
    root = str(row["mask"][0] | row["mask"][1] << 64)
    verdict = row["verdict"]
    checker = args.checker.resolve()
    output = EXP / "output"
    output.mkdir(exist_ok=True)
    pruned = output / f"terminal-{args.index}-pruned.csv.gz"
    dag = output / f"terminal-{args.index}-dag.json.gz"
    assert not pruned.exists() and not dag.exists(), "refusing to overwrite existing artifacts"

    import subprocess

    def run(cmd):
        return json.loads(subprocess.run(cmd, text=True, capture_output=True, check=True).stdout)

    started = time.monotonic()
    receipt = run([str(checker), str(trace), "--pruned", str(pruned), "--json-dag", str(dag),
                   "--expect-root", root, "--expect-verdict", str(verdict)])
    assert receipt["trusted_leaves"] == 0, "terminal-only closure requires zero trusted leaves"
    receipt["wall_seconds"] = time.monotonic() - started
    receipt["trace_sha256"] = digest(trace)
    receipt["pruned_sha256"] = digest(pruned)
    receipt["trace_bytes"] = trace.stat().st_size
    receipt["pruned_bytes"] = pruned.stat().st_size
    replay = run([str(checker), str(pruned), "--expect-root", receipt["root_mask"],
                  "--expect-verdict", str(receipt["verdict"])])
    assert all(replay[k] == receipt[k] for k in
               ("root_mask", "verdict", "nodes", "edges", "terminal_nodes", "trusted_leaves"))
    assert replay["orphan_nodes"] == 0
    receipt["pruned_roundtrip_verified"] = True
    receipt["pruned_roundtrip_seconds"] = replay["total_seconds"]
    receipt["certificate_sha256"] = digest(dag)
    receipt["certificate_bytes"] = dag.stat().st_size
    receipt["checker_source_sha256"] = digest(
        ROOT / "research/experiments/n11-adaptive-verify-20261013/scripts/check_trace.cpp")
    receipt["checker_binary_sha256"] = digest(checker)
    receipt["probe_manifest"] = str(manifest_path.relative_to(ROOT))
    receipt["probe_manifest_sha256"] = digest(manifest_path)
    receipt["solver_binary_sha256"] = manifest["solver_binary_sha256"]
    receipt["probe_search_nodes"] = row["nodes"]
    receipt["probe_wall_seconds"] = row["wall_seconds"]
    receipt["probe_peak_rss_kib"] = row["peak_rss_kib"]
    receipt["s5_index"] = args.index
    receipt["evidence_class"] = "independent-terminal-only-verification"
    receipt["raw_label_trust"] = "solver-trusted completed label from the update8 10M probe"
    receipt["trust"] = ("independent terminal-only verification: local geometry, canonical ranking, "
                        "complete universal boundaries, existential witnesses and terminal parity all "
                        "rechecked; zero trusted leaves; raw solver label upgraded solely by this receipt")
    (output / f"receipt-{args.index}.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")

    result = dict(schema="n11-night-update8-terminal-verify-v1", index=args.index,
                  receipt={k: receipt[k] for k in
                           ("root_mask", "verdict", "nodes", "edges", "terminal_nodes", "trusted_leaves",
                            "orphan_nodes", "pruned_roundtrip_verified", "checker_source_sha256")})
    if args.rerun_python:
        sys.path.insert(0, str(ROOT / "research/experiments/n11-proof-dag-engine-20261011/scripts"))
        from dag_verifier import verify_certificate
        import gzip
        started = time.monotonic()
        with gzip.open(dag, "rt") as stream:
            cert = json.load(stream)
        checked = verify_certificate(cert)
        assert all(checked[k] == receipt[k] for k in checked)
        result["fresh_python_verification"] = checked
        result["python_wall_seconds"] = time.monotonic() - started
    (output / f"terminal-verify-{args.index}.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
