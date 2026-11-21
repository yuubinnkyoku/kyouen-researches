"""Shared dual-layout resolver for the published lane scripts.

Layout A (authoring/sandbox kit): scripts sit in <kit>/lane/, pinned inputs in
<kit>/inv/ (byte-identical copies, sha-pinned by each script), experiment
files under <kit>/lane/exp/.

Layout B (published repo): scripts sit in
research/experiments/n11-class1297036830122704896-exclusive-s5-jsreplica-probe-20261121/scripts/
and every pinned input is read from its published repo location.
"""
from pathlib import Path

GEOM_REL = "research/experiments/n11-strategy-redesign-20261010/output/geometry.json.gz"
GEOM_SHA = "146be80b5794462c2444e983fc4c4a6e76d3b464bfd5e86fac14509024100b54"
CACHE_REL = ("research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-40960-20261121/"
             "output/merged-exact-s5-after-js-probe-13.cache")
CACHE_SHA = "60e0dc3476920d4e99043dd4f132398ea72e4dfdcd9f3dbb8fc686ba65bc28c6"
SUPPLY_REL = (CACHE_REL.rsplit("/", 1)[0] + "/post-probe/shared-s5-tasks.csv")
LEDGER_REL = (CACHE_REL.rsplit("/", 1)[0] + "/post-probe/candidate-classes.csv")
PROFILE_REL = "research/experiments/n11-strategy-redesign-20261010/output/historical-cost-profile.json"
QUAR_REL = "results/n11-s5-evidence-quarantine.json"
JSRELAY_REL = ("research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-40960-20261121/"
               "scripts/jsreplay.js")
INDEP_REL = "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
POLICY_REL = "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"


def resolve(script_file):
    here = Path(script_file).resolve().parent
    kit = here.parent
    exp = None
    paths = {}
    if (kit / "lane").resolve() == here and (kit / "inv" / "geometry.json.gz").exists():
        exp = kit / "lane" / "exp"
        paths.update(geometry=kit / "inv" / "geometry.json.gz",
                     cache=kit / "inv" / "merged-exact-s5-after-js-probe-13.cache",
                     supply=kit / "inv" / "shared-s5-tasks.csv",
                     ledger=kit / "inv" / "candidate-classes.csv",
                     profile=kit / "inv" / "historical-cost-profile.json",
                     quar=kit / "inv" / "n11-s5-evidence-quarantine.json",
                     jsrelay=kit / "inv" / "jsreplay.js",
                     indep=kit / "inv" / "independent.py",
                     policy=kit / "inv" / "s5_evidence_policy.py")
    else:
        # published layout: <repo>/research/experiments/<exp>/scripts/x.py
        # here.parents: [0]=exp dir, [1]=experiments, [2]=research, [3]=repo
        repo = here.parents[3]
        exp = here.parent
        paths.update(geometry=repo / GEOM_REL, cache=repo / CACHE_REL,
                     supply=repo / SUPPLY_REL, ledger=repo / LEDGER_REL,
                     profile=repo / PROFILE_REL, quar=repo / QUAR_REL,
                     jsrelay=repo / JSRELAY_REL, indep=repo / INDEP_REL,
                     policy=repo / POLICY_REL)
    paths["exp"] = exp
    return paths
