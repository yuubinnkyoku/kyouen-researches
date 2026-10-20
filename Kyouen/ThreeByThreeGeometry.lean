import Kyouen.Rules

namespace Kyouen.ThreeByThreeGeometry

open Kyouen.SquareBoard

/-- The four corner points of a 3×3 board form a forbidden quadruple
    (they are concyclic): the 3×3 instance of the rule that four distinct
    concyclic points are forbidden. -/
theorem three_by_three_corners_forbidden :
    ForbiddenFour (n := 3) ⟨0, by decide⟩ ⟨2, by decide⟩
      ⟨6, by decide⟩ ⟨8, by decide⟩ := by
  decide

end Kyouen.ThreeByThreeGeometry