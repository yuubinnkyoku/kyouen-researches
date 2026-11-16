#!/usr/bin/env python3
"""Reconstruct the tmp-cost58c and tmp-cost84a extraction intermediates from
the published cost-58c / cost-84a certificates (the fold scripts' runtime
inputs).  Follows the published reconstruct_tmp_cost70g_20261116.py pattern:
these two directories were never published as tmp outputs, so after a
workspace loss their inputs are re-derived from the published certificates,
the published verifiers (verify_bit7_win7_cert.ts --consumed-out,
verify_win7_certificate_bigint_independent.mjs) and legal_candidates.py."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
SCRIPTS = HERE / "scripts"

LANES = {
    "tmp-cost58c": {
        "certs": "class2-lane-cost58c-certificates",
        "child": "00000000000000801206000040000000",
        "bits": [1, 3, 6, 18, 22, 24, 32, 35, 42, 43, 44, 56, 66, 67, 73, 75,
                 78, 79, 86, 88, 89, 91, 92, 99, 102, 103, 105, 109, 114, 116,
                 117, 118, 120],
    },
    "tmp-cost84a": {
        "certs": "class2-lane-cost84a-certificates",
        "child": "00000000000040809002000000000800",
        "bits": [1, 62, 70, 90],
    },
}


def main():
    sys.path.insert(0, str(SCRIPTS))
    from legal_candidates import legal_candidates
    for tmp_name, cfg in LANES.items():
        TMP = OUT / tmp_name
        CERTS = OUT / cfg["certs"]
        CV = int(cfg["child"], 16)
        TMP.mkdir(parents=True, exist_ok=True)
        moves_all = {}
        for bit in cfg["bits"]:
            root = f"{CV | (1 << bit):032x}"
            st, cand = legal_candidates(root)
            moves_all[str(bit)] = {"root": root, "stones": st, "moves": cand}
        (TMP / "legal-moves.json").write_text(
            json.dumps(moves_all, indent=1) + "\n")
        for bit in cfg["bits"]:
            root = moves_all[str(bit)]["root"]
            cert = CERTS / f"bit{bit}-root-{root}.cert"
            parts = sorted(CERTS.glob(f"bit{bit}-root-{root}.cert.part*of2"))
            if parts:
                data = b"".join(p.read_bytes().replace(b"\r\n", b"\n")
                                for p in parts)
            else:
                data = cert.read_bytes()
            whole = TMP / f"bit{bit}.cert"
            whole.write_bytes(data)
            (TMP / f"bit{bit}.cert-receipt.json").write_text(json.dumps({
                "bit": bit, "root_hex": root,
                "rows": len(data.splitlines()) - 2,
                "bytes": len(data), "md5": hashlib.md5(data).hexdigest(),
                "sha256": hashlib.sha256(data).hexdigest(),
            }, indent=1) + "\n")
            moves = ",".join(map(str, moves_all[str(bit)]["moves"]))
            ts = subprocess.run(
                ["node", "--experimental-strip-types",
                 str(SCRIPTS / "verify_bit7_win7_cert.ts"),
                 "--cert", str(whole), "--root", root, "--root-check",
                 "--subroots", moves, "--consumed-out",
                 str(TMP / f"bit{bit}.consumed.txt")],
                check=True, capture_output=True, text=True)
            (TMP / f"bit{bit}.tsverify.json").write_text(ts.stdout)
            bj = subprocess.run(
                ["node", str(SCRIPTS /
                             "verify_win7_certificate_bigint_independent.mjs"),
                 str(whole), str(len(moves_all[str(bit)]["moves"]))],
                check=True, capture_output=True, text=True)
            (TMP / f"bit{bit}.bigint.json").write_text(bj.stdout)
            print(f"{tmp_name}: bit{bit} reconstructed", flush=True)
        print("reconstructed", TMP, flush=True)


if __name__ == "__main__":
    main()
