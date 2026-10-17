import Std
import Kyouen.CertificateSoundness

namespace Kyouen.Grundy

/-- A finite impartial game DAG with explicit children. -/
structure Game (σ : Type) where
  children : σ → List σ
  rank : σ → Nat
  rank_lt : ∀ s t, t ∈ children s → rank t < rank s

/-- Membership-decidable `mex`: smallest missing natural below `bound + 1`. -/
def mex (xs : List Nat) : Nat :=
  match (List.range (xs.length + 1)).find? (fun n => decide (n ∉ xs)) with
  | some n => n
  | none => xs.length + 1

theorem mex_empty : mex [] = 0 := by
  simp [mex]

/-- The Grundy value by well-founded recursion over `rank`. -/
def grundy {σ : Type} (G : Game σ) (s : σ) : Nat :=
  mex ((G.children s).map (grundy G))
  termination_by G.rank s
  decreasing_by exact G.rank_lt s _ ‹_›

/-- Terminal states have Grundy value zero. -/
theorem grundy_of_no_children {σ : Type} (G : Game σ) (s : σ)
    (h : G.children s = []) : grundy G s = 0 := by
  unfold grundy
  simp [h, mex_empty]

/-- A one-step move always changes the stone count by exactly one. -/
def SizeStep {σ : Type} (children : σ → List σ) (size : σ → Nat) : Prop :=
  ∀ s t, t ∈ children s → size t = size s + 1

/-- A uniform-capacity game: every maximal path has exactly `cap` moves. -/
structure UniformTerminal {σ : Type} (G : Game σ) (size : σ → Nat) (cap : Nat) : Prop where
  step : SizeStep G.children size
  bounded : ∀ s, size s ≤ cap
  terminal : ∀ s, size s = cap → G.children s = []
  progress : ∀ s, size s < cap → G.children s ≠ []

/-- Remaining moves from `s` under a uniform terminal `cap`. -/
def remaining {σ : Type} (size : σ → Nat) (cap : Nat) (s : σ) : Nat :=
  cap - size s

abbrev Even (n : Nat) : Prop := ∃ k, n = 2 * k
abbrev Odd (n : Nat) : Prop := ∃ k, n = 2 * k + 1

theorem remaining_step {σ : Type} {G : Game σ} {size : σ → Nat} {cap : Nat}
    (h : UniformTerminal G size cap) {s t : σ} (hmem : t ∈ G.children s) :
    remaining size cap t + 1 = remaining size cap s := by
  unfold remaining
  have hstep := h.step s t hmem
  have hle : size s ≤ cap := h.bounded s
  have hlet : size t ≤ cap := h.bounded t
  omega

/-- Uniform-length games are losing exactly at even remaining length. -/
theorem losing_of_even_remaining {σ : Type} {G : Game σ} {size : σ → Nat} {cap : Nat}
    (h : UniformTerminal G size cap) (s : σ)
    (heven : Even (remaining size cap s)) :
    Losing G.children s := by
  suffices hgen : ∀ r (u : σ), remaining size cap u = r → Even r → Losing G.children u from
    hgen _ s rfl heven
  intro r
  induction r using Nat.strongRecOn with
  | ind r ih =>
      intro u hr heven
      apply Losing.all
      intro v hmem
      have hrv : remaining size cap v + 1 = r := by
        have hstep := remaining_step h hmem
        rw [hr] at hstep
        omega
      have hlt : remaining size cap v < r := by omega
      have hevenParam := heven
      have hodd : Odd (remaining size cap v) := by
        rcases hevenParam with ⟨k, hk⟩
        refine ⟨k - 1, ?_⟩
        omega
      have hsize : size u < cap := by
        have hstepSize := h.step u v hmem
        have hle := h.bounded v
        omega
      have hcap : size v < cap := by
        cases hodd with
        | intro k hk =>
            have : 0 < remaining size cap v := by
              rw [hk]
              omega
            unfold remaining at this
            omega
      have hne : G.children v ≠ [] := h.progress v hcap
      rcases List.exists_mem_of_ne_nil (G.children v) hne with ⟨w, hwmem⟩
      have hstep2 := remaining_step h hwmem
      have hrw : remaining size cap w + 2 = r := by omega
      have hlt2 : remaining size cap w < r := by omega
      have heven2 : Even (remaining size cap w) := by
        rcases hevenParam with ⟨k, hk⟩
        refine ⟨k - 1, ?_⟩
        omega
      exact Winning.move hwmem (ih (remaining size cap w) hlt2 w rfl heven2)

/-- Uniform-length games are winning exactly at odd remaining length. -/
theorem winning_of_odd_remaining {σ : Type} {G : Game σ} {size : σ → Nat} {cap : Nat}
    (h : UniformTerminal G size cap) (s : σ)
    (hodd : Odd (remaining size cap s)) :
    Winning G.children s := by
  have hne : G.children s ≠ [] := h.progress s (by
    unfold remaining at hodd
    have hle := h.bounded s
    omega)
  rcases List.exists_mem_of_ne_nil (G.children s) hne with ⟨t, hmem⟩
  have hstep := remaining_step h hmem
  have heven : Even (remaining size cap t) := by
    rcases hodd with ⟨k, hk⟩
    -- remaining t + 1 = remaining s = 2*k+1, so remaining t = 2*k
    refine ⟨k, ?_⟩
    omega
  exact Winning.move hmem (losing_of_even_remaining h t heven)

end Kyouen.Grundy

namespace Kyouen.UniformExtra

open Kyouen.Grundy

theorem remaining_le_cap {σ : Type} {size : σ → Nat} {cap : Nat} (s : σ) (hs : size s ≤ cap) :
    remaining size cap s ≤ cap := by
  unfold remaining
  omega

theorem remaining_zero_of_size_cap {σ : Type} {size : σ → Nat} {cap : Nat} (s : σ) (hs : size s = cap) :
    remaining size cap s = 0 := by
  unfold remaining
  omega

theorem even_zero : Even 0 := by
  unfold Even
  refine ⟨0, ?_⟩
  rfl

theorem odd_one : Odd 1 := by
  unfold Odd
  refine ⟨0, ?_⟩
  rfl

theorem mex_range (k : Nat) : mex (List.range k) = k := by
  unfold mex
  rw [List.length_range]
  have hfound :
      (List.range (k + 1)).find? (fun m => decide (m ∉ List.range k)) = some k := by
    rw [List.find?_range_eq_some]
    refine ⟨?_, ?_, ?_⟩
    · show decide (k ∉ List.range k) = true
      apply decide_eq_true
      simp
    · simp
    · intro j hj
      have : j ∈ List.range k := by simp [hj]
      simp [this]
  rw [hfound]

theorem mex_range_empty : mex (List.range 0) = 0 := by
  simp [mex_empty]