import Kyouen.CertificateSoundness
import Lean.Elab.Tactic.Omega

/-!
# Odd-threshold block games and the mirror strategy (K0337)

Blocks are predicates on a finite board; safety means fewer than `q` occupied
points in each block. Besides a fixed-point-free involution preserving blocks,
we require every block containing a mirror pair to be invariant. Mere symmetry
of an odd-uniform forbidden hypergraph does not imply this hypothesis.
-/

namespace Kyouen.OddInvolution

variable {α : Type} [DecidableEq α]

/-- Symmetry is membership invariance, independent of list ordering. -/
def Symmetric (τ : α → α) (s : List α) : Prop :=
  ∀ x, τ x ∈ s ↔ x ∈ s

/-- A finite set with a fixed-point-free involution has even cardinality. -/
theorem even_length (τ : α → α) (hinv : ∀ x, τ (τ x) = x)
    (hfree : ∀ x, τ x ≠ x) (s : List α) (hn : s.Nodup)
    (hs : Symmetric τ s) : s.length % 2 = 0 := by
  have aux : ∀ k (l : List α), l.length = k → l.Nodup →
      Symmetric τ l → l.length % 2 = 0 := by
    intro k
    induction k using Nat.strongRecOn with
    | ind k ih =>
      intro l hl hn hs
      cases l with
      | nil => rfl
      | cons a l =>
        have ha : a ∉ l := (List.nodup_cons.mp hn).1
        have hnl := (List.nodup_cons.mp hn).2
        have hta : τ a ∈ l := by
          have := (hs a).2 (by simp)
          simpa [hfree a] using this
        have he : (l.erase (τ a)).length = l.length - 1 :=
          List.length_erase_of_mem hta
        have hsym : Symmetric τ (l.erase (τ a)) := by
          intro x
          simp only [hnl.mem_erase_iff]
          have h1 := hs x
          simp only [List.mem_cons] at h1
          constructor
          · rintro ⟨htne, htl⟩
            have hxa : x ≠ a := by intro h; subst x; exact htne rfl
            have hxta : x ≠ τ a := by
              intro h
              subst x
              exact ha (by simpa only [hinv] using htl)
            exact ⟨hxta, (h1.mp (by simp [htl])).resolve_left hxa⟩
          · rintro ⟨hxne, hxl⟩
            have htne : τ x ≠ τ a := by
              intro h
              have : x = a := by simpa only [hinv] using congrArg τ h
              subst x
              exact ha hxl
            have htxa : τ x ≠ a := by
              intro h
              have : x = τ a := by simpa only [hinv] using congrArg τ h
              exact hxne this
            exact ⟨htne, (h1.mpr (by simp [hxl])).resolve_left htxa⟩
        have hlt : (l.erase (τ a)).length < k := by
          simp only [List.length_cons] at hl
          omega
        have hp := ih _ hlt _ rfl (hnl.erase _) hsym
        have hpos := List.length_pos_of_mem hta
        simp only [List.length_cons]
        omega
  exact aux _ s rfl hn hs

/-- Safety in a block game with a common occupancy threshold. -/
def Safe (blocks : List (α → Bool)) (q : Nat) (s : List α) : Prop :=
  ∀ B ∈ blocks, s.countP B < q

instance (blocks : List (α → Bool)) (q : Nat) (s : List α) :
    Decidable (Safe blocks q s) := by
  unfold Safe
  infer_instance

/-- The two block hypotheses required in addition to an involution. -/
structure BlockSymmetry (τ : α → α) (blocks : List (α → Bool)) : Prop where
  reflect : ∀ B ∈ blocks, (fun x => B (τ x)) ∈ blocks
  pair : ∀ B ∈ blocks, ∀ p, B p = true → B (τ p) = true →
    ∀ x, B (τ x) = B x

omit [DecidableEq α] in
private theorem reflected_count (τ : α → α) (hinv : ∀ x, τ (τ x) = x)
    {s : List α} (hn : s.Nodup) (hs : Symmetric τ s) (B : α → Bool) :
    s.countP (fun x => B (τ x)) = s.countP B := by
  have hmap : (s.map τ).Nodup := by
    change (s.map τ).Pairwise (fun x y => x ≠ y)
    rw [List.pairwise_map]
    apply List.Pairwise.imp_of_mem (R := fun x y => x ≠ y) _ hn
    intro x y _ _ hne heq
    exact hne (by simpa only [hinv] using congrArg τ heq)
  have hp : (s.map τ).Perm s := by
    apply (List.perm_ext_iff_of_nodup hmap hn).2
    intro x
    simp only [List.mem_map]
    constructor
    · rintro ⟨y, hy, rfl⟩
      exact (hs y).2 hy
    · intro hx
      exact ⟨τ x, (hs x).2 hx, hinv x⟩
  simpa only [List.countP_map, Function.comp_def] using hp.countP_eq B

