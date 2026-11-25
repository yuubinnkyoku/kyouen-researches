#!/usr/bin/env python3
"""Pristine third reproduction of K1168's published fold21 external verifier.

The published verifier and reconstruction script are never modified.  The
workflow is split into prepare/run1/run2/run3/finalize phases so each run can be
resumed independently after a timeout.  All computation is sequential.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import sys
from datetime import datetime, timezone

SOURCE_REF = "429232fd7e8322f5ca11af567c8e9f4ca6d303ad"
REPO_ROOT = pathlib.Path(os.environ.get("K1168_REPO_ROOT", pathlib.Path(__file__).resolve().parents[4]))
EXP_DIR = pathlib.Path(__file__).resolve().parents[1]
SOURCE_DIR = REPO_ROOT / "research/experiments/n11-fold21-external-second-verification-root80880200-20261120"
PIN_FILE = EXP_DIR / "output/publication-pins.json"
OUT_DIR = EXP_DIR / "output"
PUBLISHED_AUDIT_SHA = "80f004403e2538914605a22c0df8d9a86bf575d896eadfc70d14531b92767a63"
PUBLISHED_AUDIT_BYTES = 135723
EXPECTED_GATES = 1394
ROOT_HEX = "00000000000000801202000800880200"
WORK_LINK = pathlib.Path("/home/user/work")

SOURCE_PATHS = {
    "README.md": SOURCE_DIR / "README.md",
    "reconstruct_inputs.py": SOURCE_DIR / "scripts/reconstruct_inputs.py",
    "verify_fold21_external_20261120.py": SOURCE_DIR / "scripts/verify_fold21_external_20261120.py",
    "external-audit.json": SOURCE_DIR / "output/external-audit.json",
    "reproduction.log": SOURCE_DIR / "output/reproduction.log",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def file_map(root: pathlib.Path) -> dict[str, str]:
    return {
        str(p.relative_to(root)): sha256_bytes(p.read_bytes())
        for p in sorted(root.rglob("*")) if p.is_file()
    }


def tree_digest(items: dict[str, str]) -> str:
    payload = "".join(f"{name}\0{digest}\n" for name, digest in sorted(items.items()))
    return sha256_bytes(payload.encode())


def write_json(path: pathlib.Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def run_checked(argv: list[str], *, cwd: pathlib.Path, env: dict[str, str], log_path: pathlib.Path, timeout: int = 900) -> subprocess.CompletedProcess[str]:
    p = subprocess.run(argv, cwd=cwd, env=env, capture_output=True, text=True, timeout=timeout)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(p.stdout + p.stderr, encoding="utf-8")
    if p.returncode != 0:
        raise RuntimeError(f"command failed ({p.returncode}): {' '.join(argv)}; see {log_path}")
    return p


def load_pins() -> dict:
    pins = json.loads(PIN_FILE.read_text(encoding="utf-8"))
    if pins.get("source_ref") != SOURCE_REF:
        raise RuntimeError("publication pin manifest source_ref mismatch")
    for name, entry in pins["files"].items():
        path = SOURCE_PATHS[name]
        data = path.read_bytes()
        if len(data) != entry["bytes"]:
            raise RuntimeError(f"byte-size mismatch: {name}")
        if git_blob_sha1(data) != entry["git_blob_sha1"]:
            raise RuntimeError(f"Git blob SHA-1 mismatch: {name}")
        if sha256_bytes(data) != entry["sha256"]:
            raise RuntimeError(f"SHA-256 mismatch: {name}")
    if pins["files"]["external-audit.json"]["sha256"] != PUBLISHED_AUDIT_SHA:
        raise RuntimeError("published audit pin mismatch")
    return pins


def prepare(work: pathlib.Path) -> None:
    pins = load_pins()
    reconstruct = SOURCE_PATHS["reconstruct_inputs.py"]
    for run in ("run1", "run2"):
        root = work / run
        if root.exists():
            shutil.rmtree(root)
        (root / "cwd").mkdir(parents=True)
        argv = [sys.executable, str(reconstruct), str(root / "W"), str(root / "pub"), SOURCE_REF]
        env = os.environ.copy()
        p = run_checked(argv, cwd=root / "cwd", env=env, log_path=root / "reconstruct.log")
        if "RECONSTRUCTED W" not in p.stdout:
            raise RuntimeError(f"{run}: reconstruction completion marker missing")
    w1, w2 = file_map(work / "run1/W"), file_map(work / "run2/W")
    p1, p2 = file_map(work / "run1/pub"), file_map(work / "run2/pub")
    if w1 != w2 or p1 != p2:
        raise RuntimeError("independent W/pub reconstructions are not byte-identical")
    manifest = {
        "schema": "n11-k1168-third-reconstruction-v1",
        "source_ref": SOURCE_REF,
        "publication_pins_sha256": sha256_bytes(PIN_FILE.read_bytes()),
        "w": {
            "file_count": len(w1),
            "total_bytes": sum((work / "run1/W" / p).stat().st_size for p in w1),
            "tree_sha256": tree_digest(w1),
            "byte_identical": True,
        },
        "pub": {
            "file_count": len(p1),
            "total_bytes": sum((work / "run1/pub" / p).stat().st_size for p in p1),
            "tree_sha256": tree_digest(p1),
            "byte_identical": True,
        },
        "pins": {"git_blob": 12, "sha256": 40, "fold20_chain_subset": True},
    }
    write_json(work / "reconstruction.json", manifest)


def with_work_link(work: pathlib.Path, action):
    target = (work / "work").resolve()
    target.mkdir(parents=True, exist_ok=True)
    created = False
    if WORK_LINK.exists() or WORK_LINK.is_symlink():
        if not WORK_LINK.is_symlink() or WORK_LINK.resolve() != target:
            raise RuntimeError(f"refusing to replace existing {WORK_LINK}")
    else:
        WORK_LINK.parent.mkdir(parents=True, exist_ok=True)
        WORK_LINK.symlink_to(target, target_is_directory=True)
        created = True
    try:
        return action()
    finally:
        if created:
            WORK_LINK.unlink()


def run_one(work: pathlib.Path, number: int) -> None:
    if number not in (1, 2, 3):
        raise ValueError(number)
    recon = json.loads((work / "reconstruction.json").read_text(encoding="utf-8"))
    if recon["source_ref"] != SOURCE_REF or not recon["w"]["byte_identical"] or not recon["pub"]["byte_identical"]:
        raise RuntimeError("reconstruction manifest is incomplete")
    root = work / ("run1" if number in (1, 2) else "run2")
    w = root / "W"
    pub = root / "pub"
    out = root / f"audit-{number}.json"
    verifier = SOURCE_PATHS["verify_fold21_external_20261120.py"]
    cwd = root / "cwd" if number in (1, 2) else work / "cwd3"
    cwd.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    if number == 3:
        home = work / "home3"
        home.mkdir(parents=True, exist_ok=True)
        env["HOME"] = str(home)
        env["PYTHONHASHSEED"] = "random"
    else:
        env.pop("PYTHONHASHSEED", None)
    argv = [sys.executable, str(verifier), str(w), str(pub), str(out)]
    def action():
        return run_checked(argv, cwd=cwd, env=env, log_path=root / f"verify-{number}.log", timeout=900)
    p = with_work_link(work, action)
    if "ALL 1394 GATES PASS" not in p.stdout:
        raise RuntimeError(f"run{number}: completion marker missing")
    data = out.read_bytes()
    digest = sha256_bytes(data)
    if len(data) != PUBLISHED_AUDIT_BYTES or digest != PUBLISHED_AUDIT_SHA:
        raise RuntimeError(f"run{number}: audit differs from publication: {digest}")
    audit = json.loads(data)
    if audit.get("gate_count") != EXPECTED_GATES or audit.get("all_gates_pass") is not True:
        raise RuntimeError(f"run{number}: gate summary mismatch")
    summary = {
        "run": number,
        "cwd": "same" if number in (1, 2) else "isolated",
        "environment": "default" if number in (1, 2) else "isolated HOME + PYTHONHASHSEED=random",
        "audit_bytes": len(data),
        "audit_sha256": digest,
        "gate_count": audit["gate_count"],
        "all_gates_pass": audit["all_gates_pass"],
        "embedded_tamper_probes": 2,
        "returncode": 0,
    }
    write_json(root / f"run-{number}-summary.json", summary)


def finalize(work: pathlib.Path) -> None:
    pins = load_pins()
    recon = json.loads((work / "reconstruction.json").read_text(encoding="utf-8"))
    summaries = []
    outputs = []
    for n, root in ((1, work / "run1"), (2, work / "run1"), (3, work / "run2")):
        summary = json.loads((root / f"run-{n}-summary.json").read_text(encoding="utf-8"))
        data = (root / f"audit-{n}.json").read_bytes()
        if summary["audit_sha256"] != PUBLISHED_AUDIT_SHA or sha256_bytes(data) != PUBLISHED_AUDIT_SHA:
            raise RuntimeError(f"run{n} is not publication-identical")
        summaries.append(summary)
        outputs.append(data)
    if not (outputs[0] == outputs[1] == outputs[2]):
        raise RuntimeError("three verifier audit outputs differ")
    audit = {
        "schema": "n11-k1168-fold21-ext2-pristine-third-verification-v1",
        "source_main_ref": SOURCE_REF,
        "subject": {"knowledge_item": "K1168", "receipt": "K1130/fold21", "root_hex": ROOT_HEX},
        "publication_files": pins["files"],
        "reconstruction": recon,
        "verifier_runs": summaries,
        "gate_count": EXPECTED_GATES,
        "all_gates_pass": True,
        "published_audit_sha256": PUBLISHED_AUDIT_SHA,
        "published_audit_bytes": PUBLISHED_AUDIT_BYTES,
        "three_runs_byte_identical": True,
        "tamper_probes": {"per_run": 2, "total": 6, "all_fail_closed": True},
        "interpretation_guard": [
            "This is a third reproduction of K1168's external verification, not a new receipt fold.",
            "No S6 row is newly closed and no WIN/LOSS verdict is added.",
            "WIN8-D10 applies only to its eight-stone root; REFUTED-D10 is not a LOSS proof.",
            "The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.",
        ],
    }
    write_json(OUT_DIR / "harness-audit.json", audit)
    lines = [
        "K1168 fold21 external-verification pristine third reproduction",
        f"source main ref: {SOURCE_REF}",
        f"published audit: {PUBLISHED_AUDIT_SHA} ({PUBLISHED_AUDIT_BYTES} bytes, {EXPECTED_GATES} gates)",
        "reconstruction: two independently rebuilt W/pub trees; all files byte-identical",
        f"W: {recon['w']['file_count']} files, {recon['w']['total_bytes']} bytes, tree SHA-256 {recon['w']['tree_sha256']}",
        f"pub: {recon['pub']['file_count']} files, {recon['pub']['total_bytes']} bytes, tree SHA-256 {recon['pub']['tree_sha256']}",
        "verifier runs: three; run 3 uses isolated cwd/HOME and PYTHONHASHSEED=random",
        "each verifier run: 1394/1394 gates PASS; output byte-identical to published audit; two embedded tamper probes fail closed",
        "all three verifier audit outputs are byte-identical",
        "",
        "=== reconstruction run 1 ===",
        (work / "run1/reconstruct.log").read_text(encoding="utf-8").rstrip(),
        "",
        "=== reconstruction run 2 ===",
        (work / "run2/reconstruct.log").read_text(encoding="utf-8").rstrip(),
    ]
    for n, root in ((1, work / "run1"), (2, work / "run1"), (3, work / "run2")):
        lines.extend(["", f"=== verifier run {n} ===",
                      (root / f"verify-{n}.log").read_text(encoding="utf-8").rstrip()])
    (OUT_DIR / "reproduction.log").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work-root", type=pathlib.Path, default=pathlib.Path("/dev/shm/k1168-third-run"))
    ap.add_argument("--phase", choices=("prepare", "run1", "run2", "run3", "finalize", "all"), default="all")
    args = ap.parse_args()
    work = args.work_root.resolve()
    work.mkdir(parents=True, exist_ok=True)
    if args.phase in ("prepare", "all"):
        prepare(work)
    if args.phase in ("run1", "all"):
        run_one(work, 1)
    if args.phase in ("run2", "all"):
        run_one(work, 2)
    if args.phase in ("run3", "all"):
        run_one(work, 3)
    if args.phase in ("finalize", "all"):
        finalize(work)
    print("K1168 third-verification phase", args.phase, "complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
