# Literature check: moment certificates for inversive-plane arcs and blocking sets

Independent check for `inversive-moment-certificates-20261124`, 2026-11-25.
The exact-arithmetic verification is in `verify_certificates.py`; the concrete
q=9 3-design / arc-witness spot check is in `design_spot_check.py`.

## Bottom line

| Claim | Verdict | Basis |
|---|---|---|
| **C.** `tau_1(q) >= 2q` for `q >= 9` | **known** | Proved by Bruen–Rothschild (1985); explicitly attributed to them in Kiss–Marcugini–Pambianco (2005). |
| **A.** `K_4(q) <= 2q+1` for `q >= 6` | **unclear** (no exact match found; possibly new as stated) | The standard design bound is `2q+4`; the improvement by 3 was not found in accessible sources. Full texts of the closest arc papers were not accessible. |
| **B.** `K_s(q) <= (s-2)q` for `5 <= s <= q-1`, `q >= 9` | **unclear** (no exact match found; technique standard, closed form possibly new) | The standard design bound is `(s-2)(q+1)+2`; the additive `s` improvement was not found in accessible sources. |

The *technique* — use the four moment identities of a 3-design as linear
constraints and multiply by a cubic that is non-negative on the allowed
intersection sizes — is a standard double-counting / linear-programming
(Farkas, Delsarte-type) certificate. It should not be claimed as a new general
method. What may be new is the explicit closed-form choice of `P_s`/`Q` and the
resulting numerical bounds. The Bruen–Rothschild abstract itself says their
technique is "counting ... in two ways [and] inequalities", so the blocking-set
proof is at least in the same double-counting family; we could not inspect the
full proof to see whether their cubic is the same as `Q(r)`.

## References found

1. **A. A. Bruen, B. L. Rothschild, "Lower bounds on blocking sets",
   *Pacific J. Math.* 118(2) (1985) 303–311.**
   DOI: <https://doi.org/10.2140/pjm.1985.118.303>
   OpenAlex: <https://openalex.org/W1993207305>
   Abstract (OpenAlex): "In a geometry the notion of blocking set ordinarily
   refers to a set of points meeting every line. ... In this paper we obtain
   lower bounds for the size of a blocking set for projective planes and
   inversive planes ... The technique is that of Glynn, counting various sets
   of intersecting ... in two ways [and] inequalities."
   This is the source of the `2q` inversive-plane bound for `q >= 9`.

2. **G. Kiss, S. Marcugini, F. Pambianco, "On blocking sets of inversive
   planes", *J. Combin. Des.* 13(4) (2005) 268–275.**
   DOI: <https://doi.org/10.1002/jcd.20037>
   OpenAlex: <https://openalex.org/W1989229720>
   Abstract: "It was shown by Bruen and Rothschild that `|S| >= 2q` for
   `q >= 9`. We prove that if `q` is sufficiently large, `C` is a fixed natural
   number and `|S| = 2q + C`, then roughly 2/3 of the circles ... meet `S` in one
   point and 1/3 ... in four points."
   This is a **structure** theorem near equality, not a `q >= 4` extension of
   the lower bound.

3. **S. S. Sane, S. S. Shrikhande, N. M. Singhi, "Maximal arcs in designs",
   *Graphs and Combinatorics* 1 (1985) 97–106.**
   DOI: <https://doi.org/10.1007/BF02582933>
   OpenAlex: <https://openalex.org/W2072187058>
   The accessible metadata/abstract describes maximal (block) arcs in symmetric
   2-designs and the `(alpha,n)`-arc terminology; it does **not** establish the
   3-design cubic moment bound used here. Treat this as a terminology /
   framework reference only unless the full text says otherwise.

4. **T. Szőnyi, "Blocking sets in finite planes and spaces", *Ratio
   Mathematica* 5 (1992) 93–106.**
   OpenAlex: <https://openalex.org/W2779660327>
   Publisher page: <http://eiris.it/ojs/index.php/ratiomathematica/article/view/196>
   Survey cited by arXiv:2510.15332 for a lower bound on blocking sets in
   inversive planes built from unions of circles. Useful survey pointer; full
   text not inspected.

5. **S. Asgarli, D. Ghioca, C. H. Yip, "Blocking sets from a union of plane
   curves", arXiv:2510.15332.**
   <https://arxiv.org/abs/2510.15332>
   Read in full. It is about projective planes and cites Szőnyi's inversive-plane
   remark; it does not contain the arc bounds A/B.

6. Adjacent arc-construction literature (titles/abstracts only):
   - "Large k-arcs in inversive planes of odd order", *J. Geom.* 66 (1999)
     187–191, DOI: <https://doi.org/10.1007/BF01225681>
   - "Complete arcs in inversive planes over prime fields", *Discrete Math.*
     (2002), <https://www.sciencedirect.com/science/article/pii/S0012365X01003971>
   These construct large arcs (lower bounds on `K_s`), not the upper bounds
   A/B. They were not read in full.

7. General method: P. Delsarte, *An algebraic approach to the association
   schemes of coding theory*, Philips Research Reports Suppl. 10 (1973), is the
   standard source for linear-programming / eigenvalue bounds in designs and
   codes. The four moment equations here are the first four moments of the
   intersection distribution; any cubic multiplier gives a valid LP/Farkas
   inequality. No single reference was found that states the exact `P_s` or
   `Q` certificates.

## Citation problems in the current parent README

- README line 62 says Kiss–Marcugini–Pambianco (2005) extended the `2q` bound
  to `q >= 4`. The abstract of the cited JCD paper does **not** support this:
  it attributes `q >= 9` to Bruen–Rothschild and proves a structure theorem for
  `q` sufficiently large. The `q = 4,5` equalities `tau_1(4)=8`, `tau_1(5)=10`
  in this repo are computational results of the parent experiment, not a
  published extension by Kiss et al.
- README line 63 cites Sane–Shrikhande–Singhi (1985) for the `(alpha,n)`-arc
  framework. That is plausible for terminology, but the paper's accessible
  metadata is about maximal arcs in symmetric 2-designs, not the 3-design
  cubic moment bound. It should not be cited as establishing A/B.
- The README's statement that no "3 moments + cubic polynomial" bound was found
  is consistent with this search, but the *method* is standard LP/Farkas; the
  novelty claim should be restricted to the explicit closed forms and bounds.

## Access limits

- Full texts of Bruen–Rothschild (Project Euclid / MSP), Kiss–Marcugini–
  Pambianco (Wiley), and Sane–Shrikhande–Singhi (Springer) were paywalled or
  blocked (HTTP 401/403/timeouts). Conclusions above use OpenAlex/Semantic
  Scholar abstracts and metadata, search snippets, and the arXiv paper's
  citations. No MathSciNet/zbMATH access.
- "Unclear" for A/B therefore reflects incomplete full-text access, not
  evidence that the results are new. A library/proxy full-text check of the
  three papers above, plus a zbMATH/MathSciNet search for "arcs in inversive
  planes" upper bounds, is the recommended next step before claiming novelty.
