"""Aggregate complete legal child boundaries in the solver's FIXED-player view.

Values: 0 UNKNOWN, 1 original first player WIN, 2 original first player LOSS.
Never negate a child when changing stone count. Even layers are OR, odd AND.
"""

def outcome(stones, children, exact):
    vals = [exact.get(k, 0) for k in children]
    if any(v not in (0, 1, 2) for v in vals):
        raise ValueError('invalid exact verdict')
    if stones % 2 == 0:
        if 1 in vals:
            return 'WIN'
        return 'LOSS' if all(v == 2 for v in vals) else 'UNKNOWN'
    if 2 in vals:
        return 'LOSS'
    return 'WIN' if all(v == 1 for v in vals) else 'UNKNOWN'
