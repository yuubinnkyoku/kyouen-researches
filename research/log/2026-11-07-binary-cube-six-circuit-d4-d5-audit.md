# Six-point affine circuits in binary cubes (d=4,5), 2026-11-07

## Result (finite exhaustive enumeration, not an all-dimensional theorem)

For the binary cube V_d={0,1}^d, a six-point **circuit** is a set of six distinct vertices with affine rank <6 and every five-point subset of affine rank 5.

| d | all six-point circuits | support 4 | support 5 |
|---|---:|---:|---:|
| 4 | 1,088 | 1,088 | 0 |
| 5 | 41,760 | 10,880 | 30,880 |

Here support is the number of coordinates on which the six vertices are not all equal. For d=4 there are C(16,6)=8,008 candidate sets; for d=5 there are C(32,6)=906,192 candidate sets. Both complete loops finished.

## Reproduction and exactness

The accompanying C++ verifier enumerates all increasing six-tuples and tests affine ranks over F_101. Each row of the rank matrix is (1,x_1,...,x_d). For d<=5, subtracting the first row reduces every nonzero maximal minor to a determinant of a square 0,±1 matrix of order at most 5. Hadamard gives absolute value <=5^(5/2)<56<101. Thus all integer minors vanish iff their residues modulo 101 vanish, so rank over F_101 equals rank over Q for these inputs. Consequently the result is exact, not a probabilistic modular test.

An independently coded floating-point Gaussian elimination on the same full enumeration gave identical counts and support histograms; this is an implementation cross-check, not a second formal proof.

For arbitrary d>=s, the number of six-point circuits whose support has size exactly s equals binom(d,s) 2^(d-s) A_s, where A_s counts full-support six-point circuits in V_s: choose the changing coordinates, assign the fixed coordinates, and translate the remaining configuration. The enumerated values are A_4=1088 and A_5=30880. This identity is a mathematical bijection, while the A_s values are finite enumeration.

## Limitations

This does not enumerate six-point circuits in d=6, nor prove the K_6<=9 bound. For d=6, an exhaustive direct six-subset scan would be much larger; the support identity gives a partial check: six-point circuits of support 4 contribute binom(6,4)*2^2*1088=65,280, and support 5 contribute binom(6,5)*2*30880=370,560. The full-support-six component remains unknown in this audit.
