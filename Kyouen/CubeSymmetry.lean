import Std
import Kyouen.CubeRules

namespace Kyouen.CubeSymmetry

open Kyouen.CubeRules

/-- Coordinate transform for a cube symmetry: axes permuted, coordinates possibly flipped. -/
def transformPoint (a b c : Nat) (fa fb fc : Bool) (p : Point) : Point :=
  let c0 := p.val / 9
  let c1 := (p.val / 3) % 3
  let c2 := p.val % 3
  let get (axis : Nat) : Nat :=
    if axis = 0 then c0 else if axis = 1 then c1 else c2
  let new0 := if fa then 2 - get a else get a
  let new1 := if fb then 2 - get b else get b
  let new2 := if fc then 2 - get c else get c
  let idx := new0 * 9 + new1 * 3 + new2
  if h : idx < 27 then ⟨idx, h⟩ else ⟨0, by decide⟩

def permutations3 : List (Nat × Nat × Nat) :=
  [(0,1,2),(0,2,1),(1,0,2),(1,2,0),(2,0,1),(2,1,0)]

def flips3 : List (Bool × Bool × Bool) :=
  [(false,false,false),(false,false,true),(false,true,false),(false,true,true),
   (true,false,false),(true,false,true),(true,true,false),(true,true,true)]

def allSpecs : List (Nat × Nat × Nat × Bool × Bool × Bool) :=
  permutations3.flatMap fun (a, b, c) =>
    flips3.map fun (f, g, h) => (a, b, c, f, g, h)

def mkSym (spec : Nat × Nat × Nat × Bool × Bool × Bool) : List Point :=
  let (a, b, c, f, g, h) := spec
  (List.finRange 27).map (fun p => transformPoint a b c f g h p)

/-- The 48 cube symmetries as point permutations. -/
def symmetryPerms : List (List Point) :=
  allSpecs.map mkSym

theorem symmetryPerms_length : symmetryPerms.length = 48 := by decide

def applySym (sym : List Point) (p : Point) : Point :=
  sym.getD p.val p

def applySymMask (sym : List Point) (mask : Nat) : Nat :=
  (List.finRange 27).foldl (fun acc p =>
    if (mask >>> p.val) &&& 1 == 1 then
      acc ||| (1 <<< (applySym sym p).val)
    else acc
  ) 0

/-- Canonical (minimum) representative of a bitmask under the 48 symmetries. -/
def canonicalMask (mask : Nat) : Nat :=
  (symmetryPerms.map (fun sym => applySymMask sym mask)).foldl Nat.min (1 <<< 27)

/-- Convert a bitmask to its point list. -/
def maskToPoints (mask : Nat) : Position :=
  (List.finRange 27).filter (fun p => (mask >>> p.val) &&& 1 == 1)

/-- Mask popcount. -/
def popcount (n : Nat) : Nat :=
  if n = 0 then 0 else (n % 2) + popcount (n / 2)
termination_by n

end Kyouen.CubeSymmetry