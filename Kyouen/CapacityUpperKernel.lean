import Std
import Kyouen.UniformCapacity

namespace Kyouen.CapacityUpperKernel

open Kyouen.Grundy

/-! # General mex lemmas -/

/-- If every number below `k` occurs in `xs` and `k` does not, then `mex xs = k`. -/
theorem mex_of_all_lt_and_missing (xs : List Nat) (k : Nat)
    (hall : ∀ i, i < k → i ∈ xs) (hmiss : k ∉ xs) : mex xs = k := by
  unfold mex
  have hle : k ≤ xs.length := by
    induction k with
    | zero => omega
    | succ k ih =>
        have hk : k ∈ xs := hall k (by omega)
        have herase : (xs.erase k).length = xs.length - 1 :=
          List.length_erase_of_mem hk
        have hall' : ∀ i, i < k → i ∈ xs.erase k := by
          intro i hi
          have hi' : i ∈ xs := hall i (by omega)
          by_cases heq : i = k
          · omega
          · exact List.mem_erase_of_ne_of_mem heq hi'
        have ih' := ih hall'
        omega
  rw [List.find?_range_eq_some]
  refine ⟨?_, ?_, ?_⟩
  · show decide (k ∉ xs) = true
    apply decide_eq_true hmiss
  · show k ∈ List.range (xs.length + 1)
    simp [hle]
  · intro j hj
    have hjmem : j ∈ xs := hall j hj
    have : decide (j ∉ xs) = false := by
      apply decide_eq_false
      intro hnot
      exact hnot hjmem
    simp [this]

/-- Forward direction: `mex xs = k` implies all numbers below `k` are in `xs`. -/
theorem mex_eq_k_all_lt {xs : List Nat} {k : Nat} (h : mex xs = k) :
    ∀ i, i < k → i ∈ xs := by
  unfold mex at h
  have hfind : (List.range (xs.length + 1)).find? (fun n => decide (n ∉ xs)) = some k := by
    simpa using h
  rw [List.find?_range_eq_some] at hfind
  rcases hfind with ⟨_hdec, _hrange, hall⟩
  intro i hi
  have hdec_i : decide (i ∉ xs) = false := by simpa using hall i hi
  exact of_decide_eq_false hdec_i

/-- Forward direction: `mex xs = k` implies `k ∉ xs`. -/
theorem mex_eq_k_not_mem {xs : List Nat} {k : Nat} (h : mex xs = k) : k ∉ xs := by
  unfold mex at h
  have hfind : (List.range (xs.length + 1)).find? (fun n => decide (n ∉ xs)) = some k := by
    simpa using h
  rw [List.find?_range_eq_some] at hfind
  rcases hfind with ⟨hdec, _hrange, _hall⟩
  exact of_decide_eq_true hdec

/-- xor with 1 increments an even number. -/
theorem xor_one_even (k : Nat) (he : k % 2 = 0) : k ^^^ 1 = k + 1 := by
  apply Nat.eq_of_testBit_eq
  intro i
  cases i with
  | zero =>
      have hk0 : Nat.testBit k 0 = false := by
        rw [Nat.testBit_zero]
        simp [he]
      simp [Nat.testBit_xor, Nat.testBit_zero, hk0]
  | succ j =>
      have h1 : Nat.testBit 1 (j + 1) = false := by
        rw [Nat.testBit_succ]
        simp
      rw [Nat.testBit_xor, h1]
      simp [Bool.xor_false]
      rw [Nat.testBit_succ, Nat.testBit_succ]
      have hdiv : (k + 1) / 2 = k / 2 := by
        have hk : k = 2 * (k / 2) := by omega
        omega
      rw [hdiv]

/-- xor with 1 is an involution. -/
theorem xor_one_invol (n : Nat) : (n ^^^ 1) ^^^ 1 = n := by
  simp [Nat.xor_assoc]

/-- xor with 1 decrements an odd number. -/
theorem xor_one_odd (k : Nat) (ho : k % 2 = 1) : k ^^^ 1 = k - 1 := by
  have he : (k - 1) % 2 = 0 := by omega
  have this : (k - 1) ^^^ 1 = k := by
    rw [xor_one_even (k - 1) he]
    omega
  have h2 : (k ^^^ 1) = ((k - 1) ^^^ 1) ^^^ 1 := by rw [this]
  rw [xor_one_invol (k - 1)] at h2
  exact h2

