import Kyouen.Rules
import Lean.Elab.Tactic.Grind

/-!
# Integer-coordinate circle/line meaning of the rule determinant

A circle is represented by a nonzero integer scale and the squared-distance
equation `(scale*x-cx)^2 + (scale*y-cy)^2 = radiusSq`. Thus its centre is
`(cx/scale,cy/scale)` and squared radius is `radiusSq/scale^2`. This avoids
adding a real-number library to the certificate checker. The theorem connects
the actual rule determinant to these equations, not to a second determinant
test. Real Euclidean geometry and square roots are not defined in this module.
-/

namespace Kyouen.IntegerGeometry

abbrev Point := Int × Int

def norm (p : Point) : Int := p.1 * p.1 + p.2 * p.2
def cross (u v : Point) : Int := u.1 * v.2 - u.2 * v.1
def sub (p a : Point) : Point := (p.1 - a.1, p.2 - a.2)

def det3 (a b c d e f g h i : Int) : Int :=
  a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)

def determinant (a b c d : Point) : Int :=
  norm a * det3 b.1 b.2 1 c.1 c.2 1 d.1 d.2 1 -
  a.1 * det3 (norm b) b.2 1 (norm c) c.2 1 (norm d) d.2 1 +
  a.2 * det3 (norm b) b.1 1 (norm c) c.1 1 (norm d) d.1 1 -
  det3 (norm b) b.1 b.2 (norm c) c.1 c.2 (norm d) d.1 d.2

def AllFour (P : Point → Prop) (a b c d : Point) : Prop :=
  P a ∧ P b ∧ P c ∧ P d

/-- A genuine line: at least one normal coefficient is nonzero. -/
def OnLine (a b c d : Point) : Prop :=
  ∃ A B C : Int, (A ≠ 0 ∨ B ≠ 0) ∧
    AllFour (fun p => A * p.1 + B * p.2 + C = 0) a b c d

/-- A circle in cleared-denominator squared-distance coordinates. -/
def OnCircle (a b c d : Point) : Prop :=
  ∃ scale cx cy radiusSq : Int, scale ≠ 0 ∧ 0 ≤ radiusSq ∧
    AllFour (fun p => (scale * p.1 - cx) ^ 2 +
      (scale * p.2 - cy) ^ 2 = radiusSq) a b c d

private def residual (u v z : Point) : Int :=
  norm u * cross v z - norm v * cross u z + norm z * cross u v

private theorem translate (a b c d : Point) :
    determinant a b c d = -residual (sub b a) (sub c a) (sub d a) := by
  simp only [determinant, residual, det3, sub, norm, cross]
  grind

/-- A nonzero linear dependence of the lifted coordinates kills the determinant. -/
private theorem dependence (a b c d : Point) (A B C D : Int)
    (h : AllFour (fun p => A * norm p + B * p.1 + C * p.2 + D = 0) a b c d) :
    A * determinant a b c d = 0 ∧
      B * determinant a b c d = 0 ∧ C * determinant a b c d = 0 := by
  rcases h with ⟨ha, hb, hc, hd⟩
  simp only [determinant, det3, norm] at *
  grind

private theorem line_det {a b c d : Point} (h : OnLine a b c d) :
    determinant a b c d = 0 := by
  obtain ⟨B, C, D, hne, h⟩ := h
  have hh := dependence a b c d 0 B C D (by simpa using h)
  rcases hne with hB | hC
  · exact (Int.mul_eq_zero.mp hh.2.1).resolve_left hB
  · exact (Int.mul_eq_zero.mp hh.2.2).resolve_left hC

private theorem circle_det {a b c d : Point} (h : OnCircle a b c d) :
    determinant a b c d = 0 := by
  obtain ⟨s, x, y, r, hs, _, ha, hb, hc, hd⟩ := h
  have hpoly : AllFour (fun p => (s*s) * norm p + (-2*s*x) * p.1 +
      (-2*s*y) * p.2 + (x*x+y*y-r) = 0) a b c d := by
    simp only [AllFour, norm]
    grind
  have hh := (dependence a b c d _ _ _ _ hpoly).1
  exact (Int.mul_eq_zero.mp hh).resolve_left (Int.mul_ne_zero hs hs)

private theorem circle_of_equations (a : Point) (u v z : Point) (A B C : Int)
    (hA : A ≠ 0)
    (hu : A * norm u = B * u.1 + C * u.2)
    (hv : A * norm v = B * v.1 + C * v.2)
    (hz : A * norm z = B * z.1 + C * z.2) :
    OnCircle a (a.1+u.1,a.2+u.2) (a.1+v.1,a.2+v.2)
      (a.1+z.1,a.2+z.2) := by
  refine ⟨2*A, 2*A*a.1+B, 2*A*a.2+C, B^2+C^2, ?_, ?_, ?_⟩
  · omega
  · have hB := Int.sq_nonneg B
    have hC := Int.sq_nonneg C
    omega
  · simp only [AllFour, norm] at *
    grind

