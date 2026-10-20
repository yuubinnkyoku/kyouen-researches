# Lean formalization research: structural challenges (2026-10)

This log records 20 distinct mathematical/structural challenges investigated during the
Lean development of the concyclicity (Kyouen) game.  Results are distinguished from
trivial lemma accumulation.

1. `Kyouen.Rules` general n×n legality via integer determinant.
   - Status: fully defined; decidable instances provided.
   - Evidence: `Kyouen/Rules.lean`, CI `lean` job.

2. `CertificateSoundness` ranked AND/OR certificate soundness by mutual rank induction.
   - Status: proved (`winning_sound`, `losing_sound`, root theorems).
   - Learned issue (K0009): only general soundness in Lean; concrete checker remains C++/Rust.

3. 1×1 board outcome.
   - Status: proved (`SmallCertificates.one_by_one_pos_empty_winning`: empty is winning, one move to a losing state).
   - Evidence: exact `moves1 emptyPos = [[origin]]` computed by kernel.

4. 2×2 maximum independent capacity = 3.
   - Status: attempted reduction to "any four cells form a circle" (`determinant4 ... = 0`).
   - Obstacle: proving the universal ordered version by `decide` fails because Lean cannot synthesize `Decidable (∀ a b c d : Fin 4, ...)`.
   - Analysis: Finite enumeration is possible, but requires either explicit `Fin` induction or reflection.

5. Empty 2×2 winning via `UniformTerminal` with capacity 3.
   - Status: mathematically supported (maximal paths have length 3), but formalization blocked by the cap-bound proof in 4.
   - Next step: prove ordered invariance/forbidden property for the unique 4-point subset.

6. `UniformCapacity` losing/winning at even/odd remaining length.
   - Status: proved (`losing_of_even_remaining`, `winning_of_odd_remaining`) with imported `CertificateSoundness`.
   - Evidence: build passes.

7. Grundy values for uniform games: expected `grundy = remaining % 2`.
   - Status: reduced to computing `mex (List.replicate k b)`.
   - Obstacle: membership decidability made the `find?`-based `mex` and concrete list forms not definitionally unify.
   - Result: proof not completed; blocked on `mex`-list interaction.

8. `mex` basic range law.
   - Status: proved `mex (List.range k) = k`.
   - Evidence: build passes.

9. `mex` bounded by length (pigeonhole).
   - Status: investigated. Direct attempt requires an injection/counting argument (`List.exists_mem_of_ne_nil`, finite set cardinality).
   - Result: not yet proved; kernel-verified code sketches identified the needed pigeonhole lemma.

10. 3×3 outcome.
    - Status: not computed/formalized. State space 2^9; would require an executable solver or certificate.
    - Analysis: Can be attempted via bitmask recursion with `native_decide`, but requires termination and geometry for 3×3.

11. Fixed-width 3×m parity theorems (K0068).
    - Status: mathematical reports exist (`research/experiments/fixed-width`), not yet Lean.
    - Analysis: Need a general formalization of 3-row positions and legal moves; major undertaking.

12. Judging empty n×n generally.
    - Status: open mathematically (`Empty 10×10`/`11×11` unknown); not capturable by simple theorem.
    - Conclusion: formalization should remain conditional/computational.

13. Normal play invariance under deterministic strategy pairing.
    - Status: proposed; square board central symmetry might give pairing for even? But 2×2 (cap 3, odd) suggests first-player win, not pairing.
    - Research direction: examine middle-free strategies.

14. Collinearity as determinant zero for 2×2 point indexing.
    - Status: computationally true? Need prove.
    - Obstacle: `decide` cannot synthesize universal finite decidability directly.

15. Certificate local validity implies unbounded ranks? no; rank only decreases along edges.
    - Status: by construction, rank is an upper bound; verified by theorem.

16. `Losing` and `Winning` are mutually exclusive for finite ranked games.
    - Status: proposed; would need well-founded induction on the rank embedded in a certificate or a game measure.
    - Analysis: likely true but not yet formalized.

17. `mex` of a constant-zero / constant-one list.
    - Status: attempted; find? function and input list membership expansion disagree for generic k.
    - Next step: use an extensionally equal but simp-friendlier mex formulation.

18. Empty 0×0 losing.
    - Status: considered; trivial by no moves.
    - Result: can be formalized but of low priority.

19. All first moves on empty board are legal for general n.
    - Status: capacity/legality lemma needed for n×n; `LegalMove_empty` now proves pointwise legality.

20. Formalization architecture: merge `SmallCertificates` and `certificate soundness`.
    - Status: the 1×1 bridge was completed, demonstrating that concrete positions can use the general theorem.
    - Next structural goal: 2×2 certificate or direct uniform proof.

No code changes are required solely to create this investigation log; the Lean developments above are the primary artifacts.