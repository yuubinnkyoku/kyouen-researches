#!/usr/bin/env python3
"""Generate Kyouen/CubeCertData.lean from certificate.b64."""
import base64
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "research/experiments/highdim-q5-cubes-20261016/certificate.b64"
OUT = ROOT / "Kyouen/CubeCertData.lean"

raw = base64.b64decode(SRC.read_text())
entries = []
for (packed,) in struct.iter_unpack("<I", raw):
    mask, kind = packed >> 1, packed & 1
    entries.append((mask, kind == 1))
entries.sort()

lines = [
    "import Kyouen.CubeSymmetry",
    "",
    "namespace Kyouen.CubeCertData",
    "",
    "def certAssoc : List (Nat × Bool) := [",
]
for mask, label in entries:
    lines.append(f"  ({mask}, {'true' if label else 'false'}),")
lines.append("]")
lines.append("")
lines.append("end Kyouen.CubeCertData")
OUT.write_text("\n".join(lines), encoding="utf-8")
print(f"wrote {len(entries)} entries to {OUT}")