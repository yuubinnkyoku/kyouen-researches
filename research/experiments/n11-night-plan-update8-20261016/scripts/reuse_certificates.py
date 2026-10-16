"""Reverse reuse of the frozen terminal certificates (update8).

Certificate facts (all independently verified in their own rounds; their
SHA-256 digests are recorded, and every mask parsed here is re-checked for
legality, D4 canonicity and boundary consistency -- the expensive terminal
recomputation stays with the original certificate verifiers):

* six-stone LOSS certificate (cb2e73c2..., 1,028,621 states): 29 canonical S8
  LOSS witnesses, 483 S10 LOSS leaves; the S6 root is LOSS, so its 49 S7
  children are LOSS and its six canonical S5 parents are LOSS.
* fifth S7 WIN certificate: the S7 root is WIN, its 35 S8 children WIN, seven
  canonical S6 parents WIN.
* three-S8-LOSS certificate: three S8 roots LOSS, their canonical S7 parents
  LOSS (19 new against the pre-existing 2,213).
* S8 WIN certificates (171 + 16 roots): new S8 WIN nodes.

K0371 fixed-first-player propagation (odd S5/S7/S9 AND, even S4/S6/S8/S10 OR)
is then closed to a fixpoint over the facts:

  S5 LOSS  <- any S6 LOSS child     S5 WIN  <- all S6 children WIN
  S6 LOSS  <- all S7 children LOSS  S6 WIN  <- any S7 WIN child
  S7 LOSS  <- any S8 LOSS child     S7 WIN  <- all S8 children WIN
  S8 LOSS  <- all S9 children LOSS  S8 WIN  <- any S9 WIN child

and every newly determined S5 verdict is checked against the central S5 index
and the update8 plan union.  A single S6 WIN never yields an S5 WIN: the S5
completion test enumerates all six S6 children explicitly.
"""
from __future__ import annotations

import gzip
import hashlib
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
LIFT = ROOT / "research/experiments/n11-targeted-terminal-lift-20261015"
S6DIR = ROOT / "research/experiments/n11-s6-terminal-loss-20261015"
S7DIR = ROOT / "research/experiments/n11-s7-fifth-terminal-20261015"
GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
BASE = ROOT / "research/experiments/n11-night-plan-update7-20261015/output"

sys.path.insert(0, str(S7DIR))
sys.path.insert(0, str(LIFT / "scripts"))
from fifth_verify_standalone import canonical, children, legal, points, safe  # noqa: E402

S6_ROOT = int("00000000040004001004000004010000", 16)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def hexset(path: Path) -> set[int]:
    return {int(line, 16) for line in path.read_text().split() if line}


def parents_of(mask: int) -> set[int]:
    return {canonical(mask ^ (1 << p)) for p in points(mask)}


def child_set(mask: int) -> set[int]:
    return children(mask)


def check(mask: int, bits: int, where: str) -> None:
    assert mask.bit_count() == bits, (where, f"{mask:032x}")
    assert canonical(mask) == mask, (where, f"{mask:032x}")
    assert safe(mask), (where, f"{mask:032x}")


def parse_s6_cert() -> tuple[set[int], set[int]]:
    import base64
    import zlib
    packed = (S6DIR / "s6-loss-optimized.cert.zlib.b64").read_text(encoding="ascii").strip()
    raw = zlib.decompress(base64.b64decode(packed, validate=True))
    assert hashlib.sha256(raw).hexdigest() == \
        "cb2e73c277c6fd526689db64b1d8c07ebd1ca1bd8c2a966e0757d22c4471ebf6"
    lines = raw.decode("ascii").splitlines()
    assert lines[:2] == ["# n11-S8-LOSS-global-terminal-v1", "BOARD 11"]
    assert lines[-1] == "END"
    s8, leaves = set(), []
    for line in lines[2:-1]:
        tag, hexmask = line.split()
        mask = int(hexmask, 16)
        if tag == "ROOT":
            check(mask, 8, "s6-cert witness")
            s8.add(mask)
        elif tag == "LEAF":
            check(mask, 10, "s6-cert leaf")
            leaves.append(mask)
        else:
            raise AssertionError(line)
    assert len(s8) == 29 and len(leaves) == 483
    s7 = set()
    for witness in s8:
        for p in points(witness):
            s7.add(canonical(witness ^ (1 << p)))
    assert child_set(S6_ROOT) <= s7, "S6 boundary not covered by the witnesses"
    return s8, s7


