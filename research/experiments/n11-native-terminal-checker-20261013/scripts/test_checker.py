"""Adversarial fixtures plus exhaustive canonical small-board cross-checks.

Fixture generation uses the full four-by-four determinant (24 permutation
terms), independent of the checker's reduced three-by-three implementation.
The existing Python verifier is used only as a comparison oracle, never by the
C++ executable, and sees the actual exported portable certificates.
"""
from functools import lru_cache
import gzip
from itertools import combinations, permutations
import json
from pathlib import Path
import subprocess
import sys
import tempfile

EXP = Path(__file__).resolve().parents[1]
ROOT = EXP.parents[2]
sys.path.insert(0, str(ROOT / "research/experiments/n11-proof-dag-engine-20261011/scripts"))
from dag_verifier import verify_certificate


def determinant4(points, n):
    rows = [[p % n, p // n, (p % n) ** 2 + (p // n) ** 2, 1] for p in points]
    result = 0
    for perm in permutations(range(4)):
        inversions = sum(perm[i] > perm[j] for i in range(4) for j in range(i + 1, 4))
        product = 1
        for i in range(4):
            product *= rows[i][perm[i]]
        result += (-1 if inversions % 2 else 1) * product
    return result


def tiny_proofs(n):
    size = n * n

    @lru_cache(None)
    def safe(mask):
        ps = [p for p in range(size) if mask >> p & 1]
        return all(determinant4(q, n) != 0 for q in combinations(ps, 4))

    @lru_cache(None)
    def canon(mask):
        values = []
        for reflected in [False, True]:
            for rotation in range(4):
                v = 0
                for p in range(size):
                    if not mask >> p & 1:
                        continue
                    x, y = p % n, p // n
                    if reflected:
                        x = n - 1 - x
                    for _ in range(rotation):
                        x, y = n - 1 - y, x
                    v |= 1 << (y * n + x)
                values.append(v)
        return min(values)

    @lru_cache(None)
    def solve(mask):
        legal = [p for p in range(size) if not mask >> p & 1 and safe(mask | 1 << p)]
        decisive = 2 if mask.bit_count() % 2 else 1
        if not legal:
            return 3 - decisive, []
        edges = [(p, canon(mask | 1 << p)) for p in legal]
        for p, child in edges:
            if solve(child)[0] == decisive:
                return decisive, [(p, child)]
        return 3 - decisive, edges

    for root in range(1 << size):
        if not safe(root) or canon(root) != root:
            continue
        verdict, _ = solve(root)
        nodes = {}

        def collect(mask):
            if mask in nodes:
                return
            value, edges = solve(mask)
            nodes[mask] = value, not edges, edges
            for _, child in edges:
                collect(child)

        collect(root)
        rows = [f"# kyouen-proof-trace-v1,n={n},root_lo={root},root_hi=0,verdict={verdict}"]
        for mask in sorted(nodes):
            value, terminal, edges = nodes[mask]
            rows.append(f"N,{mask},0,{value},{int(terminal)}")
            rows.extend(f"E,{mask},0,{move},{child},0" for move, child in edges)
        yield root, verdict, "\n".join(rows) + "\n"


VALID = """# kyouen-proof-trace-v1,n=2,root_lo=0,root_hi=0,verdict=1
N,0,0,1,0
E,0,0,0,1,0
N,1,0,1,0
E,1,0,1,3,0
E,1,0,2,3,0
E,1,0,3,6,0
N,3,0,1,0
E,3,0,2,7,0
N,6,0,1,0
E,6,0,0,7,0
N,7,0,1,1
"""


def main():
    exe = EXP / "output/check_trace"
    cases = {}
    with tempfile.TemporaryDirectory(prefix="checker-tests-", dir=EXP / "output") as temp:
        tmp = Path(temp)

        def run(name, text, expected_error=None, extra=()):
            path = tmp / f"{name}.csv"
            dag = tmp / f"{name}.json.gz"
            path.write_text(text)
            result = subprocess.run([str(exe), str(path), "--json-dag", str(dag), *extra], text=True, capture_output=True)
            if expected_error:
                assert result.returncode != 0, (name, result.stdout)
                assert expected_error in result.stderr, (name, result.stderr)
                assert not dag.exists(), name
                cases[name] = "rejected: " + expected_error
                return
            assert result.returncode == 0, (name, result.stderr)
            receipt = json.loads(result.stdout)
            cert = json.loads(gzip.decompress(dag.read_bytes()))
            python = verify_certificate(cert)
            assert all(receipt[key] == python[key] for key in python), (name, receipt, python)
            cases[name] = dict(nodes=receipt["nodes"], edges=receipt["edges"], verdict=receipt["verdict"])
            return receipt, cert

        run("valid_concrete_boundary", VALID)
        run("empty", "", "missing trace header")
        run("header_schema", VALID.replace("trace-v1", "trace-v9"), "invalid trace header")
        run("invalid_board_size", VALID.replace("n=2", "n=12"), "invalid board size")
        run("overflow_word", VALID.replace("N,0,0,1,0", "N,18446744073709551616,0,1,0"), "invalid unsigned integer")
        run("negative_word", VALID.replace("N,0,0,1,0", "N,-1,0,1,0"), "invalid unsigned integer")
        run("trailing_columns", VALID + "N,9,0,1,1,0\n", "malformed proof row")
        run("duplicate_node", VALID + "N,7,0,1,1\n", "duplicate node")
        run("invalid_node_verdict", VALID.replace("N,7,0,1,1", "N,7,0,0,1"), "invalid node verdict")
        run("invalid_terminal_flag", VALID.replace("N,7,0,1,1", "N,7,0,1,2"), "invalid node verdict/terminal marker")
        run("missing_root", VALID.replace("N,0,0,1,0\n", ""), "missing root")
        run("missing_child", VALID.replace("N,7,0,1,1\n", ""), "references missing child")
        run("external_root_mismatch", VALID, "root does not match", extra=["--expect-root", "1"])
        run("external_verdict_mismatch", VALID, "verdict does not match", extra=["--expect-verdict", "2"])
        run("terminal_polarity", "# kyouen-proof-trace-v1,n=2,root_lo=7,root_hi=0,verdict=2\nN,7,0,2,1\n", "incorrect terminal edges/parity")
        run("false_terminal", VALID.replace("N,7,0,1,1", "N,7,0,1,0"), "terminal marker disagrees")
        run("false_nonterminal", VALID.replace("N,0,0,1,0", "N,0,0,1,1"), "terminal marker disagrees")
        run("universal_missing_move", VALID.replace("E,1,0,2,3,0\n", ""), "incomplete legal boundary")
        run("universal_duplicate_move", VALID.replace("E,1,0,2,3,0", "E,1,0,1,3,0"), "duplicate concrete move")
        run("illegal_occupied_move", VALID.replace("E,1,0,1,3,0", "E,1,0,0,3,0"), "illegal or duplicate")
        run("unranked_transition", VALID.replace("E,3,0,2,7,0", "E,3,0,2,3,0"), "incorrect ranked canonical transition")
        run("wrong_canonical_transition", VALID.replace("E,1,0,3,6,0", "E,1,0,3,3,0"), "incorrect ranked canonical transition")
        run("child_polarity", VALID.replace("N,7,0,1,1", "N,7,0,2,1"), "incorrect fixed-player child polarity")
        run("extra_existential_witness", VALID.replace("E,0,0,0,1,0", "E,0,0,0,1,0\nE,0,0,1,1,0"), "exactly one witness")
        run("missing_existential_witness", VALID.replace("E,0,0,0,1,0\n", ""), "exactly one witness")
        run("out_of_board_root", "# kyouen-proof-trace-v1,n=2,root_lo=16,root_hi=0,verdict=1\nN,16,0,1,1\n", "out-of-board reachable node")
        run("noncanonical_root", "# kyouen-proof-trace-v1,n=2,root_lo=8,root_hi=0,verdict=1\nN,8,0,1,0\n", "noncanonical reachable node")
        run("unsafe_circle", "# kyouen-proof-trace-v1,n=2,root_lo=15,root_hi=0,verdict=2\nN,15,0,2,1\n", "unsafe occupied node")
        run("unsafe_line", "# kyouen-proof-trace-v1,n=4,root_lo=15,root_hi=0,verdict=2\nN,15,0,2,1\n", "unsafe occupied node")
        orphan, cert = run("orphan_semantics_excluded", VALID + "N,15,0,2,1\nN,16,0,1,1\nE,16,0,0,99,0\n")
        assert orphan["orphan_nodes"] == 2 and set(cert["nodes"]) == {"0", "1", "3", "6", "7"}
        small_counts = {}
        for n in (1, 2, 3):
            total = 0
            for root, verdict, trace in tiny_proofs(n):
                receipt, _ = run(f"exhaustive_n{n}_root{root}", trace)
                assert receipt["verdict"] == verdict
                total += 1
            small_counts[n] = total
        # Exercise gzip input and pruning normalization separately.
        csv = tmp / "valid.csv.gz"
        csv.write_bytes(gzip.compress(VALID.encode(), mtime=0))
        result = subprocess.run([str(exe), str(csv)], text=True, capture_output=True, check=True)
        assert json.loads(result.stdout)["nodes"] == 5
        # A damaged gzip checksum must never be accepted as a completed proof.
        damaged = bytearray(csv.read_bytes())
        damaged[-8] ^= 1
        csv.write_bytes(damaged)
        rejected = subprocess.run([str(exe), str(csv)], text=True, capture_output=True)
        assert rejected.returncode != 0 and "gzip trace read error" in rejected.stderr
        cases["damaged_gzip_crc"] = "rejected: gzip trace read error"
    report = dict(adversarial_and_regression_cases=cases, exhaustive_canonical_safe_roots=small_counts,
                  total_cases=len(cases), python_comparison="all accepted exported DAGs independently verified")
    (EXP / "output/test-report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(dict(total_cases=len(cases), exhaustive_canonical_safe_roots=small_counts)))


if __name__ == "__main__":
    main()