/-- Key mex lemma. -/
theorem mex_xor_one_union (A : List Nat) (k : Nat) (hk : mex A = k) :
    mex (A.map (fun a => a ^^^ 1) ++ [k]) = k ^^^ 1 := by
  have hallA : ∀ i, i < k → i ∈ A := mex_eq_k_all_lt hk
  have missA : k ∉ A := mex_eq_k_not_mem hk
  apply mex_of_all_lt_and_missing
  · intro i hi
    by_cases heven : k % 2 = 0
    · have hkxor : k ^^^ 1 = k + 1 := xor_one_even k heven
      rw [hkxor] at hi
      by_cases hik : i = k
      · simp [List.mem_append, List.mem_singleton]
      · have hilt : i < k := by omega
        have himem : i ^^^ 1 ∈ A := by
          have hlt : i ^^^ 1 < k := by
            by_cases hip : i % 2 = 0
            · have : i + 1 < k := by omega
              omega
            · omega
          exact hallA (i ^^^ 1) hlt
        simp [List.mem_append, List.mem_map]
        refine ⟨i ^^^ 1, himem, ?_⟩
        simp [xor_one_invol]
    · have hkxor : k ^^^ 1 = k - 1 := xor_one_odd k (by omega)
      rw [hkxor] at hi
      have hilt : i < k := by omega
      have himem : i ^^^ 1 ∈ A := by
        have hlt : i ^^^ 1 < k := by
          by_cases hip : i % 2 = 0
          · omega
          · omega
        exact hallA (i ^^^ 1) hlt
      simp [List.mem_append, List.mem_map]
      refine ⟨i ^^^ 1, himem, ?_⟩
      simp [xor_one_invol]
  · by_cases heven : k % 2 = 0
    · have hkxor : k ^^^ 1 = k + 1 := xor_one_even k heven
      rw [hkxor]
      have hne : k + 1 ≠ k := by omega
      have hnotmap : k + 1 ∉ A.map (fun a => a ^^^ 1) := by
        simp [List.mem_map]
        intro a ha heq
        have : a = (k + 1) ^^^ 1 := by
          rw [heq]; simp [xor_one_invol]
        rw [this] at ha
        have : (k + 1) ^^^ 1 = k := by
          have ho : (k + 1) % 2 = 1 := by omega
          exact xor_one_odd (k + 1) ho
        rw [this] at ha
        exact missA ha
      simp [List.mem_append, List.mem_singleton, hne, hnotmap]
    · have hkxor : k ^^^ 1 = k - 1 := xor_one_odd k (by omega)
      rw [hkxor]
      have hne : k - 1 ≠ k := by omega
      have hnotmap : k - 1 ∉ A.map (fun a => a ^^^ 1) := by
        simp [List.mem_map]
        intro a ha heq
        have : a = (k - 1) ^^^ 1 := by
          rw [heq]; simp [xor_one_invol]
        rw [this] at ha
        have : (k - 1) ^^^ 1 = k := by
          have he : (k - 1) % 2 = 0 := by omega
          exact xor_one_even (k - 1) he
        rw [this] at ha
        exact missA ha
      simp [List.mem_append, List.mem_singleton, hne, hnotmap]

/-! # Abstract upper kernel -/

section UpperKernel

variable {U : Type}
variable (sumTop : U → Nat) (bmin : U → Nat) (children : U → List U) (r n : Nat)

def sigma (u : U) : Nat := r - sumTop u
def p (u : U) : Nat := (n * bmin u) % 2

variable (hsum_le : ∀ u, sumTop u ≤ r)
variable (hchild_dec : ∀ u v, v ∈ children u → sumTop v = sumTop u + 1)
variable (hchild_empty : ∀ u, sigma u = 0 → children u = [])

def H (u : U) : Nat :=
  mex ((children u).map (fun v => H v ^^^ p u ^^^ p v))
termination_by sigma u
decreasing_by
  have hinc : sumTop v = sumTop u + 1 := hchild_dec u v (by assumption)
  unfold sigma
  omega

def tval (u v : U) : Nat := H v ^^^ p u ^^^ p v

variable (h_diamond : ∀ u, sigma u % 2 = 0 → 2 ≤ sigma u →
  ∀ v1 v2, v1 ∈ children u → v2 ∈ children u →
    H v1 ≤ 1 → H v2 ≤ 1 → v1 ≠ v2 →
    ∃ z, z ∈ children v1 ∧ z ∈ children v2)