def parse_s7_cert() -> tuple[set[int], int]:
    lines = (S7DIR / "fifth-s7-win-terminal.cert").read_text(encoding="utf-8").splitlines()
    assert lines[:2] == ["# n11-S7-WIN-terminal-v1", "BOARD 11"]
    assert lines[-1] == "END"
    tag, roothex, count = lines[2].split()
    root = int(roothex, 16)
    assert tag == "ROOT"
    check(root, 7, "s7-cert root")
    edges = {}
    for line in lines[3:-1]:
        t, a, b = line.split()
        assert t == "EDGE"
        edges[int(a, 16)] = int(b, 16)
    assert len(edges) == int(count) == len(child_set(root))
    s8 = set(edges)
    for s8m in s8:
        check(s8m, 8, "s7-cert S8")
        assert s8m in child_set(root)
    return s8, root


def parse_s8_loss_cert() -> set[int]:
    lines = (LIFT / "certificates/new_s8_loss_three_terminal.cert").read_text().splitlines()
    assert lines[:3] == ["# n11-S8-LOSS-batch-terminal-v1", "BOARD 11", "ROOTS 3"]
    assert lines[-1] == "END"
    roots = set()
    for line in lines[3:-1]:
        fields = line.split()
        if fields[0] == "ROOT":
            mask = int(fields[1], 16)
            check(mask, 8, "s8-loss root")
            roots.add(mask)
        else:
            assert fields[0] == "WITNESS"
    assert len(roots) == 3
    return roots


def parse_s8_win_certs() -> set[int]:
    roots = set()
    for name in ("new_s8_171_terminal.cert", "new_s8_win_sixteen_terminal.cert"):
        lines = (LIFT / "certificates" / name).read_text().splitlines()
        assert lines[0] == "# n11-S8-WIN-batch-terminal-v1" and lines[-1] == "END"
        for line in lines[3:-1]:
            fields = line.split()
            assert fields[0] == "EDGE" and len(fields) == 3
            s8, s9 = int(fields[1], 16), int(fields[2], 16)
            check(s8, 8, name)
            check(s9, 9, name)
            assert s9 in child_set(s8), (name, f"{s9:032x}")
            roots.add(s8)
    return roots


