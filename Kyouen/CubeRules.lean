import Std
import Kyouen.CertificateSoundness

namespace Kyouen.CubeRules

/-- A point of the 3×3×3 board, indexed like itertools.product(range(3), repeat=3). -/
abbrev Point := Fin 27

/-- A position is a list of occupied points. -/
abbrev Position := List Point

private def coord (p : Point) (axis : Nat) : Int :=
  match axis with
  | 0 => Int.ofNat (p.val / 9)
  | 1 => Int.ofNat ((p.val / 3) % 3)
  | _ => Int.ofNat (p.val % 3)

def x (p : Point) : Int := coord p 0
def y (p : Point) : Int := coord p 1
def z (p : Point) : Int := coord p 2

def q (p : Point) : Int := x p * x p + y p * y p + z p * z p

/-- 4×4 integer determinant. -/
def det4
    (a00 a01 a02 a03 a10 a11 a12 a13 a20 a21 a22 a23 a30 a31 a32 a33 : Int) : Int :=
  a00 * (a11 * (a22 * a33 - a23 * a32) - a12 * (a21 * a33 - a23 * a31) + a13 * (a21 * a32 - a22 * a31)) -
  a01 * (a10 * (a22 * a33 - a23 * a32) - a12 * (a20 * a33 - a23 * a30) + a13 * (a20 * a32 - a22 * a30)) +
  a02 * (a10 * (a21 * a33 - a23 * a31) - a11 * (a20 * a33 - a23 * a30) + a13 * (a20 * a31 - a21 * a30)) -
  a03 * (a10 * (a21 * a32 - a22 * a31) - a11 * (a20 * a32 - a22 * a30) + a12 * (a20 * a31 - a21 * a30))

/-- Five distinct points are forbidden when their lifted 5×5 determinant vanishes.
    Equivalently, the 4×4 determinant of coordinate differences is zero. -/
def ForbiddenFive (a b c d e : Point) : Prop :=
  a ≠ b ∧ a ≠ c ∧ a ≠ d ∧ a ≠ e ∧
  b ≠ c ∧ b ≠ d ∧ b ≠ e ∧
  c ≠ d ∧ c ≠ e ∧
  d ≠ e ∧
  det4
    (q b - q a) (x b - x a) (y b - y a) (z b - z a)
    (q c - q a) (x c - x a) (y c - y a) (z c - z a)
    (q d - q a) (x d - x a) (y d - y a) (z d - z a)
    (q e - q a) (x e - x a) (y e - y a) (z e - z a)
  = 0

instance (a b c d e : Point) : Decidable (ForbiddenFive a b c d e) := by
  unfold ForbiddenFive
  infer_instance

/-- Combinations of `n` elements from a list. -/
def combinations {α : Type} (xs : List α) (n : Nat) : List (List α) :=
  match n with
  | 0 => [[]]
  | n + 1 =>
      match xs with
      | [] => []
      | x :: xs =>
          (combinations xs n).map (fun c => x :: c) ++ combinations xs (n + 1)

/-- Executable check for a forbidden 5-subset. -/
def containsForbiddenBool (s : Position) : Bool :=
  combinations s 5 |>.any fun five =>
    match five with
    | [a, b, c, d, e] => decide (ForbiddenFive a b c d e)
    | _ => false

/-- A position already contains a forbidden 5-tuple. -/
def ContainsForbidden (s : Position) : Prop :=
  containsForbiddenBool s = true

instance (s : Position) : Decidable (ContainsForbidden s) := by
  unfold ContainsForbidden
  infer_instance

/-- A safe move adds an unused point without creating a forbidden 5-tuple. -/
def LegalMove (s : Position) (p : Point) : Prop :=
  p ∉ s ∧ ¬ ContainsForbidden (p :: s)

instance (s : Position) (p : Point) : Decidable (LegalMove s p) := by
  unfold LegalMove
  infer_instance

/-- All safe child positions. -/
def moves (s : Position) : List Position :=
  (List.finRange 27).filterMap fun p =>
    if LegalMove s p then some (p :: s) else none

/-- The empty position. -/
def empty : Position := []

end Kyouen.CubeRules