# 5x25 q=7 row-deficient maximal nonexistence — class-split sweep

Date: 2026-11-15 (UTC). Fast lane, successor of K0836 (5x24 witness-free).

## Status

IN FLIGHT — claim by the fast lane. CNFs generated (56), sweep running.
Witness frontier of (5,7): widths 19..24 are verified witness-free
(K0738-K0759, K0816, K0821, K0834, K0835, K0836); this lane decides 5x25.
A witness here gives M_{5,7} >= 26; witness-free here extends the free set to
{19,...,25} (sharp form M = 19 or >= 27). Upper 158 (K0332 substitution) unchanged.

Protocol identical to the K0834/K0835/K0836 lanes: 17 direct classes + {0},{1}
complete k x minpos decomposition (k=0..4 and k=5 x minpos=0..12 — the sound
bound grows to floor((m-1)/2) = 12 at m=25) + lex=H cross-checks on {0,1},{2} +
5x18 positive control. kissat 4.0.4 official binary.
