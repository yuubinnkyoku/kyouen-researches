#!/usr/bin/env python3
"""Transcription check for verify_y22_universal.py (run before the machine).

Fail-closed check that every block of verify_y22_universal.py that is
declared as a published transcription equals the published bytes:

  (1) engine block (@@TRANSCRIPTION-ENGINE-*@@): mex / H_ordered /
      H_canonical / q_odd / single_token -- must equal, byte for byte,
      the same block of the published y=21 universal machine
      verify_y21_universal.py (commit 8960e633, itself the
      transcription chain of the y=9..y=20 proof machines);
  (2) cand21 block (@@TRANSCRIPTION-CAND21-*@@): the B-child of every
      y=22 point and the x=22 merger child value. Must equal the
      published verify_y21_universal.py cand21 block after the
      block-local word-boundary rename Y -> Y21 AND independently the
      published cand21.py table block (K1248 fit experiment, proved by
      the published y=21 machine K1255) after the same rename
      (two-source byte-equality);
  (3) cand22 block (@@TRANSCRIPTION-CAND22-*@@): the claim under test.
      Must equal the published cand22.py table block (K1256 fit
      experiment, current main bytes, fit driver excluded) byte for
      byte.

Extraction anchors are structural (no line numbers): the engine block
runs from "def mex(values):" to the TRANSCRIPTION-ENGINE-END marker
line of the published y=21 machine; the cand21 block of the published
y=21 machine runs from the "Y = 21" literal to its CAND21-END marker
line; the cand21.py / cand22.py table blocks run from the "Y = 21" /
"Y = 22" literal to "def main".

Output: output/transcriptions-check-y22.json (sorted keys, no clock).
Exit 0 on PASS, 1 on FAIL.
"""
import json
import re
import sys
from pathlib import Path


def _find_repo_root(start: Path) -> Path:
    for p in [start, *start.parents]:
        if (p / "AGENTS.md").is_file():
            return p
    raise SystemExit("FAIL-CLOSED: repo root with AGENTS.md not found")


def _block(text: str, marker: str) -> str:
    a = text.index(f"# @@TRANSCRIPTION-{marker}-START@@\n") + len(f"# @@TRANSCRIPTION-{marker}-START@@\n")
    b = text.index(f"# @@TRANSCRIPTION-{marker}-END@@")
    return text[a:b].rstrip("\n") + "\n"


def _src_block(text: str, start_lit: str, end_marker: str) -> str:
    lines = text.split("\n")
    i_start = next(i for i, l in enumerate(lines) if l == start_lit)
    i_end = next(i for i, l in enumerate(lines) if l.startswith(end_marker) and i > i_start)
    return "\n".join(lines[i_start:i_end]).rstrip("\n") + "\n"


def _engine_block_y21machine(text: str) -> str:
    i0 = text.index("def mex(values):")
    i1 = text.index("# @@TRANSCRIPTION-ENGINE-END@@")
    return text[i0:i1].rstrip("\n") + "\n"


def _src_block_machine(text: str, start_lit: str, marker: str) -> str:
    lines = text.split("\n")
    i_start = next(i for i, l in enumerate(lines) if l == start_lit)
    i_end = next(i for i, l in enumerate(lines[i_start:], start=i_start)
                 if l == f"# @@TRANSCRIPTION-{marker}-END@@")
    return "\n".join(lines[i_start:i_end]).rstrip("\n") + "\n"


def main() -> int:
    here = Path(__file__).resolve().parent
    root = _find_repo_root(here)
    v22_path = here.parent / "verify_y22_universal.py"
    v21_path = root / "research/experiments/vertical-fiber-two-token-y21-universal-proof-20261123/verify_y21_universal.py"
    c21fit = root / "research/experiments/vertical-fiber-two-token-y21-parametric-fit-20261123/cand21.py"
    c22fit = root / "research/experiments/vertical-fiber-two-token-y22-parametric-fit-20261123/cand22.py"
    for p in (v22_path, v21_path, c21fit, c22fit):
        if not p.is_file():
            raise SystemExit(f"FAIL-CLOSED: published source missing: {p}")

    v22 = v22_path.read_text(encoding="utf-8")
    v21 = v21_path.read_text(encoding="utf-8")
    c21 = c21fit.read_text(encoding="utf-8")
    c22 = c22fit.read_text(encoding="utf-8")

    report = {"check": "y22 verifier transcription byte-equality vs published bytes",
              "verifier": str(v22_path.relative_to(root))}

    # (1) engine block
    got = _block(v22, "ENGINE")
    want = _engine_block_y21machine(v21)
    report["engine"] = {"equal": got == want, "bytes": len(got)}
    # (2) cand21 block (Y -> Y21 word-boundary rename on both sources)
    got = _block(v22, "CAND21")
    want_machine = re.sub(r"\bY\b", "Y21", _src_block_machine(v21, "Y = 21", "CAND21"))
    want_fit = re.sub(r"\bY\b", "Y21", _src_block(c21, "Y = 21", "def main"))
    report["cand21"] = {"equal_machine_verbatim_renamed": got == want_machine,
                       "equal_fit_verbatim_renamed": got == want_fit,
                       "sources_agree": want_machine == want_fit,
                       "bytes": len(got)}
    # (3) cand22 block (no rename; driver excluded)
    got = _block(v22, "CAND22")
    want22 = _src_block(c22, "Y = 22", "def main")
    report["cand22"] = {"equal_fit_verbatim": got == want22, "bytes": len(got)}

    report["overall"] = "PASS" if (
        report["engine"]["equal"]
        and report["cand21"]["equal_machine_verbatim_renamed"]
        and report["cand21"]["equal_fit_verbatim_renamed"]
        and report["cand22"]["equal_fit_verbatim"]) else "FAIL"

    out = here.parent / "output"
    out.mkdir(parents=True, exist_ok=True)
    (out / "transcriptions-check-y22.json").write_text(
        json.dumps(report, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))
    return 0 if report["overall"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
