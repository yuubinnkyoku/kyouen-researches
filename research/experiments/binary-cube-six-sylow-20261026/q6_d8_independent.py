"""Independent integer-only audit of D8 fixed support counts for q=6."""
from math import gcd, lcm


def permute(x, p):
    return sum(((x >> i) & 1) << p[i] for i in range(5))


def orbits(generators):
    remaining = set(range(32))
    result = []
    while remaining:
        orbit = {min(remaining)}
        stack = list(orbit)
        while stack:
            x = stack.pop()
            for g in generators:
                y = permute(x, g)
                if y not in orbit:
                    orbit.add(y)
                    stack.append(y)
        remaining -= orbit
        result.append(sorted(orbit))
    return result


def admissible(columns):
    k = len(columns)
    a = [[(x >> i) & 1 for x in columns] for i in range(5)]
    if len({tuple(row) for row in a}) != 5 or any(not any(row) for row in a):
        return False
    rank, pivots = 0, []
    for j in range(k):
        p = next((i for i in range(rank, 5) if a[i][j]), None)
        if p is None:
            continue
        a[rank], a[p] = a[p], a[rank]
        pivot = a[rank][j]
        for i in range(5):
            if i == rank or not a[i][j]:
                continue
            coefficient = a[i][j]
            row = [pivot * x - coefficient * y for x, y in zip(a[i], a[rank])]
            divisor = 0
            for x in row:
                divisor = gcd(divisor, abs(x))
            a[i] = [x // divisor for x in row] if divisor else row
        divisor = 0
        for x in a[rank]:
            divisor = gcd(divisor, abs(x))
        if divisor > 1:
            a[rank] = [x // divisor for x in a[rank]]
        pivots.append(j)
        rank += 1
        if rank == 5:
            break
    piv = [a[i][pivots[i]] for i in range(rank)]
    denominator = lcm(*piv)
    basis = [[x * (denominator // piv[i]) for x in a[i]] for i in range(rank)]
    count = 0
    for bits in range(1 << rank):
        if all(sum(basis[i][j] for i in range(rank) if bits >> i & 1)
               in (0, denominator) for j in range(k)):
            count += 1
            if count > 6:
                return False
    return count == 6


def count_fixed(generators, k):
    orbit_list = orbits(generators)
    sizes = [len(o) for o in orbit_list]
    candidates = valid = 0
    for mask in range(1 << len(orbit_list)):
        if sum(size for i, size in enumerate(sizes) if mask >> i & 1) != k:
            continue
        candidates += 1
        columns = [x for i, o in enumerate(orbit_list) if mask >> i & 1 for x in o]
        valid += admissible(columns)
    return candidates, valid


def main():
    rotation = (1, 2, 3, 0, 4)
    reflection = (3, 2, 1, 0, 4)
    half_turn = (2, 3, 0, 1, 4)
    diagonal = tuple(rotation[reflection[i]] for i in range(5))
    groups = {
        'D8': [rotation, reflection],
        'C4': [rotation],
        'V4a': [half_turn, reflection],
        'V4b': [half_turn, diagonal],
    }
    expected = {
        10: [(168, 94), (168, 94), (652, 380), (9620, 5108)],
        11: [(204, 142), (204, 142), (812, 564), (12792, 8320)],
        12: [(236, 178), (236, 178), (968, 766), (16060, 11908)],
        13: [(260, 211), (260, 211), (1108, 957), (19112, 15479)],
        14: [(280, 248), (280, 248), (1220, 1110), (21612, 18610)],
        15: [(300, 283), (300, 283), (1292, 1221), (23256, 20925)],
    }
    for k in range(10, 16):
        for (name, generators), want in zip(groups.items(), expected[k]):
            result = count_fixed(generators, k)
            assert result == want, (k, name, result, want)
            print(f'k={k} {name}: candidates={result[0]} valid={result[1]}')


if __name__ == '__main__':
    main()
