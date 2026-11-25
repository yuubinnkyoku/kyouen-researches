import Kyouen.Rules
import Kyouen.CertificateSoundness

namespace Kyouen.SquareCert2x2

open Kyouen Kyouen.SquareBoard

abbrev P2 := SquareBoard.Point 2
abbrev S2 := SquareBoard.Position 2

def certEntries : List (S2 × Kyouen.Entry) := [
  ([], { outcome := Kyouen.Outcome.winning, rank := 4 }),
  ([⟨3, by decide⟩], { outcome := Kyouen.Outcome.losing, rank := 3 }),
  ([⟨2, by decide⟩, ⟨3, by decide⟩], { outcome := Kyouen.Outcome.winning, rank := 2 }),
  ([⟨1, by decide⟩, ⟨2, by decide⟩, ⟨3, by decide⟩], { outcome := Kyouen.Outcome.losing, rank := 1 }),
  ([⟨0, by decide⟩, ⟨2, by decide⟩, ⟨3, by decide⟩], { outcome := Kyouen.Outcome.losing, rank := 1 }),
  ([⟨1, by decide⟩, ⟨3, by decide⟩], { outcome := Kyouen.Outcome.winning, rank := 2 }),
  ([⟨2, by decide⟩, ⟨1, by decide⟩, ⟨3, by decide⟩], { outcome := Kyouen.Outcome.losing, rank := 1 }),
  ([⟨0, by decide⟩, ⟨1, by decide⟩, ⟨3, by decide⟩], { outcome := Kyouen.Outcome.losing, rank := 1 }),
  ([⟨0, by decide⟩, ⟨3, by decide⟩], { outcome := Kyouen.Outcome.winning, rank := 2 }),
  ([⟨2, by decide⟩, ⟨0, by decide⟩, ⟨3, by decide⟩], { outcome := Kyouen.Outcome.losing, rank := 1 }),
  ([⟨1, by decide⟩, ⟨0, by decide⟩, ⟨3, by decide⟩], { outcome := Kyouen.Outcome.losing, rank := 1 }),
  ([⟨2, by decide⟩], { outcome := Kyouen.Outcome.losing, rank := 3 }),
  ([⟨3, by decide⟩, ⟨2, by decide⟩], { outcome := Kyouen.Outcome.winning, rank := 2 }),
  ([⟨1, by decide⟩, ⟨3, by decide⟩, ⟨2, by decide⟩], { outcome := Kyouen.Outcome.losing, rank := 1 }),
  ([⟨0, by decide⟩, ⟨3, by decide⟩, ⟨2, by decide⟩], { outcome := Kyouen.Outcome.losing, rank := 1 }),
  ([⟨1, by decide⟩, ⟨2, by decide⟩], { outcome := Kyouen.Outcome.winning, rank := 2 }),
  ([⟨3, by decide⟩, ⟨1, by decide⟩, ⟨2, by decide⟩], { outcome := Kyouen.Outcome.losing, rank := 1 }),
  ([⟨0, by decide⟩, ⟨1, by decide⟩, ⟨2, by decide⟩], { outcome := Kyouen.Outcome.losing, rank := 1 }),
  ([⟨0, by decide⟩, ⟨2, by decide⟩], { outcome := Kyouen.Outcome.winning, rank := 2 }),
  ([⟨3, by decide⟩, ⟨0, by decide⟩, ⟨2, by decide⟩], { outcome := Kyouen.Outcome.losing, rank := 1 }),
  ([⟨1, by decide⟩, ⟨0, by decide⟩, ⟨2, by decide⟩], { outcome := Kyouen.Outcome.losing, rank := 1 }),
  ([⟨1, by decide⟩], { outcome := Kyouen.Outcome.losing, rank := 3 }),
  ([⟨3, by decide⟩, ⟨1, by decide⟩], { outcome := Kyouen.Outcome.winning, rank := 2 }),
  ([⟨2, by decide⟩, ⟨3, by decide⟩, ⟨1, by decide⟩], { outcome := Kyouen.Outcome.losing, rank := 1 }),
  ([⟨0, by decide⟩, ⟨3, by decide⟩, ⟨1, by decide⟩], { outcome := Kyouen.Outcome.losing, rank := 1 }),
  ([⟨2, by decide⟩, ⟨1, by decide⟩], { outcome := Kyouen.Outcome.winning, rank := 2 }),
  ([⟨3, by decide⟩, ⟨2, by decide⟩, ⟨1, by decide⟩], { outcome := Kyouen.Outcome.losing, rank := 1 }),
  ([⟨0, by decide⟩, ⟨2, by decide⟩, ⟨1, by decide⟩], { outcome := Kyouen.Outcome.losing, rank := 1 }),
  ([⟨0, by decide⟩, ⟨1, by decide⟩], { outcome := Kyouen.Outcome.winning, rank := 2 }),
  ([⟨3, by decide⟩, ⟨0, by decide⟩, ⟨1, by decide⟩], { outcome := Kyouen.Outcome.losing, rank := 1 }),
  ([⟨2, by decide⟩, ⟨0, by decide⟩, ⟨1, by decide⟩], { outcome := Kyouen.Outcome.losing, rank := 1 }),
  ([⟨0, by decide⟩], { outcome := Kyouen.Outcome.losing, rank := 3 }),
  ([⟨3, by decide⟩, ⟨0, by decide⟩], { outcome := Kyouen.Outcome.winning, rank := 2 }),
  ([⟨2, by decide⟩, ⟨3, by decide⟩, ⟨0, by decide⟩], { outcome := Kyouen.Outcome.losing, rank := 1 }),
  ([⟨1, by decide⟩, ⟨3, by decide⟩, ⟨0, by decide⟩], { outcome := Kyouen.Outcome.losing, rank := 1 }),
  ([⟨2, by decide⟩, ⟨0, by decide⟩], { outcome := Kyouen.Outcome.winning, rank := 2 }),
  ([⟨3, by decide⟩, ⟨2, by decide⟩, ⟨0, by decide⟩], { outcome := Kyouen.Outcome.losing, rank := 1 }),
  ([⟨1, by decide⟩, ⟨2, by decide⟩, ⟨0, by decide⟩], { outcome := Kyouen.Outcome.losing, rank := 1 }),
  ([⟨1, by decide⟩, ⟨0, by decide⟩], { outcome := Kyouen.Outcome.winning, rank := 2 }),
  ([⟨3, by decide⟩, ⟨1, by decide⟩, ⟨0, by decide⟩], { outcome := Kyouen.Outcome.losing, rank := 1 }),
  ([⟨2, by decide⟩, ⟨1, by decide⟩, ⟨0, by decide⟩], { outcome := Kyouen.Outcome.losing, rank := 1 }),
]

