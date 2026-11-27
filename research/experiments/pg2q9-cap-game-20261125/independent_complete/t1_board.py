"""Task 1: verify the board is PG(2,9), with an explicit isomorphism."""

from __future__ import annotations

import json
import time

import pg


def main():
    t0 = time.time()
    n, b, blocks = pg.load_board()
    board_axioms, bdata = pg.check_plane(n, b, blocks)

    field = pg.check_field()
    m_points, m_index, m_lines = pg.build_model()
    model_axioms, mdata = pg.check_plane(len(m_points), len(m_lines), m_lines)

    phi, b_frame, m_frame, nodes = pg.find_isomorphism(n, blocks, m_points, m_lines)
    iso_ok = pg.verify_isomorphism(phi, n, blocks, m_lines)

    # Also verify inverse and that all model lines have a board preimage line.
    inv = {v: k for k, v in phi.items()}
    inv_ok = True
    board_linesets = {frozenset(B) for B in blocks}
    for B in m_lines:
        img = frozenset(inv[p] for p in B)
        if img not in board_linesets:
            inv_ok = False
            break

    out = {
        "board_axioms": board_axioms,
        "field": field,
        "model_axioms": model_axioms,
        "isomorphism": {
            "found": iso_ok,
            "inverse_found": inv_ok,
            "search_nodes": nodes,
            "board_frame": list(b_frame),
            "model_frame": list(m_frame),
            "phi_board_to_model": [phi[i] for i in range(n)],
        },
        "seconds": round(time.time() - t0, 3),
    }
    (pg.HERE / "out").mkdir(exist_ok=True)
    (pg.HERE / "out" / "t1_board.json").write_text(
        json.dumps(out, indent=1), encoding="utf-8"
    )
    print("board axioms:", board_axioms)
    print("field:", field)
    print("model axioms:", model_axioms)
    print("isomorphism found:", iso_ok, "inverse:", inv_ok, "nodes:", nodes)
    print("board frame:", b_frame, "model frame:", m_frame)
    print("seconds:", out["seconds"])
    assert board_axioms["all_ok"] and model_axioms["all_ok"]
    assert iso_ok and inv_ok
    assert all(field[k] for k in field if k not in ("mult_group_profile",))


if __name__ == "__main__":
    main()
