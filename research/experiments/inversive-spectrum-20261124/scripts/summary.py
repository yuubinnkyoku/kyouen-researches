"""Print the K_s(q) table and write output/summary.md."""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
OUT = EXP / "output"


def main() -> None:
    data = json.loads((OUT / "spectrum_results.json").read_text(encoding="utf-8"))
    rows = sorted(data["results"], key=lambda r: (r["q"], r["s"]))
    lines = [
        "| q | s | exact K_s | theorem bound (s-2)(q+1)+2 | witness | d=q+1-s | tau_d | d(q+1) |",
        "|---:|---:|---:|---:|:---:|---:|---:|---:|",
    ]
    for r in rows:
        lines.append(
            f"| {r['q']} | {r['s']} | **{r['exact']}** | {r.get('bound_theorem')} | "
            f"{'yes' if r.get('witness_verified') else '-'} | {r.get('dual_d', '-')} | "
            f"{r.get('tau_d', '-')} | {r.get('tau_linear_bound', '-')} |")
    md = "\n".join(lines)
    (OUT / "summary.md").write_text(md + "\n", encoding="utf-8")
    print(md)
    partial = OUT / "bounds_partial.json"
    if partial.exists():
        print()
        print(json.dumps(json.loads(partial.read_text(encoding="utf-8")), indent=1))


if __name__ == "__main__":
    main()
