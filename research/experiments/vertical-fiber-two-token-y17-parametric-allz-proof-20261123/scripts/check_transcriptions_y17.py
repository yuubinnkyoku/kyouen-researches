#!/usr/bin/env python3
"""Transcription check for verify_y17_universal.py (run before the machine).

Fail-closed check that every block of verify_y17_universal.py that is
declared as a published transcription equals the published bytes:

  (1) engine block (@@TRANSCRIPTION-ENGINE-*@@): mex / H_ordered /
      H_canonical / q_odd / single_token -- must equal, byte for byte,
      the same block of the published y=16 universal machine
      verify_y16_universal.py (part2, commit b706b214, itself the
      transcription chain of the y=9..y=15 proof machines);
  (2) cand16 block (@@TRANSCRIPTION-CAND16-*@@): the B-child of every
      y=17 point. Must equal the published verify_y16_universal.py
      cand16 block after the block-local word-boundary rename Y -> Y16
      AND independently the published cand16.py table block
      (K1237 fit experiment) after the same rename (two-source
      byte-equality);
  (3) cand17 block (@@TRANSCRIPTION-CAND17-*@@): the claim under test.
      Must equal the published cand17.py table block (K1240 fit
      experiment, commit 6ca80e0e, fit driver excluded) byte for byte.

Extraction anchors are structural (no line numbers): the engine block
runs from "def mex(values):" to the single_token "raise ValueError"
sentinel; the cand16 block of the published y=16 machine runs from the
"Y = 16" literal to "def opts16"; the cand16.py / cand17.py table
blocks run from the "Y = 16" / "Y = 17" literal to "def main".

Output: output/transcriptions-check-y17.json (sorted keys, no clock).
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


def _engine_block(text: str) -> str:
    i0 = text.index("def mex(values):")
    i1 = text.index("# =====================================================================\n# Published y=15 two-token closed form")
    return text[i0:i1].rstrip("\n") + "\n"


def main() -> int:
    here = Path(__file__).resolve().parent
    root = _find_repo_root(here)
    v17_path = here.parent / "verify_y17_universal.py"
    v16_path = root / "research/experiments/vertical-fiber-two-token-y16-parametric-allz-proof-20261122/verify_y16_universal.py"
    c16fit = root / "research/experiments/vertical-fiber-two-token-y16-parametric-allz-fit-20261122/cand16.py"
    c17fit = root / "research/experiments/vertical-fiber-two-token-y17-parametric-allz-fit-20261123/cand17.py"
    for p in (v16_path, c16fit, c17fit):
        if not p.is_file():
            raise SystemExit(f"FAIL-CLOSED: published source missing: {p}")

    v17 = v17_path.read_text(encoding="utf-8")
    v16 = v16_path.read_text(encoding="utf-8")
    c16 = c16fit.read_text(encoding="utf-8")
    c17 = c17fit.read_text(encoding="utf-8")

    report = {"check": "y17 verifier transcription byte-equality vs published bytes",
              "verifier": str(v17_path.relative_to(root))}

    # (1) engine block
    got = _block(v17, "ENGINE")
    want = _engine_block(v16)
    report["engine"] = {"equal": got == want, "bytes": len(got)}
    # (2) cand16 block (Y -> Y16 word-boundary rename on both sources)
    got = _block(v17, "CAND16")
    want_machine = re.sub(r"\bY\b", "Y16", _src_block(v16, "Y = 16", "def opts16"))
    want_fit = re.sub(r"\bY\b", "Y16", _src_block(c16, "Y = 16", "def main"))
    report["cand16"] = {"equal_machine_verbatim_renamed": got == want_machine,
                        "equal_fit_verbatim_renamed": got == want_fit,
                        "sources_agree": want_machine == want_fit,
                        "bytes": len(got)}
    # (3) cand17 block (no rename; driver excluded)
    got = _block(v17, "CAND17")
    want17 = _src_block(c17, "Y = 17", "def main")
    report["cand17"] = {"equal_fit_verbatim": got == want17, "bytes": len(got)}

    report["overall"] = "PASS" if (
        report["engine"]["equal"]
        and report["cand16"]["equal_machine_verbatim_renamed"]
        and report["cand16"]["equal_fit_verbatim_renamed"]
        and report["cand17"]["equal_fit_verbatim"]) else "FAIL"

    out = here.parent / "output"
    out.mkdir(parents=True, exist_ok=True)
    (out / "transcriptions-check-y17.json").write_text(
        json.dumps(report, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))
    return 0 if report["overall"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