/-- If not both 0 and 1 occur, mex ≤ 1. -/
theorem mex_le_one_of_not_both (xs : List Nat)
    (h : ¬ (0 ∈ xs ∧ 1 ∈ xs)) : mex xs ≤ 1 := by
  by_cases h0 : 0 ∈ xs
  · by_cases h1 : 1 ∈ xs
    · exact (h ⟨h0, h1⟩).elim
    · have hall : ∀ i, i < 1 → i ∈ xs := by intro i hi; omega
      have heq : mex xs = 1 := mex_of_all_lt_and_missing xs 1 hall h1
      omega
  · have hall : ∀ i, i < 0 → i ∈ xs := by intro i hi; omega
    have heq : mex xs = 0 := mex_of_all_lt_and_missing xs 0 hall h0
    omega

/-- If all elements of `S` are bits and `mex S ≤ 1`, then every element
    equals `(mex S) xor 1`. -/
theorem all_elements_eq_xor_one_of_mex_le_one (S : List Nat)
    (hbits : ∀ x, x ∈ S → x = 0 ∨ x = 1)
    (hmex : mex S ≤ 1) (x : Nat) (hx : x ∈ S) :
    x = (mex S) ^^^ 1 := by
  by_cases h0 : mex S = 0
  · have hxor : (mex S) ^^^ 1 = 1 := by rw [h0]; decide
    rw [hxor]
    have hmiss : 0 ∉ S := mex_eq_k_not_mem (by
      have : mex S = 0 := h0
      exact this)
    cases hbits x hx with
    | inl h => exact (hmiss (by simpa [h])).elim
    | inr h => exact h
  · have hmex1 : mex S = 1 := by omega
    have hxor : (mex S) ^^^ 1 = 0 := by rw [hmex1]; decide
    rw [hxor]
    have hmiss : 1 ∉ S := mex_eq_k_not_mem hmex1
    cases hbits x hx with
    | inl h => exact h
    | inr h => exact (hmiss (by simpa [h])).elim