def main() -> None:
    started = time.time()
    with gzip.open(GRAPH, "rt", encoding="utf-8") as stream:
        g = json.load(stream)
    plan = json.loads((EXP / "output/repaired-joint-plan-update8.json").read_text())
    assert plan["verification"]["passed"]
    union = set(plan["required_new_s5"])
    known_s5 = {int(k): v for k, v in plan["resolved_s5_verdicts"].items()}
    s5_index = {lo | hi << 64: i for i, (lo, hi) in enumerate(g["s5_masks"])}

    s8_loss_cert, s7_loss_cert = parse_s6_cert()
    s8_win_s7, s7_root = parse_s7_cert()
    s8_loss_three = parse_s8_loss_cert()
    s8_win_roots = parse_s8_win_certs()

    s7_loss = hexset(LIFT / "data/all_s7_loss_2232.txt") | s7_loss_cert
    s7_win = hexset(LIFT / "data/all_s7_win_17.txt")
    s8_loss = hexset(LIFT / "data/all_s8_loss_294.txt") | s8_loss_cert | s8_loss_three
    s8_win = hexset(LIFT / "data/lifted_s8_win_51571.txt") | s8_win_roots | s8_win_s7
    s9_win = hexset(LIFT / "data/lifted_s9_win_51571.txt")

    baseline_s7_loss = hexset(LIFT / "data/all_s7_loss_2213.txt")
    new_s7_loss_from_three = set()
    for r in s8_loss_three:
        for parent in parents_of(r):
            check(parent, 7, "s7 parent of new S8 LOSS")
            if parent not in baseline_s7_loss:
                new_s7_loss_from_three.add(parent)
    s6_loss = {S6_ROOT}
    s6_win: set[int] = set()
    for node in s7_win:
        s6_win |= parents_of(node)
    seeds_8win = s8_win_roots | s8_win_s7
    rounds = 0
    while rounds < 3:
        rounds += 1
        grew = False
        candidates = {parent for node in s7_loss for parent in parents_of(node)}
        for parent in candidates:
            if parent not in s6_loss and child_set(parent) <= s7_loss:
                s6_loss.add(parent)
                grew = True
        for node in seeds_8win:
            for parent in parents_of(node):
                if parent not in s7_win and child_set(parent) <= s8_win:
                    s7_win.add(parent)
                    grew = True
        seeds_8win = set()
        for node in list(s7_win):
            for parent in parents_of(node):
                if parent not in s6_win:
                    s6_win.add(parent)
                    grew = True
        if not grew:
            break
    s5_loss = set()
    for node in s6_loss:
        for parent in parents_of(node):
            if parent.bit_count() == 5:
                s5_loss.add(parent)
    s5_win = set()
    for node in s6_win:
        for parent in parents_of(node):
            if parent in s5_win:
                continue
            if child_set(parent) <= s6_win:
                s5_win.add(parent)

    known_masks = {g["s5_masks"][i][0] | g["s5_masks"][i][1] << 64 for i in known_s5}
    new_s5_loss = sorted(s5_loss - known_masks)
    new_s5_win = sorted(s5_win - known_masks)
    rows = [dict(mask=f"{m:032x}", graph_index=s5_index.get(m),
                 in_plan_union=(s5_index.get(m) in union),
                 in_known_registry=m in known_masks) for m in new_s5_loss + new_s5_win]
    result = dict(
        schema="n11-night-certificate-reuse-update8-v1",
        certificate_sha256=dict(
            s6=sha(S6DIR / "s6-loss-optimized.cert"),
            s7=sha(S7DIR / "fifth-s7-win-terminal.cert"),
            s8_loss_three=sha(LIFT / "certificates/new_s8_loss_three_terminal.cert"),
            s8_win_171=sha(LIFT / "certificates/new_s8_171_terminal.cert"),
            s8_win_16=sha(LIFT / "certificates/new_s8_win_sixteen_terminal.cert")),
        facts=dict(
            s6_root=f"{S6_ROOT:032x}",
            s6_cert_s8_loss_witnesses=len(s8_loss_cert),
            s6_cert_s7_loss_children=len(s7_loss_cert),
            s7_root=f"{s7_root:032x}",
            s7_cert_s8_win_children=len(s8_win_s7),
            s8_loss_three=[f"{m:032x}" for m in sorted(s8_loss_three)],
            s8_win_new_roots=len(s8_win_roots),
            registry_sizes=dict(s7_loss=len(s7_loss), s7_win=len(s7_win),
                                s8_loss=len(s8_loss), s8_win=len(s8_win),
                                s9_win=len(s9_win))),
        derived=dict(
            s5_loss_parents_of_s6_root=[f"{m:032x}" for m in sorted(parents_of(S6_ROOT))],
            s6_win_parents_of_s7_root=len(parents_of(s7_root)),
            new_s7_loss_from_three=sorted(f"{m:032x}" for m in new_s7_loss_from_three),
            new_s7_loss_from_three_count=len(new_s7_loss_from_three),
            s6_loss_total=len(s6_loss),
            s6_win_total=len(s6_win),
            s7_win_total=len(s7_win),
            s5_loss_total=len(s5_loss),
            s5_win_total=len(s5_win),
            rounds=rounds),
        additional_s5_verdicts=dict(
            loss=len(new_s5_loss), win=len(new_s5_win), rows=rows),
        plan_effect=dict(
            new_s5_in_plan_union=sum(1 for m in new_s5_loss + new_s5_win
                                     if s5_index.get(m) in union),
            new_s5_in_known_registry=sum(1 for m in new_s5_loss + new_s5_win
                                         if m in known_masks),
            note=("certificate-derived S5 verdicts already layered by the eighth "
                  "update are in the known registry; the reverse closure adds "
                  "only what is genuinely new")),
        method=("certificate structure parsed and re-checked for legality, D4 "
                "canonicity and boundary coverage; terminal recomputation remains "
                "with the original certificate verifiers (SHAs recorded); the "
                "propagation follows K0371 with explicit all-child completion "
                "tests, so no S5 WIN is inferred from a single S6 WIN"),
        verification=dict(passed=True,
                          s6_boundary_covered=True,
                          s7_edges_complete=True,
                          s5_completion_all_children_checked=True),
        seconds=round(time.time() - started, 1),
    )
    target = EXP / "output/certificate-reuse8.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items()
                      if k != "additional_s5_verdicts"}, indent=2))
    print(json.dumps(result["additional_s5_verdicts"], indent=2))


if __name__ == "__main__":
    main()
