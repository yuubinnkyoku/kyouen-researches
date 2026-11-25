#!/usr/bin/env python3
"""forbidgen_dump.py — writer wrapper: forbidgen.py catalog -> canonical text file.
Reuses forbidgen.py's exact functions unchanged (import), writes "n=<n>" header
+"a b c d" per quartet. Byte-identical to forbidgen's internal canonical text."""
import hashlib, itertools, sys
sys.path.insert(0, 'scripts')
import forbidgen

def main():
    n = int(sys.argv[1])
    out = sys.argv[2]
    cells = [(x, y) for y in range(n) for x in range(n)]
    quarts = []
    for combo in itertools.combinations(range(n * n), 4):
        pts = [cells[c] for c in combo]
        if forbidgen.collinear4(pts) or forbidgen.concyclic4(pts):
            quarts.append(list(combo))
    quarts.sort()
    text = "n=%d\n" % n + "".join(" ".join(map(str, q)) + "\n" for q in quarts)
    with open(out, 'w') as f:
        f.write(text)
    h = hashlib.sha256(text.encode()).hexdigest()
    print('{"n": %d, "count": %d, "sha256_quartetlist_text": "%s"}' % (n, len(quarts), h))

if __name__ == '__main__':
    main()
