"""Evidence-aware routing for fixed-first-player S5/S6 search.

The planner never assigns probabilities to unresolved outcomes.  It reuses
exact evidence first, then chooses work from the requested proof polarity.
"""

from __future__ import annotations

from typing import Mapping, Sequence

UNKNOWN = 0
WIN = 1
LOSS = 2


def fixed_first_outcome(
    stones: int, child_verdicts: Sequence[int], expected_children: int
) -> int:
    """Aggregate exact/unknown child values from the original first player's view.

    Even layers are OR; odd layers are AND.  Existential witnesses are decisive
    with a partial boundary.  Universal claims require the complete child set.
    """
    if stones < 0 or expected_children < 0 or len(child_verdicts) > expected_children:
        raise ValueError("invalid layer or child count")
    if any(value not in (UNKNOWN, WIN, LOSS) for value in child_verdicts):
        raise ValueError("invalid verdict")

    if stones % 2 == 0:
        if WIN in child_verdicts:
            return WIN
        if len(child_verdicts) != expected_children:
            return UNKNOWN
        return LOSS if all(value == LOSS for value in child_verdicts) else UNKNOWN

    if LOSS in child_verdicts:
        return LOSS
    if len(child_verdicts) != expected_children:
        return UNKNOWN
    return WIN if all(value == WIN for value in child_verdicts) else UNKNOWN


def _verified_independent_root(proof: Mapping[str, object] | None) -> int | None:
    if proof is None:
        return None
    verified = proof.get("verified")
    if verified is False:
        return None
    if verified is not True:
        raise ValueError("independent proof verified flag must be boolean")
    trusted = proof.get("trusted_leaf_count")
    verdict = proof.get("root_verdict")
    if type(trusted) is not int or trusted != 0:
        raise ValueError("an independent proof DAG must have zero integer trusted leaves")
    if type(verdict) is not int or verdict not in (WIN, LOSS):
        raise ValueError("a verified proof DAG needs an exact integer root verdict")
    return int(verdict)


def choose_strategy(
    *,
    goal: str,
    expected_s6_children: int,
    direct_s5_verdict: int = UNKNOWN,
    saved_s6_verdicts: Mapping[str, int] | None = None,
    s6_children: Sequence[str] | None = None,
    s6_cost_hints: Mapping[str, int] | None = None,
    direct_s5_attempted: bool = False,
    independent_proof: Mapping[str, object] | None = None,
    paired_profile: Mapping[str, object] | None = None,
) -> dict[str, object]:
    """Choose A-E only from exact evidence, proof polarity, and measured costs.

    Goals are ``s5_loss`` and ``s5_win``.  Cost hints only order probes; they
    never affect outcome claims.  A/B comparisons are used only when the caller
    supplies an explicitly same-environment completed profile.
    """
    if goal not in {"s5_loss", "s5_win"}:
        raise ValueError("goal must be s5_loss or s5_win")
    if expected_s6_children < 0:
        raise ValueError("expected child count must be nonnegative")
    if direct_s5_verdict not in (UNKNOWN, WIN, LOSS):
        raise ValueError("invalid direct S5 verdict")

    proof_verdict = _verified_independent_root(independent_proof)
    if proof_verdict is not None:
        return {
            "mode": "E",
            "action": "reuse_independent_proof_dag",
            "verdict": proof_verdict,
            "trust": "terminal-only independent proof; trusted leaves 0",
            "next_s6": [],
        }

    if direct_s5_verdict in (WIN, LOSS):
        return {
            "mode": "A",
            "action": "reuse_exact_direct_s5",
            "verdict": direct_s5_verdict,
            "trust": "solver-trusted exact replay unless separately proof-closed",
            "next_s6": [],
        }

    saved = dict(saved_s6_verdicts or {})
    if any(value not in (UNKNOWN, WIN, LOSS) for value in saved.values()):
        raise ValueError("invalid saved S6 verdict")
    children = list(s6_children) if s6_children is not None else None
    if children is not None:
        if len(children) != expected_s6_children or len(set(children)) != len(children):
            raise ValueError("S6 child key list must be complete and unique")
        if not set(saved).issubset(children):
            raise ValueError("saved S6 verdict refers to a non-child")
    recovered = fixed_first_outcome(5, list(saved.values()), expected_s6_children)
    if recovered in (WIN, LOSS):
        return {
            "mode": "C",
            "action": "reconstruct_from_saved_s6_boundary",
            "verdict": recovered,
            "trust": "solver-trusted S6 leaves unless independent proof DAGs are supplied",
            "next_s6": [],
        }

    costs = dict(s6_cost_hints or {})
    if any(not isinstance(value, int) or value < 0 for value in costs.values()):
        raise ValueError("S6 cost hints must be nonnegative node counts")

    if goal == "s5_loss":
        if children is None:
            pending: list[str] = []
        else:
            pending = [key for key in children if saved.get(key, UNKNOWN) == UNKNOWN]
        # The sort is a workload order only; it does not estimate which child
        # is LOSS. No target keys means the caller must finish geometry/raw
        # preflight before the plan can be dispatched.
        ordered = sorted(
            pending,
            key=lambda key: (costs.get(key, 2**63 - 1), children.index(key) if children else 0, key),
        )
        return {
            "mode": "D",
            "action": (
                "probe_s6_children_until_loss_witness_or_full_boundary"
                if children is not None
                else "materialize_target_s6_boundary_before_dispatch"
            ),
            "verdict": UNKNOWN,
            "trust": "no verdict inferred from probe order or partial S6 WIN values",
            "next_s6": ordered,
            "early_stop": "one exact S6 LOSS proves S5 LOSS; all S6 WIN proves S5 WIN",
            "cost_order_is_outcome_prediction": False,
        }

    # Proving S5 WIN requires every legal S6 child WIN.  A capped direct
    # UNKNOWN supplies no evidence that a full decomposition is cheaper.
    if paired_profile is not None and paired_profile.get("same_environment") is True:
        direct_nodes = paired_profile.get("direct_nodes")
        split_nodes = paired_profile.get("split_nodes")
        if (
            isinstance(direct_nodes, int)
            and isinstance(split_nodes, int)
            and direct_nodes > 0
            and split_nodes > 0
            and paired_profile.get("both_complete") is True
        ):
            mode = "A" if direct_nodes <= split_nodes else "B"
            return {
                "mode": mode,
                "action": "use_lower_measured_complete_cost",
                "verdict": UNKNOWN,
                "trust": "cost choice only; resulting exact values still require exact replay",
                "next_s6": [],
                "measured_nodes": {"direct": direct_nodes, "split": split_nodes},
            }

    return {
        "mode": None,
        "action": "require_same_environment_paired_benchmark",
        "verdict": UNKNOWN,
        "trust": "no unsupported cost or outcome prediction",
        "next_s6": [],
        "reason": (
            "S5 WIN requires all legal S6 children WIN; the available history does "
            "not establish that a complete split costs less than direct S5 DFPN."
        ),
        "direct_s5_attempted": direct_s5_attempted,
    }