/-- Upper bound for the abstract upper kernel. -/
theorem H_upper (u : U) :
    (sigma u % 2 = 0 → H u ≤ 1) ∧ (sigma u % 2 = 1 → H u ≤ 2) := by
  have aux : ∀ k, ∀ u, sigma u = k →
      (k % 2 = 0 → H u ≤ 1) ∧ (k % 2 = 1 → H u ≤ 2) := by
    intro k
    induction k using Nat.strongRecOn with
    | ind k ih =>
        intro u hsu
        constructor
        · intro he
          by_cases hk0 : k = 0
          · have hch : children u = [] := hchild_empty u (by rw [hsu, hk0])
            have : H u = 0 := by
              unfold H
              rw [hch]
              simp [mex_empty]
            omega
          · have hnotboth : ¬ (0 ∈ (children u).map (fun v => H v ^^^ p u ^^^ p v) ∧
                                1 ∈ (children u).map (fun v => H v ^^^ p u ^^^ p v)) := by
              intro ⟨h0, h1⟩
              rcases List.mem_map.mp h0 with ⟨v0, hv0mem, hv0eq⟩
              rcases List.mem_map.mp h1 with ⟨v1, hv1mem, hv1eq⟩
              have hv0sig : sigma v0 = k - 1 := by
                have hinc := hchild_dec u v0 hv0mem
                rw [hsu] at hinc
                unfold sigma
                omega
              have hv1sig : sigma v1 = k - 1 := by
                have hinc := hchild_dec u v1 hv1mem
                rw [hsu] at hinc
                unfold sigma
                omega
              have hv0bound : H v0 ≤ 2 := (ih (k - 1) (by omega) v0 hv0sig).2 (by omega)
              have hv1bound : H v1 ≤ 2 := (ih (k - 1) (by omega) v1 hv1sig).2 (by omega)
              have hv0single : H v0 ≤ 1 := by
                by_cases h : H v0 = 2
                · exfalso
                  rw [h] at hv0eq
                  have : (2 : Nat) ^^^ (p u ^^^ p v0) ≠ 0 := by
                    cases (show p u = 0 ∨ p u = 1 by unfold p; omega) with
                    | inl hpu =>
                      cases (show p v0 = 0 ∨ p v0 = 1 by unfold p; omega) with
                      | inl hpv => simp [hpu, hpv]
                      | inr hpv => simp [hpu, hpv]
                    | inr hpu =>
                      cases (show p v0 = 0 ∨ p v0 = 1 by unfold p; omega) with
                      | inl hpv => simp [hpu, hpv]
                      | inr hpv => simp [hpu, hpv]
                  omega
                · omega
              have hv1single : H v1 ≤ 1 := by
                by_cases h : H v1 = 2
                · exfalso
                  rw [h] at hv1eq
                  have : (2 : Nat) ^^^ (p u ^^^ p v1) ≠ 0 := by
                    cases (show p u = 0 ∨ p u = 1 by unfold p; omega) with
                    | inl hpu =>
                      cases (show p v1 = 0 ∨ p v1 = 1 by unfold p; omega) with
                      | inl hpv => simp [hpu, hpv]
                      | inr hpv => simp [hpu, hpv]
                    | inr hpu =>
                      cases (show p v1 = 0 ∨ p v1 = 1 by unfold p; omega) with
                      | inl hpv => simp [hpu, hpv]
                      | inr hpv => simp [hpu, hpv]
                  omega
                · omega
              have hne : v0 ≠ v1 := by
                intro heq
                rw [heq] at hv0eq
                have : (0 : Nat) = 1 := by
                  rw [hv0eq] at hv1eq
                  simpa using hv1eq
                omega
              rcases h_diamond u (by omega) (by omega) v0 v1 hv0mem hv1mem hv0single hv1single hne with ⟨z, hz0, hz1⟩
              have hv0sig : sigma v0 = k - 1 := by
                have hinc := hchild_dec u v0 hv0mem
                rw [hsu] at hinc
                unfold sigma
                omega
              have hv1sig : sigma v1 = k - 1 := by
                have hinc := hchild_dec u v1 hv1mem
                rw [hsu] at hinc
                unfold sigma
                omega
              have hzsig : sigma z = (sigma u) - 2 := by
                have hinc0 := hchild_dec v0 z hz0
                rw [hv0sig] at hinc0
                unfold sigma
                omega
              have hzbound : H z ≤ 1 := (aux (k - 2) (by omega) z (by
                have : sigma z = k - 2 := by
                  rw [hsu] at hzsig
                  exact hzsig
                exact this)).1 (by omega)
              -- v0 single: all its children transformed values equal (H v0)^^^1
              have hz0val : H z ^^^ p v0 ^^^ p z = (H v0) ^^^ 1 := by
                have hvsig : sigma v0 = k - 1 := hv0sig
                have hchildrenbits : ∀ w, w ∈ children v0 →
                    (H w ^^^ p v0 ^^^ p w) = 0 ∨ (H w ^^^ p v0 ^^^ p w) = 1 := by
                  intro w hw
                  have hwsig : sigma w = sigma v0 - 1 := by
                    have hinc := hchild_dec v0 w hw
                    rw [hv0sig] at hinc
                    unfold sigma
                    omega
                  have hwbound : H w ≤ 1 := (aux (sigma v0 - 1) (by omega) w hwsig).1 (by omega)
                  have hp1 : p v0 ≤ 1 := by unfold p; omega
                  have hp2 : p w ≤ 1 := by unfold p; omega
                  omega
                have hmexv0 : mex ((children v0).map (fun w => H w ^^^ p v0 ^^^ p w)) = H v0 := by
                  unfold H
                  rfl
                have hmexle : mex ((children v0).map (fun w => H w ^^^ p v0 ^^^ p w)) ≤ 1 := by
                  rw [hmexv0]
                  exact hv0single
                have hall := all_elements_eq_xor_one_of_mex_le_one
                  ((children v0).map (fun w => H w ^^^ p v0 ^^^ p w))
                  (by
                    intro x hx
                    rcases List.mem_map.mp hx with ⟨w, hw, rfl⟩
                    exact hchildrenbits w hw)
                  hmexle
                have hzmem : (H z ^^^ p v0 ^^^ p z) ∈ (children v0).map (fun w => H w ^^^ p v0 ^^^ p w) := by
                  simp [List.mem_map]
                  exact ⟨z, hz0, rfl⟩
                exact hall _ hzmem
              have hz1val : H z ^^^ p v1 ^^^ p z = (H v1) ^^^ 1 := by
                have hvsig : sigma v1 = k - 1 := hv1sig
                have hchildrenbits : ∀ w, w ∈ children v1 →
                    (H w ^^^ p v1 ^^^ p w) = 0 ∨ (H w ^^^ p v1 ^^^ p w) = 1 := by
                  intro w hw
                  have hwsig : sigma w = sigma v1 - 1 := by
                    have hinc := hchild_dec v1 w hw
                    rw [hv1sig] at hinc
                    unfold sigma
                    omega
                  have hwbound : H w ≤ 1 := (aux (sigma v1 - 1) (by omega) w hwsig).1 (by omega)
                  have hp1 : p v1 ≤ 1 := by unfold p; omega
                  have hp2 : p w ≤ 1 := by unfold p; omega
                  omega
                have hmexv1 : mex ((children v1).map (fun w => H w ^^^ p v1 ^^^ p w)) = H v1 := by
                  unfold H
                  rfl
                have hmexle : mex ((children v1).map (fun w => H w ^^^ p v1 ^^^ p w)) ≤ 1 := by
                  rw [hmexv1]
                  exact hv1single
                have hall := all_elements_eq_xor_one_of_mex_le_one
                  ((children v1).map (fun w => H w ^^^ p v1 ^^^ p w))
                  (by
                    intro x hx
                    rcases List.mem_map.mp hx with ⟨w, hw, rfl⟩
                    exact hchildrenbits w hw)
                  hmexle
                have hzmem : (H z ^^^ p v1 ^^^ p z) ∈ (children v1).map (fun w => H w ^^^ p v1 ^^^ p w) := by
                  simp [List.mem_map]
                  exact ⟨z, hz1, rfl⟩
                exact hall _ hzmem
              have hpar : (H v0) ^^^ (H v1) = p v0 ^^^ p v1 := by
                have h := congrArg (fun t => t ^^^ (H z ^^^ p z)) (hz0val.trans hz1val.symm)
                -- hz0val: A0 = a0^^^1; hz1val: A1 = a1^^^1; A0^^^A1 = p v0 ^^^ p v1
                have hleft : (H z ^^^ p v0 ^^^ p z) ^^^ (H z ^^^ p v1 ^^^ p z) = p v0 ^^^ p v1 := by
                  simp [Nat.xor_assoc, Nat.xor_comm, Nat.xor_left_comm]
                have hright : ((H v0) ^^^ 1) ^^^ ((H v1) ^^^ 1) = (H v0) ^^^ (H v1) := by
                  simp [Nat.xor_assoc]
                rw [hz0val, hz1val] at hleft
                rw [hright] at hleft
                exact hleft.symm
              rw [hv0eq, hv1eq] at hpar
              -- tval0 ^^^ tval1 = (H v0 ^^^ p u ^^^ p v0) ^^^ (H v1 ^^^ p u ^^^ p v1)
              -- = (H v0 ^^^ H v1) ^^^ (p v0 ^^^ p v1) = 0
              have : (H v0 ^^^ p u ^^^ p v0) = (H v1 ^^^ p u ^^^ p v1) := by
                have h1 : (H v0 ^^^ p u ^^^ p v0) ^^^ (H v1 ^^^ p u ^^^ p v1) = 0 := by
                  simp [Nat.xor_assoc, Nat.xor_comm, Nat.xor_left_comm, hpar]
                exact (Nat.xor_eq_zero_iff).mp h1
              rw [this]
              have : (0 : Nat) = 0 := rfl
              omega
            have hmex : mex ((children u).map (fun v => H v ^^^ p u ^^^ p v)) ≤ 1 :=
              mex_le_one_of_not_both _ hnotboth
            unfold H
            omega
        · intro ho
          have hmiss : 2 ∉ (children u).map (fun v => H v ^^^ p u ^^^ p v) := by
            simp [List.mem_map]
            intro v hv heq
            have hvsig : sigma v = k - 1 := by
              have hinc := hchild_dec u v hv
              rw [hsu] at hinc
              unfold sigma
              omega
            have hvbound : H v ≤ 1 := (ih (k - 1) (by omega) v hvsig).1 (by omega)
            have hvval : H v ^^^ p u ^^^ p v ≤ 1 := by
              have hp1 : p u ≤ 1 := by unfold p; omega
              have hp2 : p v ≤ 1 := by unfold p; omega
              omega
            omega
          have hmex : mex ((children u).map (fun v => H v ^^^ p u ^^^ p v)) ≤ 2 := by
            by_cases h0 : 0 ∈ (children u).map (fun v => H v ^^^ p u ^^^ p v)
            · by_cases h1 : 1 ∈ (children u).map (fun v => H v ^^^ p u ^^^ p v)
              · have heq : mex ((children u).map (fun v => H v ^^^ p u ^^^ p v)) = 2 :=
                  mex_of_all_lt_and_missing _ 2
                    (by intro i hi; cases i with | zero => simpa | succ j => cases j with | zero => simpa | succ k => omega)
                    hmiss
                omega
              · have heq : mex ((children u).map (fun v => H v ^^^ p u ^^^ p v)) = 1 :=
                  mex_of_all_lt_and_missing _ 1 (by intro i hi; omega) h1
                omega
            · have heq : mex ((children u).map (fun v => H v ^^^ p u ^^^ p v)) = 0 :=
                mex_of_all_lt_and_missing _ 0 (by intro i hi; omega) h0
              omega
          unfold H
          omega
  exact aux (sigma u) u rfl

end UpperKernel

end Kyouen.CapacityUpperKernel