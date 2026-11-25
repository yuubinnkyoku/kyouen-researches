#!/usr/bin/env python3
"""AST-compare the sibling own build vs the published y=22 machine.

Docstrings are removed from both syntax trees (module + every function);
comments are ignored by the parser. The claim: the remaining syntax trees
are identical, i.e. the published machine is fully determined (modulo its
own docstring/comment prose) by the published sources plus the declared
transformation recipe.

Prints a per-topLevel-node diff when trees differ. Exit 0 iff identical.
"""
import ast
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OWN = HERE / "verify_y22_universal.py"
PUB = ROOT / "published/verify_y22_universal.py"


def strip_docstrings(tree: ast.Module) -> ast.Module:
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef,
                             ast.ClassDef)):
            body = node.body
            if (body and isinstance(body[0], ast.Expr)
                    and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                node.body = body[1:]
    return tree


def dump_nodes(path: Path):
    src = path.read_text(encoding="utf-8")
    tree = strip_docstrings(ast.parse(src))
    return [(getattr(n, "name", n.__class__.__name__),
             ast.dump(n, include_attributes=False)) for n in tree.body]


def main() -> int:
    own = dump_nodes(OWN)
    pub = dump_nodes(PUB)
    if own == pub:
        print("AST-IDENTICAL (docstrings stripped; comments ignored)")
        return 0
    print(f"DIFFERING: own {len(own)} nodes vs published {len(pub)} nodes")
    i = 0
    misses = 0
    while i < max(len(own), len(pub)):
        a = own[i] if i < len(own) else ("<none>", "")
        b = pub[i] if i < len(pub) else ("<none>", "")
        if a != b:
            misses += 1
            print(f"--- node {i}: own={a[0]} vs pub={b[0]}")
            if a[1] != b[1]:
                print(f"own dump: {a[1][:3000]}")
                print(f"pub dump: {b[1][:3000]}")
        i += 1
    print(f"total differing nodes: {misses}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
