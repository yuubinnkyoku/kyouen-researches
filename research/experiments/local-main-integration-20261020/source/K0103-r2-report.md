# K0103 r2 bounded attempt report

## Result

No 10×10 empty-board KYOENC4 certificate was generated in this bounded
attempt. Therefore no Rust certificate verification was performed. K0103
remains open.

## Objective

Advance K0103 by producing a single empty-board 10×10 KYOENC4 proof DAG and
verifying it with the independent Rust checker.

## Method

- Solver/certifier used: `cpp/solvers/kyouen_solver_10_kyoenc4.cpp` (KYOENC4
  certificate mode), compiled in WSL with `g++ -std=c++20 -O2`.
- Invocation form:
  `kyouen_solver_10_kyoenc4 --certificate "" OUTPUT.cert [shrink] [load]
  [max_nodes] ...`
- Empty initial state was represented by an empty point-id list.
- Intended output path: `scratchpad/K0103-empty-10x10.cert`.
- Run log: `scratchpad/K0103-run.log`.

## Attempts

1. Parameters: `shrink=3`, `load=80`, `max_nodes=10000000`.
   - Progress: 50,331,648 visited nodes at 216.687 seconds.
   - Termination: `memo table full` (`TableFull` exception).
   - Output certificate: not written.

2. Parameters: `shrink=1`, `load=90`, `max_nodes=10000000`.
   - Progress: 184,549,376 visited nodes at 581.006 seconds.
   - Termination: 10-minute wall-clock bound reached; process stopped.
   - Output certificate: not written (`scratchpad/K0103-empty-10x10.cert` absent).

## Observations

- The solver did not complete the empty-board solve in either attempt, so no
  root outcome was recomputed by this attempt.
- Observed throughput in attempt 2 was approximately
  184,549,376 / 581.006 ≈ 317,000 visited nodes/second.
- No 10×10 empty-board KYOENC4 certificate exists in the repository by scan
  prior to this attempt; none was produced here.
- The certificate writer is only reached after `solve()` returns; since
  `solve()` did not return, no partial certificate file was emitted.

## Rust verification status

Not run, because no certificate file exists.

Toolchain readiness (verified separately, not as certificate verification):

- `cargo test` in `rust/independent-verifier`: 9 tests passed.
- `kyouen-cert-verify` binary built successfully in release mode.
- If a certificate is produced later, verify with:
  `rust/independent-verifier/target/release/kyouen-cert-verify <certificate.cert>`

## Conclusion

This bounded attempt did not generate a single empty-board 10×10 KYOENC4 DAG.
K0103 remains open. The solver throughput observed here is far below what
would be needed to complete the full empty-board search within ~10 minutes.