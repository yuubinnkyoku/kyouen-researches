import Kyouen.Rules
import Kyouen.UniformCapacity

/-! General consequences of the executable rules and ranked game interface.
No finite-board enumeration or additional axioms are used. -/
namespace Kyouen.StructuralConsequences

open SquareBoard

theorem winning_iff_exists_losing {σ : Type} (m : σ → List σ) (s : σ) :
    Winning m s ↔ ∃ t, t ∈ m s ∧ Losing m t := by
  constructor
  · intro h; cases h with | move ht hl => exact ⟨_, ht, hl⟩
  · rintro ⟨t, ht, hl⟩; exact Winning.move ht hl

theorem losing_iff_all_winning {σ : Type} (m : σ → List σ) (s : σ) :
    Losing m s ↔ ∀ t, t ∈ m s → Winning m t := by
  constructor
  · intro h; cases h with | all h => exact h
  · exact Losing.all

theorem terminal_losing {σ : Type} {m : σ → List σ} {s : σ}
    (h : m s = []) : Losing m s := by
  apply Losing.all
  simp [h]

theorem terminal_not_winning {σ : Type} {m : σ → List σ} {s : σ}
    (h : m s = []) : ¬ Winning m s := by
  rw [winning_iff_exists_losing]
  simp [h]

theorem winning_has_move {σ : Type} {m : σ → List σ} {s : σ}
    (h : Winning m s) : m s ≠ [] := by
  intro he
  exact terminal_not_winning he h

theorem unique_child_winning_iff {σ : Type} {m : σ → List σ} {s t : σ}
    (h : m s = [t]) : Winning m s ↔ Losing m t := by
  rw [winning_iff_exists_losing, h]
  simp

theorem unique_child_losing_iff {σ : Type} {m : σ → List σ} {s t : σ}
    (h : m s = [t]) : Losing m s ↔ Winning m t := by
  rw [losing_iff_all_winning, h]
  simp

theorem forbidden_iff_witness {n : Nat} (s : Position n) :
    ContainsForbidden s ↔ ∃ a ∈ s, ∃ b ∈ s, ∃ c ∈ s, ∃ d ∈ s,
      ForbiddenFour a b c d := by
  simp [ContainsForbidden, containsForbiddenBool, List.any_eq_true]

theorem forbidden_monotone {n : Nat} {s t : Position n}
    (hst : ∀ p, p ∈ s → p ∈ t) (h : ContainsForbidden s) : ContainsForbidden t := by
  obtain ⟨a, ha, b, hb, c, hc, d, hd, hf⟩ := (forbidden_iff_witness s).mp h
  exact (forbidden_iff_witness t).mpr
    ⟨a, hst a ha, b, hst b hb, c, hst c hc, d, hst d hd, hf⟩

theorem safe_hereditary {n : Nat} {s t : Position n}
    (hst : ∀ p, p ∈ s → p ∈ t) (h : ¬ ContainsForbidden t) : ¬ ContainsForbidden s :=
  fun hs => h (forbidden_monotone hst hs)

theorem forbidden_cons {n : Nat} {s : Position n} (p : Point n)
    (h : ContainsForbidden s) : ContainsForbidden (p :: s) :=
  forbidden_monotone (by intro q hq; exact List.mem_cons_of_mem p hq) h

theorem safe_of_safe_cons {n : Nat} {s : Position n} {p : Point n}
    (h : ¬ ContainsForbidden (p :: s)) : ¬ ContainsForbidden s :=
  fun hs => h (forbidden_cons p hs)

theorem legal_result_safe {n : Nat} {s : Position n} {p : Point n}
    (h : LegalMove s p) : ¬ ContainsForbidden (p :: s) := h.2

theorem legal_source_safe {n : Nat} {s : Position n} {p : Point n}
    (h : LegalMove s p) : ¬ ContainsForbidden s := safe_of_safe_cons h.2

theorem occupied_not_legal {n : Nat} {s : Position n} {p : Point n}
    (h : p ∈ s) : ¬ LegalMove s p := fun hl => hl.1 h

theorem forbidden_not_legal {n : Nat} {s : Position n}
    (h : ContainsForbidden s) (p : Point n) : ¬ LegalMove s p :=
  fun hl => legal_source_safe hl h

