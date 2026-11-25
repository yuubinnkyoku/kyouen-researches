"""Dual-layout resolver for the parked-2-keys L50M ladder scripts (third-cost
class 1297036830122704896:0 continuation lane).

Layout A (kit): scripts sit in <kit>/lane/, pinned inputs in <kit>/inv/
(byte-identical copies, sha-pinned by the audit), experiment files under
<kit>/lane/exp/.

Layout B (published repo): scripts sit in
research/experiments/n11-class1297036830122704896-parked2-s5-l50m-ladder-20261121/scripts/
and every pinned input is read from its published repo location, including the
parent probe's audit JSON and the chain cache increment published by the
parent lane.
"""
from pathlib import Path

GEOM_REL = "research/experiments/n11-strategy-redesign-20261010/output/geometry.json.gz"
GEOM_SHA = "146be80b5794462c2444e983fc4c4a6e76d3b464bfd5e86fac14509024100b54"
# chain base = the parent probe's byte-preserving increment (5,793 rows)
BASE_REL = ("research/experiments/n11-class1297036830122704896-exclusive-s5-jsreplica-probe-20261121/"
            "output/merged-exact-s5-after-class-excl-1.cache")
BASE_SHA = "bb4495e0586404876db05856c5b8573c62361dadd826b6f68f6f8cae611190b0"
# parent probe audit (the machine record that parked these two keys at 15M)
PARENT_AUDIT_REL = ("research/experiments/n11-class1297036830122704896-exclusive-s5-jsreplica-probe-20261121/"
                    "output/probe-audit.json")
PARENT_AUDIT_SHA = "950a716b68530e62cdf5fdd094be5b399c2f983d5b16b4cdec9352dca9b93fd2"
REPLY27 = "research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-40960-20261121"
SUPPLY_REL = REPLY27 + "/output/post-probe/shared-s5-tasks.csv"
QUAR_REL = "results/n11-s5-evidence-quarantine.json"
JSRELAY_REL = REPLY27 + "/scripts/jsreplay.js"
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
                     cache=kit / "inv" / "merged-exact-s5-chain-after-class-excl-1.cache",
                     parent_audit=kit / "inv" / "parent-probe-audit.json",
                     supply=kit / "inv" / "shared-s5-tasks.csv",
                     quar=kit / "inv" / "n11-s5-evidence-quarantine.json",
                     jsrelay=kit / "inv" / "jsreplay.js",
                     indep=kit / "inv" / "independent.py",
                     policy=kit / "inv" / "s5_evidence_policy.py")
    else:
        repo = here.parents[3]
        exp = here.parent
        paths.update(geometry=repo / GEOM_REL, cache=repo / BASE_REL,
                     parent_audit=repo / PARENT_AUDIT_REL,
                     supply=repo / SUPPLY_REL, quar=repo / QUAR_REL,
                     jsrelay=repo / JSRELAY_REL, indep=repo / INDEP_REL,
                     policy=repo / POLICY_REL)
    paths["exp"] = exp
    return paths