def cert (s : S2) : Option Kyouen.Entry :=
  (certEntries.find? (fun e => e.1 == s)).map (fun e => e.2)

def certPosList : List S2 := certEntries.map (fun e => e.1)

-- Generic helpers
theorem find?_mem {α : Type} {p : α → Bool} {xs : List α} {a : α}
    (h : xs.find? p = some a) : a ∈ xs := by
  induction xs with
  | nil => simp [List.find?] at h
  | cons x xs ih =>
      simp [List.find?] at h
      by_cases hpx : p x = true
      · simp [hpx] at h; subst h; simp
      · simp [hpx] at h; have := ih h; simp [this]

theorem find?_pred {α : Type} {p : α → Bool} {xs : List α} {a : α}
    (h : xs.find? p = some a) : p a = true := by
  induction xs with
  | nil => simp [List.find?] at h
  | cons x xs ih =>
      simp [List.find?] at h
      by_cases hpx : p x = true
      · simp [hpx] at h; subst h; exact hpx
      · simp [hpx] at h; exact ih h

theorem mem_of_cert_some {s : S2} {e : Kyouen.Entry} (hs : cert s = some e) :
    s ∈ certPosList := by
  unfold cert at hs
  cases hcl : certEntries.find? (fun e => e.1 == s) with
  | none => simp [hcl] at hs
  | some entry =>
      simp [hcl] at hs
      have hmem_assoc : entry ∈ certEntries := find?_mem (α := S2 × Kyouen.Entry) (p := fun e => e.1 == s) (xs := certEntries) (a := entry) hcl
      have hpred : (entry.1 == s) = true := find?_pred (α := S2 × Kyouen.Entry) (p := fun e => e.1 == s) (xs := certEntries) (a := entry) hcl
      have heq : entry.1 = s := eq_of_beq hpred
      have hmaskmem : entry.1 ∈ certPosList := by
        unfold certPosList
        exact List.mem_map.mpr ⟨entry, hmem_assoc, rfl⟩
      exact heq ▸ hmaskmem

