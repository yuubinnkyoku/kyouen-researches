"""Independently verify one shared proof trace or portable multi-root bundle."""
import argparse
import csv
import gzip
import json
from pathlib import Path
import sys

SCRIPTS = Path(__file__).resolve().parents[2] / "n11-proof-dag-engine-20261011" / "scripts"
INDEPENDENT = Path(__file__).resolve().parents[2] / "n11-independent-exact-audit-20261010" / "scripts"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(INDEPENDENT))
from dag_verifier import aggregate, verify_certificate  # noqa: E402
from independent import Board  # noqa: E402


def _check_graph(board_size, roots, nodes):
    if board_size < 1 or not roots or not nodes:
        raise ValueError("empty proof bundle")
    board = Board(board_size)
    visiting, done = set(), {}

    def visit(ident):
        if ident in visiting:
            raise ValueError("cycle in proof bundle")
        if ident in done:
            return done[ident]
        node = nodes.get(ident)
        if not isinstance(node, dict):
            raise ValueError("edge references a missing node")
        try:
            mask = int(node["mask"])
            verdict = node["verdict"]
            stones = node["stones"]
            terminal = node["terminal"]
            legal_count = node["legal_count"]
            edges = node["edges"]
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError("malformed proof node") from exc
        if ident != str(mask) or type(verdict) is not int or verdict not in (1, 2):
            raise ValueError("noncanonical identifier or invalid verdict")
        if type(stones) is not int or stones != mask.bit_count():
            raise ValueError("wrong stone count")
        if type(terminal) is not bool or not isinstance(edges, list):
            raise ValueError("malformed terminal/edge fields")
        if type(legal_count) is not int:
            raise ValueError("missing or malformed legal move count")
        if node.get("trusted") or node.get("trusted_leaf"):
            raise ValueError("trusted leaves are forbidden")
        try:
            legal = board.legal(mask)
        except (TypeError, ValueError) as exc:
            raise ValueError("unsafe or out-of-board position") from exc
        if board.canonical(mask) != mask:
            raise ValueError("position is not D4-canonical")
        moves = set(board.points(legal))
        if legal_count != len(moves):
            raise ValueError("wrong legal move count")
        if terminal != (not moves):
            raise ValueError("terminal marker disagrees with geometry")
        visiting.add(ident)
        if not moves:
            if edges or aggregate(stones, ()) != verdict:
                raise ValueError("incorrect terminal verdict")
        else:
            labels, child_values = [], []
            for edge in edges:
                if not isinstance(edge, dict) or set(edge) != {"move", "child"}:
                    raise ValueError("malformed edge")
                move, child_id = edge["move"], edge["child"]
                if type(move) is not int or move not in moves or not isinstance(child_id, str):
                    raise ValueError("illegal move label or child reference")
                if move in labels:
                    raise ValueError("duplicate move label")
                labels.append(move)
                child = nodes.get(child_id)
                if not isinstance(child, dict):
                    raise ValueError("edge references a missing child")
                try:
                    child_mask = int(child["mask"])
                except (KeyError, TypeError, ValueError) as exc:
                    raise ValueError("malformed child position") from exc
                if child_mask != board.canonical(mask | (1 << move)) or child_mask.bit_count() != stones + 1:
                    raise ValueError("edge has a nonlegal or incorrectly ranked transition")
                child_values.append(visit(child_id))
            decisive = 2 if stones % 2 else 1
            existential = verdict == decisive
            if existential:
                if len(edges) != 1 or child_values != [verdict]:
                    raise ValueError("existential node lacks one decisive witness")
            elif set(labels) != moves or len(labels) != len(moves):
                raise ValueError("universal node omits or duplicates a legal move")
            elif aggregate(stones, child_values) != verdict:
                raise ValueError("universal node has an incorrect fixed-player verdict")
        visiting.remove(ident)
        done[ident] = verdict
        return verdict

    root_receipts = []
    root_ids = set()
    for root in roots:
        root_id, ident, expected = root["id"], root["root"], root["verdict"]
        if root_id in root_ids:
            raise ValueError("duplicate proof root id")
        root_ids.add(root_id)
        if ident not in nodes or expected not in (1, 2):
            raise ValueError("missing root or invalid root verdict")
        actual = visit(ident)
        if actual != expected:
            raise ValueError("root verdict disagrees with its proof")
        root_receipts.append({"id": root_id, "root": ident, "verdict": actual})
    if len(done) != len(nodes):
        raise ValueError("proof bundle contains nodes unreachable from every root")
    return {"roots": root_receipts, "nodes": len(done),
            "edges": sum(len(node["edges"]) for node in nodes.values()),
            "terminal_nodes": sum(bool(node["terminal"]) for node in nodes.values()),
            "trusted_leaves": 0}


