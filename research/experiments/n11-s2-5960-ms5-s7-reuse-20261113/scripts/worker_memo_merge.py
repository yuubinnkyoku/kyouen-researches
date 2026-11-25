"""Sentinel-aware algebra for merging independent KYOEN memo records."""

UNBOUND = 255


def _check_depth(value):
    if not isinstance(value, int) or value < 0 or value > UNBOUND:
        raise ValueError("memo depth must be an integer in [0, 255]")


def max_bound(a, b):
    """Join two negative-depth bounds; 255 means absent and is the identity."""
    _check_depth(a)
    _check_depth(b)
    if a == UNBOUND:
        return b
    if b == UNBOUND:
        return a
    return max(a, b)


def bound_at_least(value, required):
    """Whether value retains at least the finite bound required by a seed.

    An absent required bound imposes no condition.  An absent final bound
    cannot satisfy a finite requirement.
    """
    _check_depth(value)
    _check_depth(required)
    if required == UNBOUND:
        return True
    if value == UNBOUND:
        return False
    return value >= required


def combine_values(win, lose, nowin, nolose, rec):
    """Combine (win, lose, nowin, nolose) records from independent workers.

    win/lose are best-known positive bounds (min); nowin/nolose are
    best-known negative bounds (max).  255 means no bound in every field,
    so it is the identity for min on positive fields and for max_bound on
    negative fields.
    """
    if len(rec) != 4:
        raise ValueError("memo record must contain four bounds")
    vals = (win, lose, nowin, nolose) + tuple(rec)
    for value in vals:
        _check_depth(value)
    return (min(win, rec[0]), min(lose, rec[1]),
            max_bound(nowin, rec[2]), max_bound(nolose, rec[3]))


def conflict_kind(win, lose, nowin, nolose):
    """Return the first logical contradiction present in a merged record."""
    if win < UNBOUND and lose < UNBOUND:
        return "win_and_lose"
    if win < UNBOUND and nowin < UNBOUND and nowin >= win:
        return "win_le_nowin"
    if lose < UNBOUND and nolose < UNBOUND and nolose >= lose:
        return "lose_le_nolose"
    return None
