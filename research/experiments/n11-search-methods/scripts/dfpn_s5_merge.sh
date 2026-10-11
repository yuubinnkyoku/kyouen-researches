#!/usr/bin/env bash
# Deterministic, fail-closed and atomic merge of 11x11 S5 worker verdict caches.
# Existing output is also an input: cooperative writers cannot silently lose rows.
# Usage: dfpn_s5_merge.sh <out.csv> <base.csv> [worker.csv ...]
set -euo pipefail
if (( $# < 2 )); then
  echo 'usage: dfpn_s5_merge.sh <out.csv> <base.csv> [worker.csv ...]' >&2
  exit 2
fi
SCRIPT_PATH="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")"
python3 - "$SCRIPT_PATH" "$@" <<'PY'
import csv
import os
from pathlib import Path
import sys
import tempfile

script = Path(sys.argv[1]).resolve()
root = script.parents[4]
output = Path(sys.argv[2]).resolve()
inputs = [Path(p) for p in sys.argv[3:]]
policy_dir = root / 'research/experiments/n11-frontier-selection-20261005/scripts'
sys.path.insert(0, str(policy_dir))
try:
    from s5_evidence_policy import REGISTRY, quarantined_cache_keys
    # The current policy may silently return an empty set when the registry
    # is missing. Require the evidence registry even before that is fixed.
    # Serialize cooperative writers BEFORE reading any evidence. Locking the
    # output inode is unsafe: os.replace swaps it, so use a stable lock file.
    # The descriptor stays open until this short-lived process exits.
    output.parent.mkdir(parents=True, exist_ok=True)
    # Never follow a sidecar alias: on POSIX it can make two writers lock
    # different inodes after os.replace; on Windows an empty alias target
    # could also receive the msvcrt byte-lock marker.  O_NOFOLLOW closes
    # the check/open race where supported.
    import stat
    lock_path = str(output) + '.lock'
    if os.path.islink(lock_path):
        raise ValueError(f'symlinked S5 cache lock is unsafe: {lock_path}')
    flags = os.O_CREAT | os.O_RDWR | getattr(os, 'O_NOFOLLOW', 0)
    lock_fd = os.open(lock_path, flags, 0o600)
    lock_stat = os.fstat(lock_fd)
    if not stat.S_ISREG(lock_stat.st_mode) or lock_stat.st_nlink != 1:
        raise ValueError(f'non-unique/nonregular S5 cache lock is unsafe: {lock_path}')
    if os.name == 'nt':
        # Windows Python has no fcntl. Lock a stable byte instead of the
        # replaceable destination inode, and keep the descriptor until exit.
        import msvcrt
        if os.fstat(lock_fd).st_size == 0:
            os.write(lock_fd, b'\0')
        os.lseek(lock_fd, 0, os.SEEK_SET)
        msvcrt.locking(lock_fd, msvcrt.LK_LOCK, 1)
    else:
        import fcntl
        fcntl.flock(lock_fd, fcntl.LOCK_EX)
    # Hard links are not resolved by Path.resolve(). Replacing one name would
    # silently split the inode and let another writer commit to the old name.
    # Reject this unsafe alias class rather than pretending sidecar locks
    # coordinate names that are not uniquely identifiable.
    existing_mode = None
    if output.exists():
        existing_stat = output.stat()
        if not stat.S_ISREG(existing_stat.st_mode):
            raise ValueError(f'nonregular S5 cache output is unsafe: {output}')
        if existing_stat.st_nlink != 1:
            raise ValueError(f'hard-linked S5 cache output is unsafe: {output}')
        # Atomic replacement otherwise resets the destination to the
        # NamedTemporaryFile default (0600), breaking existing group readers.
        # Only preserve ordinary permission bits, never setuid/setgid/sticky.
        existing_mode = stat.S_IMODE(existing_stat.st_mode) & 0o777
    # Always union with a previously committed destination, including when
    # another worker has just finished. Revalidate it like every other input.
    if output.is_file() and all(output.resolve() != p.resolve() for p in inputs):
        inputs.append(output)

    if not REGISTRY.is_file():
        raise ValueError(f'missing S5 evidence quarantine registry: {REGISTRY}')
    quarantine = quarantined_cache_keys()
    if not isinstance(quarantine, set):
        raise ValueError('invalid S5 quarantine result')

    # Validate keys independently of the producer: only canonical SAFE
    # five-stone states are admissible.  Otherwise a D4 alias could bypass
    # the per-key WIN/LOSS conflict check.
    def canonical_and_safe(lo, hi):
        pts = [i for i in range(121)
               if ((lo if i < 64 else hi) >> (i % 64)) & 1]
        if len(pts) != 5:
            return False
        masks = []
        for reflection in (False, True):
            for rotation in range(4):
                mask = 0
                for p in pts:
                    x, y = p % 11, p // 11
                    if reflection:
                        x = 10 - x
                    for _ in range(rotation):
                        x, y = y, 10 - x
                    mask |= 1 << (11 * y + x)
                masks.append((mask & ((1 << 64) - 1), mask >> 64))
        if (lo, hi) != min(masks, key=lambda k: (k[1], k[0])):
            return False
        from itertools import combinations
        for four in combinations(pts, 4):
            coords = [(v % 11, v // 11) for v in four]
            x0, y0 = coords[-1]
            a, b, c = [((x*x + y*y) - (x0*x0 + y0*y0),
                         x-x0, y-y0) for x, y in coords[:-1]]
            det = (a[0]*(b[1]*c[2]-b[2]*c[1])
                   -a[1]*(b[0]*c[2]-b[2]*c[0])
                   +a[2]*(b[0]*c[1]-b[1]*c[0]))
            if det == 0:
                return False
        return True

    # Validate ALL sources and ALL conflicts before opening the output.
    verdicts = {}
    unknown = quarantined = 0
    for path in inputs:
        if not path.is_file():
            raise ValueError(f'missing S5 cache input: {path}')
        with path.open(newline='', encoding='utf-8') as stream:
            for lineno, row in enumerate(csv.reader(stream), 1):
                if not row or (row[0].strip().startswith('#')):
                    continue
                if len(row) != 6 or row[0] != 's5verdict':
                    raise ValueError(f'invalid S5 cache row: {path}:{lineno}')
                try:
                    lo, hi, stones, result, nodes = map(int, row[1:])
                except ValueError as exc:
                    raise ValueError(f'noninteger S5 cache row: {path}:{lineno}') from exc
                if (stones != 5 or result not in (0, 1, 2) or nodes < 0
                        or not (0 <= lo < 2**64 and 0 <= hi < 2**57)
                        or lo.bit_count() + hi.bit_count() != 5):
                    raise ValueError(f'invalid S5 evidence: {path}:{lineno}')
                if not canonical_and_safe(lo, hi):
                    raise ValueError(f'noncanonical or unsafe S5 key: {path}:{lineno}')
                if result == 0:
                    unknown += 1
                    continue
                key = (lo, hi)
                previous = verdicts.get(key)
                if previous is not None and previous[0] != result:
                    raise ValueError(f'CONFLICT key={key}: {previous[0]} vs {result} at {path}:{lineno}')
                if previous is None:
                    verdicts[key] = (result, nodes)
                else:
                    # Same exact verdict, different search costs: order-independent.
                    verdicts[key] = (result, min(previous[1], nodes))
    for key in quarantine:
        if key in verdicts:
            del verdicts[key]
            quarantined += 1

    output.parent.mkdir(parents=True, exist_ok=True)
    name = None
    try:
        with tempfile.NamedTemporaryFile('w', encoding='utf-8', newline='',
                dir=output.parent, prefix=f'.{output.name}.', suffix='.tmp',
                delete=False) as stream:
            name = stream.name
            stream.write('# s5 verdict cache: n=11 schema=1 (canonical key -> WIN/LOSS, UNKNOWN never stored)\n')
            for (lo, hi), (result, nodes) in sorted(verdicts.items()):
                stream.write(f's5verdict,{lo},{hi},5,{result},{nodes}\n')
            stream.flush()
            if existing_mode is not None:
                if hasattr(os, 'fchmod'):
                    os.fchmod(stream.fileno(), existing_mode)
                else:
                    os.chmod(stream.name, existing_mode)
            os.fsync(stream.fileno())
        os.replace(name, output)
    finally:
        if name is not None and os.path.exists(name):
            os.unlink(name)
    print(f'merged keys: {len(verdicts)}; UNKNOWN dropped: {unknown}; quarantined keys: {quarantined}')
    print(f'written: {output}')
    print('MERGE_OK')
except (OSError, ValueError, ImportError) as exc:
    print(f'MERGE_REFUSED: {exc}', file=sys.stderr)
    sys.exit(1)
PY
