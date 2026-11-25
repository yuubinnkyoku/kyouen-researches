import Std
import Kyouen.CubeRules
import Kyouen.CubeSymmetry
import Kyouen.CubeCertificate

namespace Kyouen.CubeBridge

open Kyouen
open Kyouen.CubeRules
open Kyouen.CubeSymmetry
open Kyouen.CubeCertificate

def Distinct (s : Position) : Prop :=
  ∀ p, p ∈ s → s.count p = 1

instance (s : Position) : Decidable (Distinct s) := by
  unfold Distinct
  infer_instance

def maskOfPosition : Position -> Nat
  | [] => 0
  | q :: qs => (1 <<< q.val) ||| maskOfPosition qs

-- Membership in maskToPoints is testBit.
theorem mem_maskToPoints {m : Nat} {p : Point} (hp : p.val < 27) :
    p ∈ maskToPoints m ↔ Nat.testBit m p.val = true := by
  simp [maskToPoints, List.mem_filter, Nat.testBit]

-- maskOfPosition distributes over cons (definitional).
theorem maskOfPosition_cons (q : Point) (qs : Position) :
    maskOfPosition (q :: qs) = (1 <<< q.val) ||| maskOfPosition qs := rfl

-- Bit-level characterization of maskOfPosition.
theorem testBit_maskOfPosition {s : Position} {j : Nat} :
    Nat.testBit (maskOfPosition s) j = true ↔ ∃ q ∈ s, q.val = j := by
  induction s with
  | nil =>
      simp [maskOfPosition, Nat.testBit]
  | cons q qs ih =>
      rw [maskOfPosition_cons]
      constructor
      · intro h
        rw [Nat.testBit_or] at h
        cases hbit : Nat.testBit (1 <<< q.val) j with
        | true =>
            refine ⟨q, by simp, ?_⟩
            have : (1 <<< q.val).testBit j = true := hbit
            -- q.val = j
            rw [Nat.testBit_shiftLeft] at this
            by_cases hji : j ≥ q.val
            · have : (decide (j ≥ q.val) && Nat.testBit 1 (j - q.val)) = true := this
              simp [hji] at this
              have : Nat.testBit 1 (j - q.val) = true := this
              have : j - q.val = 0 :=
                (Nat.testBit_one_eq_true_iff_self_eq_zero (i := j - q.val)).mp this
              omega
            · simp [hji] at this
        | false =>
            have : Nat.testBit (maskOfPosition qs) j = true := by
              simp [Nat.testBit_or, hbit] at h
              exact h
            rcases ih.mp this with ⟨r, hr, hrj⟩
            exact ⟨r, by simp [hr], hrj⟩
      · intro h
        rcases h with ⟨r, hr, hrj⟩
        simp at hr
        cases hr with
        | inl hreq =>
            have hqj : q.val = j := by rw [← hreq]; exact hrj
            have : Nat.testBit (1 <<< q.val) j = true := by
              rw [Nat.testBit_shiftLeft]
              have hji : j ≥ q.val := by omega
              simp [hji, hqj]
            rw [Nat.testBit_or]
            simp [this]
        | inr hrqs =>
            have : Nat.testBit (maskOfPosition qs) j = true := ih.mpr ⟨r, hrqs, hrj⟩
            rw [Nat.testBit_or]
            simp [this]

theorem mem_maskToPoints_maskOfPosition {s : Position} {p : Point} :
    p ∈ maskToPoints (maskOfPosition s) ↔ p ∈ s := by
  have hp : p.val < 27 := p.isLt
  rw [mem_maskToPoints hp]
  constructor
  · intro h
    have htb : Nat.testBit (maskOfPosition s) p.val = true := h
    rcases testBit_maskOfPosition.mp htb with ⟨q, hq, hqj⟩
    have : q = p := Fin.ext hqj
    subst this
    exact hq
  · intro hp_mem
    have htb : Nat.testBit (maskOfPosition s) p.val = true :=
      testBit_maskOfPosition.mpr ⟨p, hp_mem, rfl⟩
    exact htb

end Kyouen.CubeBridge