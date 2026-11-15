#!/usr/bin/env python3
"""Reconstruct the tmp-cost62a extraction intermediates from the published
cost-62a certificates (the fold script's runtime inputs)."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
TMP = OUT / "tmp-cost62a"
CERTS = OUT / "class2-lane-cost62a-certificates"
ROOTS = {\n    7: "00000000040000003800000008100080",\n    15: "00000000040000003800000008108000",\n    35: "00000000040000003800000808100000",\n    76: "00000000040010003800000008100000",\n    81: "00000000040200003800000008100000",\n    98: "00000004040000003800000008100000",\n}
SCRIPTS = HERE / "scripts"


def main():
    sys.path.insert(0, str(SCRIPTS))
    from legal_candidates import legal_candidates
    TMP.mkdir(parents=True, exist_ok=True)
    moves_all = {}
    for bit, root in ROOTS.items():
        st, cand = legal_candidates(root)
        moves_all[str(bit)] = {"root": root, "stones": st, "moves": cand}
    (TMP / "legal-moves.json").write_text(json.dumps(moves_all, indent=1) + "\n")
    for bit, root in ROOTS.items():
        cert = CERTS / f"bit{bit}-root-{root}.cert"
        parts = sorted(CERTS.glob(f"bit{bit}-root-{root}.cert.part*of2"))
        data = b"".join(p.read_bytes() for p in parts) if parts else cert.read_bytes()
        whole = TMP / f"bit{bit}.cert"
        whole.write_bytes(data)
        (TMP / f"bit{bit}.cert-receipt.json").write_text(json.dumps({
            "bit": bit, "root_hex": root, "rows": len(data.splitlines()) - 2,
            "bytes": len(data), "md5": hashlib.md5(data).hexdigest(),
            "sha256": hashlib.sha256(data).hexdigest(),
        }, indent=1) + "\n")
        moves = ",".join(map(str, moves_all[str(bit)]["moves"]))
        ts = subprocess.run(["node", "--experimental-strip-types",
                             str(SCRIPTS / "verify_bit7_win7_cert.ts"),
                             "--cert", str(whole), "--root", root, "--root-check",
                             "--subroots", moves, "--consumed-out",
                             str(TMP / f"bit{bit}.consumed.txt")],
                            check=True, capture_output=True, text=True)
        (TMP / f"bit{bit}.tsverify.json").write_text(ts.stdout)
        bj = subprocess.run(["node", str(SCRIPTS / "verify_win7_certificate_bigint_independent.mjs"),
                             str(whole), str(len(moves_all[str(bit)]["moves"]))],
                            check=True, capture_output=True, text=True)
        (TMP / f"bit{bit}.bigint.json").write_text(bj.stdout)
    print("reconstructed", TMP)


if __name__ == "__main__":
    main()