theorem legal_hereditary {n : Nat} {s t : Position n} {p : Point n}
    (hst : ∀ q, q ∈ s → q ∈ t) (h : LegalMove t p) : LegalMove s p := by
  refine ⟨fun hp => h.1 (hst p hp), ?_⟩
  apply safe_hereditary (t := p :: t) _ h.2
  intro q hq
  rcases List.mem_cons.mp hq with he | hs
  · exact List.mem_cons.mpr (Or.inl he)
  · exact List.mem_cons.mpr (Or.inr (hst q hs))

theorem legal_preserves_nodup {n : Nat} {s : Position n} {p : Point n}
    (hs : s.Nodup) (h : LegalMove s p) : (p :: s).Nodup :=
  List.nodup_cons.mpr ⟨h.1, hs⟩

theorem legal_adds_one {n : Nat} (s : Position n) (p : Point n) :
    (p :: s).length = s.length + 1 := rfl

theorem legal_strict_length {n : Nat} (s : Position n) (p : Point n) :
    s.length < (p :: s).length := by simp

theorem legal_not_equal {n : Nat} (s : Position n) (p : Point n) : p :: s ≠ s := by
  intro h
  have := congrArg List.length h
  simp at this

theorem forbidden_membership_invariant {n : Nat} {s t : Position n}
    (h : ∀ p, p ∈ s ↔ p ∈ t) : ContainsForbidden s ↔ ContainsForbidden t :=
  ⟨forbidden_monotone (fun p => (h p).mp),
   forbidden_monotone (fun p => (h p).mpr)⟩

theorem legal_membership_invariant {n : Nat} {s t : Position n}
    (h : ∀ p, p ∈ s ↔ p ∈ t) (p : Point n) : LegalMove s p ↔ LegalMove t p := by
  have hc : ContainsForbidden (p :: s) ↔ ContainsForbidden (p :: t) :=
    forbidden_membership_invariant (by intro q; simp only [List.mem_cons, h q])
  simp only [LegalMove, h p, hc]

open Grundy

theorem terminal_iff_capacity {σ : Type} {G : Game σ} {size : σ → Nat} {cap : Nat}
    (h : UniformTerminal G size cap) (s : σ) : G.children s = [] ↔ size s = cap := by
  constructor
  · intro hs
    have hb := h.bounded s
    by_cases he : size s = cap
    · exact he
    · exact False.elim (h.progress s (by omega) hs)
  · exact h.terminal s

theorem remaining_zero_iff_capacity {σ : Type} {G : Game σ} {size : σ → Nat} {cap : Nat}
    (h : UniformTerminal G size cap) (s : σ) : remaining size cap s = 0 ↔ size s = cap := by
  have hb := h.bounded s
  unfold remaining
  omega

theorem terminal_iff_remaining_zero {σ : Type} {G : Game σ} {size : σ → Nat} {cap : Nat}
    (h : UniformTerminal G size cap) (s : σ) : G.children s = [] ↔ remaining size cap s = 0 := by
  rw [terminal_iff_capacity h, remaining_zero_iff_capacity h]

theorem move_decreases_remaining {σ : Type} {G : Game σ} {size : σ → Nat} {cap : Nat}
    (h : UniformTerminal G size cap) {s t : σ} (ht : t ∈ G.children s) :
    remaining size cap t < remaining size cap s := by
  have := remaining_step h ht
  omega

theorem two_moves_remaining {σ : Type} {G : Game σ} {size : σ → Nat} {cap : Nat}
    (h : UniformTerminal G size cap) {s t u : σ}
    (ht : t ∈ G.children s) (hu : u ∈ G.children t) :
    remaining size cap u + 2 = remaining size cap s := by
  have := remaining_step h ht
  have := remaining_step h hu
  omega

theorem capacity_losing {σ : Type} {G : Game σ} {size : σ → Nat} {cap : Nat}
    (h : UniformTerminal G size cap) {s : σ} (hs : size s = cap) : Losing G.children s :=
  terminal_losing (h.terminal s hs)

theorem capacity_grundy_zero {σ : Type} {G : Game σ} {size : σ → Nat} {cap : Nat}
    (h : UniformTerminal G size cap) {s : σ} (hs : size s = cap) : grundy G s = 0 :=
  grundy_of_no_children G s (h.terminal s hs)

