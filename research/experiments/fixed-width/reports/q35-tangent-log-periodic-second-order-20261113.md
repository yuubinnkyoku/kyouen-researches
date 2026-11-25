# 3×m, q=5: tangent-circle count has a nonconstant logarithmically periodic second-order term

Date: 2026-11-13. Status: mathematical consequence of the previously proved complete tangent-family classification; **not** a statement about the total count of all five-point circles.

Let \(a_0=8,a_1=48,a_{j+2}=6a_{j+1}-a_j\), and use the established exact identity
\[
T_5(m)=2\sum_{j\ge0}(m-a_j)_+,\qquad m\in\mathbb Z_{\ge1}.
\]
Put
\[
\lambda=3+2\sqrt2,\quad C=4+3\sqrt2,\quad D=4-3\sqrt2.
\]
Then \(a_j=C\lambda^j+D\lambda^{-j}\) exactly, with \(-1<D<0\). Define \(x=\log_\lambda(m/C)\) and \(\theta=\{x\}\).

**Theorem (uniform bounded-error refinement).** For integer \(m\to\infty\),
\[
T_5(m)=\frac{2m\log(m/C)}{\log\lambda}
+m H(\{\log_\lambda(m/C)\})+O(1),
\]
where the continuous 1-periodic function (endpoints identified) is
\[
H(t)=2(1-t)-\frac{2\lambda^{1-t}}{\lambda-1},\qquad 0\le t<1.
\]
In particular the normalized remainder
\[
\frac{T_5(m)-(2/\log\lambda)m\log(m/C)}m
\]
does **not** converge; its set of subsequential limits is exactly the nondegenerate interval \(H([0,1])\).

**Proof.** Let \(N=\#\{j\ge0:a_j<m\}\). For all sufficiently large integer \(m\), \(N=\lfloor x\rfloor+1\). Indeed, \(a_j=C\lambda^j+D\lambda^{-j}\) differs from \(C\lambda^j\) by strictly less than 1, and the former is an integer; therefore no integer \(m\) lies strictly between these two numbers. Consequently \(a_j<m\iff C\lambda^j<m\) except possibly equality \(m=a_j\), where the corresponding summand vanishes, so the formula for \(T_5\) is unchanged if the zero term is included. At such an equality, \(x<j\), giving \(N=j\), consistently. (For the finite initial range \(x<0\), truncate \(N\) at zero.)

Sum both geometric progressions:
\[
T_5(m)=2Nm-2C\frac{\lambda^N-1}{\lambda-1}
-2D\frac{1-\lambda^{-N}}{1-\lambda^{-1}}.
\]
Since \(N=x+1-\theta\) and \(C\lambda^N=m\lambda^{1-\theta}\), this is the asserted formula with an explicitly bounded residual
\[
\frac{2C}{\lambda-1}-\frac{2D(1-\lambda^{-N})}{1-\lambda^{-1}}.
\]
The endpoint values of \(H\) agree. It is not constant, since \(H''(t)=-2(\log\lambda)^2\lambda^{1-t}/(\lambda-1)<0\). For any \(t\in[0,1]\), choosing integer \(m_k\) nearest \(C\lambda^{k+t}\) gives \(\{\log_\lambda(m_k/C)\}\to t\) on the circle, hence all values of \(H\) occur as subsequential limits. Compactness gives no other limits. QED.

**Independent arithmetic check to run:** generate \(a_j\) using only the integer recurrence, compute \(T_5(m)\) by direct summation, and compare the bounded residual above for a broad integer range. This proof itself is symbolic and does not rely on that check.

**Scope / open problem.** This concerns only tangent-type circles. The total five-point-circle count \(F_5(m)\), including non-tangent families, is not covered. The periodic correction shows that replacing the \(O(m)\) error by a constant multiple of \(m\) is impossible for \(T_5\).
