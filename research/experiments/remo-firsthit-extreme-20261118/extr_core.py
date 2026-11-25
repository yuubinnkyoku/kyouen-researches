#!/usr/bin/env python3
"""K0959 core: extreme-value decomposition of the first-hit time
F(M) (worst first hit over live kappa classes), prime M <= 2000.

Observation toolkit only (no universal claims): OLS power fits,
surrogate recovery of the "flattening" artifact, log-law residuals,
bucket medians, BH worst-class identification, extreme-value
amplification vs an iid-exponential baseline.

Setting (K0950/K0956 notation): F(M) = (M+1) t* + kappa* is the
largest first-hit K over the live classes of M; F_t = t*,
F_kappa = kappa*, F_C = gcd(M+1, kappa*+2), F_type = branch/smooth
per K0956's FIRSTHIT table (F_by_M, 303 rows).
"""
from __future__ import annotations

import math


def power_fit(xs, ys):
    """OLS fit ys ~ a * xs^beta; returns (a, beta, r2) in log space."""
    n = len(xs)
    lx = [math.log(x) for x in xs]
    ly = [math.log(y) for y in ys]
    mx = sum(lx) / n
    my = sum(ly) / n
    sxx = sum((u - mx) ** 2 for u in lx)
    sxy = sum((u - mx) * (v - my) for u, v in zip(lx, ly))
    beta = sxy / sxx
    a = math.exp(my - beta * mx)
    ss_res = sum((v - (math.log(a) + beta * u)) ** 2
                 for u, v in zip(lx, ly))
    ss_tot = sum((v - my) ** 2 for v in ly)
    return a, beta, 1.0 - ss_res / ss_tot


def through_origin_fit(xs, ys, law):
    """alpha minimizing sum (ys - alpha*law(xs))^2 + R^2."""
    L = [law(x) for x in xs]
    num = sum(y * l for y, l in zip(ys, L))
    den = sum(l * l for l in L)
    alpha = num / den
    my = sum(ys) / len(ys)
    ss_res = sum((y - alpha * l) ** 2 for y, l in zip(ys, L))
    ss_tot = sum((y - my) ** 2 for y in ys)
    return alpha, 1.0 - ss_res / ss_tot


def median(v):
    s = sorted(v)
    n = len(s)
    return s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])


def spearman(a, b):
    ra = _ranks(a)
    rb = _ranks(b)
    return _pearson(ra, rb)


def _ranks(v):
    order = sorted(range(len(v)), key=lambda i: v[i])
    r = [0.0] * len(v)
    i = 0
    while i < len(v):
        j = i
        while j + 1 < len(v) and v[order[j + 1]] == v[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            r[order[k]] = avg
        i = j + 1
    return r


def _pearson(a, b):
    n = len(a)
    ma = sum(a) / n
    mb = sum(b) / n
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    da = math.sqrt(sum((x - ma) ** 2 for x in a))
    db = math.sqrt(sum((y - mb) ** 2 for y in b))
    return num / (da * db)
