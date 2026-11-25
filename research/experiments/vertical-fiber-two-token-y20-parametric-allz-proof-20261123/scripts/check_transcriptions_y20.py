#!/usr/bin/env python3
"""Transcription check for verify_y20_universal.py (run before the machine).

Fail-closed check that every block of verify_y20_universal.py that is
declared as a published transcription equals the published bytes:

  (1) engine block (@@TRANSCRIPTION-ENGINE-*@@): mex / H_ordered /
      H_canonical / q_odd / single_token -- must equal, byte for byte,
      the same block of the published y=19 universal machine
      verify_y19_universal.py (commit 99b7e070, itself the
      transcription chain of the y=9..y=18 proof machines);
  (2) cand19 block (@@TRANSCRIPTION-CAND19-*@@): the B-child of every
      y=20 point. Must equal the published verify_y19_universal.py
      cand19 block after the block-local word-boundary rename Y -> Y19
      AND independently the published cand19.py table block
      (K1243 fit experiment, whose universal proof is the published
      y=19 machine) after the same rename (two-source byte-equality);
  (3) cand20 block (@@TRANSCRIPTION-CAND20-*@@): the claim under test.
      Must equal the published cand20.py table block (K1246 fit
      experiment, current main bytes, fit driver excluded) byte for
      byte.

Extraction anchors are structural (no line numbers): the engine block
runs from "def mex(values):" to the TRANSCRIPTION-ENGINE-END marker
line of the published y=19 machine; the cand19 block of the published
y=19 machine runs from the "Y = 19" literal to its CAND19-END marker
line; the cand19.py / cand20.py table blocks run from the "Y = 19" /
"Y = 20" literal to "def main".

Output: output/transcriptions-check-y20.json (sorted keys, no clock).
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


def _engine_block_y19machine(text: str) -> str:
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
    v20_path = here.parent / "verify_y20_universal.py"
    v19_path = root / "research/experiments/vertical-fiber-two-token-y19-parametric-allz-proof-20261123/verify_y19_universal.py"
    c19fit = root / "research/experiments/vertical-fiber-two-token-y19-parametric-allz-fit-20261123/cand19.py"
    c20fit = root / "research/experiments/vertical-fiber-two-token-y20-parametric-allz-fit-20261123/cand20.py"
    for p in (v20_path, v19_path, c19fit, c20fit):
        if not p.is_file():
            raise SystemExit(f"FAIL-CLOSED: published source missing: {p}")

    v20 = v20_path.read_text(encoding="utf-8")
    v19 = v19_path.read_text(encoding="utf-8")
    c19 = c19fit.read_text(encoding="utf-8")
    c20 = c20fit.read_text(encoding="utf-8")

    report = {"check": "y20 verifier transcription byte-equality vs published bytes",
              "verifier": str(v20_path.relative_to(root))}

    # (1) engine block
    got = _block(v20, "ENGINE")
    want = _engine_block_y19machine(v19)
    report["engine"] = {"equal": got == want, "bytes": len(got)}
    # (2) cand19 block (Y -> Y19 word-boundary rename on both sources)
    got = _block(v20, "CAND19")
    want_machine = re.sub(r"\bY\b", "Y19", _src_block_machine(v19, "Y = 19", "CAND19"))
    want_fit = re.sub(r"\bY\b", "Y19", _src_block(c19, "Y = 19", "def main"))
    report["cand19"] = {"equal_machine_verbatim_renamed": got == want_machine,
                        "equal_fit_verbatim_renamed": got == want_fit,
                        "sources_agree": want_machine == want_fit,
                        "bytes": len(got)}
    # (3) cand20 block (no rename; driver excluded)
    got = _block(v20, "CAND20")
    want20 = _src_block(c20, "Y = 20", "def main")
    report["cand20"] = {"equal_fit_verbatim": got == want20, "bytes": len(got)}

    report["overall"] = "PASS" if (
        report["engine"]["equal"]
        and report["cand19"]["equal_machine_verbatim_renamed"]
        and report["cand19"]["equal_fit_verbatim_renamed"]
        and report["cand20"]["equal_fit_verbatim"]) else "FAIL"

    out = here.parent / "output"
    out.mkdir(parents=True, exist_ok=True)
    (out / "transcriptions-check-y20.json").write_text(
        json.dumps(report, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))
    return 0 if report["overall"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
