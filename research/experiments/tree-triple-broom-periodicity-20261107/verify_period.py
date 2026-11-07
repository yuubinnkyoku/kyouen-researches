#!/usr/bin/env python3
"""Finite induction certificate, not extrapolation of a long prefix."""
from functools import lru_cache
import json
from pathlib import Path


def mex(values):
    value = 0
    while value in values:
        value += 1
    return value


def sequences(limit):
    path, broom = [0, 1], [2, 1]
    for n in range(2, limit + 1):
        path.append(mex({path[n - 2]} | {
            path[i] ^ path[n - 3 - i] for i in range(n - 2)}))
        broom.append(mex({1 ^ path[n], path[n - 1], path[n - 2], broom[n - 2]} | {
            broom[i] ^ path[n - 3 - i] for i in range(n - 2)}))
    return path, broom


def broom_edges(length):
    return [(0, v) for v in (1, 2, 3)] + (
        [(0, 4)] + [(v, v + 1) for v in range(4, length + 3)] if length else [])


def direct_subset_game(length, triple):
    """Raw occupied subsets: no path splitting, twin reduction or recurrence."""
    n = length + 4
    forbidden = [(1 << a) | (1 << b) for a, b in broom_edges(length)]
    if triple:
        forbidden.append(14)

    @lru_cache(None)
    def game(occupied):
        options = set()
        for v in range(n):
            if occupied >> v & 1:
                continue
            child = occupied | (1 << v)
            if all(child & h != h for h in forbidden):
                options.add(game(child))
        return mex(options)

    value = game(0)
    return value, game.cache_info().currsize


def closed_neighborhood_game(length):
    """A third formulation for the pair-only game: delete closed neighborhoods."""
    n = length + 4
    neighborhoods = [1 << i for i in range(n)]
    for a, b in broom_edges(length):
        neighborhoods[a] |= 1 << b
        neighborhoods[b] |= 1 << a

    @lru_cache(None)
    def game(available):
        return mex({game(available & ~neighborhoods[v])
                    for v in range(n) if available >> v & 1})

    return game((1 << n) - 1)


def certify_period(sequence, start, period):
    # proof.md proves why this finite comparison window implies all later n.
    last_comparison = 2 * start + period + 1
    assert len(sequence) > last_comparison + period
    assert all(sequence[n] == sequence[n + period]
               for n in range(start, last_comparison + 1))
    block = sequence[start:start + period]
    assert all(any(block[j] != block[(j + shift) % period] for j in range(period))
               for shift in range(1, period))
    assert sequence[start - 1] != sequence[start - 1 + period]
    return dict(start=start, period=period, comparisons=[start, last_comparison],
                values_needed_through=last_comparison + period,
                last_failure=[start - 1, sequence[start - 1], sequence[start - 1 + period]],
                block=block)


def main():
    # 691 is enough for the joint induction certificate. Extra 1500 checks are
    # diagnostics and do not replace that induction argument.
    path, broom = sequences(1502)
    p_certificate = certify_period(path, 52, 34)
    b_certificate = certify_period(broom, 311, 34)
    assert all(path[n] == path[n + 34] for n in range(311, 658))
    direct = []
    for length in range(19):
        pair, pair_states = direct_subset_game(length, False)
        full, full_states = direct_subset_game(length, True)
        assert pair == path[length + 2] == closed_neighborhood_game(length)
        assert full == broom[length]
        direct.append(dict(length=length, pair=pair, full=full,
                           pair_safe_states=pair_states, full_safe_states=full_states))
    residue_table = [dict(residue=r, full=broom[340 + r], pair=path[342 + r]) for r in range(34)]
    inert = [row["residue"] for row in residue_table if row["full"] == row["pair"]]
    flips = [row["residue"] for row in residue_table if (row["full"] == 0) != (row["pair"] == 0)]
    assert inert == [5, 12]
    assert flips == [2, 6, 13, 18, 22, 26, 32]
    assert max(broom[:692]) == 15
    for radius in (1, 10, 100, 1000, 10 ** 6):
        # Same rooted radius-R ball, same tail parity, same marked Steiner tree.
        block = (max(radius, 311) + 34) // 34
        a, b = 34 * block + 5, 34 * block + 13
        assert a > radius and b > radius and a % 2 == b % 2
        assert residue_table[a % 34]["full"] == residue_table[a % 34]["pair"]
        assert (residue_table[b % 34]["full"] == 0) != (residue_table[b % 34]["pair"] == 0)
    output = dict(audit="PASS", path_certificate=p_certificate,
                  joint_broom_certificate=b_certificate,
                  independent_subset_checks=len(direct) * 2,
                  independent_pair_neighborhood_checks=len(direct),
                  safe_subset_states=sum(row["pair_safe_states"] + row["full_safe_states"] for row in direct),
                  inert_residues=inert, winner_flip_residues=flips,
                  residue_table=residue_table, direct_small_games=direct,
                  values={"path": path[:694], "broom": broom[:692]})
    target = Path(__file__).with_name("output") / "period_audit.json"
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in output.items()
                      if key not in {"values", "residue_table", "direct_small_games"}}, indent=2))


if __name__ == "__main__":
    main()
