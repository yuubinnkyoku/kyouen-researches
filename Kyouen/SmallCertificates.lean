import Kyouen.Rules
import Kyouen.CertificateSoundness

namespace Kyouen.SmallCertificates

open Kyouen Kyouen.SquareBoard

abbrev P1 := SquareBoard.Point 1
abbrev S1 := SquareBoard.Position 1

def origin : P1 := ⟨0, by decide⟩

def emptyPos : S1 := []

def afterOrigin : S1 := [origin]

def moves1 := SquareBoard.moves 1

def cert : Certificate S1
  | [] => some { outcome := .winning, rank := 1 }
  | [ _ ] => some { outcome := .losing, rank := 0 }
  | _ => none

theorem one_by_one_pos_empty_winning :
    Winning moves1 emptyPos := by
  have hvalid : LocallyValid moves1 cert := by
    intro s e hs
    cases s with
    | nil =>
        simp only [cert, Option.some.injEq] at hs
        subst e
        refine ⟨
          afterOrigin,
          { outcome := .losing, rank := 0 },
          ?_,
          rfl,
          rfl,
          by decide
        ⟩
        simp [moves1, afterOrigin, origin, SquareBoard.moves, SquareBoard.LegalMove,
          SquareBoard.ContainsForbidden]
        decide
    | cons p rest =>
        cases rest with
        | nil =>
            have hp : p = origin := Fin.ext (by omega)
            subst hp
            simp only [cert, Option.some.injEq] at hs
            subst e
            intro t ht
            have hempty : moves1 [origin] = [] := by decide
            simp [hempty] at ht
        | cons q qs =>
            simp [cert] at hs
  exact root_winning_of_valid hvalid rfl

theorem after_origin_losing : Losing moves1 afterOrigin := by
  have hvalid : LocallyValid moves1 cert := by
    intro s e hs
    cases s with
    | nil =>
        simp only [cert, Option.some.injEq] at hs
        subst e
        refine ⟨
          afterOrigin,
          { outcome := .losing, rank := 0 },
          ?_,
          rfl,
          rfl,
          by decide
        ⟩
        simp [moves1, afterOrigin, origin, SquareBoard.moves, SquareBoard.LegalMove,
          SquareBoard.ContainsForbidden]
        decide
    | cons p rest =>
        cases rest with
        | nil =>
            have hp : p = origin := Fin.ext (by omega)
            subst hp
            simp only [cert, Option.some.injEq] at hs
            subst e
            intro t ht
            have hempty : moves1 [origin] = [] := by decide
            simp [hempty] at ht
        | cons q qs =>
            simp [cert] at hs
  exact Kyouen.root_losing_of_valid hvalid rfl