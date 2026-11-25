"""Task 1: validate the three boards as s=2 incidence structures."""

from __future__ import annotations

import json

import g2common as C


def main():
    out = {}
    for name, path in C.BOARDS.items():
        n, blocks = C.load_board(path)
        checks = C.validate_board(n, blocks)
        checks["board_path"] = str(path.relative_to(C.REPO)).replace("\\", "/")
        checks["sha256"] = C.sha256(path)
        checks["size_bytes"] = path.stat().st_size
        out[name] = checks
        print(name)
        for key in (
            "n", "b", "k", "line_size_histogram", "point_degree",
            "pairs_seen", "pairs_possible", "pair_multiplicity_histogram",
            "line_intersection_size_histogram", "any_two_lines_meet_in_at_most_one_point",
            "each_pair_at_most_one_line", "each_pair_exactly_one_line",
            "uniform_line_size", "point_degree_constant",
            "parallel_class_count", "parallel_class_size_histogram",
            "parallel_classes_are_cliques", "parallel_class_count_is_k_plus_1",
            "every_two_lines_meet", "valid_s2_incidence_structure",
        ):
            print("  ", key, "=", checks.get(key))
        print()
    (C.OUT / "task1_boards.json").write_text(json.dumps(out, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