/-- For distinct first two points, the determinant vanishes exactly on a
circle or line in integer-coordinate squared-distance form. -/
theorem determinant_zero_iff (a b c d : Point) (hab : a ≠ b) :
    determinant a b c d = 0 ↔ OnCircle a b c d ∨ OnLine a b c d := by
  constructor
  · intro hdet
    let u := sub b a
    let v := sub c a
    let z := sub d a
    have hres : residual u v z = 0 := by
      rw [translate] at hdet
      exact Int.neg_eq_zero.mp hdet
    have hreturn : ∀ A B C, A ≠ 0 →
        A * norm u = B*u.1+C*u.2 → A * norm v = B*v.1+C*v.2 →
        A * norm z = B*z.1+C*z.2 → OnCircle a b c d := by
      intro A B C hA hu hv hz
      have hh := circle_of_equations a u v z A B C hA hu hv hz
      have hadd (p : Point) : (a.1+(sub p a).1,a.2+(sub p a).2) = p := by
        apply Prod.ext <;> simp only [sub] <;> omega
      simpa only [u, v, z, hadd] using hh
    by_cases hv : cross u v = 0
    · by_cases hz : cross u z = 0
      · right
        refine ⟨-u.2, u.1, u.2*a.1-u.1*a.2, ?_, ?_⟩
        · by_cases hx : u.1 = 0
          · left
            intro hy
            have heq : a = b := by
              simp only [u, sub] at hx hy
              apply Prod.ext <;> omega
            exact hab heq
          · exact Or.inr hx
        · simp only [AllFour]
          simp only [cross, u, v, z, sub] at hv hz ⊢
          grind
      · left
        apply hreturn (cross u z) (norm u*z.2-norm z*u.2)
          (u.1*norm z-z.1*norm u) hz
        all_goals simp only [residual, norm, cross] at *
        all_goals grind
    · left
      apply hreturn (cross u v) (norm u*v.2-norm v*u.2)
        (u.1*norm v-v.1*norm u) hv
      all_goals simp only [residual, norm, cross] at *
      all_goals grind
  · rintro (h | h)
    · exact circle_det h
    · exact line_det h

/-- Public coordinates of the square-board rule, without changing its encoding. -/
def boardPoint {n : Nat} (p : SquareBoard.Point n) : Point :=
  (Int.ofNat (p.val % n), Int.ofNat (p.val / n))

theorem rule_determinant {n : Nat} (a b c d : SquareBoard.Point n) :
    SquareBoard.determinant4 a b c d =
      determinant (boardPoint a) (boardPoint b) (boardPoint c) (boardPoint d) := by
  rfl

theorem boardPoint_injective {n : Nat} {a b : SquareBoard.Point n}
    (h : boardPoint a = boardPoint b) : a = b := by
  have hx := congrArg Prod.fst h
  have hy := congrArg Prod.snd h
  have hxm : a.val % n = b.val % n := Int.ofNat_inj.mp hx
  have hym : a.val / n = b.val / n := Int.ofNat_inj.mp hy
  have ha := Nat.mod_add_div a.val n
  have hb := Nat.mod_add_div b.val n
  rw [hxm, hym] at ha
  apply Fin.ext
  omega

/-- The exact forbidden-four rule, now expressed by circle or line equations. -/
theorem forbiddenFour_iff {n : Nat} (a b c d : SquareBoard.Point n) :
    SquareBoard.ForbiddenFour a b c d ↔
      a ≠ b ∧ a ≠ c ∧ a ≠ d ∧ b ≠ c ∧ b ≠ d ∧ c ≠ d ∧
        (OnCircle (boardPoint a) (boardPoint b) (boardPoint c) (boardPoint d) ∨
         OnLine (boardPoint a) (boardPoint b) (boardPoint c) (boardPoint d)) := by
  have hab (h : a ≠ b) : boardPoint a ≠ boardPoint b :=
    fun heq => h (boardPoint_injective heq)
  simp only [SquareBoard.ForbiddenFour, rule_determinant]
  constructor
  · rintro ⟨h1, h2, h3, h4, h5, h6, hd⟩
    exact ⟨h1, h2, h3, h4, h5, h6,
      (determinant_zero_iff _ _ _ _ (hab h1)).mp hd⟩
  · rintro ⟨h1, h2, h3, h4, h5, h6, hg⟩
    exact ⟨h1, h2, h3, h4, h5, h6,
      (determinant_zero_iff _ _ _ _ (hab h1)).mpr hg⟩

end Kyouen.IntegerGeometry
