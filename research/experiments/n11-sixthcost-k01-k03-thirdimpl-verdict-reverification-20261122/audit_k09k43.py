#!/usr/bin/env python3
"""Fail-closed audit of the k09..k43 resolved-rows third-implementation batch of
research/experiments/n11-sixthcost-k01-k03-thirdimpl-verdict-reverification-20261122/
(declaration research/log/2026-11-26-n11-sixthcost-k09-k43-resolved32-thirdimpl-batch-single-owner-note.md,
push 4d1b7db7 at HEAD 4e87e67b). Scope: the THIRTY fifth-resumption resolved-LOSS
rows k09..k43 (parked k20/k33/k38 excluded, no new verdict for them) plus the TWO
parked4-L50M-ladder WIN rows k13/k19 whose consumption gate requires third-impl
scrutiny. Every replica raw is re-verified by sha256 pin and row fields, every
third-impl cold run is re-derived from out/, every C4 fail-closed input gate is
re-checked against its pinned mismatch string. Deterministic; byte-identical output
across runs in a fixed layout (resolved-path detail strings only being
layout-dependent, as in the k06/k07/k08 auditor); exits 1 on any gate failure.
This audit consumes no verdict; the delegated pinned C++ second-implementation
gate stays with the scrutiny owner.
"""
import hashlib, json, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "out"
KIT = ROOT.parent  # local kit layout: rows.tsv sibling of the experiment-dir copy
PROBE = ROOT.parent / "n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121"
PARKED = ROOT.parent / "n11-sixthcost-class10376293541461626880-parked4-s5-l50m-ladder-20261126"

