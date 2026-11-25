import Kyouen.Rules

namespace Kyouen.TwoByTwoGeometry

open Kyouen.SquareBoard

/-- The four points of a 2×2 board form a forbidden quadruple (they are concyclic). -/
theorem two_by_two_corners_forbidden :
    ForbiddenFour (n := 2) ⟨0, by decide⟩ ⟨1, by decide⟩
      ⟨2, by decide⟩ ⟨3, by decide⟩ := by
  decide

end Kyouen.TwoByTwoGeometry