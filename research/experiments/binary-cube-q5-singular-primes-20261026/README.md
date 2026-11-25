# q=5 binary-cube sections: singular primes 127 and 139 (2026-10-26)

Let \(E_{d,5}\) be the number of distinct five-vertex hyperplane sections of the binary \(d\)-cube (K0561), for \(d\ge5\). Extend the **exponential formula** to \(F(0)=\cdots=F(4)=0\), without assigning a geometric interpretation below dimension 5:

\[
120F(d)=\sum_{a\in\{2,4,6,8,10,12,14,16,18,20,24,32\}}c_a a^d,
\]
where the exact coefficients are in [verify.py](verify.py). For \(d\ge5\), \(F(d)=E_{d,5}\).

## New theorem: two singular zero branches

For \(p=127\) or \(139\), put \(P=p-1\), \(d=Pk+j\), \(0\le j<P\). The zero residues of \(F(d)\bmod p\) are respectively

- \(p=127\): \(J=\{0,1,2,3,4\}\);
- \(p=139\): \(J=\{0,1,2,3,4,27\}\).

All zero residues except one have nonzero slope \(D_j=(F(j+P)-F(j))/p\bmod p\). The singular residues are \(j=1\) for 127 and \(j=2\) for 139. Each **simple** zero residue lifts uniquely to a \(k\bmod p^{t-1}\) for every \(t\ge1\). For the simple residues among \(j=0,\ldots,4\), this residue is always \(k=0\); for \(p=139,j=27\), the explicit digit recurrence in [verify.py](verify.py) determines it.

The singular residue behaves differently:

1. For \(t=1\), every \(k\) gives \(p\mid F(Pk+j)\).
2. For \(t=2\), **every** \(k\) gives \(p^2\mid F(Pk+j)\).
3. For every \(t\ge3\), **exactly two** residues \(k\bmod p^{t-2}\) give \(p^t\mid F(Pk+j)\), and each lifts uniquely forever. At \(t=3\) they are \(k=0,7\pmod{127}\) and \(k=0,36\pmod{139}\).

One branch is exactly \(k=0\) at every level, reflecting \(F(j)=0\) in the formal extension. The actual dimensions in this progression start at \(d=j+Pp^{t-2}\), not \(d=j<5\).

**The least period** of \(E_{d,5}\bmod p^t\) on \(d\ge5\) is exactly \((p-1)p^{t-1}\) for every \(t\ge1\). The zero-residue counts per full period are:

| p | t=1 | t=2 | t>=3 |
|---|---:|---:|---:|
| 127 | 5 | 131 | 258 |
| 139 | 6 | 144 | 283 |

For \(t\ge3\), the two singular branches each contribute \(p\) residue classes modulo the full period; each simple branch contributes one.

## Proof for all dimensions

Because \(p>32\), all bases \(a\) and 120 are \(p\)-adic units. Let \(u_a=(a^P-1)/p\). Then

\[
F(j+Pk)=\frac1{120}\sum_a c_a a^j(1+pu_a)^k.
\]

Fermat's theorem makes \(F(j)\bmod p\) depend only on \(j\bmod P\). At a simple zero, the first-order coefficient \(D_j\bmod p\) is nonzero. The binomial expansion gives, for all \(s\ge0\),

\[
F(j+P(k+p^s h))-F(j+Pk)
\equiv p^{s+1}hD_j\pmod{p^{s+2}}.
\]

Thus a simple zero has precisely one lift per digit.

At the singular residue \(j\), \(F(j)=0\) **exactly** and \(D_j=0\bmod p\), so \(F(j+Pk)\) is divisible by \(p^2\) for every integer \(k\). Define \(H(k)=F(j+Pk)/p^2\). The first two binomial coefficients give

\[
\begin{aligned}
p=127,\ j=1:\quad&H(k)\equiv112k(k-7)\pmod{127},\\
p=139,\ j=2:\quad&H(k)\equiv104k(k-36)\pmod{139}.
\end{aligned}
\]

Every higher term (\(h\ge3\)) has a factor \(p^{h-2}\binom{k}{h}\); since \(p\ge127\), its polynomial coefficients are \(p\)-integral and divisible by \(p\), and the series converges \(p\)-adically. Therefore \(H\) is a restricted \(p\)-adic analytic function reducing to these quadratics. Both roots of each quadratic are distinct and simple. Hensel's lemma gives exactly two and only two \(p\)-adic zero branches. The digit update for a root \(k\bmod p^s\) is

\[
k'=k-p^s\left(H(k)/p^s\right)H'(k)^{-1}\pmod{p^{s+1}},
\]

with \(H'\bmod p\) equal to the derivative of the displayed quadratic. The verifier performs the same update using modular exponentiation and exact integer divisions.

The finite sets \(J\) have no nontrivial translational symmetry in \(\mathbb Z/P\mathbb Z\), so \(P\) is the least period modulo \(p\). For \(t\ge2\), the simple zero \(j=0\) has nonzero slope, and a translation by \(Pp^{t-2}\) changes its value by a nonzero multiple of \(p^{t-1}\) modulo \(p^t\). Euler's period \(Pp^{t-1}\) is therefore minimal. This works on the tail \(d\ge5\).

## Exact coefficients and independent arithmetic checks

The simple slopes \(D_j\) are:

- 127: \(\{0:103,2:95,3:41,4:29\}\), singular \(j=1\).
- 139: \(\{0:130,1:48,3:17,4:114,27:11\}\), singular \(j=2\).

The two singular residues \(k\bmod p^{t-2}\) for \(t=3,4,5,6\) are:

- 127: \((0,7),(0,3944),(0,745878),(0,215826093)\).
- 139: \((0,36),(0,11017),(0,2174969),(0,268051250)\).

Run `python verify.py`. It compares the exponential formula with a second-kind Stirling recurrence for all \(d\le2(p-1)+4\) modulo \(p^3\); checks all \(j,k\) modulo \(P,p\) at precision \(p^2\); checks the singular quadratics and every \(k\bmod p\) at precision \(p^3\); and verifies every root lift through \(t=13\). These are two independent **arithmetic algorithms relying on the same K0561 coefficients**, not independent geometric enumeration.

## Exact maxima on 5<=d<=10^18

The unbounded zero-branch theorem and finite exact modular lifting give:

| p | maximum \(v_p(E_{d,5})\) | maximizing dimensions |
|---|---:|---|
| 127 | **9** (28 dimensions) | \(d=67142358380853379+67142358380853378h\), \(0\le h<14\), or \(d=60679142437356451+67142358380853378h\), \(0\le h<14\) |
| 139 | **9** (15 dimensions) | \(d=138351122843254304+138351122843254302h\), \(0\le h<7\), or \(d=1735183532561258+138351122843254302h\), \(0\le h<8\) |

At \(t=10\) no zero progression meets the range. No scan of \(10^{18}\) dimensions was performed. This concerns binary-cube hyperplane sections, **not** the planar circle game or the 11×11 root search.
