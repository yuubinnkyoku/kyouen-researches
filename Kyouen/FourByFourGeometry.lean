import Kyouen.Rules

namespace Kyouen.FourByFourGeometry

open Kyouen
open Kyouen.SquareBoard

/-- Four collinear lattice points in the first row of a 4×4 board form a
    forbidden quadruple: they lie on a common line, so their `determinant4`
    vanishes.  This is the 4×4 instance of the rule that four distinct
    collinear points are forbidden, analogous to the 2×2 and 3×3 concyclic
    quadruple lemmas. -/
theorem four_by_four_first_row_forbidden :
    ForbiddenFour (n := 4) ⟨0, by decide⟩ ⟨1, by decide⟩ ⟨2, by decide⟩ ⟨3, by decide⟩ := by
  decide

end Kyouen.FourByFourGeometry