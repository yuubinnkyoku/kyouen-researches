# n11 central-reply: class-8785 z003 if-adopted base control (Part Y refresh cross-host reproduction, 2026-11-22)

Read-only planning/audit control experiment (no solver search, no new
verdicts). It re-runs the published Part Y refresh scenario script
(`refresh_19root_frontier.py`, sha256
`8867152695245aa23f3cd6849b3050e5bfec9365276d3da7998a0d607469a31c`,
byte-equal to `../n11-central-reply-8784-closure-reaudit-20261122/scripts/`)
on this host, against the pinned inputs fetched byte-exact from the repo
canonical copies (commit `0a369d6c` pinned raw):

* dependency-graph `54f9c3643eeba139ea5e8d3babb1db9744d19f00f3cf024bbf192ec0d408c00b`
* merged chain cache (6,027 rows)
  `95e868d6762925b9a27ad963a825a9ad4fd5131a864eb82fac0db77d7acdb326`
* update8 plan `b658290aa941c105035aa3b9b13741cd95b5032b9b7fb7d61b2aed0d0cea6719`
* Board source `954d3a104c1723ebb15b8c9bae63a4494f07f9eb73446a6d067c4fd6a4ba189f`
* evidence policy `78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2`
* quarantine registry `81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9`

Results (machine-verified on this host):

* the script was executed **twice**; all four outputs are byte-identical
  between the runs (determinism 2/2);
* `output/closure-classes.csv` (`61943b85...`), `output/per-root-coverage.csv`
  (`33f01a0c...`) and `output/refresh-summary.json` (`25987add...`) are
  **byte-equal to the published Part Y canonical re-audit outputs**
  (cross-host byte-exact reproduction);
* `output/probe-worklist.csv` (65,154 rows, sha256
  `1807e4d21f6fb757ea21850c6bda4d822cb76ac59abfa9bcd1cc7b53bd7055ef`,
  matching the Part Y/Z record) is regenerable from the pinned inputs and is
  not republished here.

This base control anchors the batch-11 z003 IF-ADOPTED scenario experiment
(`../n11-centralreply-class8785-win-z003-ifadopted-20261122/`): every scenario
delta there is measured against these BASE outputs. No verdict is consumed
anywhere; the standard 11x11 empty board, the 19 central-reply roots and
every class remain UNKNOWN. Node counts are not verdicts.
