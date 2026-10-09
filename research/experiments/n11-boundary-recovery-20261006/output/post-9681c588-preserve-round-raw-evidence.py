#!/usr/bin/env python3
"""Copy raw probe inputs, outputs, and logs from .local into immutable experiment evidence."""
from __future__ import annotations
import hashlib, json, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "research/experiments/n11-boundary-recovery-20261006/output"
PREFIX = "post-9681c588-next98"
def sha(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()
copied = []
for round_name in ("round3", "round4"):
    collected_path = OUT / f"{PREFIX}-{round_name}-collected-manifest.json"
    collected = json.loads(collected_path.read_text(encoding="utf-8"))
    destination = OUT / f"{PREFIX}-{round_name}-raw"
    destination.mkdir(parents=True, exist_ok=True)
    for target in collected["summary"]["target_statuses"]:
        for kind in ("input", "output", "log"):
            ref = target.get(kind)
            if not ref:
                continue
            source = ROOT / ref["path"].replace("\\", "/")
            if not source.is_file():
                raise SystemExit(f"missing source file: {source}")
            blob = source.read_bytes()
            digest = hashlib.sha256(blob).hexdigest()
            if digest != ref["sha256"] or len(blob) != ref["bytes"]:
                raise SystemExit(f"source hash/size mismatch: {source}")
            dest = destination / source.name
            if dest.exists():
                if sha(dest) != digest:
                    raise SystemExit(f"refusing to overwrite distinct raw evidence: {dest}")
            else:
                shutil.copyfile(source, dest)
            copied.append({"round": round_name, "kind": kind,
                           "source": ref["path"].replace("\\", "/"),
                           "path": dest.resolve().relative_to(ROOT.resolve()).as_posix(),
                           "bytes": len(blob), "sha256": digest})
report = {"schema":"n11-reply27-preserved-local-raw-evidence-v1",
          "claim":"Files were copied byte-for-byte from .local; original source files remain in place.",
          "files":copied}
p = OUT / "post-9681c588-preserved-raw-files.json"
p.write_text(json.dumps(report, indent=2, sort_keys=True)+"\n", encoding="utf-8", newline="\n")
print(f"PRESERVED_RAW_ROWS_OK files={len(copied)} round3={sum(r['round']=='round3' for r in copied)} round4={sum(r['round']=='round4' for r in copied)}")