/-- After a legal move from a symmetric safe set, its mirror is still safe. -/
theorem mirror_safe (τ : α → α) (hinv : ∀ x, τ (τ x) = x)
    (hfree : ∀ x, τ x ≠ x) {blocks : List (α → Bool)}
    (hb : BlockSymmetry τ blocks) {q : Nat} (hq : q % 2 = 1)
    {s : List α} (hn : s.Nodup) (hs : Symmetric τ s)
    {p : α} (hlegal : Safe blocks q (p :: s)) :
    Safe blocks q (τ p :: p :: s) := by
  intro B hB
  have hsingle := hlegal B hB
  by_cases ht : B (τ p) = true
  · by_cases hp : B p = true
    · have heven : (s.filter B).length % 2 = 0 := by
        apply even_length τ hinv hfree _ (hn.filter B)
        intro x
        simp only [List.mem_filter, hs x, hb.pair B hB p hp ht x]
      rw [← List.countP_eq_length_filter] at heven
      simp only [List.countP_cons, hp, ht, ite_true] at hsingle ⊢
      omega
    · have href := hlegal (fun x => B (τ x)) (hb.reflect B hB)
      have hc := reflected_count τ hinv hn hs B
      simp only [List.countP_cons, ht, ite_true] at href
      simp [ht, hp]
      omega
  · simpa [List.countP_cons, ht] using hsingle

/-- Legal moves enumerate every unused board vertex whose addition is safe. -/
def moves (board : List α) (blocks : List (α → Bool)) (q : Nat)
    (s : List α) : List (List α) :=
  board.filterMap fun p =>
    if p ∉ s ∧ Safe blocks q (p :: s) then some (p :: s) else none

theorem mem_moves {board : List α} {blocks : List (α → Bool)} {q : Nat}
    {s t : List α} : t ∈ moves board blocks q s ↔
      ∃ p, p ∈ board ∧ p ∉ s ∧ Safe blocks q (p :: s) ∧ t = p :: s := by
  simp only [moves, List.mem_filterMap]
  constructor
  · rintro ⟨p, hp, h⟩
    split at h
    next hlegal => exact ⟨p, hp, hlegal.1, hlegal.2, (Option.some.inj h).symm⟩
    next => contradiction
  · rintro ⟨p, hp, hnot, hsafe, rfl⟩
    exact ⟨p, hp, by simp [hnot, hsafe]⟩

/-- K0337's abstract sufficient condition: every symmetric safe set is P.

The response is the actual unused mirror vertex; termination follows from
strictly increasing occupation within the finite board. No certificate or
external solver is assumed.
-/
theorem symmetric_losing (board : List α) (blocks : List (α → Bool))
    (q : Nat) (τ : α → α) (hinv : ∀ x, τ (τ x) = x)
    (hfree : ∀ x, τ x ≠ x) (hboard : Symmetric τ board)
    (hb : BlockSymmetry τ blocks) (hq : q % 2 = 1)
    (s : List α) (hn : s.Nodup) (hsub : s ⊆ board)
    (hsafe : Safe blocks q s) (hs : Symmetric τ s) :
    Losing (moves board blocks q) s := by
  have aux : ∀ k (u : List α), board.length - u.length = k →
      u.Nodup → u ⊆ board → Safe blocks q u → Symmetric τ u →
      Losing (moves board blocks q) u := by
    intro k
    induction k using Nat.strongRecOn with
    | ind k ih =>
      intro u hk hnu hsu _ hsym
      apply Losing.all
      intro t ht
      obtain ⟨p, hp, hpnot, hpsafe, rfl⟩ := mem_moves.mp ht
      have htboard : τ p ∈ board := (hboard p).2 hp
      have htnot : τ p ∉ p :: u := by
        simp only [List.mem_cons, not_or]
        exact ⟨hfree p, fun h => hpnot ((hsym p).1 h)⟩
      have hrSafe := mirror_safe τ hinv hfree hb hq hnu hsym hpsafe
      have hrMem : τ p :: p :: u ∈ moves board blocks q (p :: u) :=
        mem_moves.mpr ⟨τ p, htboard, htnot, hrSafe, rfl⟩
      apply Winning.move hrMem
      have hrn : (τ p :: p :: u).Nodup := by
        simp only [List.nodup_cons]
        exact ⟨htnot, hpnot, hnu⟩
      have hrsub : τ p :: p :: u ⊆ board := by
        intro x hx
        simp only [List.mem_cons] at hx
        rcases hx with rfl | rfl | hx
        · exact htboard
        · exact hp
        · exact hsu hx
      have hrSym : Symmetric τ (τ p :: p :: u) := by
        intro x
        have hxp : τ x = p ↔ x = τ p :=
          ⟨fun h => by simpa only [hinv] using congrArg τ h,
            fun h => by simp [h, hinv]⟩
        have hxtp : τ x = τ p ↔ x = p :=
          ⟨fun h => by simpa only [hinv] using congrArg τ h,
            fun h => by simp [h]⟩
        simp only [List.mem_cons, hxp, hxtp, hsym x]
        exact or_left_comm
      have hrbound := hrn.length_le_of_subset hrsub
      have hrlt : board.length - (τ p :: p :: u).length < k := by
        simp only [List.length_cons] at hrbound ⊢
        omega
      exact ih _ hrlt _ rfl hrn hrsub hrSafe hrSym
  exact aux _ s rfl hn hsub hsafe hs

end Kyouen.OddInvolution