theorem one_remaining_winning {σ : Type} {G : Game σ} {size : σ → Nat} {cap : Nat}
    (h : UniformTerminal G size cap) {s : σ} (hs : remaining size cap s = 1) :
    Winning G.children s := by
  apply winning_of_odd_remaining h s
  exact ⟨0, by omega⟩

theorem two_remaining_losing {σ : Type} {G : Game σ} {size : σ → Nat} {cap : Nat}
    (h : UniformTerminal G size cap) {s : σ} (hs : remaining size cap s = 2) :
    Losing G.children s := by
  apply losing_of_even_remaining h s
  exact ⟨1, by omega⟩

theorem singleton_safe {n : Nat} (p : Point n) : ¬ ContainsForbidden [p] := by
  simp [ContainsForbidden, containsForbiddenBool, ForbiddenFour]

theorem pair_safe {n : Nat} (p q : Point n) : ¬ ContainsForbidden [p, q] := by
  simp [ContainsForbidden, containsForbiddenBool, ForbiddenFour]

theorem triple_safe {n : Nat} (p q r : Point n) : ¬ ContainsForbidden [p, q, r] := by
  simp [ContainsForbidden, containsForbiddenBool, ForbiddenFour]

theorem singleton_legal_iff {n : Nat} (p q : Point n) : LegalMove [p] q ↔ q ≠ p := by
  simp [LegalMove, pair_safe]

theorem pair_legal_iff {n : Nat} (p q r : Point n) :
    LegalMove [p, q] r ↔ r ≠ p ∧ r ≠ q := by
  simp [LegalMove, triple_safe]

theorem child_iff {n : Nat} (s t : Position n) :
    t ∈ moves n s ↔ ∃ p, LegalMove s p ∧ t = p :: s := by
  simp only [moves, List.mem_filterMap]
  constructor
  · rintro ⟨p, _, hp⟩
    by_cases hl : LegalMove s p
    · simp only [hl, ↓reduceIte, Option.some.injEq] at hp
      exact ⟨p, hl, hp.symm⟩
    · simp [hl] at hp
  · rintro ⟨p, hl, rfl⟩
    exact ⟨p, by simp, by simp [hl]⟩

theorem child_length {n : Nat} {s t : Position n} (h : t ∈ moves n s) :
    t.length = s.length + 1 := by
  obtain ⟨p, _, rfl⟩ := (child_iff s t).mp h
  rfl

theorem child_strict_length {n : Nat} {s t : Position n} (h : t ∈ moves n s) :
    s.length < t.length := by have := child_length h; omega

theorem no_self_child {n : Nat} (s : Position n) : s ∉ moves n s := by
  intro h
  have := child_strict_length h
  omega

theorem child_safe {n : Nat} {s t : Position n} (h : t ∈ moves n s) :
    ¬ ContainsForbidden t := by
  obtain ⟨p, hp, rfl⟩ := (child_iff s t).mp h
  exact hp.2

theorem child_nodup {n : Nat} {s t : Position n} (hs : s.Nodup)
    (h : t ∈ moves n s) : t.Nodup := by
  obtain ⟨p, hp, rfl⟩ := (child_iff s t).mp h
  exact legal_preserves_nodup hs hp

theorem child_contains_parent {n : Nat} {s t : Position n} (h : t ∈ moves n s) :
    ∀ p, p ∈ s → p ∈ t := by
  obtain ⟨q, _, rfl⟩ := (child_iff s t).mp h
  intro p hp
  exact List.mem_cons_of_mem q hp

theorem forbidden_no_children {n : Nat} {s : Position n} (h : ContainsForbidden s) :
    moves n s = [] := by
  apply List.eq_nil_iff_forall_not_mem.mpr
  intro t ht
  obtain ⟨p, hp, _⟩ := (child_iff s t).mp ht
  exact forbidden_not_legal h p hp

theorem empty_has_every_singleton {n : Nat} (p : Point n) :
    [p] ∈ moves n (empty n) :=
  (child_iff _ _).mpr ⟨p, Rules.Basic.LegalMove_empty n p, rfl⟩

theorem no_two_cycle {n : Nat} {s t : Position n} (h : t ∈ moves n s) :
    s ∉ moves n t := by
  intro ht
  have := child_strict_length h
  have := child_strict_length ht
  omega

end Kyouen.StructuralConsequences
