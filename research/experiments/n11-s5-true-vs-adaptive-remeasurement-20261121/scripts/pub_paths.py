"""Shared dual-layout resolver for the true-vs-adaptive cost re-measurement.

Layout A (authoring/sandbox kit): scripts sit in <kit>/lane/, pinned inputs in
<kit>/inv/ (byte-identical copies of published repo files, sha-pinned by each
script), outputs under <kit>/lane/exp/output/.

Layout B (published repo): scripts sit in
research/experiments/n11-s5-true-vs-adaptive-remeasurement-20261121/scripts/
and every pinned input is read from its published repo location.
"""
from pathlib import Path

GEOM_REL = "research/experiments/n11-strategy-redesign-20261010/output/geometry.json.gz"
GEOM_SHA = "146be80b5794462c2444e983fc4c4a6e76d3b464bfd5e86fac14509024100b54"
PROFILE_REL = "research/experiments/n11-strategy-redesign-20261010/output/historical-cost-profile.json"
PROFILE_SHA = "6b2971e53059ac36af7bf161a61d90d65f85e604e27b93d013e7a2853fdceddc"
RSRC_REL = ("research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-40960-20261121")
SUPPLY_REL = (RSRC_REL + "/output/post-probe/shared-s5-tasks.csv")
SUPPLY_SHA = "31f0d29b820a69508af0c352c22f09b244bff5b9ae79476679047cdb160ea954"
LEDGER_REL = (RSRC_REL + "/output/post-probe/candidate-classes.csv")
LEDGER_SHA = "2a4c2382d812102f8132339c871b07ee998e933c80da876759e51e84f64fda80"
PROBE13_REL = (RSRC_REL + "/output/merged-exact-s5-after-js-probe-13.cache")
PROBE13_SHA = "60e0dc3476920d4e99043dd4f132398ea72e4dfdcd9f3dbb8fc686ba65bc28c6"
PREV_EXP_REL = "research/experiments/n11-class1297036830122704896-exclusive-s5-jsreplica-probe-20261121"
CHAIN_REL = PREV_EXP_REL + "/output/merged-exact-s5-after-class-excl-1.cache"
CHAIN_SHA = "bb4495e0586404876db05856c5b8573c62361dadd826b6f68f6f8cae611190b0"
SELECT_REL = PREV_EXP_REL + "/output/exclusive-selection.json"
SELECT_SHA = "ef048309b3bd3ae3134c583374712e0c6aff64175006879063995c0eaeafafb7"
RECFIND_REL = ("research/experiments/n11-s5-frontier-census-20261121/output/reconciliation-findings.json")
RECFIND_SHA = "a93d87dc436f28ffea63760c766178a55af259f545884a8557300f7eb7e2e9cb"
FOURTH_EXP_REL = ("research/experiments/n11-fourthcost-class-s5-exclusive-probe-1297107061427929088-20261121")
FOURTHKEYS_REL = FOURTH_EXP_REL + "/output/fourth-cost-exclusive-keys.json"
FOURTHKEYS_SHA = "b9f4d9419e0f9edf5b97c6867568a30b3ac149811edeb4c98ef5ec0fcd9bbb6a"
FOURTHNOTE_REL = "research/log/2026-11-21-n11-fourthcost-exclusive-probe-pass1-complete.md"
FOURTHNOTE_SHA = "96ad1dfebbe4ef0b7105f8236abe340bc357e37367ea6b5f13a2aa410e20cd0e"
INDEP_REL = "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
INDEP_SHA = "954d3a104c1723ebb15b8c9bae63a4494f07f9eb73446a6d067c4fd6a4ba189f"
POLICY_REL = "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"
POLICY_SHA = "78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2"


def resolve(script_file):
    here = Path(script_file).resolve().parent
    kit = here.parent
    if (kit / "lane").resolve() == here and (kit / "inv" / "geometry.json.gz").exists():
        inv = kit / "inv"
        paths = dict(
            geometry=inv / "geometry.json.gz",
            profile=inv / "historical-cost-profile.json",
            supply=inv / "shared-s5-tasks.csv",
            ledger=inv / "candidate-classes.csv",
            probe13=inv / "probe13-cache-60e0dc34.cache",
            chain=inv / "chain-cache-bb4495e0.cache",
            sel=inv / "thirdcost-selection.json",
            recfind=inv / "reconciliation-findings.json",
            fourthkeys=inv / "fourth-cost-exclusive-keys.json",
            fourthnote=inv / "fourthcost-pass1-complete.md",
            indep=inv / "independent.py",
            policy=inv / "s5_evidence_policy.py",
            repo_root=None)
    else:
        repo_root = None
        for cand in [here, *here.parents]:
            if cand.name == "research":
                repo_root = cand.parent
                break
        if repo_root is None:
            raise SystemExit("published layout expected: research/ not found above " + str(here))
        paths = dict(
            geometry=repo_root / GEOM_REL,
            profile=repo_root / PROFILE_REL,
            supply=repo_root / SUPPLY_REL,
            ledger=repo_root / LEDGER_REL,
            probe13=repo_root / PROBE13_REL,
            chain=repo_root / CHAIN_REL,
            sel=repo_root / SELECT_REL,
            recfind=repo_root / RECFIND_REL,
            fourthkeys=repo_root / FOURTHKEYS_REL,
            fourthnote=repo_root / FOURTHNOTE_REL,
            indep=repo_root / INDEP_REL,
            policy=repo_root / POLICY_REL,
            repo_root=repo_root)
    exp = kit / "lane" / "exp" if (kit / "lane").resolve() == here else \
        paths["repo_root"] / "research/experiments/n11-s5-true-vs-adaptive-remeasurement-20261121"
    paths["exp"] = exp
    paths["out"] = exp / "output"
    return paths
