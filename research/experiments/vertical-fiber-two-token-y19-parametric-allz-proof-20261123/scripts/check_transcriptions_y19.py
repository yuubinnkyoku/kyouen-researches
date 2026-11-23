#!/usr/bin/env python3
"""Transcription check for verify_y19_universal.py (run before the machine).

Fail-closed check that every block of verify_y19_universal.py that is
declared as a published transcription equals the published bytes:

  (1) engine block (@@TRANSCRIPTION-ENGINE-*@@): mex / H_ordered /
      H_canonical / q_odd / single_token -- must equal, byte for byte,
      the same block of the published y=18 universal machine
      verify_y18_universal.py (commit d29acbd8, itself the
      transcription chain of the y=9..y=17 proof machines);
  (2) cand18 block (@@TRANSCRIPTION-CAND18-*@@): the B-child of every
      y=19 point. Must equal the published verify_y18_universal.py
      cand18 block after the block-local word-boundary rename Y -> Y18
      AND independently the published cand18.py table block
      (K1242 fit experiment, whose universal proof is the published
      y=18 machine) after the same rename (two-source byte-equality);
  (3) cand19 block (@@TRANSCRIPTION-CAND19-*@@): the claim under test.
      Must equal the published cand19.py table block (K1243 fit
      experiment, current main bytes, fit driver excluded) byte for
      byte.

Extraction anchors are structural (no line numbers): the engine block
runs from "def mex(values):" to the TRANSCRIPTION-ENGINE-END marker
line of the published y=18 machine; the cand18 block of the published
y=18 machine runs from the "Y = 18" literal to its CAND18-END marker
line; the cand18.py / cand19.py table blocks run from the "Y = 18" /
"Y = 19" literal to "def main".

Output: output/transcriptions-check-y19.json (sorted keys, no clock).
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


def _engine_block_y18machine(text: str) -> str:
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
    v19_path = here.parent / "verify_y19_universal.py"
    v18_path = root / "research/experiments/vertical-fiber-two-token-y18-parametric-allz-proof-20261123/verify_y18_universal.py"
    c18fit = root / "research/experiments/vertical-fiber-two-token-y18-parametric-allz-fit-20261123/cand18.py"
    c19fit = root / "research/experiments/vertical-fiber-two-token-y19-parametric-allz-fit-20261123/cand19.py"
    for p in (v19_path, v18_path, c18fit, c19fit):
        if not p.is_file():
            raise SystemExit(f"FAIL-CLOSED: published source missing: {p}")

    v19 = v19_path.read_text(encoding="utf-8")
    v18 = v18_path.read_text(encoding="utf-8")
    c18 = c18fit.read_text(encoding="utf-8")
    c19 = c19fit.read_text(encoding="utf-8")

    report = {"check": "y19 verifier transcription byte-equality vs published bytes",
              "verifier": str(v19_path.relative_to(root))}

    # (1) engine block
    got = _block(v19, "ENGINE")
    want = _engine_block_y18machine(v18)
    report["engine"] = {"equal": got == want, "bytes": len(got)}
    # (2) cand18 block (Y -> Y18 word-boundary rename on both sources)
    got = _block(v19, "CAND18")
    want_machine = re.sub(r"\bY\b", "Y18", _src_block_machine(v18, "Y = 18", "CAND18"))
    want_fit = re.sub(r"\bY\b", "Y18", _src_block(c18, "Y = 18", "def main"))
    report["cand18"] = {"equal_machine_verbatim_renamed": got == want_machine,
                        "equal_fit_verbatim_renamed": got == want_fit,
                        "sources_agree": want_machine == want_fit,
                        "bytes": len(got)}
    # (3) cand19 block (no rename; driver excluded)
    got = _block(v19, "CAND19")
    want19 = _src_block(c19, "Y = 19", "def main")
    report["cand19"] = {"equal_fit_verbatim": got == want19, "bytes": len(got)}

    report["overall"] = "PASS" if (
        report["engine"]["equal"]
        and report["cand18"]["equal_machine_verbatim_renamed"]
        and report["cand18"]["equal_fit_verbatim_renamed"]
        and report["cand19"]["equal_fit_verbatim"]) else "FAIL"

    out = here.parent / "output"
    out.mkdir(parents=True, exist_ok=True)
    (out / "transcriptions-check-y19.json").write_text(
        json.dumps(report, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))
    return 0 if report["overall"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
