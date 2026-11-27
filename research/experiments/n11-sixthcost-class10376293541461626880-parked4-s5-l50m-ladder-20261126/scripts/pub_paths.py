"""Path/sha resolver for the parked-4-keys L50M ladder scripts (sixth-cost
class 10376293541461626880:65536 continuation lane).

Layout (published repo): scripts sit in
research/experiments/n11-sixthcost-class10376293541461626880-parked4-s5-l50m-ladder-20261126/scripts/
and every pinned input is read from its published repo location: the frozen
geometry, the canonical chain head of record (the Part EM head 6e49dd84), the
parent sixth-cost probe batch's machine selection JSON and published parked
raw rows, the reply27 probe-13 supply ledger, the S5 quarantine registry, and
the pinned independent-geometry python + canonical-safe policy files.
"""
from pathlib import Path

REPO_MARKERS = ("research", "results")

GEOM_REL = "research/experiments/n11-strategy-redesign-20261010/output/geometry.json.gz"
GEOM_SHA = "146be80b5794462c2444e983fc4c4a6e76d3b464bfd5e86fac14509024100b54"
# chain head of record at lane time: Part EM emloss21 loss-only adoption head (6,792 rows)
BASE_REL = ("research/experiments/n11-centralreply-emloss21-adoption-predecl-20261126/"
            "output/merged-exact-s5-chain-plus-emloss21-20261126.cache")
BASE_SHA = "6e49dd841b7bfcb335d86ef2479c95f47ab7acbcf41ace389a8b8eb95c778c9d"
# parent sixth-cost probe batch: machine selection + published parked raw rows
PARENT_EXP = ("research/experiments/n11-sixthcost-class-s5-exclusive-probe-"
              "10376293541461626880-20261121")
SEL_REL = PARENT_EXP + "/output/sixth-cost-exclusive-keys.json"
SEL_SHA = "d5e9b059611849f7b7e69c7370a0e66cd7535c43b3a043ce9f5bfc0e5ff72e87"
PARENT_RAW_REL = PARENT_EXP + "/output/raw"
REPLY27 = "research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-40960-20261121"
SUPPLY_REL = REPLY27 + "/output/post-probe/shared-s5-tasks.csv"
SUPPLY_SHA = "31f0d29b820a69508af0c352c22f09b244bff5b9ae79476679047cdb160ea954"
QUAR_REL = "results/n11-s5-evidence-quarantine.json"
QUAR_SHA = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"
JSRELAY_REL = None  # the lane's own byte-clone scripts/jsreplay.js
JS_SHA = "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df"
INDEP_REL = "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
INDEP_SHA = "954d3a104c1723ebb15b8c9bae63a4494f07f9eb73446a6d067c4fd6a4ba189f"
POLICY_REL = "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"
POLICY_SHA = "78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2"


def resolve(script_file):
    here = Path(script_file).resolve().parent          # .../scripts
    exp = here.parent                                  # .../<exp dir>
    repo = here.parents[3]                             # repo root
    paths = {
        "exp": exp,
        "geometry": repo / GEOM_REL,
        "cache": repo / BASE_REL,
        "parent_raw": repo / PARENT_RAW_REL,
        "selection": repo / SEL_REL,
        "supply": repo / SUPPLY_REL,
        "quar": repo / QUAR_REL,
        "jsrelay": here / "jsreplay.js",
        "indep": repo / INDEP_REL,
        "policy": repo / POLICY_REL,
    }
    return paths
