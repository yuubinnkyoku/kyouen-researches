import Std
import Kyouen.CertificateSoundness
import Kyouen.CubeRules
import Kyouen.CubeSymmetry
import Kyouen.CubeCertData

set_option maxRecDepth 100000

namespace Kyouen.CubeCertificate

open Kyouen
open Kyouen.CubeRules
open Kyouen.CubeSymmetry
open Kyouen.CubeCertData

/-- Quotient game moves: from a canonical mask, list canonical child masks. -/
def cubeMoves (mask : Nat) : List Nat :=
  (List.finRange 27).filterMap fun p =>
    let bit := 1 <<< p.val
    if (mask &&& bit) != 0 then none
    else if containsForbiddenBool (maskToPoints (mask ||| bit)) then none
    else some (canonicalMask (mask ||| bit))

def certLabel (mask : Nat) : Option Bool :=
  certAssoc.find? (fun e => e.1 == mask) |>.map (fun e => e.2)

def cert (mask : Nat) : Option Entry :=
  match certLabel mask with
  | some label => some { outcome := if label then .winning else .losing, rank := 27 - popcount mask }
  | none => none

def certMaskList : List Nat := certAssoc.map (fun e => e.1)

def checkMask (mask : Nat) : Bool :=
  match cert mask with
  | none => true
  | some e =>
      match e.outcome with
      | .winning =>
          (cubeMoves mask).any (fun t =>
            match cert t with
            | some child => decide (child.outcome = .losing) && decide (child.rank < e.rank)
            | none => false)
      | .losing =>
          (cubeMoves mask).all (fun t =>
            match cert t with
            | some child => decide (child.outcome = .winning) && decide (child.rank < e.rank)
            | none => false)

def certValidBool : Bool := certMaskList.all checkMask

-- Generic helper: find? equality implies membership.
theorem find?_mem {α : Type} {p : α → Bool} {xs : List α} {a : α}
    (h : xs.find? p = some a) : a ∈ xs := by
  induction xs with
  | nil =>
      simp [List.find?] at h
  | cons x xs ih =>
      simp [List.find?] at h
      by_cases hpx : p x = true
      · simp [hpx] at h
        subst h
        simp
      · simp [hpx] at h
        have := ih h
        simp [this]

-- Generic helper: find? equality implies predicate holds.
theorem find?_pred {α : Type} {p : α → Bool} {xs : List α} {a : α}
    (h : xs.find? p = some a) : p a = true := by
  induction xs with
  | nil =>
      simp [List.find?] at h
  | cons x xs ih =>
      simp [List.find?] at h
      by_cases hpx : p x = true
      · simp [hpx] at h
        subst h
        exact hpx
      · simp [hpx] at h
        exact ih h

theorem mem_of_cert_some {mask : Nat} {e : Entry} (hs : cert mask = some e) :
    mask ∈ certMaskList := by
  unfold cert at hs
  cases hcl : certLabel mask with
  | none =>
      simp [hcl] at hs
  | some label =>
      simp [hcl] at hs
      unfold certLabel at hcl
      rcases Option.map_eq_some_iff.mp hcl with ⟨entry, hfind, hlab⟩
      have hmem_assoc : entry ∈ certAssoc := find?_mem hfind
      have hpred : (entry.fst == mask) = true :=
        find?_pred (α := Nat × Bool) (p := fun e => e.fst == mask) (xs := certAssoc) (a := entry) hfind
      have heq : entry.fst = mask := eq_of_beq hpred
      have hmaskmem : entry.fst ∈ certMaskList := by
        unfold certMaskList
        exact List.mem_map.mpr ⟨entry, hmem_assoc, rfl⟩
      exact heq ▸ hmaskmem

-- The certificate is locally valid.
theorem cert_valid_bool : certValidBool = true := by
  native_decide

theorem cert_valid : LocallyValid cubeMoves cert := by
  intro s e hs
  have hmem : s ∈ certMaskList := mem_of_cert_some hs
  have hall : certMaskList.all checkMask = true := cert_valid_bool
  have hcheck : checkMask s = true := List.all_eq_true.mp hall s hmem
  cases heo : e.outcome with
  | winning =>
      have hany : (cubeMoves s).any (fun t =>
            match cert t with
            | some child => decide (child.outcome = .losing) && decide (child.rank < e.rank)
            | none => false) = true := by
        simp only [checkMask, hs, heo] at hcheck
        exact hcheck
      rcases List.any_eq_true.mp hany with ⟨t, htmem, httrue⟩
      cases hct : cert t with
      | none =>
          simp [hct] at httrue
      | some child =>
          simp [hct] at httrue
          have ho : child.outcome = .losing := httrue.1
          have hr : child.rank < e.rank := httrue.2
          exact ⟨t, child, htmem, hct, ho, hr⟩
  | losing =>
      have halltrue : (cubeMoves s).all (fun t =>
            match cert t with
            | some child => decide (child.outcome = .winning) && decide (child.rank < e.rank)
            | none => false) = true := by
        simp only [checkMask, hs, heo] at hcheck
        exact hcheck
      intro t htmem
      have htall := List.all_eq_true.mp halltrue t htmem
      cases hct : cert t with
      | none =>
          simp [hct] at htall
      | some child =>
          simp [hct] at htall
          have ho : child.outcome = .winning := htall.1
          have hr : child.rank < e.rank := htall.2
          exact ⟨child, rfl, ho, hr⟩

-- Helper: a single-stone orbit is winning if it has a legal move to a 2-stone P rep.
theorem one_stone_winning_of (mask stone : Nat)
    (hmem : (canonicalMask (mask ||| (1 <<< stone))) ∈ cubeMoves mask)
    (hcert : cert (canonicalMask (mask ||| (1 <<< stone))) =
      some { outcome := .losing, rank := 27 - popcount (canonicalMask (mask ||| (1 <<< stone))) }) :
    Winning cubeMoves mask := by
  let t := canonicalMask (mask ||| (1 <<< stone))
  have hl : Losing cubeMoves t := root_losing_of_valid cert_valid hcert
  exact Winning.move hmem hl

-- Single-stone canonical positions (four orbits) are winning.
theorem one_stone_winning_1 : Winning cubeMoves 1 := by
  apply one_stone_winning_of 1 1
  · native_decide
  · native_decide

theorem one_stone_winning_2 : Winning cubeMoves 2 := by
  apply one_stone_winning_of 2 0
  · native_decide
  · native_decide

theorem one_stone_winning_16 : Winning cubeMoves 16 := by
  apply one_stone_winning_of 16 0
  · native_decide
  · native_decide

theorem one_stone_winning_8192 : Winning cubeMoves 8192 := by
  apply one_stone_winning_of 8192 0
  · native_decide
  · native_decide

-- Empty board is losing (second player wins).
theorem empty_board_losing : Losing cubeMoves 0 := by
  apply Losing.all
  intro t ht
  have hor : t = 1 ∨ t = 2 ∨ t = 16 ∨ t = 8192 := by
    have hall : ∀ u, u ∈ cubeMoves 0 → (u = 1 ∨ u = 2 ∨ u = 16 ∨ u = 8192) := by native_decide
    exact hall t ht
  rcases hor with (rfl | rfl | rfl | rfl)
  · exact one_stone_winning_1
  · exact one_stone_winning_2
  · exact one_stone_winning_16
  · exact one_stone_winning_8192

end Kyouen.CubeCertificate