def read_trace_bundle(path):
    roots, nodes, edge_rows = [], {}, {}
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8", newline="") as stream:
        first = stream.readline().rstrip("\r\n")
        if not first.startswith("# kyouen-proof-trace-bundle-v1,"):
            raise ValueError("missing shared proof trace bundle header")
        header = dict(item.split("=", 1) for item in first[2:].split(",")[1:])
        board_size = int(header["n"])
        for row in csv.reader(stream):
            if not row:
                continue
            if row[0] == "R" and len(row) == 5:
                roots.append({"id": row[1],
                              "root": str(int(row[2]) | (int(row[3]) << 64)),
                              "verdict": int(row[4])})
            elif row[0] == "N" and len(row) == 6:
                mask = int(row[1]) | (int(row[2]) << 64)
                ident = str(mask)
                if ident in nodes:
                    raise ValueError("duplicate proof node in shared trace")
                terminal_mark = int(row[4])
                if terminal_mark not in (0, 1):
                    raise ValueError("invalid terminal marker in shared trace")
                nodes[ident] = {"mask": ident, "stones": mask.bit_count(),
                                "verdict": int(row[3]), "terminal": bool(terminal_mark),
                                "legal_count": int(row[5]), "edges": []}
                edge_rows[ident] = []
            elif row[0] == "E" and len(row) == 6:
                parent = str(int(row[1]) | (int(row[2]) << 64))
                move = int(row[3])
                child = str(int(row[4]) | (int(row[5]) << 64))
                edge_rows.setdefault(parent, []).append({"move": move, "child": child})
            else:
                raise ValueError("malformed shared proof trace row")
    if not roots:
        raise ValueError("proof trace bundle has no roots")
    for parent, edges in edge_rows.items():
        if parent not in nodes:
            raise ValueError("edge appears without a node")
        nodes[parent]["edges"] = edges
    for node in nodes.values():
        for edge in node["edges"]:
            if edge["child"] not in nodes:
                raise ValueError("proof trace references a missing child")
    return {"schema": "kyouen-proof-dag-multi-root-v1", "board_size": board_size,
            "proposition": "original_first_player_wins", "roots": roots, "nodes": nodes}


def verify_bundle(certificate):
    if certificate.get("schema") != "kyouen-proof-dag-multi-root-v1":
        raise ValueError("unsupported shared proof bundle schema")
    if certificate.get("proposition") != "original_first_player_wins":
        raise ValueError("unsupported proposition")
    if "trusted" in certificate or "trusted_leaves" in certificate:
        raise ValueError("trusted leaves are forbidden")
    return _check_graph(certificate.get("board_size"), certificate.get("roots"),
                        certificate.get("nodes"))


def verify_trace(path):
    certificate = read_trace_bundle(Path(path))
    receipt = verify_bundle(certificate)
    return certificate, receipt


def verify_saved(path):
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        certificate = json.load(stream)
    return verify_bundle(certificate)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--trace", type=Path)
    group.add_argument("--certificate", type=Path)
    ap.add_argument("--out", type=Path,
                    help="save a deterministically compressed bundle when verifying a trace")
    ap.add_argument("--receipt", type=Path,
                    help="write the verification receipt to this path")
    args = ap.parse_args()
    if args.trace:
        certificate, receipt = verify_trace(args.trace)
        if args.out:
            if args.out.exists():
                ap.error(f"refusing to overwrite {args.out}")
            payload = (json.dumps(certificate, sort_keys=True,
                                  separators=(",", ":")) + "\n").encode()
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_bytes(gzip.compress(payload, mtime=0))
    elif args.out:
        ap.error("--out is only valid with --trace")
    else:
        receipt = verify_saved(args.certificate)
    if args.receipt:
        if args.receipt.exists():
            ap.error(f"refusing to overwrite {args.receipt}")
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(receipt, sort_keys=True,
                                          separators=(",", ":")) + "\n",
                                encoding="utf-8")
    print(json.dumps(receipt, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
