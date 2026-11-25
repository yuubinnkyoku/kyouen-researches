import Kyouen.OddInvolution
import Kyouen.IntegerGeometry
import Lean.Elab.GuardMsgs

/-! Small kernel-checked boundary cases for the new abstract interfaces. -/

namespace Kyouen.FormalizationChecks

open OddInvolution

private def board : List (Bool × Bool) :=
  [(false, false), (false, true), (true, false), (true, true)]

private def mirror (p : Bool × Bool) : Bool × Bool := (!p.1, p.2)

private def blocks : List ((Bool × Bool) → Bool) := [fun _ => true]

/-- A nonempty block really forbids the third stone on this four-point board. -/
example : ¬ Safe blocks 3 [(false, false), (false, true), (true, false)] := by decide

/-- Instantiate the sufficient condition, including the actual block hypotheses. -/
example : Losing (moves board blocks 3) [] := by
  apply symmetric_losing board blocks 3 mirror
  · intro x; cases x with | mk x y => cases x <;> rfl
  · intro x; cases x with | mk x y => cases x <;> cases y <;> decide
  · intro x; cases x with | mk x y => cases x <;> cases y <;> decide
  · constructor
    · intro B hB
      simp only [blocks, List.mem_cons, List.not_mem_nil, or_false] at hB
      subst B
      simp [blocks]
    · intro B hB p _ _ x
      simp only [blocks, List.mem_cons, List.not_mem_nil, or_false] at hB
      subst B
      rfl
  · decide
  · simp
  · simp
  · decide
  · intro x; simp

/-- Oddness is essential: with threshold two the same board is winning. -/
example : Winning (moves board blocks 2) [] := by
  apply Winning.move (t := [(false, false)]) (by decide)
  apply Losing.all
  intro t ht
  have hterminal : moves board blocks 2 [(false, false)] = [] := by decide
  simp [hterminal] at ht

open IntegerGeometry

example : OnCircle (0,0) (1,0) (0,1) (1,1) :=
  ⟨2, 1, 1, 2, by decide, by decide, by unfold AllFour; decide⟩

example : OnLine (0,0) (1,0) (2,0) (3,0) :=
  ⟨0, 1, 0, Or.inr (by decide), by unfold AllFour; decide⟩

/-- Exercise the branch where the first three points are collinear but the
fourth is not: no circle or line contains all four. -/
example : ¬ (OnCircle (0,0) (1,0) (2,0) (0,1) ∨
    OnLine (0,0) (1,0) (2,0) (0,1)) := by
  intro h
  have hd := (determinant_zero_iff (0,0) (1,0) (2,0) (0,1) (by decide)).mpr h
  have hn : determinant (0,0) (1,0) (2,0) (0,1) ≠ 0 := by decide
  exact hn hd

/-- Directly test the connection to the encoded square-board rule. -/
example : SquareBoard.ForbiddenFour
    (n := 2) ⟨0, by decide⟩ ⟨1, by decide⟩ ⟨2, by decide⟩ ⟨3, by decide⟩ := by
  apply (forbiddenFour_iff _ _ _ _).mpr
  refine ⟨by decide, by decide, by decide, by decide, by decide, by decide, Or.inl ?_⟩
  exact ⟨2, 1, 1, 2, by decide, by decide, by unfold AllFour; decide⟩

-- Audit for accidental sorryAx or native_decide trust extensions.
/-- info: 'Kyouen.OddInvolution.symmetric_losing' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms OddInvolution.symmetric_losing
/-- info: 'Kyouen.IntegerGeometry.determinant_zero_iff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms IntegerGeometry.determinant_zero_iff
/-- info: 'Kyouen.IntegerGeometry.forbiddenFour_iff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms IntegerGeometry.forbiddenFour_iff

end Kyouen.FormalizationChecks