def checkPos (s : S2) : Bool :=
  match cert s with
  | none => true
  | some e =>
      match e.outcome with
      | .winning =>
          (SquareBoard.moves 2 s).any (fun t =>
            match cert t with
            | some child => decide (child.outcome = Kyouen.Outcome.losing) && decide (child.rank < e.rank)
            | none => false)
      | .losing =>
          (SquareBoard.moves 2 s).all (fun t =>
            match cert t with
            | some child => decide (child.outcome = Kyouen.Outcome.winning) && decide (child.rank < e.rank)
            | none => false)

def certValidBool : Bool := certPosList.all checkPos

theorem cert_valid_bool : certValidBool = true := by
  native_decide

theorem cert_valid : Kyouen.LocallyValid (SquareBoard.moves 2) cert := by
  intro s e hs
  have hmem : s ∈ certPosList := mem_of_cert_some hs
  have hall : certPosList.all checkPos = true := cert_valid_bool
  have hcheck : checkPos s = true := List.all_eq_true.mp hall s hmem
  cases heo : e.outcome with
  | winning =>
      have hany : (SquareBoard.moves 2 s).any (fun t =>
            match cert t with
            | some child => decide (child.outcome = Kyouen.Outcome.losing) && decide (child.rank < e.rank)
            | none => false) = true := by
        simp only [checkPos, hs, heo] at hcheck
        exact hcheck
      rcases List.any_eq_true.mp hany with ⟨t, htmem, httrue⟩
      cases hct : cert t with
      | none => simp [hct] at httrue
      | some child =>
          simp [hct] at httrue
          have ho : child.outcome = Kyouen.Outcome.losing := httrue.1
          have hr : child.rank < e.rank := httrue.2
          exact ⟨t, child, htmem, hct, ho, hr⟩
  | losing =>
      have halltrue : (SquareBoard.moves 2 s).all (fun t =>
            match cert t with
            | some child => decide (child.outcome = Kyouen.Outcome.winning) && decide (child.rank < e.rank)
            | none => false) = true := by
        simp only [checkPos, hs, heo] at hcheck
        exact hcheck
      intro t htmem
      have htall := List.all_eq_true.mp halltrue t htmem
      cases hct : cert t with
      | none => simp [hct] at htall
      | some child =>
          have ho : child.outcome = Kyouen.Outcome.winning := by
            simp [hct] at htall
            exact htall.1
          have hr : child.rank < e.rank := by
            simp [hct] at htall
            exact htall.2
          exact ⟨child, rfl, ho, hr⟩

-- Empty board is winning (first player).
theorem empty_board_winning : Kyouen.Winning (SquareBoard.moves 2) [] := by
  have hroot : cert [] = some { outcome := Kyouen.Outcome.winning, rank := 4 } := by
    native_decide
  exact Kyouen.root_winning_of_valid cert_valid hroot

end Kyouen.SquareCert2x2