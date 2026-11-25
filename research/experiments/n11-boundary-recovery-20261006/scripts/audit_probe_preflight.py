#!/usr/bin/env python3
"""Fail-closed source binding for a dual-tight s5 probe (no verdict inference).

A raw-history audit may exclude previously budget-exhausted UNKNOWN keys. A
saved-s6 audit must cover the *same* parent keys, not merely the same count.
Both audits must refer to the exact cache and target input being dispatched.
"""
from __future__ import annotations


def _keys(rows, *, label):
    try:
        values = [tuple(map(int, row)) for row in rows]
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label}: malformed canonical keys") from exc
    if any(len(key) != 2 for key in values) or len(set(values)) != len(values):
        raise ValueError(f"{label}: duplicate or malformed canonical keys")
    return set(values)


def validate_audits(target_keys, target_sha, cache_sha, raw, saved, budget):
    """Return (ready_keys, blocked_keys); reject stale, mixed or unsafe audits.

    ``target_keys`` is the canonical s5 key set from the actual target CSV.
    A same/higher-budget UNKNOWN is excluded from direct replay, never treated
    as a LOSS/WIN. Any exact hit requires cache reconciliation before dispatch.
    """
    target_keys = set(target_keys)
    if not target_keys or budget < 1:
        raise ValueError("empty target set or invalid budget")
    if raw.get("schema") != "n11-s5-raw-history-audit-v1":
        raise ValueError("unexpected raw-history audit schema")
    if raw.get("requested_budget") != budget:
        raise ValueError("raw-history audit budget is missing or differs; rerun audit")
    raw_targets = raw.get("targets", {})
    if (raw_targets.get("sha256") != target_sha
            or raw_targets.get("count") != len(target_keys)
            or _keys(raw_targets.get("keys", []), label="raw targets") != target_keys):
        raise ValueError("raw-history audit is not bound to the current targets")
    raw_cache = raw.get("current_cache", {})
    if (raw_cache.get("sha256") != cache_sha
            or raw_cache.get("target_exact_intersection") != 0
            or raw_cache.get("hits")):
        raise ValueError("raw-history audit is stale or cache has target hits")
    if raw.get("exact_verdict_conflicts") or raw.get("prior_exact"):
        raise ValueError("raw-history contains a conflict or unmerged exact result")
    blocked_rows = raw.get("prior_unknown_same_budget_or_higher", [])
    if not isinstance(blocked_rows, list):
        raise ValueError("malformed blocked history")
    try:
        blocked = {tuple(map(int, row["key"])) for row in blocked_rows}
        if any(len(row["key"]) != 2 or row["verdict"] != 0
               or row["budget"] < budget for row in blocked_rows):
            raise ValueError("blocked history is not a same-budget UNKNOWN")
    except (TypeError, KeyError) as exc:
        raise ValueError("malformed blocked history") from exc
    if not blocked <= target_keys:
        raise ValueError("blocked history contains keys outside the target set")
    ready = _keys(raw.get("dispatch_ready_keys", []), label="dispatch-ready")
    if ready != target_keys - blocked:
        raise ValueError("dispatch-ready set does not equal targets minus blocked UNKNOWNs")

    if saved.get("schema") != "n11-next3-saved-s6-parent-boundary-audit-v1":
        raise ValueError("unexpected saved-s6 audit schema")
    if saved.get("current_cache", {}).get("sha256") != cache_sha:
        raise ValueError("saved-s6 audit was made against a different exact cache")
    saved_targets = saved.get("targets", {})
    if saved_targets.get("sha256") != target_sha:
        raise ValueError("saved-s6 audit is not bound to the current target file")
    parents = saved_targets.get("parents", [])
    try:
        saved_keys = _keys((row["key"] for row in parents), label="saved-s6 parents")
    except (TypeError, KeyError) as exc:
        raise ValueError("malformed saved-s6 parents") from exc
    if (saved_keys != target_keys
            or any(row.get("outcome") != "UNKNOWN" for row in parents)
            or saved.get("targets", {}).get("status_counts") != {"UNKNOWN": len(target_keys)}):
        raise ValueError("saved-s6 audit is not bound to the same UNKNOWN parents")
    comparison = saved.get("cache_comparison", {})
    if (comparison.get("new_exact") != 0
            or comparison.get("unknown_parents") != len(target_keys)
            or comparison.get("opposite_verdict_conflicts")):
        raise ValueError("saved-s6 audit contains new exact results or conflicts")
    sources = saved.get("source_audit", {})
    if (sources.get("exact_conflict_count") != 0
            or sources.get("source_hashes_validated") is not True):
        raise ValueError("saved-s6 source evidence has not passed hash/conflict checks")
    return ready, blocked
