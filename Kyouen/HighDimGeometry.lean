import Kyouen.CubeRules

namespace Kyouen.HighDimGeometry

open Kyouen
open Kyouen.CubeRules

/-- Five vertices of a 2×2×2 cube form a forbidden 5-tuple in the 3D q=5
    game: any five vertices of an axis-aligned 2×2×2 cube lie on the same
    sphere, so their lifted determinant vanishes.  This is the high-dimensional
    analogue of the 2×2 and 3×3 concyclic quadruple lemmas. -/
theorem five_vertices_of_two_by_two_by_two_cube_forbidden :
    ForbiddenFive 0 1 3 4 9 := by
  decide

end Kyouen.HighDimGeometry