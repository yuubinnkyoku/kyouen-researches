# wsearch34 status (2026-11-21 session)

- Fixed wsearch34.js (subPid cell-mixing bug + per-b PAIR22/P11 tables) validated at
  m=8 against brute_3x8_4.json family row-profile counts (Y0 3290, Y1 3020) and
  slowref34.js; matches exactly.
- Family sweep m=12..25: witnesses in-family through m=23 (matches parallel-run kissat
  band m=4..23 SAT published at HEAD 91f2f0f1), FAMILY EXTINCTION at m=24 and m=25
  (complete enumeration of (3,a,3) family, both Y, full sweep, no witnesses).
- m=23 family witnesses (total 6 configs) recorded in family-counts.jsonl; each
  verified SAFE+MAXIMAL by two systems: sat.js verifyConfig and witness_check.py
  (independent exact-integer determinant geometry).
- Next: non-family def profiles at m=24: crossing-count lemma (non-horizontal line
  meets each row once => deficient-row empty cells can only be circle-blocked) kills
  all k<=5 profiles at m=24; remaining: (3,2,2), (3,2,1), (2,2,2) (+row perms).
  Tool x enumerating these could decide 3x24 def-mode completely (lane-first UNSAT
  verdict would move M_{3,4} lower edge 24 -> 25).

# dx34 extension session 2 (2026-11-21, later)

- Built dx34.js (direct + fast circle-class enumeration of ALL def profiles).
  Validation chain: direct == brute_3x{4..8}_4.json per-profile EXACT (def totals
  182/674/1724/4607/11542); fast == direct m=4..8 all supported profiles;
  direct == fast at m=12 (13 profiles); fast witnesses at m=11/12 pass 2-system
  verification (verifyConfig + witness_check.py).
- Crossing-count lemma kills all k<=5 profiles for m>=24 (supply bound).
- Sweeps: non-family profiles ALL ZERO at m=24, 25, 26 (each profile complete
  enumeration; (3,2,2) 3 placements, (3,2,1)-type 6, (3,1,1)+perms, (2,2,2)).
- Family extinct at 24 (prior), 25 (prior), 26 (this session, wsearch34).
- THEOREM (machine-checked): deficient-mode UNSAT for 3 x m, q=4, m in {24,25,26}.
  With the published m=4..23 witness band, M_{3,4} in [27,69] (previous frontier [24,69]).
- Non-family extinction onsets: (3,2,2)@edge alive only to m=12 (38@m=11, 4@m=12),
  all other non-family shapes dead by m=12; => for m>=13 def-mode space is exactly
  the (3,a,3)-family. Future widths only need family machinery (wsearch34) +
  the lemma for k<=5 (supply bound scales with m, check per m).
- Next executable: m=27 family (Y=0,1; ~110s each), then non-family chunk; m=28 family;
  m=29 family (capped ~170s/Y, near timeout: run one Y per call); m=30 needs A-chunked
  family search or kissat (defer to parallel run who has kissat).
