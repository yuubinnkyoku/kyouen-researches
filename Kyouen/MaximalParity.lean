import Std
import Lean.Elab.Tactic.Omega

/-!
# Maximal-position parity and binary Grundy numbers (K0305)

This is the game-theoretic part of K0305, independent of lattice geometry.
Every move adds one object. A mex labelling assigns Grundy numbers, and a
predecessor exists for each non-root position, as in a hereditary safety game.
-/

namespace Kyouen.MaximalParity

variable {σ : Type}

/-- A Grundy labelling satisfies the defining mex rule at every position. -/
def MexLabelling (moves : σ → List σ) (g : σ → Nat) : Prop :=
  ∀ s, (∀ t, t ∈ moves s → g t ≠ g s) ∧
    (∀ k, k < g s → ∃ t, t ∈ moves s ∧ g t = k)

/-- A terminal (maximal) position has no legal moves. -/
def Terminal (moves : σ → List σ) (s : σ) : Prop := moves s = []

/-- Every maximal position has the same parity of occupied-object count. -/
def TerminalParity (moves : σ → List σ) (size : σ → Nat)
    (ε : Nat) : Prop :=
  ∀ s, Terminal moves s → size s % 2 = ε

private theorem terminal_grundy_zero
    {moves : σ → List σ} {g : σ → Nat}
    (hmex : MexLabelling moves g) {s : σ}
    (hs : Terminal moves s) : g s = 0 := by
  by_cases h : g s = 0
  · exact h
  · have hpos : 0 < g s := by omega
    obtain ⟨t, ht, _⟩ := (hmex s).2 0 hpos
    simp only [Terminal] at hs
    simp [hs] at ht

/-- Common parity of maximal sizes determines every Grundy value. -/
theorem grundy_eq_parity_of_terminal_parity
    (moves : σ → List σ) (size : σ → Nat) (g : σ → Nat)
    (bound ε : Nat)
    (hmex : MexLabelling moves g)
    (hbound : ∀ s, size s ≤ bound)
    (hstep : ∀ s t, t ∈ moves s → size t = size s + 1)
    (hε : ε < 2)
    (hterminal : TerminalParity moves size ε) :
    ∀ s, g s = (ε + size s) % 2 := by
  have aux : ∀ d : Nat, ∀ s, bound - size s = d →
      g s = (ε + size s) % 2 := by
    intro d
    induction d using Nat.strongRecOn with
    | ind d ih =>
      intro s hs
      cases hchildren : moves s with
      | nil =>
          have hg : g s = 0 := terminal_grundy_zero hmex hchildren
          have hp : size s % 2 = ε := hterminal s hchildren
          omega
      | cons t ts =>
          have hmem : t ∈ moves s := by simp [hchildren]
          obtain ⟨hneq, hbelow⟩ := hmex s
          have hall : ∀ u, u ∈ moves s →
              g u = (ε + size s + 1) % 2 := by
            intro u hu
            have huSz := hstep s u hu
            have huBound := hbound u
            have hud : bound - size u < d := by omega
            have hh := ih (bound - size u) hud u rfl
            omega
          have hbinary : g s < 2 := by
            by_cases hb : g s < 2
            · exact hb
            · have hk0 : 0 < g s := by omega
              have hk1 : 1 < g s := by omega
              obtain ⟨u, hu, hgu⟩ := hbelow 0 hk0
              obtain ⟨v, hv, hgv⟩ := hbelow 1 hk1
              have heq : g u = g v := by rw [hall u hu, hall v hv]
              omega
          have hne := hneq t hmem
          have htval := hall t hmem
          omega
  intro s
  exact aux (bound - size s) s rfl

/-- In a binary Grundy game, each move reverses the Grundy value. -/
theorem binary_values_flip
    (moves : σ → List σ) (g : σ → Nat)
    (hmex : MexLabelling moves g)
    (hbinary : ∀ s, g s < 2) :
    ∀ s t, t ∈ moves s → g s + g t = 1 := by
  intro s t ht
  have hne := (hmex s).1 t ht
  have hs := hbinary s
  have htv := hbinary t
  omega

/-- Binary Grundy values imply a common parity for maximal sizes. -/
theorem terminal_parity_of_binary_grundy
    (moves : σ → List σ) (size : σ → Nat) (g : σ → Nat)
    (root : σ)
    (hmex : MexLabelling moves g)
    (hstep : ∀ s t, t ∈ moves s → size t = size s + 1)
    (hroot : size root = 0)
    (hparent : ∀ s, s ≠ root → ∃ p, s ∈ moves p)
    (hbinary : ∀ s, g s < 2) :
    TerminalParity moves size (g root) := by
  have hflip := binary_values_flip moves g hmex hbinary
  have heq : ∀ k : Nat, ∀ s, size s = k →
      g s = (g root + size s) % 2 := by
    intro k
    induction k using Nat.strongRecOn with
    | ind k ih =>
      intro s hs
      by_cases hr : s = root
      · subst s
        have hbr := hbinary root
        omega
      · obtain ⟨p, hp⟩ := hparent s hr
        have hsz := hstep p s hp
        have hpred : size p < k := by omega
        have heqp := ih (size p) hpred p rfl
        have hfl := hflip p s hp
        have hbroot := hbinary root
        have hbs := hbinary s
        omega
  intro s hterm
  have hg := terminal_grundy_zero hmex hterm
  have hgs := heq (size s) s rfl
  have hb := hbinary root
  omega

/-- K0305: binary Grundy values are equivalent to uniform maximal parity. -/
theorem binary_grundy_iff_terminal_parity
    (moves : σ → List σ) (size : σ → Nat) (g : σ → Nat)
    (root : σ) (bound : Nat)
    (hmex : MexLabelling moves g)
    (hbound : ∀ s, size s ≤ bound)
    (hstep : ∀ s t, t ∈ moves s → size t = size s + 1)
    (hroot : size root = 0)
    (hparent : ∀ s, s ≠ root → ∃ p, s ∈ moves p) :
    (∀ s, g s < 2) ↔
      ∃ ε : Nat, ε < 2 ∧ TerminalParity moves size ε := by
  constructor
  · intro hbinary
    exact ⟨g root, hbinary root,
      terminal_parity_of_binary_grundy moves size g root
        hmex hstep hroot hparent hbinary⟩
  · rintro ⟨ε, hε, hterm⟩ s
    rw [grundy_eq_parity_of_terminal_parity moves size g bound ε
      hmex hbound hstep hε hterm s]
    omega

end Kyouen.MaximalParity
