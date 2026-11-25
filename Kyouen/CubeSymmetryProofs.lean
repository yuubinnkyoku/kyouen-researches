import Std
import Kyouen.CubeRules
import Kyouen.CubeSymmetry

namespace Kyouen.CubeSymmetryProofs

open Kyouen
open Kyouen.CubeRules
open Kyouen.CubeSymmetry

-- Bijectivity of every symmetry.
def allSymBijective : Bool :=
  symmetryPerms.all (fun sym =>
    (List.finRange 27).all (fun p =>
      (List.finRange 27).all (fun q =>
        ((applySym sym p == applySym sym q) == (p == q)))))

theorem all_sym_bijective : allSymBijective = true := by native_decide

-- Every symmetry has an inverse in the set.
def allSymHasInverse : Bool :=
  symmetryPerms.all (fun sym =>
    symmetryPerms.any (fun inv =>
      (List.finRange 27).all (fun p => applySym inv (applySym sym p) == p)))

theorem all_sym_has_inverse : allSymHasInverse = true := by native_decide

-- ForbiddenFive is invariant under every symmetry.
def allForbiddenInvariant : Bool :=
  symmetryPerms.all (fun sym =>
    (combinations (List.finRange 27) 5).all (fun five =>
      match five with
      | [a, b, c, d, e] =>
          if decide (ForbiddenFive a b c d e) then
            decide (ForbiddenFive (applySym sym a) (applySym sym b) (applySym sym c) (applySym sym d) (applySym sym e))
          else true
      | _ => true))

theorem all_forbidden_invariant : allForbiddenInvariant = true := by native_decide

end Kyouen.CubeSymmetryProofs