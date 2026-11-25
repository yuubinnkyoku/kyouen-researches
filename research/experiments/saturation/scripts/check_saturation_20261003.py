#!/usr/bin/env python3
"""Check saturation witnesses, direction bounds and completed finite exclusions."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "output"


def stable(value):
    if isinstance(value, dict):
        return {k: (v.split(", ")[0] + ", " + Path(v.split(", ")[1]).name
                    if k == "inherited_lower_bound" else stable(v))
                for k, v in value.items() if k not in ("seconds", "source_sha256")}
    if isinstance(value, list):
        return list(map(stable, value))
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full-exclusion", action="store_true",
                        help="Also repeat the 1.5 billion-node seven-stone exclusion")
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="kyouen-saturation-audits-") as audit_tmp:
        for stem in ("saturation_20261003", "saturation_20261003_extra"):
            saved = json.loads((DATA / (stem + "_verified.json")).read_text())
            target = Path(audit_tmp) / (stem + "_verified.json")
            command = [sys.executable, str(HERE / (stem + "_verify.py")), "--output", str(target)]
            if stem.endswith("extra") and args.full_exclusion:
                command.append("--rerun-exact")
            subprocess.run(command, check=True)
            # Source hashes describe the historical run. A path migration changes
            # sources; compare all mathematical data and retain the frozen receipt.
            assert stable(json.loads(target.read_text())) == stable(saved)
    expected = json.loads((DATA / "saturation_20261003_exact_results.json").read_text())["results"]
    with tempfile.TemporaryDirectory(prefix="kyouen-saturation-check-") as tmp:
        binary = str(Path(tmp) / "exact")
        subprocess.run(["g++", "-O3", "-std=c++17", str(HERE / "saturation_20261003_exact.cpp"),
                        "-o", binary], check=True)
        for case in expected:
            if case["k"] == 7 and not args.full_exclusion:
                continue
            observed = json.loads(subprocess.check_output([binary, "11", str(case["k"])], text=True))
            assert stable(observed) == stable(case)
            print(f"11x11, {case['k']} stones: full exclusion reproduced", flush=True)
    print("Saturation certificates and direction bounds verified")


if __name__ == "__main__":
    main()
