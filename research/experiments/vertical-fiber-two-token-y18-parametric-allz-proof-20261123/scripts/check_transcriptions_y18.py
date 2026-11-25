#!/usr/bin/env python3
"""Transcription check for verify_y18_universal.py (run before the machine).

Fail-closed check that every block of verify_y18_universal.py that is
declared as a published transcription equals the published bytes:

  (1) engine block (@@TRANSCRIPTION-ENGINE-*@@): mex / H_ordered /
      H_canonical / q_odd / single_token -- must equal, byte for byte,
      the same block of the published y=17 universal machine
      verify_y17_universal.py (part2, commit ab23d120, itself the
      transcription chain of the y=9..y=16 proof machines);
  (2) cand17 block (@@TRANSCRIPTION-CAND17-*@@): the B-child of every
      y=18 point. Must equal the published verify_y17_universal.py
      cand17 block after the block-local word-boundary rename Y -> Y17
      AND independently the published cand17.py table block
      (K1240 fit experiment) after the same rename (two-source
      byte-equality);
  (3) cand18 block (@@TRANSCRIPTION-CAND18-*@@): the claim under test.
      Must equal the published cand18.py table block (K1242 fit
      experiment, commit 9e898f45, fit driver excluded) byte for byte.

Extraction anchors are structural (no line numbers): the engine block
runs from "def mex(values):" to the published y=16 closed-form header
marker line of the y=17 machine; the cand17 block of the published y=17
machine runs from the "Y = 17" literal to its CAND17-END marker line;
the cand17.py / cand18.py table blocks run from the "Y = 17" / "Y = 18"
literal to "def main".

Output: output/transcriptions-check-y18.json (sorted keys, no clock).
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


def _engine_block_y17machine(text: str) -> str:
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
    v18_path = here.parent / "verify_y18_universal.py"
    v17_path = root / "research/experiments/vertical-fiber-two-token-y17-parametric-allz-proof-20261123/verify_y17_universal.py"
    c17fit = root / "research/experiments/vertical-fiber-two-token-y17-parametric-allz-fit-20261123/cand17.py"
    c18fit = root / "research/experiments/vertical-fiber-two-token-y18-parametric-allz-fit-20261123/cand18.py"
    for p in (v18_path, v17_path, c17fit, c18fit):
        if not p.is_file():
            raise SystemExit(f"FAIL-CLOSED: published source missing: {p}")

    v18 = v18_path.read_text(encoding="utf-8")
    v17 = v17_path.read_text(encoding="utf-8")
    c17 = c17fit.read_text(encoding="utf-8")
    c18 = c18fit.read_text(encoding="utf-8")

    report = {"check": "y18 verifier transcription byte-equality vs published bytes",
              "verifier": str(v18_path.relative_to(root))}

    # (1) engine block
    got = _block(v18, "ENGINE")
    want = _engine_block_y17machine(v17)
    report["engine"] = {"equal": got == want, "bytes": len(got)}
    # (2) cand17 block (Y -> Y17 word-boundary rename on both sources)
    got = _block(v18, "CAND17")
    want_machine = re.sub(r"\bY\b", "Y17", _src_block_machine(v17, "Y = 17", "CAND17"))
    want_fit = re.sub(r"\bY\b", "Y17", _src_block(c17, "Y = 17", "def main"))
    report["cand17"] = {"equal_machine_verbatim_renamed": got == want_machine,
                        "equal_fit_verbatim_renamed": got == want_fit,
                        "sources_agree": want_machine == want_fit,
                        "bytes": len(got)}
    # (3) cand18 block (no rename; driver excluded)
    got = _block(v18, "CAND18")
    want18 = _src_block(c18, "Y = 18", "def main")
    report["cand18"] = {"equal_fit_verbatim": got == want18, "bytes": len(got)}

    report["overall"] = "PASS" if (
        report["engine"]["equal"]
        and report["cand17"]["equal_machine_verbatim_renamed"]
        and report["cand17"]["equal_fit_verbatim_renamed"]
        and report["cand18"]["equal_fit_verbatim"]) else "FAIL"

    out = here.parent / "output"
    out.mkdir(parents=True, exist_ok=True)
    (out / "transcriptions-check-y18.json").write_text(
        json.dumps(report, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))
    return 0 if report["overall"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
