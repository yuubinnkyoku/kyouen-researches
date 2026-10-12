"""Validate joint S4 choices against independently enumerated legal responses."""
from __future__ import annotations


def audit_joint_entries(entries, expected_paid, legal_options, s4_masks,
                        s4_cost, check_s4, failures):
    seen, union = set(), set()
    for pos, entry in enumerate(entries):
        if not isinstance(entry, dict):
            failures.append(f"joint entry {pos}: not an object")
            continue
        identity = tuple(entry.get(key) for key in ("first", "reply", "third"))
        if any(type(value) is not int for value in identity):
            failures.append(f"joint entry {pos}: invalid first/reply/third")
            continue
        if identity in seen:
            failures.append(f"joint entry {pos}: duplicate third {identity}")
            continue
        seen.add(identity)
        allowed = legal_options.get(identity)
        if allowed is None:
            failures.append(f"joint entry {pos}: unknown or free third {identity}")
            continue
        chosen = entry.get("s4_class_index")
        if type(chosen) is not int or not 0 <= chosen < len(s4_masks):
            failures.append(f"joint entry {pos}: invalid S4 index {chosen!r}")
            continue
        if chosen not in allowed:
            failures.append(f"joint entry {pos}: S4 {chosen} is not a legal response to {identity}")
            continue
        mask = entry.get("s4_mask")
        if (not isinstance(mask, list) or len(mask) != 2 or
                any(type(value) is not int or value < 0 for value in mask) or
                s4_masks[chosen] != mask[0] | (mask[1] << 64)):
            failures.append(f"joint entry {pos}: S4 mask mismatch for {identity}")
        count = entry.get("unknown_s5_children")
        if type(count) is not int or count != len(s4_cost[chosen]):
            failures.append(f"joint entry {pos}: unknown S5 count mismatch for {identity}")
        check_s4(chosen)
        union.update(s4_cost[chosen])
    if seen != expected_paid:
        failures.append(f"joint paid third set mismatch: missing={len(expected_paid - seen)}, "
                        f"extra={len(seen - expected_paid)}")
    return union
