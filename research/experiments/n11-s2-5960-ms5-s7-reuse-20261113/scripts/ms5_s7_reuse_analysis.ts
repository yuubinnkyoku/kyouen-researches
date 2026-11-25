/**
 * ms5_s7_reuse_analysis.ts — n11 S2 {59,60} milestone-5
 * Independent re-derivation of the S6 worklist (keys, classes, cost) and the
 * S7 certificate-reuse candidate partition. Deterministic; no network needed.
 *
 * Oracle inputs (K0675-conditioned): 78 FW + 16 SW base positions (5 stones),
 * 14 LOSS sweep keys. Certificates: focus2154_62certs/verified.json
 * (27 WIN7 + 35 LOSS7). Board 11x11, cells 0..120 row-major.
 * Run with any modern TS/JS runtime (node >= 16 after stripping types).
 */
// See git history: the full body is the program executed for the 2026-11-13
// run; it is reproduced verbatim in research/log/2026-11-13-n11-ms5-worklist-derivation-and-s7-reuse-partition.md.