def sha256(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()

gates = {}
def gate(name, ok, detail=""):
    gates[name] = {"pass": bool(ok), "detail": detail}
    return ok

def parse_row(path):
    for line in pathlib.Path(path).read_text().splitlines():
        if line.startswith("third,") or line.startswith("replay,"):
            return line
    return ""

def input_candidates(fname):
    # published layout: input/ next to this script; kit layout: inv5/ sibling.
    return [ROOT / "input" / fname, KIT / "inv5" / fname]

def raw_candidates(name, fname):
    # loss rows: kit raws5/ flat, or out/<row>-replica-raws/, or the probe-lane
    # originals (published repo layout). win rows: kit raws4/, out/kNN-replica-raws/,
    # or the parked4 ladder originals.
    if name in ("k13", "k19"):
        return [KIT / "raws4" / fname,
                OUT / (name + "-replica-raws") / fname,
                PARKED / "output" / "raw" / fname]
    return [KIT / "raws5" / fname,
            OUT / (name + "-replica-raws") / fname,
            PROBE / "output" / "raw" / fname]

def find_raw(name, fname):
    return next((c for c in raw_candidates(name, fname) if c.exists()), None)

ROWS = json.loads(r"""{"k09": {"expansions": "4622038", "files": {"at15m-run1-k09.out.csv": ["2", "4018184", "15000000", "8ad953baf0a3de2db492b6242d087a6eba3fe687c91d2e85dadf284d92f27b09", "5", "87", "0", "10377419441368469504", "65536"], "at15m-run2-k09.out.csv": ["2", "4018184", "15000000", "3bbadffc78845e85086bdff8c926e6c2a43e295dc4e4c6a11d644649b66cb2da", "5", "87", "0", "10377419441368469504", "65536"], "at2m-k09.out.csv": ["0", "2000000", "2000000", "830b870ffeb9e646e949eb669053797a7c4fcaf74982f27aa6e83a050c0ae8b4", "5", "87", "0", "10377419441368469504", "65536"]}, "hi": "65536", "legal": "87", "lo": "10377419441368469504", "name": "k09", "nruns": 2, "rep_nodes": "4018184", "rep_result": "2", "result": "2", "stage": "loss15", "suffixes": ["a", "b"], "ttHits": "2607830", "ttOverwrites": "652622", "win": false}, "k10": {"expansions": "4945820", "files": {"at15m-run1-k10.out.csv": ["2", "4295355", "15000000", "e29a71292f1e90d14e06adc83e91e508659c10d82fb44ecaaf98caa9c2faac96", "5", "84", "0", "10378545341275312128", "65536"], "at15m-run2-k10.out.csv": ["2", "4295355", "15000000", "17e01019a008a2e6ffe5d3bc5371f0e437276ba50c0dc03a0658efbf6d5ac19f", "5", "84", "0", "10378545341275312128", "65536"], "at2m-k10.out.csv": ["0", "2000000", "2000000", "289f227f74d043e94d01ff66fc0fb79d442366dd64df1c470341120f4247657c", "5", "84", "0", "10378545341275312128", "65536"]}, "hi": "65536", "legal": "84", "lo": "10378545341275312128", "name": "k10", "nruns": 2, "rep_nodes": "4295355", "rep_result": "2", "result": "2", "stage": "loss15", "suffixes": ["a", "b"], "ttHits": "2741107", "ttOverwrites": "888907", "win": false}, "k11": {"expansions": "8105873", "files": {"at15m-run1-k11.out.csv": ["2", "7012218", "15000000", "09945e30a02937e99ae20795d989d6035194cdaa0a5611fe5a9e837cdd7068f3", "5", "86", "0", "10412322338480590848", "65536"], "at15m-run2-k11.out.csv": ["2", "7012218", "15000000", "a562d639db1e3fbbda72bb5181b3895a4597fd71a1989dbad0f1ee4fec439020", "5", "86", "0", "10412322338480590848", "65536"], "at2m-k11.out.csv": ["0", "2000000", "2000000", "ad82b26860bce8873b302baa4f0479d895f27673e7b25b3270600d48cd604ccf", "5", "86", "0", "10412322338480590848", "65536"]}, "hi": "65536", "legal": "86", "lo": "10412322338480590848", "name": "k11", "nruns": 2, "rep_nodes": "7012218", "rep_result": "2", "result": "2", "stage": "loss15", "suffixes": ["a", "b"], "ttHits": "4437184", "ttOverwrites": "3911738", "win": false}, "k12": {"expansions": "6593392", "files": {"at15m-run1-k12.out.csv": ["2", "5688761", "15000000", "43c4494ed5bcaea898640b8755325c1f2b27a9aeff6ce66f5202dfa3e190b897", "5", "83", "0", "10952754293765050368", "65536"], "at15m-run2-k12.out.csv": ["2", "5688761", "15000000", "43c4494ed5bcaea898640b8755325c1f2b27a9aeff6ce66f5202dfa3e190b897", "5", "83", "0", "10952754293765050368", "65536"], "at2m-k12.out.csv": ["0", "2000000", "2000000", "e7dd51a50bbf132c677d37f1e825c8a5ec05c5736d7c80c2aee5af984c0e0380", "5", "83", "0", "10952754293765050368", "65536"]}, "hi": "65536", "legal": "83", "lo": "10952754293765050368", "name": "k12", "nruns": 2, "rep_nodes": "5688761", "rep_result": "2", "result": "2", "stage": "loss15", "suffixes": ["a", "b"], "ttHits": "3638963", "ttOverwrites": "2404936", "win": false}, "k13": {"expansions": "19433195", "files": {"base15m-1152921573327376384-536870912.out.csv": ["0", "15000000", "15000000", "c911a74041642a526584f4c0612908d0564d2595b1872aeffa1b57ec296d4f67", "5", "95", "0", "1152921573327376384", "536870912"], "l50m-margin-1152921573327376384-536870912.out.csv": ["1", "16402480", "32000000", "9b6a0026caf8781d268d9e9da16b2cc7389ffd1e23aae92dc136c1d2464c94eb", "5", "95", "0", "1152921573327376384", "536870912"], "l50m-run1-1152921573327376384-536870912.out.csv": ["1", "16402480", "50000000", "b14273ee1a2b2c60375041f979db13f37c4b0b0b77d51e561bdf8abbac683985", "5", "95", "0", "1152921573327376384", "536870912"], "l50m-run2-1152921573327376384-536870912.out.csv": ["1", "16402480", "50000000", "155ffe291e6d1c106bda6e31515ae481032b63fee8578bdde52d26101ab4ebe4", "5", "95", "0", "1152921573327376384", "536870912"], "l50m-run3-verify-1152921573327376384-536870912.out.csv": ["1", "16402480", "50000000", "979b11478c30b16c03630a1700e04421d25df7bf9437e981d2c0b35bf4799968", "5", "95", "0", "1152921573327376384", "536870912"]}, "hi": "536870912", "legal": "95", "lo": "1152921573327376384", "name": "k13", "nruns": 3, "rep_nodes": "16402480", "rep_result": "1", "result": "1", "stage": "win", "suffixes": ["a", "b", "v-legal"], "ttHits": "10181270", "ttOverwrites": "15238891", "win": true}, "k14": {"expansions": "7836133", "files": {"at15m-run1-k14.out.csv": ["2", "6801611", "15000000", "db48c6fe5e314feeea1b6f60da2277a8eb23cbc6b3e7f20ceb093f9a16b9bf1f", "5", "99", "0", "1152956757699461120", "536870912"], "at15m-run2-k14.out.csv": ["2", "6801611", "15000000", "eab08cd4719ebf2c32bd61144a8ec86e22665a2adfc84134ca44274339fd38d3", "5", "99", "0", "1152956757699461120", "536870912"], "at2m-k14.out.csv": ["0", "2000000", "2000000", "5c651471e0cb48b5a69e0863eca442a7b61b3fdb4b719d16570dd175aa435846", "5", "99", "0", "1152956757699461120", "536870912"]}, "hi": "536870912", "legal": "99", "lo": "1152956757699461120", "name": "k14", "nruns": 2, "rep_nodes": "6801611", "rep_result": "2", "result": "2", "stage": "loss15", "suffixes": ["a", "b"], "ttHits": "4297914", "ttOverwrites": "3642312", "win": false}, "k15": {"expansions": "6903671", "files": {"at15m-run1-k15.out.csv": ["2", "5947870", "15000000", "41ed7c0f35ae119dfd08714b2e04d63d4b836777dc6dff9254631c4070454a26", "5", "99", "0", "1297036692683751424", "1064960"], "at15m-run2-k15.out.csv": ["2", "5947870", "15000000", "c4e2f73508b326b43ab8f527656c5ffd47c3e903f2a2f8bbbfbbf719388cb2a6", "5", "99", "0", "1297036692683751424", "1064960"], "at2m-k15.out.csv": ["0", "2000000", "2000000", "8ddc4d2928e9a753a638553d0cc6ef14e2a8bfbcbba0e9aec4b26479b12201f1", "5", "99", "0", "1297036692683751424", "1064960"]}, "hi": "1064960", "legal": "99", "lo": "1297036692683751424", "name": "k15", "nruns": 2, "rep_nodes": "5947870", "rep_result": "2", "result": "2", "stage": "loss15", "suffixes": ["a", "b"], "ttHits": "3790763", "ttOverwrites": "2712282", "win": false}, "k16": {"expansions": "12650074", "files": {"at15m-run1-k16.out.csv": ["2", "10883904", "15000000", "9446b88264791b9f0900e6c380179fad593c203e9c5e5f5c4fef182b94273956", "5", "95", "0", "1297036761403228160", "536870912"], "at15m-run2-k16.out.csv": ["2", "10883904", "15000000", "9446b88264791b9f0900e6c380179fad593c203e9c5e5f5c4fef182b94273956", "5", "95", "0", "1297036761403228160", "536870912"], "at2m-k16.out.csv": ["0", "2000000", "2000000", "1470c4fc82da1800d90e5cb0c4d723ffcf3ec51f5f1a957dbcff2ec9ff2c66b2", "5", "95", "0", "1297036761403228160", "536870912"]}, "hi": "536870912", "legal": "95", "lo": "1297036761403228160", "name": "k16", "nruns": 2, "rep_nodes": "10883904", "rep_result": "2", "result": "2", "stage": "loss15", "suffixes": ["a", "b"], "ttHits": "6857256", "ttOverwrites": "8455770", "win": false}, "k17": {"expansions": "1405334", "files": {"at15m-run1-k17.out.csv": ["2", "1241921", "15000000", "f82e89fd68e227a95cb0602d610423210d6f1ac5ece72ed5a19a837eac183476", "5", "96", "0", "10376293541461626880", "65537"], "at15m-run2-k17.out.csv": ["2", "1241921", "15000000", "f82e89fd68e227a95cb0602d610423210d6f1ac5ece72ed5a19a837eac183476", "5", "96", "0", "10376293541461626880", "65537"], "at2m-k17.out.csv": ["2", "1241921", "2000000", "f2834fe5c2d7e37c1ab375277080f86ca05fc03b2b317d49229eb8a122905e9a", "5", "96", "0", "10376293541461626880", "65537"], "at2m-run2-k17.out.csv": ["2", "1241921", "2000000", "f2834fe5c2d7e37c1ab375277080f86ca05fc03b2b317d49229eb8a122905e9a", "5", "96", "0", "10376293541461626880", "65537"]}, "hi": "65537", "legal": "96", "lo": "10376293541461626880", "name": "k17", "nruns": 2, "rep_nodes": "1241921", "rep_result": "2", "result": "2", "stage": "loss2m15m", "suffixes": ["a", "b"], "ttHits": "826431", "ttOverwrites": "47", "win": false}, "k18": {"expansions": "2098799", "files": {"at15m-run1-k18.out.csv": ["2", "1838655", "15000000", "5ffe97ab364ef3c6a30fcf757304fa5a2641816094fd5be8ae58b0dfd29dbadf", "5", "91", "0", "10376293541461626880", "65544"], "at15m-run2-k18.out.csv": ["2", "1838655", "15000000", "c411dbb19dc6bf6fac39827aa18d1df73d050ec3bf5520a53a422774d0fe2132", "5", "91", "0", "10376293541461626880", "65544"], "at2m-k18.out.csv": ["2", "1838655", "2000000", "302da911d9923ef373acd6c5e5caea7d2a7a6dc584e538d1462db8c093b3713c", "5", "91", "0", "10376293541461626880", "65544"], "at2m-run2-k18.out.csv": ["2", "1838655", "2000000", "302da911d9923ef373acd6c5e5caea7d2a7a6dc584e538d1462db8c093b3713c", "5", "91", "0", "10376293541461626880", "65544"]}, "hi": "65544", "legal": "91", "lo": "10376293541461626880", "name": "k18", "nruns": 2, "rep_nodes": "1838655", "rep_result": "2", "result": "2", "stage": "loss2m15m", "suffixes": ["a", "b"], "ttHits": "1184660", "ttOverwrites": "2153", "win": false}, "k19": {"expansions": "17955947", "files": {"base15m-10376293541461626880-65664.out.csv": ["0", "15000000", "15000000", "34e9a2b7aef6f5c60eb2dfbb2813cb663cf383af71e5852720529bfa01337539", "5", "95", "0", "10376293541461626880", "65664"], "l50m-margin-10376293541461626880-65664.out.csv": ["1", "15379062", "32000000", "be8f4289607c24e1cba48b3bd4efac15e80874fec7987cef3c037d7de53a7517", "5", "95", "0", "10376293541461626880", "65664"], "l50m-run1-10376293541461626880-65664.out.csv": ["1", "15379062", "50000000", "0e1287abba7d7f012f8e42bc9f774ec6cc093b46c54fb40f570f7c6d1c891abb", "5", "95", "0", "10376293541461626880", "65664"], "l50m-run2-10376293541461626880-65664.out.csv": ["1", "15379062", "50000000", "0e1287abba7d7f012f8e42bc9f774ec6cc093b46c54fb40f570f7c6d1c891abb", "5", "95", "0", "10376293541461626880", "65664"], "l50m-run3-verify-10376293541461626880-65664.out.csv": ["1", "15379062", "50000000", "eb624fcf4e753114ad708406b35683eedb3b1811be80fdb005c2eeed726ad3a5", "5", "95", "0", "10376293541461626880", "65664"]}, "hi": "65664", "legal": "95", "lo": "10376293541461626880", "name": "k19", "nruns": 3, "rep_nodes": "15379062", "rep_result": "1", "result": "1", "stage": "win", "suffixes": ["a", "b", "v-legal"], "ttHits": "9504863", "ttOverwrites": "13761643", "win": true}, "k21": {"expansions": "4202005", "files": {"at15m-run1-k21.out.csv": ["2", "3649839", "15000000", "a8c70a5a5cb4d343603a1b8be86a13a10a91ea59a67d1fc806a152acdfe0ff4f", "5", "90", "0", "10376293541461626880", "67174400"], "at15m-run2-k21.out.csv": ["2", "3649839", "15000000", "934d60aa76cfad44c945c1509caff1c7604a73cd2b2dda002ae71008ab5f47c2", "5", "90", "0", "10376293541461626880", "67174400"], "at2m-k21.out.csv": ["0", "2000000", "2000000", "027bffe2cdec9fc03cce47a1cb7493472357a112d40fbe19f78259adf23ffef0", "5", "90", "0", "10376293541461626880", "67174400"]}, "hi": "67174400", "legal": "90", "lo": "10376293541461626880", "name": "k21", "nruns": 2, "rep_nodes": "3649839", "rep_result": "2", "result": "2", "stage": "loss15", "suffixes": ["a", "b"], "ttHits": "2326723", "ttOverwrites": "392033", "win": false}, "k22": {"expansions": "8820734", "files": {"at15m-run1-k22.out.csv": ["2", "7527812", "15000000", "c5ae72f9ec839e1a451e279705a743f383769105bc165c49f0fe8c0a32013538", "5", "98", "0", "10376293541461626880", "268500992"], "at15m-run2-k22.out.csv": ["2", "7527812", "15000000", "789c8d31bced36108f022a8157d3efd883b441fb86f4f330b0a61855c7a7f89e", "5", "98", "0", "10376293541461626880", "268500992"], "at2m-k22.out.csv": ["0", "2000000", "2000000", "a85953a759240f8f91726c16edc0568b8a0068c9666a0c2af55e9bbc90da4639", "5", "98", "0", "10376293541461626880", "268500992"]}, "hi": "268500992", "legal": "98", "lo": "10376293541461626880", "name": "k22", "nruns": 2, "rep_nodes": "7527812", "rep_result": "2", "result": "2", "stage": "loss15", "suffixes": ["a", "b"], "ttHits": "4653093", "ttOverwrites": "4626471", "win": false}, "k23": {"expansions": "12654986", "files": {"at15m-run1-k23.out.csv": ["2", "10938326", "15000000", "4b1de3ccaf7e3bc4852f63ed6bb57409da994e9cac68ae90e3a8966d422846ca", "5", "97", "0", "10376293541461626912", "65536"], "at15m-run2-k23.out.csv": ["2", "10938326", "15000000", "cd4f2f1f303e49e58c3e7d17c27b0eb50ecbb66f4a25ecb9254f6a2e9ab38085", "5", "97", "0", "10376293541461626912", "65536"], "at2m-k23.out.csv": ["0", "2000000", "2000000", "57a9a999235292892dce3d0e8db6c3147cd91bcadb5711d854d7d9900de8b2de", "5", "97", "0", "10376293541461626912", "65536"]}, "hi": "65536", "legal": "97", "lo": "10376293541461626912", "name": "k23", "nruns": 2, "rep_nodes": "10938326", "rep_result": "2", "result": "2", "stage": "loss15", "suffixes": ["a", "b"], "ttHits": "6739220", "ttOverwrites": "8460682", "win": false}, "k24": {"expansions": "5616289", "files": {"at15m-run1-k24.out.csv": ["2", "4796315", "15000000", "37d77c3762bc95e08a095d21d192b6e5bfa7cfad7b21282bce9807bf68aca464", "5", "93", "0", "10376293541461627904", "65536"], "at15m-run2-k24.out.csv": ["2", "4796315", "15000000", "9866fabeddb14ab503166944acf61772501c80cbd801faaf1f3aec974f4697b6", "5", "93", "0", "10376293541461627904", "65536"], "at2m-k24.out.csv": ["0", "2000000", "2000000", "a1f0b3b68645cb7b9c254f6254200cbea1cafc1c4fac229fd0e7578a2a81f6f1", "5", "93", "0", "10376293541461627904", "65536"]}, "hi": "65536", "legal": "93", "lo": "10376293541461627904", "name": "k24", "nruns": 2, "rep_nodes": "4796315", "rep_result": "2", "result": "2", "stage": "loss15", "suffixes": ["a", "b"], "ttHits": "3010163", "ttOverwrites": "1467038", "win": false}, "k25": {"expansions": "6336310", "files": {"at15m-run1-k25.out.csv": ["2", "5496449", "15000000", "3bbb1dc2a8a6fd67ce9039a4c0a87fa9715a26bc567e0f23dabd5044d1d91227", "5", "91", "0", "10376293541461659648", "65536"], "at15m-run2-k25.out.csv": ["2", "5496449", "15000000", "768b87150adfa3e87b134ee8f511f9851a58a1d0a571cff049dabef1ce443d2a", "5", "91", "0", "10376293541461659648", "65536"], "at2m-k25.out.csv": ["0", "2000000", "2000000", "b10147cbe3930b57b571f3e98697fde16ad231d07655f00f932cb2feeb6ccf7a", "5", "91", "0", "10376293541461659648", "65536"]}, "hi": "65536", "legal": "91", "lo": "10376293541461659648", "name": "k25", "nruns": 2, "rep_nodes": "5496449", "rep_result": "2", "result": "2", "stage": "loss15", "suffixes": ["a", "b"], "ttHits": "3564228", "ttOverwrites": "2153523", "win": false}, "k26": {"expansions": "16684962", "files": {"at15m-run1-k26.out.csv": ["2", "14439424", "15000000", "d53e0cb756dddc9e9d0a84a6a50b75cefd812f51337a2b3ef19752253d2b254e", "5", "95", "0", "10376293541462151168", "65536"], "at15m-run2-k26.out.csv": ["2", "14439424", "15000000", "5530922e24a48f5b71a15c4fa3a9357b964b90c158c8bc7ee72d65b3a7964cdd", "5", "95", "0", "10376293541462151168", "65536"], "at2m-k26.out.csv": ["0", "2000000", "2000000", "736209bbbc321d5202dfb5baa2539df68d298a2b5465801c4e18c7e7c485f817", "5", "95", "0", "10376293541462151168", "65536"]}, "hi": "65536", "legal": "95", "lo": "10376293541462151168", "name": "k26", "nruns": 2, "rep_nodes": "14439424", "rep_result": "2", "result": "2", "stage": "loss15", "suffixes": ["a", "b"], "ttHits": "8721684", "ttOverwrites": "12490658", "win": false}, "k27": {"expansions": "2578044", "files": {"at15m-run1-k27.out.csv": ["2", "2250306", "15000000", "5bc995699e804475f107570b1c06fca903693d4bc2ef47340739fdc482eacd6c", "5", "93", "0", "10376293541478404096", "65536"], "at15m-run2-k27.out.csv": ["2", "2250306", "15000000", "5bc995699e804475f107570b1c06fca903693d4bc2ef47340739fdc482eacd6c", "5", "93", "0", "10376293541478404096", "65536"], "at2m-k27.out.csv": ["0", "2000000", "2000000", "dad5b085f1d80f0a7400dfb7792f90e63b4a6ce5c0ebb2d493147f262a93618b", "5", "93", "0", "10376293541478404096", "65536"]}, "hi": "65536", "legal": "93", "lo": "10376293541478404096", "name": "k27", "nruns": 2, "rep_nodes": "2250306", "rep_result": "2", "result": "2", "stage": "loss15", "suffixes": ["a", "b"], "ttHits": "1458498", "ttOverwrites": "10504", "win": false}, "k28": {"expansions": "2177958", "files": {"at2m-k28.out.csv": ["2", "1918850", "2000000", "189092ef700e69750ad9be96aaf9abf4fe8eda0559432cef8cd58bc50faa1ed1", "5", "98", "0", "10376293541528735744", "65536"], "at2m-run2-k28.out.csv": ["2", "1918850", "2000000", "189092ef700e69750ad9be96aaf9abf4fe8eda0559432cef8cd58bc50faa1ed1", "5", "98", "0", "10376293541528735744", "65536"]}, "hi": "65536", "legal": "98", "lo": "10376293541528735744", "name": "k28", "nruns": 2, "rep_nodes": "1918850", "rep_result": "2", "result": "2", "stage": "loss2m", "suffixes": ["a", "b"], "ttHits": "1274689", "ttOverwrites": "2777", "win": false}, "k29": {"expansions": "5797487", "files": {"at15m-run1-k29.out.csv": ["2", "4996919", "15000000", "b7e2d3c78ba07a94aefc3305a7ddeed136e95fd460530dfa3066a30abe391428", "5", "97", "0", "10376293541595844608", "65536"], "at15m-run2-k29.out.csv": ["2", "4996919", "15000000", "b7e2d3c78ba07a94aefc3305a7ddeed136e95fd460530dfa3066a30abe391428", "5", "97", "0", "10376293541595844608", "65536"], "at2m-k29.out.csv": ["0", "2000000", "2000000", "bf4d012246b6c830399f6f153610d8fe1edc77521cad33b7dfdd2c43ff7b76f0", "5", "97", "0", "10376293541595844608", "65536"]}, "hi": "65536", "legal": "97", "lo": "10376293541595844608", "name": "k29", "nruns": 2, "rep_nodes": "4996919", "rep_result": "2", "result": "2", "stage": "loss15", "suffixes": ["a", "b"], "ttHits": "3237734", "ttOverwrites": "1635160", "win": false}, "k30": {"expansions": "4531296", "files": {"at15m-run1-k30.out.csv": ["2", "3933511", "15000000", "69a156a55a86e302f80bee81a36d144af7b48934402baaba315bf892689a550d", "5", "95", "0", "10376293610181103616", "65536"], "at15m-run2-k30.out.csv": ["2", "3933511", "15000000", "43ddd5818ba82c09726e6780beefc5d35874482bf276d831805d253de579475a", "5", "95", "0", "10376293610181103616", "65536"], "at2m-k30.out.csv": ["0", "2000000", "2000000", "8af30f012f8b28a267215f95aae3a78d761d27550fe74ab69fdc6d455938cca3", "5", "95", "0", "10376293610181103616", "65536"]}, "hi": "65536", "legal": "95", "lo": "10376293610181103616", "name": "k30", "nruns": 2, "rep_nodes": "3933511", "rep_result": "2", "result": "2", "stage": "loss15", "suffixes": ["a", "b"], "ttHits": "2619620", "ttOverwrites": "597949", "win": false}, "k31": {"expansions": "5269285", "files": {"at15m-run1-k31.out.csv": ["2", "4560796", "15000000", "6dddbe547438e9726e532bcddbd9c8e9327635418cf03697e95dfccdfda551b3", "5", "92", "0", "10376856491415048192", "65536"], "at15m-run2-k31.out.csv": ["2", "4560796", "15000000", "6dddbe547438e9726e532bcddbd9c8e9327635418cf03697e95dfccdfda551b3", "5", "92", "0", "10376856491415048192", "65536"], "at2m-k31.out.csv": ["0", "2000000", "2000000", "807d45296efddf7df344d27a9a5c6fe3762eda3c3ee47cd97ab47171d3cbd7d8", "5", "92", "0", "10376856491415048192", "65536"]}, "hi": "65536", "legal": "92", "lo": "10376856491415048192", "name": "k31", "nruns": 2, "rep_nodes": "4560796", "rep_result": "2", "result": "2", "stage": "loss15", "suffixes": ["a", "b"], "ttHits": "2862847", "ttOverwrites": "1151374", "win": false}, "k32": {"expansions": "2235267", "files": {"at2m-k32.out.csv": ["2", "1989908", "2000000", "8c8ebb3eb42da60e57bde403cc0dfe15c72f256b526a6c4c73e42722bc668312", "5", "93", "0", "10664523917613338624", "65536"], "at2m-run2-k32.out.csv": ["2", "1989908", "2000000", "8c8ebb3eb42da60e57bde403cc0dfe15c72f256b526a6c4c73e42722bc668312", "5", "93", "0", "10664523917613338624", "65536"]}, "hi": "65536", "legal": "93", "lo": "10664523917613338624", "name": "k32", "nruns": 2, "rep_nodes": "1989908", "rep_result": "2", "result": "2", "stage": "loss2m", "suffixes": ["a", "b"], "ttHits": "1374600", "ttOverwrites": "3852", "win": false}, "k34": {"expansions": "9966873", "files": {"at15m-run1-k34.out.csv": ["2", "8567123", "15000000", "c0de8c6a0df4e6bb33eadcbc8bd7aa89f8df3ced8d65d12a34e8544a7233ffb2", "5", "96", "0", "14987979559889014784", "65536"], "at15m-run2-k34.out.csv": ["2", "8567123", "15000000", "8021ec79348e2467ab0b5f9760089ab3ec2b91d0bfdb81dd95bab42e73737313", "5", "96", "0", "14987979559889014784", "65536"], "at2m-k34.out.csv": ["0", "2000000", "2000000", "2ce58086b3bfc0b487bd6e170c0480257cf8cf8c7793d251eb39d89d2d170d15", "5", "96", "0", "14987979559889014784", "65536"]}, "hi": "65536", "legal": "96", "lo": "14987979559889014784", "name": "k34", "nruns": 2, "rep_nodes": "8567123", "rep_result": "2", "result": "2", "stage": "loss15", "suffixes": ["a", "b"], "ttHits": "5293840", "ttOverwrites": "5772570", "win": false}, "k35": {"expansions": "16896018", "files": {"at15m-run1-k35.out.csv": ["2", "14273589", "15000000", "7722a6488ab33017f9da9ff947d906264d6432019d3cc9040d733169cd98c57f", "5", "100", "0", "1152921573327372288", "553648128"], "at15m-run2-k35.out.csv": ["2", "14273589", "15000000", "95b1014485c87666913a5266b182e6d514628ae477096c5a9989ee18b806e52c", "5", "100", "0", "1152921573327372288", "553648128"], "at2m-k35.out.csv": ["0", "2000000", "2000000", "0101327dced0f46d4087c4aa631d2917de30bbfe6215cc7ea104fe64d0199201", "5", "100", "0", "1152921573327372288", "553648128"]}, "hi": "553648128", "legal": "100", "lo": "1152921573327372288", "name": "k35", "nruns": 2, "rep_nodes": "14273589", "rep_result": "2", "result": "2", "stage": "loss15", "suffixes": ["a", "b"], "ttHits": "8726341", "ttOverwrites": "12701714", "win": false}, "k36": {"expansions": "3440325", "files": {"at15m-run1-k36.out.csv": ["2", "3007021", "15000000", "562ba346acc6a4e3da8d3f80ab61aebfc5738192983ff3924a98cce89053276e", "5", "100", "0", "1224979167365300224", "536870912"], "at15m-run2-k36.out.csv": ["2", "3007021", "15000000", "562ba346acc6a4e3da8d3f80ab61aebfc5738192983ff3924a98cce89053276e", "5", "100", "0", "1224979167365300224", "536870912"], "at2m-k36.out.csv": ["0", "2000000", "2000000", "4d535300bcbc168b9478b9cde812ac0f581b19762bb1d17f969cdb2da3935c64", "5", "100", "0", "1224979167365300224", "536870912"]}, "hi": "536870912", "legal": "100", "lo": "1224979167365300224", "name": "k36", "nruns": 2, "rep_nodes": "3007021", "rep_result": "2", "result": "2", "stage": "loss15", "suffixes": ["a", "b"], "ttHits": "1961576", "ttOverwrites": "107949", "win": false}, "k37": {"expansions": "9510402", "files": {"at15m-run1-k37.out.csv": ["2", "8083885", "15000000", "eb00397435727be266f9783871e3932cd8c7a0ecd9a27585dbfa77b1411c2265", "5", "103", "0", "1297036692683751424", "17825792"], "at15m-run2-k37.out.csv": ["2", "8083885", "15000000", "c07990271dba7346c280fd6ed70bb8facb119916d5ab12fa3ae7933c7f0a325d", "5", "103", "0", "1297036692683751424", "17825792"], "at2m-k37.out.csv": ["0", "2000000", "2000000", "de8fcc1ed30fa40a319ec61dd9c01f657fb5e81ce617b0c6d8ab71534581762f", "5", "103", "0", "1297036692683751424", "17825792"]}, "hi": "17825792", "legal": "103", "lo": "1297036692683751424", "name": "k37", "nruns": 2, "rep_nodes": "8083885", "rep_result": "2", "result": "2", "stage": "loss15", "suffixes": ["a", "b"], "ttHits": "4989499", "ttOverwrites": "5316103", "win": false}, "k39": {"expansions": "6611082", "files": {"at15m-run1-k39.out.csv": ["2", "5725348", "15000000", "af3bb4c3513561c1760c7aa774b9d2ee984930d3dd1e4ce7ba4ba2ae60f49ee0", "5", "100", "0", "10376293541461626880", "66560"], "at15m-run2-k39.out.csv": ["2", "5725348", "15000000", "af3bb4c3513561c1760c7aa774b9d2ee984930d3dd1e4ce7ba4ba2ae60f49ee0", "5", "100", "0", "10376293541461626880", "66560"], "at2m-k39.out.csv": ["0", "2000000", "2000000", "a7951d82df52cd7dc2aeabea6882f21a245e846281335d7c2740c0edba407130", "5", "100", "0", "10376293541461626880", "66560"]}, "hi": "66560", "legal": "100", "lo": "10376293541461626880", "name": "k39", "nruns": 2, "rep_nodes": "5725348", "rep_result": "2", "result": "2", "stage": "loss15", "suffixes": ["a", "b"], "ttHits": "3659270", "ttOverwrites": "2422272", "win": false}, "k40": {"expansions": "6894081", "files": {"at15m-run1-k40.out.csv": ["2", "5926395", "15000000", "9dc4b27ecd03bcaeb0bd58475700a273a63d9b2a4ea47d33c4ce4542e6ea592b", "5", "102", "0", "10376293541461626880", "67584"], "at15m-run2-k40.out.csv": ["2", "5926395", "15000000", "7a6d41d848ec2e32e28a30e387a93bbbbad426bb5670cf39a10d962e544084e6", "5", "102", "0", "10376293541461626880", "67584"], "at2m-k40.out.csv": ["0", "2000000", "2000000", "643406dccb4b66c6b6e2153a2fef5b60120b5d49dc648066ddd9a8ed0865c44b", "5", "102", "0", "10376293541461626880", "67584"]}, "hi": "67584", "legal": "102", "lo": "10376293541461626880", "name": "k40", "nruns": 2, "rep_nodes": "5926395", "rep_result": "2", "result": "2", "stage": "loss15", "suffixes": ["a", "b"], "ttHits": "3725971", "ttOverwrites": "2703506", "win": false}, "k41": {"expansions": "7704061", "files": {"at15m-run1-k41.out.csv": ["2", "6536846", "15000000", "542ca03402b81721f4a529d14dd240017d4fd81836f8ce458009c0bbbf6bddfd", "5", "100", "0", "10376293541461626884", "65536"], "at15m-run2-k41.out.csv": ["2", "6536846", "15000000", "542ca03402b81721f4a529d14dd240017d4fd81836f8ce458009c0bbbf6bddfd", "5", "100", "0", "10376293541461626884", "65536"], "at2m-k41.out.csv": ["0", "2000000", "2000000", "1b613c597a42a50a81beb6b2911f9b60493de64ab3b301b3db3f3a7ffe93ac80", "5", "100", "0", "10376293541461626884", "65536"]}, "hi": "65536", "legal": "100", "lo": "10376293541461626884", "name": "k41", "nruns": 2, "rep_nodes": "6536846", "rep_result": "2", "result": "2", "stage": "loss15", "suffixes": ["a", "b"], "ttHits": "4018770", "ttOverwrites": "3510186", "win": false}, "k42": {"expansions": "10223560", "files": {"at15m-run1-k42.out.csv": ["2", "8486305", "15000000", "f1fab0ea787967329db92b3e9d81606ba5af7756ca7b195188599b0540313503", "5", "101", "0", "10376293541461627136", "65536"], "at15m-run2-k42.out.csv": ["2", "8486305", "15000000", "a810cda5cb75e9cef92d8ec70a94e58c337a4f614a0e084c9d4beff8a12cac0c", "5", "101", "0", "10376293541461627136", "65536"], "at2m-k42.out.csv": ["0", "2000000", "2000000", "61cf72b7071e4c4cc6a0d36f3d3d2660cdb0fc4b743b3afbe365ae4be92b61c9", "5", "101", "0", "10376293541461627136", "65536"]}, "hi": "65536", "legal": "101", "lo": "10376293541461627136", "name": "k42", "nruns": 2, "rep_nodes": "8486305", "rep_result": "2", "result": "2", "stage": "loss15", "suffixes": ["a", "b"], "ttHits": "5244634", "ttOverwrites": "6029256", "win": false}, "k43": {"expansions": "8061097", "files": {"at15m-run1-k43.out.csv": ["2", "6916669", "15000000", "78668844f8c0b33d5baf5bac9d2cd49c7b047452a5b2464cf8024ed756f1c3dc", "5", "103", "0", "10376293541461692416", "65536"], "at15m-run2-k43.out.csv": ["2", "6916669", "15000000", "78668844f8c0b33d5baf5bac9d2cd49c7b047452a5b2464cf8024ed756f1c3dc", "5", "103", "0", "10376293541461692416", "65536"], "at2m-k43.out.csv": ["0", "2000000", "2000000", "7175fb05f2ffe544ff397b2288058934b4ecc381c33612d9ed23b7ee002cf434", "5", "103", "0", "10376293541461692416", "65536"]}, "hi": "65536", "legal": "103", "lo": "10376293541461692416", "name": "k43", "nruns": 2, "rep_nodes": "6916669", "rep_result": "2", "result": "2", "stage": "loss15", "suffixes": ["a", "b"], "ttHits": "4354662", "ttOverwrites": "3867018", "win": false}}""")
INPINS = json.loads(r"""{"batch-k13.input.csv": ["298dd6e6b6655d12aefaae138a2e1d85388220546ff68e4d6b7081c6097b0526", "target,0,5,1152921573327376384,536870912,95,0,0,0,0,0"], "batch-k19.input.csv": ["88c107d7d060ef756a394d722de3a80b4ee60bad5647785cbbb65eb088da6190", "target,0,5,10376293541461626880,65664,95,0,0,0,0,0"], "k09.input.csv": ["30f624ad720881d7f0862a87dde4ad0c98334955e0bef9cbb3d13f3e6018f7a5", "target,0,5,10377419441368469504,65536,87,0,0,0,0,0"], "k10.input.csv": ["debad4e6882244bd988a048232cc321c8271cdb0c806e57a76b575bcbf0f6bfe", "target,0,5,10378545341275312128,65536,84,0,0,0,0,0"], "k11.input.csv": ["397fa6818809dab6753a32ba4a1f461c72053db43eefac416d4751a7f27ebaf4", "target,0,5,10412322338480590848,65536,86,0,0,0,0,0"], "k12.input.csv": ["f138355625ee60e2a896841714a36a2a816dc87021593af84ddcc2b051fb6248", "target,0,5,10952754293765050368,65536,83,0,0,0,0,0"], "k14.input.csv": ["b3705f4dbc20412de9323d8a7cdc7c69d319b87ac68d0f0f1c242c016e389043", "target,0,5,1152956757699461120,536870912,99,0,0,0,0,0"], "k15.input.csv": ["c9d9e147cf24ccb1b2a905abd7ac42507ef46894df3a6c356f8e5df2493fe14c", "target,0,5,1297036692683751424,1064960,99,0,0,0,0,0"], "k16.input.csv": ["d9a02354620fbab2bf401b7e59097d2647de3e22b1c0a2852cdd1696b0ba702d", "target,0,5,1297036761403228160,536870912,95,0,0,0,0,0"], "k17.input.csv": ["71795886d6f48b47967849e56865d1b99e2348d95d599cec1f4523e028bce664", "target,0,5,10376293541461626880,65537,96,0,0,0,0,0"], "k18.input.csv": ["d45a966f2e28c356647d3fbbf2608e12957c0457d12dc4e07b146e2e809607df", "target,0,5,10376293541461626880,65544,91,0,0,0,0,0"], "k21.input.csv": ["11be0160ff5f7ae9fe2df718706cfc5513ab098247b698c79f0b3afd1a04edc0", "target,0,5,10376293541461626880,67174400,90,0,0,0,0,0"], "k22.input.csv": ["f7e1f23551c8c03fe9741f8ca52e219de1be0bbc2c57b54b69b65cf3f3b0e0a2", "target,0,5,10376293541461626880,268500992,98,0,0,0,0,0"], "k23.input.csv": ["4058bc9fe5bd1bddab42678038eb2494e99ffe614dc7fa2d21eea5e6bdb469a3", "target,0,5,10376293541461626912,65536,97,0,0,0,0,0"], "k24.input.csv": ["a707f4484f5df0c1e448099625fb67f33b82574aa87b18a95b7b512dc61d2b01", "target,0,5,10376293541461627904,65536,93,0,0,0,0,0"], "k25.input.csv": ["0badeaf933c9b5ce57a807d33ce2354bb5d3c7536076a73f78fa50d8c60a8759", "target,0,5,10376293541461659648,65536,91,0,0,0,0,0"], "k26.input.csv": ["f237dd091ffceddfc3160cafaa8049382533edbcfc0176223eb7de54266bcf93", "target,0,5,10376293541462151168,65536,95,0,0,0,0,0"], "k27.input.csv": ["a24ae408df6b6fc85fb5556938ca1142146704c39de5f8484e79673e734b2c63", "target,0,5,10376293541478404096,65536,93,0,0,0,0,0"], "k28.input.csv": ["b8dd9bab4d7b20e126342e00e7abeb4fe3f298c86c40e98a39177f2791fb8502", "target,0,5,10376293541528735744,65536,98,0,0,0,0,0"], "k29.input.csv": ["b5b471b61d5fd6f0378d6514efaa8fdc22442324956f06e847342a3a792c7031", "target,0,5,10376293541595844608,65536,97,0,0,0,0,0"], "k30.input.csv": ["6b0d968ddacca16d4776cd7bfda70e0993c833439b92c842c87ba78f0a2e51d6", "target,0,5,10376293610181103616,65536,95,0,0,0,0,0"], "k31.input.csv": ["207b670fd26de75f7df7fe4b6e0cb165614e80f7f6805140eb4b08d365cf3e09", "target,0,5,10376856491415048192,65536,92,0,0,0,0,0"], "k32.input.csv": ["97e42b8e019ff21e6044c55e5377a6ff4c831c98abb6b8c8a14de4b5e701e135", "target,0,5,10664523917613338624,65536,93,0,0,0,0,0"], "k34.input.csv": ["aeac0db59d4d6462004c3f9a70fed9503c8fb77e947fae52f508fcca95cc8860", "target,0,5,14987979559889014784,65536,96,0,0,0,0,0"], "k35.input.csv": ["92900664b9a4d71f8c6d629e6d0167eb0c6bb33f7802e2513b4b8ee8015fa4a6", "target,0,5,1152921573327372288,553648128,100,0,0,0,0,0"], "k36.input.csv": ["95737de8241d394761e2ab7da6eceec93ae12e01ce630beb0bc1c86f1ab96c85", "target,0,5,1224979167365300224,536870912,100,0,0,0,0,0"], "k37.input.csv": ["c6f15f3d675a49de4bfaabfda338e5a37aa11b9db2a691d9e3f14a729b174d96", "target,0,5,1297036692683751424,17825792,103,0,0,0,0,0"], "k39.input.csv": ["a155e95d0619b244bc1822e039564729a8160c979f4384f5766a00b89988646e", "target,0,5,10376293541461626880,66560,100,0,0,0,0,0"], "k40.input.csv": ["51d7e6ccdd9f1be7442fe6b4e16f5ca1aeb25d06fba2c0122957c16b8658f3bf", "target,0,5,10376293541461626880,67584,102,0,0,0,0,0"], "k41.input.csv": ["de03c3cedc9fe936d31469ef5a89468ca8880749ffd6654448e46c2866045a48", "target,0,5,10376293541461626884,65536,100,0,0,0,0,0"], "k42.input.csv": ["33a7cd33eb40d1f81330590a5f4bccc328427a41ca8c040f1eccf45d11f180dd", "target,0,5,10376293541461627136,65536,101,0,0,0,0,0"], "k43.input.csv": ["ea2279fef225291747d58b6ad6e7f430025b200485f1a7d6b3beb2c2acae7f76", "target,0,5,10376293541461692416,65536,103,0,0,0,0,0"]}""")
PINS = {
    "third_impl.js": ([ROOT / "third_impl.js", KIT / "inv" / "third_impl.js"], "08ea958ff59c3234ec5ac55c5c40689bd0999a34e101a88ea0546800cc4a1998"),
    "verify_tbl.js": ([ROOT / "verify_tbl.js", KIT / "inv" / "verify_tbl.js"], "c8c52528f70b3a9b438edc3feb4e432fbe705d6be21650383d3955efc6790251"),
    "jsreplay.js": ([KIT / "inv" / "jsreplay.js", PROBE / "scripts" / "jsreplay.js"], "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df"),
}

# ---- pins of consumed scripts (unchanged program scripts) ----
for _name, (_cands, _sha) in PINS.items():
    _p = next((c for c in _cands if c.exists()), None)
    gate("pin_" + _name.replace(".", "_") + "_sha256",
         _p is not None and sha256(_p) == _sha,
         str(_p) if _p is not None else "not found in any candidate location")

# ---- row-spec input pins (published batch inputs consumed at the recorded HEADs) ----
for _fname, (_sha, _spec) in INPINS.items():
    _p = next((c for c in input_candidates(_fname) if c.exists()), None)
    gate("pin_input_" + _fname.replace(".", "_") + "_sha256",
         _p is not None and sha256(_p) == _sha and _p.read_text().strip() == _spec,
         str(_p) if _p is not None else "not found in any candidate location")

# ---- scope gate ----
NLOSS = sum(1 for r in ROWS.values() if not r["win"])
NWIN = sum(1 for r in ROWS.values() if r["win"])
gate("scope_rows_30loss_2win", NLOSS == 30 and NWIN == 2 and len(ROWS) == 32,
     "loss=%d win=%d total=%d" % (NLOSS, NWIN, len(ROWS)))

# ---- replica raw + third-impl gates, data-driven per row ----
batch = {}
for name, info in ROWS.items():
    rr = {}
    missing = False
    for fname, (result, nodes, budget, sha, stones, legal, is_or, lo, hi) in sorted(info["files"].items()):
        p = find_raw(name, fname)
        ok = p is not None and sha256(p) == sha
        gate("repl_sha_%s_%s" % (name, fname), ok,
             str(p) if p is not None else "not found in any candidate location")
        if not ok:
            missing = True
            continue
        c = parse_row(p).split(",")
        # replay,id,stones,legal,is_or,budget,result,nodes,wall_s,key_lo,key_hi
        ok = (c[0] == "replay" and c[2] == str(stones) and c[3] == str(legal)
              and c[4] == str(is_or) and c[5] == str(budget) and c[9] == str(lo)
              and c[10] == str(hi) and c[6] == str(result) and c[7] == str(nodes))
        gate("repl_row_%s_%s" % (name, fname), ok, " | ".join(c))
        rr[fname] = (c[6], c[7])
    if missing:
        continue
    tr = []
    for s in info["suffixes"]:
        f = ("%s-cold-%s.txt" % (name, s)) if s != "v-legal" else ("%s-cold-v-legal.txt" % name)
        text = (OUT / f).read_text()
        c = parse_row(OUT / f).split(",")
        tr.append(c)
        gate("third_clean_%s_%s" % (name, f), c[11] == "clean", "reason=%s" % c[11])
        gate("third_derivedlegal_%s_%s" % (name, f), c[3] == c[4] == str(info["legal"]),
             "in=%s derived=%s" % (c[3], c[4]))
        gate("third_key_%s_%s" % (name, f), c[9] == info["lo"] and c[10] == info["hi"],
             " | ".join(c))
        gate("third_rc0_%s_%s" % (name, f), text.strip().endswith("rc=0"), "rc line")
        gate("third_quads_%s_%s" % (name, f), "quads=95670" in text, "quads")
    tv = [(c[5], c[6], c[7]) for c in tr]
    uniq = set(tv)
    if info["win"]:
        wins = [(r, n) for f, (r, n) in rr.items() if r == "1"]
        gate("repl_%s_win_4runs_unanimous" % name,
             len(wins) == 4 and all(n == info["rep_nodes"] for _, n in wins), str(wins))
        base = [(r, n) for f, (r, n) in rr.items()
                if f.startswith("base15m")]
        gate("repl_%s_base15m_parked_unknown" % name, base == [("0", "15000000")], str(base))
        gate("C2_%s_win_verdict_level_vs_replica" % name,
             all(c[5] == "1" for c in tr),
             "third=%s replica=1" % sorted(set(c[5] for c in tr)))
    else:
        losses = sorted(set((r, n) for f, (r, n) in rr.items() if r == "2"))
        gate("repl_%s_loss_runs_unanimous" % name,
             losses == [(info["rep_result"], info["rep_nodes"])], str(rr))
        if info["stage"] == "loss15":
            base = [(r, n) for f, (r, n) in rr.items() if r == "0"]
            gate("repl_%s_2m_unknown" % name, base == [("0", "2000000")], str(base))
            gate("repl_%s_15m_pair_extra" % name,
                 sorted(set(n for f, (r, n) in rr.items() if r == "2")) == [info["rep_nodes"]], str(rr))
        gate("C2_%s_loss_verdict_level_vs_replica" % name,
             all(c[5] == "2" for c in tr) and info["rep_result"] == "2",
             "third=%s replica=%s" % (sorted(set(c[5] for c in tr)), info["rep_result"]))
    gate("C2_%s_determinism_%druns_identical" % (name, info["nruns"]),
         len(uniq) == 1 and uniq == {(info["result"], info["expansions"], info["ttHits"])},
         str(tv))
    gate("C2_%s_ttoverwrites_pinned" % name,
         all(("ttOverwrites=%s" % info["ttOverwrites"]) in
             (OUT / (("%s-cold-%s.txt" % (name, s)) if s != "v-legal" else ("%s-cold-v-legal.txt" % name))).read_text()
             for s in info["suffixes"]),
         "ttOverwrites=%s" % info["ttOverwrites"])
    gate("C2_%s_expansions_differ_from_replica_nodes_allowed" % name,
         all(int(c[6]) != int(n) for c in tr for n in set(v[1] for v in rr.values())),
         "third=%s replica=%s (different implementations; verdict-level agreement is the gate)"
         % (info["expansions"], sorted(set(v[1] for v in rr.values()))))
    # C4 negative gates for this row
    ng1 = "neg-gate-%s-legal%d.txt" % (name, int(info["legal"]) + 1)
    t1 = (OUT / ng1).read_text()
    gate("C4_ng1_%s_legal%d_gate_fail" % (name, int(info["legal"]) + 1),
         "GATE_FAIL" in t1
         and ("legal count mismatch: derived=%d declared=%d" % (int(info["legal"]), int(info["legal"]) + 1)) in t1
         and "rc=1" in t1, t1.strip())
    ng2 = "neg-gate-%s-stones6.txt" % name
    t2 = (OUT / ng2).read_text()
    gate("C4_ng2_%s_stones6_gate_fail" % name,
         "GATE_FAIL" in t2 and "stone count mismatch: bits=5 declared=6" in t2 and "rc=1" in t2,
         t2.strip())
    batch[name] = {
        "key": "%s:%s" % (info["lo"], info["hi"]),
        "legal": int(info["legal"]),
        "third_impl_verdict": int(info["result"]),
        "third_impl_expansions": int(info["expansions"]),
        "third_impl_tt_hits": int(info["ttHits"]),
        "third_impl_runs": info["nruns"],
        "replica_verdict": int(info["rep_result"]),
        "replica_resolution_nodes": int(info["rep_nodes"]),
        "replica_stage": info["stage"],
        "verdict_level_agreement": all(c[5] == str(info["rep_result"]) for c in tr),
        "determinism_identical": len(uniq) == 1,
    }

# ---- C1 calibration reuse (same host-session as the k06/k07/k08 addendum; the
# calibration raws were published with that addendum and are honestly reused here
# per the k04-addendum precedent; declared before any batch run) ----
vt = (OUT / "calib-verify-tbl-k06k07k08.txt").read_text()
gate("C1_verify_tbl_quads_equality",
     "replica quads 95670 mine quads 95670" in vt and "triples checked 195044 mismatches 0" in vt and "rc=0" in vt,
     vt.strip())
anch1 = parse_row(OUT / "calib-anchor-w2-k06k07k08.txt").split(",")
anch2 = parse_row(OUT / "calib-anchor-w2-run2-k06k07k08.txt").split(",")
gate("C1_anchor_w2_published_witness",
     anch1[5] == "1" and anch1[6] == "7583990" and "rc=0" in (OUT / "calib-anchor-w2-k06k07k08.txt").read_text(),
     " | ".join(anch1))
gate("C1_anchor_w2_run2_identical", (anch2[5], anch2[6]) == (anch1[5], anch1[6])
     and "rc=0" in (OUT / "calib-anchor-w2-run2-k06k07k08.txt").read_text(),
     " | ".join(anch2))

# ---- batch-level cross-row gates ----
gate("batch_30_loss_verdict_level_agreement",
     sum(1 for v in batch.values() if v["replica_verdict"] == 2 and v["third_impl_verdict"] == 2) == 30,
     str({k: v["third_impl_verdict"] for k, v in batch.items() if v["replica_verdict"] == 2}))
gate("batch_2_win_verdict_level_agreement",
     sorted(k for k, v in batch.items() if v["replica_verdict"] == 1 and v["third_impl_verdict"] == 1) == ["k13", "k19"],
     str({k: v["third_impl_verdict"] for k, v in batch.items() if v["replica_verdict"] == 1}))
gate("batch_parked_k20_k33_k38_absent",
     not any(k in batch for k in ("k20", "k33", "k38")),
     "parked keys have no new verdict in this batch")

summary = {
    "schema": "n11-sixthcost-k09k43-thirdimpl-batch-audit-v2",
    "all_pass": all(g["pass"] for g in gates.values()),
    "gates": gates,
    "row_results": batch,
    "rows_audited": len(batch),
    "rows_expected": 32,
    "consumed": False,
    "claim": ("verdict-level agreement only; no verdict consumed; the 11x11 empty board, "
              "the two-stone root {60,27} and its remaining third moves {100,108} remain "
              "UNKNOWN; k20/k33/k38 stay parked with no new verdict"),
}
print(json.dumps(summary, indent=1, sort_keys=True))
sys.exit(0 if summary["all_pass"] and summary["rows_audited"] == 32 else 1)
