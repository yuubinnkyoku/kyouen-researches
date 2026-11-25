"""
n11 class2-lane pre-sweep census v19 (head 1473, 2026-11-18).

What changed since census v18 (published as
class2-lane-next-target-presweep-1473-v18-20261118.json, git blob
11306824f2363d5002559d4d1535d91a61509929, commit b1ba66fd):

  * the cost-82d sweep COMPLETED with 0 WIN7-D10 / 82 REFUTED-D10 /
    0 capped over the 82 legal bits of the census v18 rank-1 child
    00000000020000003800000080000800 (127,619,232 candidate nodes;
    raw audit git blob 14a44c8b; claim v2 git blob cffeda69,
    commit 775277b5); this is the EIGHTH fully refuted swept row
    of the presweep-1473 band (after cost-74i, cost-75f, cost-79d,
    cost-79e, cost-80e, cost-80f and cost-81) and the band name is
    cost82d (cost82, cost82b and cost82c are already used by
    earlier bands), so no WIN7-D10 certificate exists for this row
    and the receipt fold is not needed;
  * this v19 adds the completed 82d verdict map to the twenty-one
    v18 maps (twenty-two maps total: 64h / 76c / 66i / 66j / 69j /
    64a / 71e / 72d / 73i / 73j / 73k / 73l / 74i / 75f / 78c /
    79c / 79d / 79e / 80e / 80f / 81 / 82d), marks the 82d row
    swept (fully refuted, no certificates, no receipt fold) and
    re-ranks the remaining unswept/unclaimed/unexcluded rows at
    the unchanged head 1473/174/6375/504596/4648/368510.

Method: v18 is the authoritative overlay state (rebuilt 79-source
harvest, twenty-one verdict maps, exclusions). This v19 rebuilds
the full pre-64h harvest canon map from the 79 blob-pinned sources
recorded in the v1 census harvest.files list, re-derives all
twenty-two verdict maps, giving exact per-bit classification, and
independently re-audits the twelve cost-82d raw batch files (pilot
controls, per-bit verdicts, node sums, andclose, capped, root
canons, det/v15 agreements) against the published audit JSON. It
then recomputes all 39 family rows bit-exactly, reproducing the
published v18 counts (v1 harvested hits, twenty-one-map newly
covered, open_v19 = open_v18 - newly covered by the 82d map
only). It marks the 82d row swept (fully refuted at audit
strength), re-ranks the remaining unswept/unclaimed/unexcluded
rows at the unchanged head 1473, and selects the census v18
runner-up 00000000020000003800000090000000 (cost 82) as the next
sweep target.

Checks (all asserted in this script):

  * harvest rebuild: 79 sources, 3,548 distinct verdict canons
    (353 WIN7-D10 / 3,195 REFUTED-D10), 0 conflicts, matching the
    v1 census counts bit-exactly;
  * 82d: audit counts {win7_d10: 0, refuted_d10: 82, capped: 0},
    raw-batch re-audit 82/82 per-bit verdicts + 9x3402 pilot
    controls + node sum 127,619,232 agree with the audit JSON,
    claim v2 actual_execution counts agree, confirmation 17/17
    REFUTED-D10 with root canons matching the census v18 transfer
    canons, det1/det8 re-runs field-identical, v15 cross-engine
    17/17;
  * twenty-two-map canon construction: win bits are legal bits,
    refuted = legal - win (0 capped), zero internal cross-map
    conflicts;
  * rebuilt-harvest vs twenty-two-map conflict scan: 0 verdict
    conflicts;
  * every fully swept child resolves to 0 open
    (64h/76c/66i/66j/69j/64a/71e/72d/73i/73j/73k/73l/74i/75f/78c/
    79c/79d/79e/80e/80f/81/82d);
  * the v18 ranking minus the swept 82d row is exactly the v19
    ranking: the entire remaining unswept pool is now 8 rows,
    all children of the single family parent
    00000000020000003800000080000000;
  * selected target is the cheapest remaining unswept/unclaimed/
    unexcluded row (cost 82), recorded together with its runner-up.

Search-plan bookkeeping only. No engine search is run here, no
verdict is created, no row is closed by this census itself (the 82d
row is closed at audit strength by its published sweep +
independent audit; the 11x11 empty board and all classes remain
UNKNOWN).
"""


import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
SCRIPTS = HERE / "scripts"
OUT = HERE / "output"
sys.path.insert(0, str(SCRIPTS))
from legal_candidates import legal_candidates  # noqa: E402


def git_blob_sha(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def load_out(name, pin):
    b = (OUT / name).read_bytes()
    got = git_blob_sha(b)
    assert got == pin, (name, got, pin)
    return json.loads(b)


# ------------------------------------------------------------------ D4 canon
def images(mask):
    result = [0] * 8
    for p in range(121):
        if mask >> p & 1:
            x, y = p % 11, p // 11
            coords = ((x, y), (y, 10 - x), (10 - x, 10 - y), (10 - y, x),
                      (10 - x, y), (x, 10 - y), (y, x), (10 - y, 10 - x))
            for i, (a, b) in enumerate(coords):
                result[i] |= 1 << (11 * b + a)
    return result


IMG = [images(1 << p) for p in range(121)]


def canon(mask):
    best = None
    for r in range(8):
        v = 0
        for p in range(121):
            if mask >> p & 1:
                v |= IMG[p][r]
        if best is None or v < best:
            best = v
    return best


# ------------------------------------------------------------------ inputs
V1 = load_out("class2-lane-next-target-presweep-1452-20261116.json",
              "0d9a94a272de9fe45708757f17bfea60239a3c9b")
V4 = load_out("class2-lane-next-target-presweep-1472-v4-20261117.json",
              "d70eae093e80d19660eae314bd761c21085995bb")
V6 = load_out("class2-lane-next-target-presweep-1472-v6-20261117.json",
              "c45fc0d118b7222f1e0c5d79227adc3f7ab9d1cb")
AUD69J = load_out("class2-lane-cost69j-raw-audit-20261117.json",
                  "2f6bba29ee388bdf1211400ce5599f0ba24d03e1")
CLAIM69J = load_out("class2-lane-cost69j-inflight-20261117.json",
                    "a87dcb727a2d29a34be244d2713cb21f36f85442")
MAN69J = load_out("class2-lane-cost69j-win7-certificates-20261117.json",
                  "5e8e72faa1175ffa364849d8d90b73813406fa61")
RECHECK64A = load_out(
    "class2-lane-cost64a-v17-full-row-recheck-20261117.json",
    "0afa4d28d57224544bcc3b9e8c162af205222507")
AUD71E = load_out("class2-lane-cost71e-raw-sweep-audit-20261117.json",
                  "9f56bdb74a71ef5a647432409ffd76928702870a")
CLAIM71E = load_out("class2-lane-cost71e-inflight-20261117.json",
                    "3ca1c69864f5c3d63b48ea6d96bc21f45ba06299")
AUD72D = load_out("class2-lane-cost72d-raw-sweep-audit-20261117.json",
                  "6247569a7dca86053943701a3ae099e704e0cb31")
CLAIM72D = load_out("class2-lane-cost72d-inflight-20261117.json",
                    "c64e28fdc91ba9ffaa3518dfbc9d764ec5663b05")
AUD73I = load_out("class2-lane-cost73i-raw-sweep-audit-20261117.json",
                  "33c8c6bb2b81301354e8b796f5a4751fb52aba3b")
CLAIM73I = load_out("class2-lane-cost73i-inflight-20261117.json",
                    "4a6a17e66fc1a1bfe8efb7dc6fb2400b9af6aa1d")
AUD73J = load_out("class2-lane-cost73j-raw-sweep-audit-20261117.json",
                  "4c13cbb2008c6439a95bd0818af0d09ee465484e")
CLAIM73J = load_out("class2-lane-cost73j-inflight-20261117.json",
                    "74fc3417391e30cf4cff9c2ffce059dce529ed86")
MAN73J = load_out(
    "class2-lane-cost73j-certificates/"
    "class2-lane-cost73j-win7-certificates-20261117.json",
    "e88710b5a2d4848be77a03ae5104e46aefc1279a")
V7 = load_out("class2-lane-next-target-presweep-1472-v7-20261117.json",
              "68246f3263fe6cbb49ffafa866f73b49cf3c2ebb")
FOLD76C = load_out(
    "class-frontier-cost76c-receipts-recompute-20261117.json",
    "953beaea054989e8b1de33f48b1f2ebc13ae7e11")
AUD73K = load_out("class2-lane-cost73k-raw-sweep-audit-20261117.json",
                  "85f4f73fa061c02612f5d24320d668e12468ca4e")
CLAIM73K = load_out("class2-lane-cost73k-inflight-20261117.json",
                    "7f654548efeeab47975bdafefa6bcfab3f0ba945")
MAN73K = load_out(
    "class2-lane-cost73k-certificates/"
    "class2-lane-cost73k-win7-certificates-20261117.json",
    "0892aed07d187ae2fb3b4b90a21c7adbc1002b62")
V8 = load_out("class2-lane-next-target-presweep-1473-v8-20261117.json",
              "2542914e02db14a8426a1a16ef1c2cfcd9817375")
AUD73L = load_out("class2-lane-cost73l-raw-sweep-audit-20261117.json",
                  "f2ea204413b31405b9e0f54a6a3d76205ca749b9")
CLAIM73L = load_out("class2-lane-cost73l-inflight-20261117.json",
                    "39cf0f9b31a28ad6358f157e2433477ab0659243")
MAN73L = load_out(
    "class2-lane-cost73l-certificates/"
    "class2-lane-cost73l-win7-certificates-20261117.json",
    "6e0a94aba212ba54bb5329fbea4643c9dcdb1ec4")
V9 = load_out("class2-lane-next-target-presweep-1473-v9-20261117.json",
              "af1d609490472b916eb6991e7864be98af60e9b9")
AUD74I = load_out("class2-lane-cost74i-raw-sweep-audit-20261117.json",
                  "e5c803ed6dbbfcf2398b75d2406089805dff5770")
CLAIM74I = load_out("class2-lane-cost74i-inflight-20261117.json",
                    "d915e1205f658d8297a444ef5fef6b7944397bf8")
V10 = load_out("class2-lane-next-target-presweep-1473-v10-20261117.json",
               "fc2509f0bfa49359a3053289a9af1244cafcd950")
AUD75F = load_out("class2-lane-cost75f-raw-sweep-audit-20261117.json",
                  "0951327a4b346af20ffc3c7065b96af82c531ce9")
CLAIM75F = load_out("class2-lane-cost75f-inflight-20261117.json",
                    "6df1e54d1fc7253a048ee4a7d8d0073d8bcf5e05")
BIGINT73L = load_out(
    "class2-lane-cost73l-certificates-bigint-independent-"
    "reverification-20261117.json",
    "547fe617abc179ff47f3607079d3ca8c1de4359b")
V11 = load_out("class2-lane-next-target-presweep-1473-v11-20261117.json",
               "1e2b6a2b688db1a93098edea62b5793b54efaaba")
AUD78C = load_out("class2-lane-cost78c-raw-sweep-audit-20261117.json",
                  "8e3ee7aa1827ae70b099d6a7c34d122f944b2fa3")
CLAIM78C = load_out("class2-lane-cost78c-inflight-20261117.json",
                    "1850832186ba9c8715624094f05d67aa4eb10f0b")
AUD78C16 = load_out(
    "class2-lane-cost78c-raw-batches-1-6-audit-20261118.json",
    "7460b42bb8846ad6e5e3249b3a78d39aa3e94ffa")
MAN78C = load_out(
    "class2-lane-cost78c-certificates/"
    "class2-lane-cost78c-win7-certificates-20261117.json",
    "b7fe519e923c6170e836f71e3f084f73219319d5")
V12 = load_out("class2-lane-next-target-presweep-1473-v12-20261118.json",
               "8e64d55250242a557c954ad5bad8c993bacd354b")
AUD79C = load_out("class2-lane-cost79c-raw-batches-1-9-audit-20261118.json",
                  "133f223040f62eb3edd9bc2dcfbc400c05a1cef5")
CLAIM79C = load_out("class2-lane-cost79c-inflight-20261118.json",
                    "ca517b73ffe287def7bf2c215fa4c38a6d15838a")
MAN79C = load_out(
    "class2-lane-cost79c-certificates/"
    "class2-lane-cost79c-win7-certificates-20261118.json",
    "e904a37665fb77c971ce7f9c64a3c4aa9109da4d")
BIGINT79C = load_out(
    "class2-lane-cost79c-bigint-third-impl-verify-20261118.json",
    "ed8ec44dad28a5f8811f7b33bc68cc9a5c438a97")
DET79C = load_out(
    "class2-lane-cost79c-certificates/det-reextraction.json",
    "9e415e70924b31b4b8c284b411d04b8c848a4045")
AUD79C3RD = load_out(
    "class2-lane-cost79c-certificates-third-independent-audit-20261118.json",
    "50190347cbc31fa80bf24f9545466c0f3ad9d6f3")

V13 = load_out("class2-lane-next-target-presweep-1473-v13-20261118.json",
               "fdb94e31ed2fd83ba8104f65c4f55dd2726c3bd8")
AUD79D = load_out("class2-lane-cost79d-raw-batches-1-9-audit-20261118.json",
                  "cfc6fbe390ecf326d1d9bab49b8595e2dca96aa7")
CLAIM79D = load_out("class2-lane-cost79d-inflight-20261118.json",
                    "8805876f730413dc60103d61d9c4c72b535ff7f9")
AUD79C3RDB = load_out(
    "class2-lane-cost79c-certificates-third-independent-audit-"
    "remaining16-20261118.json",
    "410fb935f855881b5b5e9992b75436483d1b3ef1")

V14 = load_out("class2-lane-next-target-presweep-1473-v14-20261118.json",
               "628e6d4e988ab50bc46e7f90bd4bd3c8c62830b1")
AUD79E = load_out("class2-lane-cost79e-raw-batches-1-9-audit-20261118.json",
                  "4e10e4771fd4a093ff62c3fda895d1462493d96e")
CLAIM79E = load_out("class2-lane-cost79e-inflight-20261118.json",
                    "f80e6025b8026c8c756c97bb62bd1b4af604c281")
V15 = load_out("class2-lane-next-target-presweep-1473-v15-20261118.json",
               "dfb61db5bec195f3f98442815753ba88d9e96fff")
AUD80E = load_out("class2-lane-cost80e-raw-batches-1-9-audit-20261118.json",
                  "53007edc9ddd4b14000da89381c9aed6a321cd17")
CLAIM80E = load_out("class2-lane-cost80e-inflight-20261118.json",
                    "9190341ad5a0abd627bd5102c9a66c94ae816ee1")
V16 = load_out("class2-lane-next-target-presweep-1473-v16-20261118.json",
               "972434a4ca5df21174dc1034ac35d118fca37fc1")
AUD80F = load_out("class2-lane-cost80f-raw-batches-1-9-audit-20261118.json",
                  "52abb7216916c4c54292613d3f0c9dd0737014e8")
CLAIM80F = load_out("class2-lane-cost80f-inflight-20261118.json",
                    "aed40c101f62e81c93dc59f3afbe65ef1cd2d61b")
V17 = load_out("class2-lane-next-target-presweep-1473-v17-20261118.json",
               "22078142d6d616335bc1bc363065d91750b6ca14")
AUD81 = load_out("class2-lane-cost81-raw-batches-1-9-audit-20261118.json",
                 "f90bdccdc25e2f11cbb3af1b152318d994e5761a")
CLAIM81 = load_out("class2-lane-cost81-inflight-20261118.json",
                   "5dc331070094343d803fe9d1e1b1222ea4e60b73")
V18 = load_out("class2-lane-next-target-presweep-1473-v18-20261118.json",
               "11306824f2363d5002559d4d1535d91a61509929")
AUD82D = load_out("class2-lane-cost82d-raw-batches-1-9-audit-20261118.json",
                  "14a44c8bce6c839d95d2e864692e272867bd0e3e")
CLAIM82D = load_out("class2-lane-cost82d-inflight-20261118.json",
                    "cffeda699c1ed0c0c9333c1b12124776f7297324")

RAW_PINS80E = {
    "class2-lane-cost80e-raw-batch1-20261118.jsonl":
        "ddce56771bf8394788c097dcccdd572c7452f982",
    "class2-lane-cost80e-raw-batch2-20261118.jsonl":
        "a8166a03485db4dd2326b43787ea90e98e6a53de",
    "class2-lane-cost80e-raw-batch3-20261118.jsonl":
        "ecf972129a8c1e8fdd0b685ebba5682aba581263",
    "class2-lane-cost80e-raw-batch4-20261118.jsonl":
        "d74929c8ef19f463419eaf44a086b27c8f4df38b",
    "class2-lane-cost80e-raw-batch5-20261118.jsonl":
        "cad89e0ba591721bf70a7f34d4c7a947017553e1",
    "class2-lane-cost80e-raw-batch6-20261118.jsonl":
        "a7ab7a2f3d1d2aa34b35825d8d27d7392819327b",
    "class2-lane-cost80e-raw-batch7-20261118.jsonl":
        "fafbc3f9a9f48858b8e56316c710e5244c690946",
    "class2-lane-cost80e-raw-batch8-20261118.jsonl":
        "6bd3dced7ca84b669a86574116daac0636957141",
    "class2-lane-cost80e-raw-batch9-confirmation-20261118.jsonl":
        "e5cea01a3eaa6097ffafddaa7c55cbbb689f041c",
    "class2-lane-cost80e-det-batch1-20261118.jsonl":
        "845a3ae1e093b9912e5a5f98e06f54c036669cd6",
    "class2-lane-cost80e-det-batch8-20261118.jsonl":
        "3549e2eadd79558f7423ba73c7e670149080af35",
    "class2-lane-cost80e-v15-crosscheck-a-20261118.jsonl":
        "e5ece4028d44890432d98e633174db5a032aac1e",
}

RAW_PINS80F = {
    "class2-lane-cost80f-raw-batch1-20261118.jsonl":
        "ad1052f5bf45fc994414a2d68d65593835120769",
    "class2-lane-cost80f-raw-batch2-20261118.jsonl":
        "8a45de5ce7a93d7d24f0d87ddb5ab7e3351b83aa",
    "class2-lane-cost80f-raw-batch3-20261118.jsonl":
        "87397fe8f14496656c05a4986493b39ef6b1ba46",
    "class2-lane-cost80f-raw-batch4-20261118.jsonl":
        "b9245607d35c5fd58c849dff59b4964fe8be182e",
    "class2-lane-cost80f-raw-batch5-20261118.jsonl":
        "f704ea0fa7821bbf165e8eea7b201dd91da3eaf2",
    "class2-lane-cost80f-raw-batch6-20261118.jsonl":
        "df198dbdca193e2871830ac5b67bef8843609662",
    "class2-lane-cost80f-raw-batch7-20261118.jsonl":
        "357bcb974f336a66a997be26d47fb4d2540302e5",
    "class2-lane-cost80f-raw-batch8-20261118.jsonl":
        "47593d298ff93a8bbc89d52e98d61772df449dfd",
    "class2-lane-cost80f-raw-batch9-confirmation-20261118.jsonl":
        "75d6ac5b8fbf1a9310966d30a999779bba500b32",
    "class2-lane-cost80f-det-batch1-20261118.jsonl":
        "978d465739290bf11fc55cae51de9f70f1e8bda9",
    "class2-lane-cost80f-det-batch8-20261118.jsonl":
        "d5f0e4f5cdac9e07f12810827204361b8b443f68",
    "class2-lane-cost80f-v15-crosscheck-a-20261118.jsonl":
        "834d0d4af14e3d29182920607d3ee669a835b824",
}

RAW_PINS81 = {
    "class2-lane-cost81-raw-batch1-20261118.jsonl":
        "de9b0820371c00340bd9f652168563acfd24ea3f",
    "class2-lane-cost81-raw-batch2-20261118.jsonl":
        "f2650a2a767df12f5db2b69c03d93900f086abb8",
    "class2-lane-cost81-raw-batch3-20261118.jsonl":
        "7cd92c1e5a38a9a6ea45f0dcfcff7c8e5a99467d",
    "class2-lane-cost81-raw-batch4-20261118.jsonl":
        "8ef37f89a268c522c8f957098e9366b3a80a76f3",
    "class2-lane-cost81-raw-batch5-20261118.jsonl":
        "6391794c1ab54794fb6b0de7cd70aa1f194d4938",
    "class2-lane-cost81-raw-batch6-20261118.jsonl":
        "afbae8f0d1d46a9b4e0ea4355320c8cb58ac98a4",
    "class2-lane-cost81-raw-batch7-20261118.jsonl":
        "4f2a413142ee11b54ad90d9f0fbc5784f672916c",
    "class2-lane-cost81-raw-batch8-20261118.jsonl":
        "8e515436a3db86baa46f819eba78cde3aba20e8f",
    "class2-lane-cost81-raw-batch9-confirmation-20261118.jsonl":
        "a1700d71e02f66c2a61c07350fe1229ce9f2317a",
    "class2-lane-cost81-det-batch1-20261118.jsonl":
        "bb3f35d6220a69a4d3b3b30b6358c0123a1eb3d8",
    "class2-lane-cost81-det-batch8-20261118.jsonl":
        "18e71d316e9372c69b846126411a1280f63297e4",
    "class2-lane-cost81-v15-crosscheck-a-20261118.jsonl":
        "f42e202a83c81e088ba5e503ab4c7747dc6fe508",
}

RAW_PINS82D = {
    "class2-lane-cost82d-raw-batch1-20261118.jsonl":
        "d4003c6bb32e49f197c74fe0045454634721746b",
    "class2-lane-cost82d-raw-batch2-20261118.jsonl":
        "308b7cea6959c557301f52174c184c7fe6348159",
    "class2-lane-cost82d-raw-batch3-20261118.jsonl":
        "ef8be054c710a4e0751ef24a5bbad15ef17e3fab",
    "class2-lane-cost82d-raw-batch4-20261118.jsonl":
        "d7033f793680f630a6fdbc3d62e2f6a652bfe6a7",
    "class2-lane-cost82d-raw-batch5-20261118.jsonl":
        "de314628adccf5f389f99f4e9e6688d2b7466333",
    "class2-lane-cost82d-raw-batch6-20261118.jsonl":
        "694735d00c50e4dc2c028620e82934366d6615c6",
    "class2-lane-cost82d-raw-batch7-20261118.jsonl":
        "bb5d68883e2c40589aff4705a410b208672a41c4",
    "class2-lane-cost82d-raw-batch8-20261118.jsonl":
        "75eb4ecad8276d6a39092c87679f14eb0473a380",
    "class2-lane-cost82d-raw-batch9-confirmation-20261118.jsonl":
        "3a16f81c80630de5a759a2b8b92a5748b514da29",
    "class2-lane-cost82d-det-batch1-20261118.jsonl":
        "83b49a0f2b7a92d8ef262e27ee817a7a52013460",
    "class2-lane-cost82d-det-batch8-20261118.jsonl":
        "77068322719ac78b41fbadd3a506243265a2708e",
    "class2-lane-cost82d-v15-crosscheck-a-20261118.jsonl":
        "6c8a273add8eecd43a20c76a635b6ac5c03a37c1",
}

RAW_PINS79E = {
    "class2-lane-cost79e-raw-batch1-20261118.jsonl":
        "f9a0afecb643bd0109891587596e56872853cb66",
    "class2-lane-cost79e-raw-batch2-20261118.jsonl":
        "4a4c31848f27ab7d045ef08f596e057716e3a149",
    "class2-lane-cost79e-raw-batch3-20261118.jsonl":
        "304eef2e690c4e3a7d6b6960b01918e329d5c1af",
    "class2-lane-cost79e-raw-batch4-20261118.jsonl":
        "7c46e966e02a7ff8012a530535b1ba5d8888d881",
    "class2-lane-cost79e-raw-batch5-20261118.jsonl":
        "3acb125186c30c1072122ca856e40f793752e910",
    "class2-lane-cost79e-raw-batch6-20261118.jsonl":
        "c09e40f474647bf8be2307d64a731957800f1b6d",
    "class2-lane-cost79e-raw-batch7-20261118.jsonl":
        "df039db8e630c74f5ad71d46d3540ebc15d21383",
    "class2-lane-cost79e-raw-batch8-20261118.jsonl":
        "ef3054bc153307e1ef50bc7d5458887cb33572a2",
    "class2-lane-cost79e-raw-batch9-confirmation-20261118.jsonl":
        "9db89516b504274122569e3d573db455b82e0192",
    "class2-lane-cost79e-det-batch1-20261118.jsonl":
        "9896faf39ca5242734d01824341ffc643f68e4e8",
    "class2-lane-cost79e-det-batch8-20261118.jsonl":
        "2af1a7d5e41fc9b700e26c4d82cf22217d6ee966",
    "class2-lane-cost79e-v15-crosscheck-a-20261118.jsonl":
        "67063383596ad5ba76dce9f4f6d2670f60ab8f2d",
}

RAW_PINS79D = {
    "class2-lane-cost79d-raw-batch1-20261118.jsonl":
        "b5c38bf819c35dd0a7ef68aeeca941b5b0e11878",
    "class2-lane-cost79d-raw-batch2-20261118.jsonl":
        "f0d2eb54db56b010e41e9d5ccbbd40d9ca8b8996",
    "class2-lane-cost79d-raw-batch3-20261118.jsonl":
        "b7c3ec5ef1833f9356806cd214b789f08fe58c25",
    "class2-lane-cost79d-raw-batch4-20261118.jsonl":
        "a7113edf4b0b806d9897a31bd4f05fe7f0e0d2c6",
    "class2-lane-cost79d-raw-batch5-20261118.jsonl":
        "8c948641c4b89596324b1db61a79a32588808239",
    "class2-lane-cost79d-raw-batch6-20261118.jsonl":
        "4874029942e23a61225a407d8ba5fa60b0dbd9a8",
    "class2-lane-cost79d-raw-batch7-20261118.jsonl":
        "966a4c51f2962e1cd4930a419969ca84f0295943",
    "class2-lane-cost79d-raw-batch8-20261118.jsonl":
        "5a827d2ed1482b02952a755eaa9027ce94c0c0fe",
    "class2-lane-cost79d-raw-batch9-confirmation-20261118.jsonl":
        "0524641f574e4b9c062d402009cf38d023acbe31",
    "class2-lane-cost79d-det-batch1-20261118.jsonl":
        "53e83a4f47973c57ab092dca3e552a4611c7c979",
    "class2-lane-cost79d-det-batch8-20261118.jsonl":
        "35678125be064d1c30a0606f94604cc8f94a6d0e",
    "class2-lane-cost79d-v15-crosscheck-a-20261118.jsonl":
        "733cc40a2e01fdb6f0eb6792c5d67c166e12c1ae",
}

RAW_PINS79C = {
    "class2-lane-cost79c-raw-batch1-20261118.jsonl":
        "a1fe6f77744440a5160c4bbcad47a5eeedae3f63",
    "class2-lane-cost79c-raw-batch2-20261118.jsonl":
        "f2d2da585d366ffae498e3041482beb32e4f1d79",
    "class2-lane-cost79c-raw-batch3-20261118.jsonl":
        "db291dbff4ab91228e35771189ff470195303bbd",
    "class2-lane-cost79c-raw-batch4-20261118.jsonl":
        "e90041663a5558d2595af6cbdf5dfd6e55962c08",
    "class2-lane-cost79c-raw-batch5-20261118.jsonl":
        "1a96f6ec0e586e979f75aad2375fcd4c925e6e41",
    "class2-lane-cost79c-raw-batch6-20261118.jsonl":
        "dd0e4b04a071c9ce5a77d8de3e28b042f4360761",
    "class2-lane-cost79c-raw-batch7-20261118.jsonl":
        "0f99b338756dcabe67dbd96fb1c34859e5163c5f",
    "class2-lane-cost79c-raw-batch8-20261118.jsonl":
        "533c4ea6933bca54e4d3cd927d8a46552246f873",
    "class2-lane-cost79c-raw-batch9-confirmation-20261118.jsonl":
        "776b0f42a7e7cbbe268020ad9e45016b940c8efc",
}

RAW_PINS = {
    "class2-lane-cost76d-raw-batch1-20261116.jsonl":
        "d3c9ae3690c7c74e2b85fb4a84e0b02bb0ee06fb",
    "class2-lane-cost77e-raw-batch1-20261116.jsonl":
        "2034e39709d598827d912074b15dc6a61df2d5ad",
    "class2-lane-cost76d-raw-batch2-20261116.jsonl":
        "9144839aefc28cf4fd78710b1c130c0a0fe80f16",
    "class2-lane-cost77e-raw-batch2-20261116.jsonl":
        "cb883d07206e0f5ff4935ff4d36bbbf4addb7202",
    "class2-lane-cost76d-raw-batch3-20261116.jsonl":
        "8dae0d02ceea0b80ba1ecb0f853778b7dc158c23",
    "class2-lane-cost77e-raw-batch3-20261116.jsonl":
        "a64d7a19456c11f79e473f9df08c785007867d75",
    "class2-lane-cost76d-raw-batch4-20261116.jsonl":
        "3c1e4557b97cc7f5cb2eb51cb79a9b02254ff11f",
    "class2-lane-cost77e-raw-batch4-20261116.jsonl":
        "32d9d9582a848c0e65e91c56dfdab40de2fa74ee",
    "class2-lane-cost76d-raw-batch5-20261116.jsonl":
        "c0c152d58a16aa9377ef8f365508699e32c71c94",
    "class2-lane-cost77e-raw-batch5-20261116.jsonl":
        "489f13e374f267fbc0a3a798e631e4fb543b4fc7",
    "class2-lane-cost76d-raw-batch6-20261116.jsonl":
        "dbf10a3064c52472fddfc204fa4f0c00eaf6772e",
    "class2-lane-cost77e-raw-batch6-20261116.jsonl":
        "5846d0470e43dc2ce49cecace0e6d628ff795765",
    "class2-lane-cost76d-raw-batch7-20261116.jsonl":
        "57c0eda0ffd3023ef44862c83c2eb547c7e4c584",
    "class2-lane-cost77e-raw-batch7-20261116.jsonl":
        "106ac2387f7d302dfcc5963abf26ca20174ec2bb",
    "class2-lane-cost76d-raw-batch8-20261116.jsonl":
        "f4862407930d5658987dc4bc1fe9766c204ecf0e",
    "class2-lane-cost77e-raw-batch8-20261116.jsonl":
        "3956be4dcc89009f07fd6e6ddb1eba8d186a8b54",
    "class2-lane-cost76d-raw-batch9-20261116.jsonl":
        "bc32bed989265468841bb076ccfa6328e94514e3",
    "class2-lane-cost77e-raw-batch9-20261116.jsonl":
        "59df74f2902e8b45dadcef9ee451c27fbe3ff953",
    "class2-lane-cost76d-raw-batch10-20261116.jsonl":
        "8855f2d6f3821c1cd7d7e33eed6d17a63ecac3ee",
    "class2-lane-cost77e-raw-batch10-20261116.jsonl":
        "d9f4fa3c5aa85fe9e408f45a88396d1edcb535c2",
}


def find_key(obj, names, depth=0):
    for n in names:
        if n in obj:
            return obj[n]
    if depth < 1:
        for k, v in obj.items():
            if k == "fold":
                continue          # fold.win_bits mixes two lanes' bits
            if isinstance(v, dict):
                r = find_key(v, names, depth + 1)
                if r is not None:
                    return r
    return None


# ------------------------------------------- 1. rebuild the v1 harvest corpus
harvest = {}
harvest_sources = 0
glob_files = 0
for entry in V1["harvest"]["files"]:
    name = entry["file"]
    if "raw-batch" in name:
        continue                  # ingested separately below
    b = (OUT / name).read_bytes()
    assert git_blob_sha(b) == entry["git_blob_sha"], name
    glob_files += 1
    d = json.loads(b)
    child = None
    for key in ("s6_child_hex", "s6_child", "child"):
        v = d.get(key)
        if isinstance(v, str) and len(v) == 32:
            child = v
            break
    assert child is not None and child == entry["child"], name
    win_bits = find_key(d, ("win7_bits", "win7_d10_bits", "win_bits"))
    assert win_bits is not None, name
    if isinstance(win_bits, dict):
        win_bits = [bb for v in win_bits.values() for bb in v]
    win_bits = sorted(set(int(bb) for bb in win_bits))
    # candidate list: file's own if present, else the enumeration
    cands = None
    for key in ("legal_candidates", "candidate_bits", "candidates"):
        v = d.get(key)
        if isinstance(v, list) and v and isinstance(v[0], int):
            cands = v
            break
    enum = sorted(legal_candidates(child)[1])
    if cands is None:
        cands = enum
    else:
        cands = sorted(set(int(bb) for bb in cands))
    assert cands == enum, name
    assert len(cands) == entry["candidates"], name
    assert len(win_bits) == entry["win7"], name
    capped_bits = find_key(d, ("capped_bits",))
    capped_n = find_key(d, ("capped", "capped_count"))
    if isinstance(capped_bits, dict):
        capped_bits = [bb for v in capped_bits.values() for bb in v]
    capped_bits = sorted(set(int(bb) for bb in capped_bits)) \
        if capped_bits else []
    assert capped_n in (None, 0, False, len(capped_bits)) \
        and not capped_bits, name
    ref_bits = find_key(d, ("refuted_d10_bits", "refuted_bits"))
    if ref_bits is not None and not isinstance(ref_bits, list):
        ref_bits = None
    if ref_bits is None:
        ref_bits = sorted(set(cands) - set(win_bits) - set(capped_bits))
    elif isinstance(ref_bits, dict):
        ref_bits = [bb for v in ref_bits.values() for bb in v]
    else:
        ref_bits = sorted(set(int(bb) for bb in ref_bits))
    assert len(ref_bits) == entry["refuted"], name
    assert not (set(win_bits) & set(ref_bits))
    assert set(win_bits) | set(ref_bits) == set(cands), name
    child_v = int(child, 16)
    for b_ in win_bits:
        c = canon(child_v | (1 << b_))
        e = harvest.get(c)
        assert e is None or e["verdict"] == "WIN7-D10", (name, b_)
        harvest[c] = {"verdict": "WIN7-D10",
                      "sources": (e["sources"] if e else []) + [name]}
    for b_ in ref_bits:
        c = canon(child_v | (1 << b_))
        e = harvest.get(c)
        assert e is None or e["verdict"] == "REFUTED-D10", (name, b_)
        harvest[c] = {"verdict": "REFUTED-D10",
                      "sources": (e["sources"] if e else []) + [name]}
    harvest_sources += 1

# 76d / 77e raw batches (canonical bit-level records)
for prefix, ncand, win_bits, child in (
        ("cost76d", 76, [19, 49],
         "00000000040000003800080008000000"),
        ("cost77e", 77, [37, 69],
         "00000000040000809002000000004000")):
    bit_recs = {}
    n_control = 0
    for n in range(1, 11):
        fname = f"class2-lane-{prefix}-raw-batch{n}-20261116.jsonl"
        b = (OUT / fname).read_bytes()
        assert git_blob_sha(b) == RAW_PINS[fname], fname
        for line in b.decode().splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            if "control" in r:
                n_control += 1
                assert r["loss"] is False and r["capped"] is False
                assert r["nodes"] == 3402, r
            else:
                assert r["bit"] not in bit_recs
                assert r["andclose"] is True and r["capped"] is False
                bit_recs[r["bit"]] = r
    assert n_control == 10, prefix
    assert len(bit_recs) == ncand, prefix
    assert sorted(bit_recs) == sorted(legal_candidates(child)[1]), prefix
    raw_win = sorted(bb for bb, r in bit_recs.items() if r["loss"] is True)
    assert raw_win == win_bits, (prefix, raw_win)
    child_v = int(child, 16)
    for bb, r in bit_recs.items():
        c = canon(child_v | (1 << bb))
        expect = "WIN7-D10" if r["loss"] is True else "REFUTED-D10"
        e = harvest.get(c)
        assert e is None or e["verdict"] == expect, (prefix, bb, expect, e)
        harvest[c] = {"verdict": expect,
                      "sources": (e["sources"] if e else [])
                      + [f"{prefix}-raw-batches"]}
    harvest_sources += 1

harvest_n = len(harvest)
harvest_win = sum(1 for v in harvest.values()
                  if v["verdict"] == "WIN7-D10")
harvest_ref = sum(1 for v in harvest.values()
                  if v["verdict"] == "REFUTED-D10")
assert harvest_sources == 79 and glob_files == 77
assert harvest_n == V1["harvest"]["distinct_verdict_canons"] == 3548
assert harvest_win == V1["harvest"]["win7_d10"] == 353
assert harvest_ref == V1["harvest"]["refuted_d10"] == 3195
print(f"rebuilt harvest: {harvest_sources} sources, {harvest_n} canons, "
      f"win {harvest_win} / refuted {harvest_ref}")

# ------------------------------------------- 2. the fifteen verdict maps
VM4 = V4["new_verdict_maps"]
AUD69J_WIN = AUD69J["verdicts"]["win7_d10_bits"]
AUD69J_REF = AUD69J["verdicts"]["refuted_d10_bits"]
assert AUD69J["verdicts"]["capped_count"] == 0
assert sorted(AUD69J_WIN) == [1, 52, 75, 109, 110, 114]
assert CLAIM69J["status"].startswith("claim v2: sweep complete")
ex = CLAIM69J.get("actual_execution") or {}
claim_win = ((ex.get("results") or {}).get("win7_d10_bits")
             or find_key(CLAIM69J,
                         ("win7_bits", "win7_d10_bits", "win_bits")))
assert claim_win is not None
assert sorted(int(bb) for bb in claim_win) == sorted(AUD69J_WIN)
man_bits = sorted(c["bit"] for c in MAN69J["certificates"])
assert man_bits == sorted(AUD69J_WIN)
man_roots = {c["bit"]: c["root"] for c in MAN69J["certificates"]}
child69j = AUD69J["target"]["s6_child"]
assert child69j == "00000000000000403800000008000020"
for bb in AUD69J_WIN:
    root = f"{int(child69j, 16) | (1 << bb):032x}"
    assert man_roots[bb] == root, (bb, root, man_roots[bb])

RC64A = RECHECK64A["v17_recheck"]["verdicts"]
assert RC64A == {"capped": 0, "refuted_d10": 64, "win7_d10": 0}
gap = RECHECK64A["census_harvest_gap"]
assert gap["corrected_status_counts"] == {
    "harvested_refuted": 8, "open": 0, "refuted_via_cost64a_v17": 56}

# 71e / 72d / 73i sweep completion checks
def check_completed(aud, claim, claim_status_prefix, expect_win):
    win = aud["verdicts"]["win7_d10_bits"]
    ref = aud["verdicts"].get("refuted_d10_bits") \
        or aud["verdicts"].get("refuted_d10_bits_count")
    assert aud["verdicts"]["capped_count"] == 0
    assert sorted(win) == sorted(expect_win), expect_win
    child = aud["target"]["s6_child"]
    legal_n = aud["target"]["legal_candidate_count"]
    st, bits = legal_candidates(child)
    assert sorted(bits) and len(bits) == legal_n
    if isinstance(ref, list):
        assert sorted(set(ref) | set(win)) == sorted(bits)
        assert len(ref) == legal_n - len(win)
    else:
        assert ref == legal_n - len(win)
    assert claim["status"].startswith(claim_status_prefix), \
        claim["status"][:60]
    ex2 = claim.get("actual_execution") or {}
    claim_win2 = ((ex2.get("results") or {}).get("win7_d10_bits"))
    return win, child, claim_win2


AUD71E_WIN, CHILD71E, CLAIM71E_WIN = check_completed(
    AUD71E, CLAIM71E, "claim v3: certificates complete",
    [3, 4, 8, 41, 54, 58, 76, 79, 94, 96, 100, 116, 119])
assert sorted(CLAIM71E_WIN) == sorted(AUD71E_WIN)
assert CHILD71E == "00000000000000c09002000000002000"
assert CLAIM71E["certificates"]["win7_d10_bits"] == AUD71E_WIN
assert CLAIM71E["certificates"]["totals"]["rows"] == 534804

AUD72D_WIN, CHILD72D, CLAIM72D_WIN = check_completed(
    AUD72D, CLAIM72D, "claim v2: sweep and certificates complete",
    [1, 6, 24, 25, 43, 49, 75, 80, 83, 98, 114])
assert sorted(CLAIM72D_WIN) == sorted(AUD72D_WIN)
assert CHILD72D == "00000000000000403800000008004000"
assert CLAIM72D["certificates"]["win7_d10_bits"] == AUD72D_WIN
assert CLAIM72D["certificates"]["totals"]["rows"] == 522517

AUD73I_WIN, CHILD73I, _ = check_completed(
    AUD73I, CLAIM73I, "claim v1: in-flight",
    [1, 9, 11, 18, 29, 38, 54, 82, 97, 100, 110, 111])
assert CHILD73I == "00000000000000403800400008000000"
# 73i claim v1 is still in-flight: the audit is the completed record
ec73i = CLAIM73I["engine_candidate_bits"]
assert sorted(ec73i["open_bits"]) == sorted(
    set(AUD73I_WIN) | (set(ec73i["open_bits"]) - set(AUD73I_WIN)))
assert sorted(ec73i["confirmation_bits"]) == \
    AUD73I["confirmation_bits"]["bits"]
assert set(AUD73I_WIN) <= set(ec73i["open_bits"])
assert (ec73i["open_bit_count"] + ec73i["confirmation_bit_count"]
        == CLAIM73I["candidate_count"] == 73)
assert all(v == "REFUTED-D10" for v in
           AUD73I["confirmation_bits"]["verdicts"].values())
assert AUD73I["cross_source_conflict_scan"]["conflicts"] == 0

# 73j sweep completion check (16 WIN + 57 REFUTED, 0 capped)
AUD73J_WIN, CHILD73J, CLAIM73J_WIN = check_completed(
    AUD73J, CLAIM73J, "claim v3: certificates complete",
    [0, 1, 6, 29, 44, 49, 52, 69, 74, 82, 87, 91, 98, 100, 110, 118])
assert sorted(CLAIM73J_WIN) == sorted(AUD73J_WIN)
assert CHILD73J == "00000000000000403800000408000000"
assert CLAIM73J["certificates"]["win7_d10_bits"] == AUD73J_WIN
assert CLAIM73J["certificates"]["totals"]["rows"] == 726778
assert CLAIM73J["certificates"]["totals"]["extraction_nodes"] == 166238087
assert CLAIM73J["certificates"]["totals"]["published_bytes"] == 26236851
man73j_bits = sorted(c["bit"] for c in MAN73J["certificates"])
assert man73j_bits == sorted(AUD73J_WIN)
man73j_roots = {c["bit"]: c["root"] for c in MAN73J["certificates"]}
for bb in AUD73J_WIN:
    root = f"{int(CHILD73J, 16) | (1 << bb):032x}"
    assert man73j_roots[bb] == root, (bb, root, man73j_roots[bb])
assert MAN73J["totals"]["rows"] == 726778
assert MAN73J["totals"]["extraction_nodes"] == 166238087
assert MAN73J["totals"]["published_bytes"] == 26236851
assert MAN73J["totals"]["fbt_drops_total"] == 0
assert MAN73J["totals"]["capped_per_move_total"] == 0
assert sorted(AUD73J["confirmation_bits"]["bits"]) == \
    [5, 14, 20, 46, 97, 103, 108]
assert all(v == "REFUTED-D10" for v in
           AUD73J["confirmation_bits"]["verdicts"].values())
assert AUD73J["confirmation_bits"]["predicted_by_census_v6_overlay"] is True
for b_, oc in AUD73J["confirmation_bits"]["outcome"].items():
    assert oc["match"] is True, (b_, oc)
assert AUD73J["cross_source_conflict_scan"]["conflicts"] == 0
claim73j_pins = CLAIM73J["actual_execution"]["raw_batch_blob_pins"]
for k_ in ("batch1", "batch2", "batch3", "batch4", "batch5", "batch6",
           "batch7", "batch8", "batch9"):
    assert AUD73J["raw_batch_pins"][k_] == claim73j_pins[k_], k_
assert claim73j_pins["audit_json"] == \
    "4c13cbb2008c6439a95bd0818af0d09ee465484e"

# 73k sweep completion check (25 WIN + 48 REFUTED, 0 capped)
AUD73K_WIN = AUD73K["verdicts"]["win7_d10_bits"]
assert AUD73K["verdicts"]["capped_count"] == 0
assert sorted(AUD73K_WIN) == [0, 7, 11, 14, 15, 26, 35, 39, 41, 44, 55,
                              58, 62, 73, 76, 87, 89, 94, 95, 97, 98,
                              103, 105, 112, 117]
assert CLAIM73K["status"].startswith("claim v3: certificates complete")
ex73k = CLAIM73K.get("actual_execution") or {}
claim73k_win = ((ex73k.get("results") or {}).get("win7_d10_bits"))
assert claim73k_win is not None
assert sorted(int(bb) for bb in claim73k_win) == sorted(AUD73K_WIN)
CHILD73K = AUD73K["target"]["s6_child"]
assert CHILD73K == "00000000000000801206000000000400"
assert AUD73K["target"]["candidate_bits"] == 73
assert AUD73K["target"]["confirmation_bits"] == [14, 23, 26, 34, 53, 55,
                                                 107]
ec73k = CLAIM73K["engine_candidate_bits"]
assert sorted(ec73k["confirmation_bits"]) == \
    AUD73K["target"]["confirmation_bits"]
assert set(AUD73K_WIN) <= set(ec73k["open_bits"]) | set(ec73k["confirmation_bits"])
assert (ec73k["open_bit_count"] + ec73k["confirmation_bit_count"]
        == CLAIM73K["candidate_count"] == 73)
man73k_bits = sorted(c["bit"] for c in MAN73K["certificates"])
assert man73k_bits == sorted(set(AUD73K_WIN) - {14, 26, 55})
man73k_roots = {c["bit"]: c["root"] for c in MAN73K["certificates"]}
for bb in man73k_bits:
    root = f"{int(CHILD73K, 16) | (1 << bb):032x}"
    assert man73k_roots[bb] == root, (bb, root, man73k_roots[bb])
assert MAN73K["totals"]["rows"] == 966535
assert MAN73K["totals"]["extraction_nodes"] == 155946109
assert MAN73K["totals"]["published_bytes"] == 34933538
assert MAN73K["totals"]["fbt_drops_total"] == 0
assert MAN73K["totals"]["capped_per_move_total"] == 0
assert MAN73K["totals"]["certificates"] == 22
claim73k_pins = CLAIM73K["actual_execution"]["raw_batch_blob_pins"]
assert claim73k_pins["audit_json"] == \
    "85f4f73fa061c02612f5d24320d668e12468ca4e"
assert (AUD73K["verdicts"]["per_bit_identical_to_concurrent_record"]
        == "73/73 (loss, nodes, capped)")

# 73l sweep completion check (34 WIN + 39 REFUTED, 0 capped)
AUD73L_WIN = AUD73L["verdicts"]["win7_d10_bits"]
AUD73L_REF = AUD73L["verdicts"]["refuted_d10_bits"]
assert AUD73L["verdicts"]["capped_count"] == 0
assert sorted(AUD73L_WIN) == [1, 2, 3, 4, 6, 8, 9, 18, 21, 23, 25,
                              28, 29, 32, 34, 41, 42, 44, 47, 53,
                              54, 61, 62, 64, 66, 80, 95, 105, 106,
                              110, 112, 113, 116, 119]
assert len(AUD73L_WIN) == 34 and len(AUD73L_REF) == 39
assert not (set(AUD73L_WIN) & set(AUD73L_REF))
CHILD73L = AUD73L["target"]["s6_child"]
assert CHILD73L == "00000000000000c09002000000400000"
st73l, bits73l = legal_candidates(CHILD73L)
cands73l = sorted(bits73l)
assert len(cands73l) == AUD73L["target"]["candidate_bits"] == 73
assert set(AUD73L_WIN) | set(AUD73L_REF) == set(cands73l)
assert CLAIM73L["status"].startswith("claim v3: certificates complete")
ex73l = CLAIM73L["actual_execution"]["results"]
assert sorted(ex73l["win7_d10_bits"]) == sorted(AUD73L_WIN)
assert sorted(ex73l["refuted_d10_bits"]) == sorted(AUD73L_REF)
assert ex73l["refuted_d10_bits_count"] == 39
ec73l = CLAIM73L["engine_candidate_bits"]
assert sorted(ec73l["confirmation_bits"]) == \
    AUD73L["confirmation_bits"]["bits"] == [65, 86, 90, 94, 97, 106,
                                            110]
assert ec73l["open_bit_count"] == 66
assert ec73l["confirmation_bit_count"] == 7
assert (ec73l["open_bit_count"] + ec73l["confirmation_bit_count"]
        == CLAIM73L["candidate_count"] == 73)
pred73l = ec73l["confirmation_verdicts_predicted"]
assert [pred73l[str(b_)] for b_ in (65, 86, 90, 94, 97)] == \
    ["REFUTED-D10"] * 5
assert pred73l["106"] == "WIN7-D10" and pred73l["110"] == "WIN7-D10"
for b_, rec in AUD73L["confirmation_bits"]["sources"].items():
    assert rec["canon_equal"] is True and rec["raw_identical"] is False
man73l_bits = sorted(c["bit"] for c in MAN73L["certificates"])
assert man73l_bits == sorted(set(AUD73L_WIN) - {106, 110})
man73l_roots = {c["bit"]: c["root"] for c in MAN73L["certificates"]}
for bb in man73l_bits:
    root = f"{int(CHILD73L, 16) | (1 << bb):032x}"
    assert man73l_roots[bb] == root, (bb, root, man73l_roots[bb])
assert MAN73L["totals"] == {"certificates": 32, "rows": 1693203,
                            "extraction_nodes": 424657112,
                            "published_bytes": 61171191,
                            "fbt_drops_total": 0,
                            "capped_per_move_total": 0}
bs73l = BIGINT73L["summary"]
assert bs73l["records"] == 32 and bs73l["verifier_pass"] == 32
assert bs73l["verifier_fail"] == 0
assert bs73l["total_rows_independently_verified"] == 1693203
assert bs73l["total_certificate_bytes_rehashed"] == 61171191
assert bs73l["total_extraction_nodes_in_manifest"] == 424657112
assert AUD73L["v15_cross_engine_check"]["win_agreement"] == \
    "34/34 loss=true"
assert AUD73L["v15_cross_engine_check"]["capped"] == 0
assert AUD73L["determinism_rerun"]["result"] == \
    "field-identical on every non-ms field"

# 74i sweep completion check (0 WIN + 74 REFUTED, 0 capped)
AUD74I_WIN = AUD74I["verdicts"]["win7_d10_bits"]
AUD74I_REF = AUD74I["verdicts"]["refuted_d10_bits"]
assert AUD74I["verdicts"]["capped_count"] == 0
assert AUD74I_WIN == [] and len(AUD74I_REF) == 74
CHILD74I = AUD74I["target"]["s6_child"]
assert CHILD74I == "00000000020000003800000088000000"
st74i, bits74i = legal_candidates(CHILD74I)
cands74i = sorted(bits74i)
assert len(cands74i) == AUD74I["target"]["candidate_bits"] == 74
assert set(AUD74I_REF) == set(cands74i)
assert CLAIM74I["status"].startswith("claim v2: sweep COMPLETE")
ex74i = CLAIM74I["actual_execution"]["results"]
assert ex74i["win7_d10_bits"] == []
assert ex74i["refuted_d10_bits_count"] == 74
assert ex74i["capped_count"] == 0
assert ex74i["candidate_nodes_total"] == 56125895
ec74i = CLAIM74I["engine_candidate_bits"]
assert sorted(ec74i["confirmation_bits"]) == \
    AUD74I["confirmation_bits"]["bits"] == [30, 71, 72, 90, 115]
assert ec74i["open_bit_count"] == 69
assert ec74i["confirmation_bit_count"] == 5
assert (ec74i["open_bit_count"] + ec74i["confirmation_bit_count"]
        == CLAIM74I["candidate_count"] == 74)
pred74i = ec74i["confirmation_verdicts_predicted"]
assert [pred74i[str(b_)] for b_ in (30, 71, 72, 90, 115)] == \
    ["REFUTED-D10"] * 5
for b_, rec in AUD74I["confirmation_bits"]["sources"].items():
    assert rec["canon_equal"] is True
    assert rec["raw_identical"] == (b_ == "30"), (b_, rec)
assert AUD74I["v15_cross_engine_check"]["verdict_agreement"] == \
    "10/10 loss=false"
assert AUD74I["v15_cross_engine_check"]["capped"] == 0
assert AUD74I["determinism_rerun"]["result"] == \
    "field-identical on every non-ms field"
assert CLAIM74I["receipt_fold"]["status"].startswith("not needed")
assert CLAIM74I["certificates"]["status"].startswith("not applicable")
assert CLAIM74I["s5"] == "00000000020000003800000080000000"

# 75f sweep completion check (0 WIN + 75 REFUTED, 0 capped)
AUD75F_WIN = AUD75F["verdicts"]["win7_d10_bits"]
AUD75F_REF = AUD75F["verdicts"]["refuted_d10_bits"]
assert AUD75F["verdicts"]["capped_count"] == 0
assert AUD75F_WIN == [] and len(AUD75F_REF) == 75
CHILD75F = AUD75F["target"]["s6_child"]
assert CHILD75F == "00000000020000003800020080000000"
st75f, bits75f = legal_candidates(CHILD75F)
cands75f = sorted(bits75f)
assert len(cands75f) == AUD75F["target"]["candidate_bits"] == 75
assert set(AUD75F_REF) == set(cands75f)
assert CLAIM75F["status"].startswith("claim v2: sweep COMPLETE")
ex75f = CLAIM75F["actual_execution"]["results"]
assert ex75f["win7_d10_bits"] == []
assert ex75f["refuted_d10_bits_count"] == 75
assert ex75f["capped_count"] == 0
assert ex75f["candidate_nodes_total"] == 76432898
ec75f = CLAIM75F["engine_candidate_bits"]
assert sorted(ec75f["confirmation_bits"]) == \
    AUD75F["confirmation_bits"]["bits"] == [27, 90, 93, 115]
assert ec75f["open_bit_count"] == 71
assert ec75f["confirmation_bit_count"] == 4
assert (ec75f["open_bit_count"] + ec75f["confirmation_bit_count"]
        == CLAIM75F["candidate_count"] == 75)
pred75f = ec75f["confirmation_verdicts_predicted"]
assert [pred75f[str(b_)] for b_ in (27, 90, 93, 115)] == \
    ["REFUTED-D10"] * 4
for b_, rec in AUD75F["confirmation_bits"]["sources"].items():
    assert rec["canon_equal"] is True
    assert rec["raw_identical"] == (b_ == "27"), (b_, rec)
assert AUD75F["v15_cross_engine_check"]["verdict_agreement"] == \
    "9/9 loss=false"
assert AUD75F["v15_cross_engine_check"]["capped"] == 0
assert AUD75F["determinism_rerun"]["result"] == \
    "field-identical on every non-ms field"
assert CLAIM75F["receipt_fold"]["status"].startswith("not needed")
assert CLAIM75F["certificates"]["status"].startswith("not applicable")
assert CLAIM75F["s5"] == "00000000020000003800000080000000"

# 78c sweep completion check (11 WIN + 67 REFUTED, 0 capped)
AUD78C_WIN = AUD78C["verdicts"]["win7_d10_bits"]
AUD78C_REF = AUD78C["verdicts"]["refuted_d10_bits"]
assert AUD78C["verdicts"]["capped_count"] == 0
assert sorted(AUD78C_WIN) == [1, 4, 9, 30, 49, 69, 75, 79, 100, 114, 116]
assert len(AUD78C_REF) == 67
assert not (set(AUD78C_WIN) & set(AUD78C_REF))
CHILD78C = AUD78C["target"]["s6_child"]
assert CHILD78C == "00000000000000403800000008000008"
st78c, bits78c = legal_candidates(CHILD78C)
cands78c = sorted(bits78c)
assert len(cands78c) == AUD78C["target"]["candidate_bits"] == 78
assert AUD78C["target"]["open_bits"] == 66
assert set(AUD78C_WIN) | set(AUD78C_REF) == set(cands78c)
assert sorted(AUD78C["target"]["confirmation_bits"]) == \
    [5, 13, 14, 20, 34, 46, 97, 103, 108, 110, 115, 118]
assert CLAIM78C["status"].startswith(
    "claim v5: COMPLETED + CERTIFICATES PUBLISHED")
ex78c = CLAIM78C["actual_execution"]
assert sorted(ex78c["win7_d10_bits"]) == sorted(AUD78C_WIN)
assert len(ex78c["refuted_d10_bits"]) == 67
assert ex78c["capped_bits"] == []
assert ex78c["candidate_nodes"] == 238626461
ec78c = CLAIM78C["engine_candidate_bits"]
assert sorted(ec78c["confirmation_bits"]) == \
    AUD78C["target"]["confirmation_bits"]
assert ec78c["open_bit_count"] == 66
assert ec78c["confirmation_bit_count"] == 12
assert (ec78c["open_bit_count"] + ec78c["confirmation_bit_count"]
        == CLAIM78C["candidate_count"] == 78)
pred78c = ec78c["confirmation_verdicts_predicted"]
assert [pred78c[str(b_)] for b_ in AUD78C["target"]["confirmation_bits"]] \
    == ["REFUTED-D10"] * 12
for b_, rec in AUD78C["confirmation_bits"]["sources"].items():
    assert rec["canon_equal"] is True, (b_, rec)
    assert rec["raw_identical"] == (b_ in ("5", "13", "14", "20",
                                           "34", "46")), (b_, rec)
assert AUD78C["v15_cross_engine_check"]["verdict_agreement"] == \
    "17/17 (16 loss=false, 1 loss=true)"
assert AUD78C["v15_cross_engine_check"]["capped"] == 0
assert AUD78C["determinism_rerun"]["result"] == \
    "field-identical on every non-ms field"
man78c_bits = sorted(c["bit"] for c in MAN78C["certificates"])
assert man78c_bits == sorted(AUD78C_WIN)
man78c_roots = {c["bit"]: c["root"] for c in MAN78C["certificates"]}
for bb in AUD78C_WIN:
    root = f"{int(CHILD78C, 16) | (1 << bb):032x}"
    assert man78c_roots[bb] == root, (bb, root, man78c_roots[bb])
assert MAN78C["totals"] == {"certificates": 11, "rows": 614003,
                            "extraction_nodes": 77967826,
                            "published_bytes": 22223603,
                            "fbt_drops_total": 0,
                            "capped_per_move_total": 0}
cert78c = CLAIM78C["certificates"]
assert cert78c["manifest"] == \
    "class2-lane-cost78c-win7-certificates-20261117.json"
assert cert78c["manifest_blob_sha"] == \
    "b7fe519e923c6170e836f71e3f084f73219319d5"
assert cert78c["totals"] == MAN78C["totals"]
assert cert78c["determinism_sample_bits"] == [69, 116]
assert CLAIM78C["receipt_fold"]["status"].startswith("pending behind")
assert AUD78C16["schema"] == \
    "n11-cost78c-raw-batches-1-6-audit-20261118-v1"
assert AUD78C16["all_pass"] is True and AUD78C16["failures"] == []
t78c16 = AUD78C16["totals"]
assert t78c16["candidate_bits"] == 54
assert t78c16["win7_d10_bits"] == [1, 4, 9, 30, 49, 69, 75, 79, 100]
assert len(t78c16["refuted_d10_bits"]) == 45
pb78c = {e["bit"]: e for e in AUD78C16["per_bit"]}
assert sorted(pb78c) == sorted(ec78c["open_bits"])[:54]
for bb, e in pb78c.items():
    exp = "WIN7-D10" if bb in set(AUD78C_WIN) else "REFUTED-D10"
    assert e["verdict"] == exp, (bb, e["verdict"], exp)
assert FOLD76C["status"] == "fold-complete"
fa = FOLD76C["frontier_after_cost76c"]
assert (fa["solved_s6_in_manifest"], fa["remaining_s5_orbits"],
        fa["unique_remaining_s6"], fa["sum_remaining_cost"],
        fa["s6_needed_by_open_classes"],
        fa["cost_needed_by_open_classes"]) == \
    (1473, 174, 6375, 504596, 4648, 368510)

# 79c sweep completion check (20 WIN + 59 REFUTED, 0 capped)
assert AUD79C["schema"] == "n11-cost79c-raw-batches-1-9-audit-20261118-v1"
assert AUD79C["all_pass"] is True and AUD79C["failures"] == []
AUD79C_T = AUD79C["totals"]
AUD79C_WIN = sorted(AUD79C_T["win7_d10_bits"])
assert AUD79C_WIN == [1, 2, 17, 21, 26, 28, 29, 30, 31, 47,
                      58, 62, 91, 96, 100, 109, 110, 113, 117, 120]
assert len(AUD79C_T["refuted_d10_bits"]) == 59
assert AUD79C_T["capped_bits"] == []
CHILD79C = AUD79C["target"]["child"]
assert CHILD79C == "00000000000000c09002000200000000"
assert AUD79C["target"]["stone_bits"] == [33, 49, 60, 63, 70, 71]
assert AUD79C["target"]["open_bits_total"] == 68
assert AUD79C["target"]["confirmation_bits_total"] == 11
st79c, bits79c = legal_candidates(CHILD79C)
cands79c = sorted(bits79c)
assert len(cands79c) == 79
assert set(AUD79C_WIN) | set(AUD79C_T["refuted_d10_bits"]) == set(cands79c)
assert not (set(AUD79C_WIN) & set(AUD79C_T["refuted_d10_bits"]))
assert AUD79C_T["candidate_nodes"] == 206090979
assert AUD79C_T["pilot_controls"] == 9 and AUD79C_T["pilot_nodes"] == 30618
assert sorted(AUD79C["confirmation_outcome"]["bits"]) == \
    [12, 20, 22, 65, 67, 86, 87, 94, 97, 106, 110]
assert AUD79C["confirmation_outcome"]["conflicts"] == 0
obs79c = AUD79C["confirmation_outcome"]["observed"]
assert [obs79c[str(b_)] for b_ in AUD79C["confirmation_outcome"]["bits"]] \
    == ["REFUTED-D10"] * 10 + ["WIN7-D10"]

# independent re-audit of the nine raw batch files
raw79c = {}
pilot79c = 0
nodes79c = 0
for fname, pin in RAW_PINS79C.items():
    b = (OUT / fname).read_bytes()
    assert git_blob_sha(b) == pin, fname
    for line in b.decode().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if "control" in r:
            pilot79c += 1
            assert r["nodes"] == 3402, (fname, r)
        else:
            assert r["bit"] not in raw79c, (fname, r["bit"])
            assert r["andclose"] is True and r["capped"] is False
            raw79c[r["bit"]] = r
assert pilot79c == 9
assert sorted(raw79c) == cands79c
audit79c_by_bit = {x["bit"]: x for x in AUD79C["per_bit"]}
for b_, r in raw79c.items():
    e = audit79c_by_bit[b_]
    exp = "WIN7-D10" if b_ in set(AUD79C_WIN) else "REFUTED-D10"
    assert e["verdict"] == exp, (b_, e["verdict"], exp)
    assert (r["loss"] is True) == (b_ in set(AUD79C_WIN)), b_
    assert r["nodes"] == e["nodes"], (b_, r["nodes"], e["nodes"])
    assert r["terminalStoneRange"] == [13, 17] == e["terminal_stone_range"], b_
    assert int(e["root_canon"], 16) == canon(int(CHILD79C, 16) | (1 << b_)), b_
    nodes79c += r["nodes"]
assert nodes79c == 206090979
assert AUD79C["checks"]["det1_det8_field_identical"]["ok"] is True
assert AUD79C["checks"]["v15a_confirmation_agreement"]["ok"] is True
assert AUD79C["confirmation_outcome"]["v15_crosscheck_agreement"] is True

# claim v2 agreement
assert CLAIM79C["status"].startswith(
    "claim v2: COMPLETED + CERTIFICATES PUBLISHED")
ex79c = CLAIM79C["actual_execution"]
assert sorted(ex79c["win7_d10_bits"]) == AUD79C_WIN
assert len(ex79c["refuted_d10_bits"]) == 59
assert ex79c["capped_bits"] == []
assert ex79c["candidate_nodes"] == 206090979
assert CLAIM79C["batches_run"] == 9
assert len(ex79c["raw_batch_files"]) == 9
assert CLAIM79C["receipt_fold"]["status"].startswith("pending behind")

# manifest agreement (19 new certificates; bit 110 canon-covered)
man79c_bits = sorted(c["bit"] for c in MAN79C["certificates"])
assert man79c_bits == sorted(set(AUD79C_WIN) - {110})
man79c_roots = {c["bit"]: c["root"] for c in MAN79C["certificates"]}
for bb in man79c_bits:
    root = f"{int(CHILD79C, 16) | (1 << bb):032x}"
    assert man79c_roots[bb] == root, (bb, root, man79c_roots[bb])
assert MAN79C["totals"] == {"certificates": 19, "rows": 1106127,
                            "extraction_nodes": 339101130,
                            "published_bytes": 39877889,
                            "fbt_drops_total": 0,
                            "capped_per_move_total": 0}
cert79c = ex79c["certificates"]
assert cert79c["manifest_blob_sha"] == \
    "e904a37665fb77c971ce7f9c64a3c4aa9109da4d"
assert cert79c["totals"] == MAN79C["totals"]
bigint_bits79c = sorted(int(k) for k in BIGINT79C["certificates_checked"])
assert bigint_bits79c == [21, 30, 117, 120]
for bb, rec in BIGINT79C["certificates_checked"].items():
    assert rec["union_missing"] == 0 and rec["union_extra"] == 0
    assert rec["verdict"] == "WIN7 certificate independently verified"
assert DET79C["bits"] == [30, 117]
assert DET79C["result"].startswith("byte-identical md5")
# bit 110 canon-covered by the published cost73k bit 87 certificate
man73k_by_bit = {c["bit"]: c for c in MAN73K["certificates"]}
assert 87 in man73k_by_bit
c110 = canon(int(CHILD79C, 16) | (1 << 110))
assert c110 == int(man73k_by_bit[87]["d4_canon_root"], 16), c110
# parallel-lane third independent audit (general circle)
assert AUD79C3RD["all_pass"] is True
assert sorted(c["bit"] for c in AUD79C3RD["certificates"]) == [1, 2, 21]
for c3 in AUD79C3RD["certificates"]:
    assert c3["union"]["missing"] == 0 and c3["union"]["extra"] == 0


# 79d sweep completion check (0 WIN + 79 REFUTED, 0 capped)
assert AUD79D["schema"] == \
    "n11-class2-lane-cost79d-raw-batches-1-9-audit-20261118-v1"
assert AUD79D["counts"] == {"win7_d10": 0, "refuted_d10": 79,
                            "capped": 0, "total_bits": 79}
CHILD79D = AUD79D["child"]
assert CHILD79D == "00000000020000003800400080000000"
assert AUD79D["total_candidate_nodes"] == 49103515
assert AUD79D["open_bits_total"] == 72
assert AUD79D["pilot_controls_pass"] == "9/9"
assert AUD79D["confirmation_prediction_match"].startswith("7/7")
assert AUD79D["confirmation_root_canons_match_census_v13_transfers"] \
    is True
st79d, bits79d = legal_candidates(CHILD79D)
cands79d = sorted(bits79d)
assert len(cands79d) == 79
perbit79d = AUD79D["per_bit"]
assert sorted(int(k) for k in perbit79d) == cands79d
for b_, e in perbit79d.items():
    assert e["verdict"] == "REFUTED-D10", (b_, e)
    assert e["batch"] in range(1, 10)
    assert e["terminal_stone_range"] == [13, 17], (b_, e)
    assert int(e["root_canon"], 16) == \
        canon(int(CHILD79D, 16) | (1 << int(b_))), b_
conf79d_bits = sorted(int(b) for b in AUD79D["confirmation_bits"])
assert conf79d_bits == [5, 27, 41, 79, 90, 93, 115]
for b_ in conf79d_bits:
    assert AUD79D["confirmation_outcome"][str(b_)] == "REFUTED-D10"
# census v13 overlay prediction agreement (transfers dict)
for b_, tr in CLAIM79D["transfers"].items():
    assert int(b_) in conf79d_bits, (b_, "transfer bit not in confirm")
    assert tr["verdict"] == "REFUTED-D10"
    assert int(tr["root_canon"], 16) == \
        int(perbit79d[b_]["root_canon"], 16), b_
# claim v2 agreement
assert CLAIM79D["status"].startswith("claim v2: COMPLETED")
assert CLAIM79D["batches_run"] == 9
assert CLAIM79D["open_bits_completed"] == 72
assert CLAIM79D["open_bits_remaining"] == 0
assert CLAIM79D["receipt_fold"]["status"].startswith("not needed")
ex79d = CLAIM79D["actual_execution"]
assert ex79d["verdicts"]["counts"] == {"win7_d10": 0,
                                       "refuted_d10": 79, "capped": 0}
assert ex79d["total_candidate_nodes"] == 49103515
assert ex79d["pilot_controls"] == \
    "9/9 batches open with pilot_d6 loss=false at exactly 3402 nodes"
assert len(ex79d["raw_files"]) == 12
assert CLAIM79D["confirmation_outcome"].startswith(
    "7/7 confirmation bits re-run fresh matched")

# independent re-audit of the twelve raw batch files
raw79d = {}
det79d = {}
pilot79d = 0
nodes79d = 0
v15_79d = {}
for fname, pin in RAW_PINS79D.items():
    b = (OUT / fname).read_bytes()
    assert git_blob_sha(b) == pin, fname
    target = None
    if fname.startswith("class2-lane-cost79d-det-"):
        target = det79d
    elif fname.startswith("class2-lane-cost79d-v15-"):
        target = v15_79d
    else:
        target = raw79d
    for line in b.decode().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if "control" in r:
            pilot79d += 1
            assert r["loss"] is False and r["capped"] is False
            if fname.startswith("class2-lane-cost79d-v15-"):
                assert r["nodes"] == 5949, (fname, r)
            else:
                assert r["nodes"] == 3402, (fname, r)
        else:
            assert r["bit"] not in target, (fname, r["bit"])
            assert r["andclose"] is True and r["capped"] is False
            assert r["loss"] is False, (fname, r)
            target[r["bit"]] = r
assert pilot79d == 12
assert sorted(raw79d) == cands79d
assert len(v15_79d) == 7 and sorted(v15_79d) == conf79d_bits
for b_, r in raw79d.items():
    e = perbit79d[str(b_)]
    assert r["nodes"] == e["nodes"], (b_, r["nodes"], e["nodes"])
    assert r["terminalStoneRange"] == [13, 17], b_
    nodes79d += r["nodes"]
assert nodes79d == 49103515
# det re-runs field-identical on every non-ms field
for det, nb in ((det79d, "class2-lane-cost79d-det-batch1-20261118.jsonl"),
                (None, "class2-lane-cost79d-det-batch8-20261118.jsonl")):
    pass
det1 = {}
for line in (OUT / "class2-lane-cost79d-det-batch1-20261118.jsonl") \
        .read_bytes().decode().splitlines():
    r = json.loads(line)
    if "control" not in r:
        det1[r["bit"]] = r
det8 = {}
for line in (OUT / "class2-lane-cost79d-det-batch8-20261118.jsonl") \
        .read_bytes().decode().splitlines():
    r = json.loads(line)
    if "control" not in r:
        det8[r["bit"]] = r
assert sorted(det1) == AUD79D["batches"]["1"]["bits"]
assert sorted(det8) == AUD79D["batches"]["8"]["bits"]
for b_, r in det1.items():
    assert raw79d[b_]["nodes"] == r["nodes"], b_
    assert raw79d[b_]["loss"] == r["loss"]
    assert raw79d[b_]["terminalStoneRange"] == r["terminalStoneRange"]
for b_, r in det8.items():
    assert raw79d[b_]["nodes"] == r["nodes"], b_
    assert raw79d[b_]["loss"] == r["loss"]
    assert raw79d[b_]["terminalStoneRange"] == r["terminalStoneRange"]


# 79e sweep completion check (0 WIN + 79 REFUTED, 0 capped)
assert AUD79E["schema"] == \
    "n11-class2-lane-cost79e-raw-batches-1-9-audit-20261118-v1"
assert AUD79E["counts"] == {"win7_d10": 0, "refuted_d10": 79,
                            "capped": 0, "total_bits": 79}
CHILD79E = AUD79E["child"]
assert CHILD79E == "00000000020000003800000880000000"
assert AUD79E["total_candidate_nodes"] == 74450533
assert AUD79E["open_bits_total"] == 72
assert AUD79E["pilot_controls_pass"] == "9/9"
assert AUD79E["confirmation_prediction_match"].startswith("7/7")
assert AUD79E["confirmation_root_canons_match_census_v14_transfers"] \
    is True
st79e, bits79e = legal_candidates(CHILD79E)
cands79e = sorted(bits79e)
assert len(cands79e) == 79
perbit79e = AUD79E["per_bit"]
assert sorted(int(k) for k in perbit79e) == cands79e
for b_, e in perbit79e.items():
    assert e["verdict"] == "REFUTED-D10", (b_, e)
    assert e["batch"] in range(1, 10)
    assert e["terminal_stone_range"] == [13, 17], (b_, e)
    assert int(e["root_canon"], 16) == \
        canon(int(CHILD79E, 16) | (1 << int(b_))), b_
conf79e_bits = sorted(int(b) for b in AUD79E["confirmation_bits"])
assert conf79e_bits == [27, 30, 46, 74, 79, 93, 115]
for b_ in conf79e_bits:
    assert AUD79E["confirmation_outcome"][str(b_)] == "REFUTED-D10"
# census v14 overlay prediction agreement (transfers dict)
for b_, tr in CLAIM79E["transfers"].items():
    assert int(b_) in conf79e_bits, (b_, "transfer bit not in confirm")
    assert tr["verdict"] == "REFUTED-D10"
    assert int(tr["root_canon"], 16) == \
        int(perbit79e[b_]["root_canon"], 16), b_
# claim v2 agreement
assert CLAIM79E["status"].startswith("claim v2: COMPLETED")
assert CLAIM79E["batches_run"] == 9
assert CLAIM79E["open_bits_completed"] == 72
assert CLAIM79E["open_bits_remaining"] == 0
assert CLAIM79E["receipt_fold"]["status"].startswith("not needed")
ex79e = CLAIM79E["actual_execution"]
assert ex79e["verdicts"]["counts"] == {"win7_d10": 0,
                                       "refuted_d10": 79, "capped": 0}
assert ex79e["total_candidate_nodes"] == 74450533
assert ex79e["pilot_controls"] == \
    "9/9 batches open with pilot_d6 loss=false at exactly 3402 nodes"
assert len(ex79e["raw_files"]) == 12
assert CLAIM79E["confirmation_outcome"].startswith(
    "7/7 confirmation bits re-run fresh matched")

# independent re-audit of the twelve raw batch files
raw79e = {}
det79e = {}
pilot79e = 0
nodes79e = 0
v15_79e = {}
for fname, pin in RAW_PINS79E.items():
    b = (OUT / fname).read_bytes()
    assert git_blob_sha(b) == pin, fname
    target = None
    if fname.startswith("class2-lane-cost79e-det-"):
        target = det79e
    elif fname.startswith("class2-lane-cost79e-v15-"):
        target = v15_79e
    else:
        target = raw79e
    for line in b.decode().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if "control" in r:
            pilot79e += 1
            assert r["loss"] is False and r["capped"] is False
            if fname.startswith("class2-lane-cost79e-v15-"):
                assert r["nodes"] == 5949, (fname, r)
            else:
                assert r["nodes"] == 3402, (fname, r)
        else:
            assert r["bit"] not in target, (fname, r["bit"])
            assert r["andclose"] is True and r["capped"] is False
            assert r["loss"] is False, (fname, r)
            target[r["bit"]] = r
assert pilot79e == 12
assert sorted(raw79e) == cands79e
assert len(v15_79e) == 7 and sorted(v15_79e) == conf79e_bits
for b_, r in raw79e.items():
    e = perbit79e[str(b_)]
    assert r["nodes"] == e["nodes"], (b_, r["nodes"], e["nodes"])
    assert r["terminalStoneRange"] == [13, 17], b_
    nodes79e += r["nodes"]
assert nodes79e == 74450533
det1e = {}
for line in (OUT / "class2-lane-cost79e-det-batch1-20261118.jsonl") \
        .read_bytes().decode().splitlines():
    r = json.loads(line)
    if "control" not in r:
        det1e[r["bit"]] = r
det8e = {}
for line in (OUT / "class2-lane-cost79e-det-batch8-20261118.jsonl") \
        .read_bytes().decode().splitlines():
    r = json.loads(line)
    if "control" not in r:
        det8e[r["bit"]] = r
assert sorted(det1e) == AUD79E["batches"]["1"]["bits"]
assert sorted(det8e) == AUD79E["batches"]["8"]["bits"]
for b_, r in det1e.items():
    assert raw79e[b_]["nodes"] == r["nodes"], b_
    assert raw79e[b_]["loss"] == r["loss"]
    assert raw79e[b_]["terminalStoneRange"] == r["terminalStoneRange"]
for b_, r in det8e.items():
    assert raw79e[b_]["nodes"] == r["nodes"], b_
    assert raw79e[b_]["loss"] == r["loss"]
    assert raw79e[b_]["terminalStoneRange"] == r["terminalStoneRange"]

# 80e sweep completion check (0 WIN + 80 REFUTED, 0 capped)
assert AUD80E["schema"] == \
    "n11-class2-lane-cost80e-raw-batches-1-9-audit-20261118-v1"
assert AUD80E["counts"] == {"win7_d10": 0, "refuted_d10": 80,
                            "capped": 0, "total_bits": 80}
CHILD80E = AUD80E["child"]
assert CHILD80E == "00000000020000003800000180000000"
assert AUD80E["total_candidate_nodes"] == 87301907
assert AUD80E["open_bits_total"] == 68
assert AUD80E["pilot_controls_pass"] == "9/9"
assert AUD80E["confirmation_prediction_match"].startswith("12/12")
assert AUD80E["confirmation_root_canons_match_census_v15_transfers"] \
    is True
assert AUD80E["v15_crosscheck"]["pilot_nodes"] == 5949
assert AUD80E["v15_crosscheck"]["agreement"] == \
    "12/12 loss=false (0 conflicts)"
st80e, bits80e = legal_candidates(CHILD80E)
cands80e = sorted(bits80e)
assert len(cands80e) == 80
perbit80e = AUD80E["per_bit"]
assert sorted(int(k) for k in perbit80e) == cands80e
for b_, e in perbit80e.items():
    assert e["verdict"] == "REFUTED-D10", (b_, e)
    assert e["batch"] in range(1, 10)
    assert e["terminal_stone_range"] == [13, 17], (b_, e)
    assert int(e["root_canon"], 16) == \
        canon(int(CHILD80E, 16) | (1 << int(b_))), b_
conf80e_bits = sorted(int(b) for b in AUD80E["confirmation_bits"])
assert conf80e_bits == [5, 27, 30, 35, 41, 46, 74, 79, 85, 90, 93, 115]
for b_ in conf80e_bits:
    assert AUD80E["confirmation_outcome"][str(b_)] == "REFUTED-D10"
# census v15 overlay prediction agreement (transfers dict)
for b_, tr in CLAIM80E["transfers"].items():
    assert int(b_) in conf80e_bits, (b_, "transfer bit not in confirm")
    assert tr["verdict"] == "REFUTED-D10"
    assert int(tr["root_canon"], 16) == \
        int(perbit80e[b_]["root_canon"], 16), b_
# claim v2 agreement
assert CLAIM80E["status"].startswith("claim v2: COMPLETED")
assert CLAIM80E["batches_run"] == 9
assert CLAIM80E["open_bits_completed"] == 68
assert CLAIM80E["open_bits_remaining"] == 0
assert CLAIM80E["receipt_fold"]["status"].startswith("not needed")
ex80e = CLAIM80E["actual_execution"]
assert ex80e["verdicts"]["counts"] == {"win7_d10": 0,
                                       "refuted_d10": 80, "capped": 0}
assert ex80e["total_candidate_nodes"] == 87301907
assert ex80e["pilot_controls"] == \
    "9/9 batches open with pilot_d6 loss=false at exactly 3402 nodes"
assert len(ex80e["raw_files"]) == 12
assert CLAIM80E["confirmation_outcome"].startswith(
    "12/12 confirmation bits re-run fresh matched")
# the swept child is the census v15 selected target and its open bits
# are exactly the census v15 sweep bits
assert V15["selected_target"]["s6_hex"] == CHILD80E
assert sorted(V15["selected_target"]["sweep_bits"]) == \
    sorted(set(cands80e) - set(conf80e_bits))
assert sorted(int(c["bit"]) for c in
              V15["selected_target"]["confirmation_bits"]) == conf80e_bits
assert sorted(CLAIM80E["engine_candidate_bits"]["open_bits"]) == \
    sorted(set(cands80e) - set(conf80e_bits))

# independent re-audit of the twelve raw batch files
raw80e = {}
det80e = {}
pilot80e = 0
nodes80e = 0
v15_80e = {}
for fname, pin in RAW_PINS80E.items():
    b = (OUT / fname).read_bytes()
    assert git_blob_sha(b) == pin, fname
    target = None
    if fname.startswith("class2-lane-cost80e-det-"):
        target = det80e
    elif fname.startswith("class2-lane-cost80e-v15-"):
        target = v15_80e
    else:
        target = raw80e
    for line in b.decode().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if "control" in r:
            pilot80e += 1
            assert r["loss"] is False and r["capped"] is False
            if fname.startswith("class2-lane-cost80e-v15-"):
                assert r["nodes"] == 5949, (fname, r)
            else:
                assert r["nodes"] == 3402, (fname, r)
        else:
            assert r["bit"] not in target, (fname, r["bit"])
            assert r["andclose"] is True and r["capped"] is False
            assert r["loss"] is False, (fname, r)
            target[r["bit"]] = r
assert pilot80e == 12
assert sorted(raw80e) == cands80e
assert len(v15_80e) == 12 and sorted(v15_80e) == conf80e_bits
for b_, r in raw80e.items():
    e = perbit80e[str(b_)]
    assert r["nodes"] == e["nodes"], (b_, r["nodes"], e["nodes"])
    assert r["terminalStoneRange"] == [13, 17], b_
    nodes80e += r["nodes"]
assert nodes80e == 87301907
det1x = {}
for line in (OUT / "class2-lane-cost80e-det-batch1-20261118.jsonl") \
        .read_bytes().decode().splitlines():
    r = json.loads(line)
    if "control" not in r:
        det1x[r["bit"]] = r
det8x = {}
for line in (OUT / "class2-lane-cost80e-det-batch8-20261118.jsonl") \
        .read_bytes().decode().splitlines():
    r = json.loads(line)
    if "control" not in r:
        det8x[r["bit"]] = r
assert sorted(det1x) == AUD80E["batches"]["1"]["bits"]
assert sorted(det8x) == AUD80E["batches"]["8"]["bits"]
for b_, r in det1x.items():
    assert raw80e[b_]["nodes"] == r["nodes"], b_
    assert raw80e[b_]["loss"] == r["loss"]
    assert raw80e[b_]["terminalStoneRange"] == r["terminalStoneRange"]
for b_, r in det8x.items():
    assert raw80e[b_]["nodes"] == r["nodes"], b_
    assert raw80e[b_]["loss"] == r["loss"]
    assert raw80e[b_]["terminalStoneRange"] == r["terminalStoneRange"]


# 80f sweep completion check (0 WIN + 80 REFUTED, 0 capped)
assert AUD80F["schema"] == \
    "n11-class2-lane-cost80f-raw-batches-1-9-audit-20261118-v1"
assert AUD80F["counts"] == {"win7_d10": 0, "refuted_d10": 80,
                            "capped": 0, "total_bits": 80}
CHILD80F = AUD80F["child"]
assert CHILD80F == "00000000020000003800200080000000"
assert AUD80F["total_candidate_nodes"] == 51125648
assert AUD80F["open_bits_total"] == 67
assert AUD80F["pilot_controls_pass"] == "9/9"
assert AUD80F["confirmation_prediction_match"].startswith("13/13")
assert AUD80F["confirmation_root_canons_match_census_v16_transfers"] \
    is True
assert AUD80F["v15_crosscheck"]["pilot_nodes"] == 5949
assert AUD80F["v15_crosscheck"]["agreement"] == \
    "13/13 loss=false (0 conflicts)"
st80f, bits80f = legal_candidates(CHILD80F)
cands80f = sorted(bits80f)
assert len(cands80f) == 80
perbit80f = AUD80F["per_bit"]
assert sorted(int(k) for k in perbit80f) == cands80f
for b_, e in perbit80f.items():
    assert e["verdict"] == "REFUTED-D10", (b_, e)
    assert e["batch"] in range(1, 10)
    assert e["terminal_stone_range"] == [13, 17], (b_, e)
    assert int(e["root_canon"], 16) == \
        canon(int(CHILD80F, 16) | (1 << int(b_))), b_
conf80f_bits = sorted(int(b) for b in AUD80F["confirmation_bits"])
assert conf80f_bits == [5, 27, 30, 35, 41, 46, 74, 79, 85, 88,
                        90, 93, 115]
for b_ in conf80f_bits:
    assert AUD80F["confirmation_outcome"][str(b_)] == "REFUTED-D10"
# census v16 overlay prediction agreement (transfers dict)
for b_, tr in CLAIM80F["transfers"].items():
    assert int(b_) in conf80f_bits, (b_, "transfer bit not in confirm")
    assert tr["verdict"] == "REFUTED-D10"
    assert int(tr["root_canon"], 16) == \
        int(perbit80f[b_]["root_canon"], 16), b_
# claim v2 agreement
assert CLAIM80F["status"].startswith("claim v2: COMPLETED")
assert CLAIM80F["batches_run"] == 9
assert CLAIM80F["open_bits_completed"] == 67
assert CLAIM80F["open_bits_remaining"] == 0
assert CLAIM80F["receipt_fold"]["status"].startswith("not needed")
ex80f = CLAIM80F["actual_execution"]
assert ex80f["verdicts"]["counts"] == {"win7_d10": 0,
                                       "refuted_d10": 80, "capped": 0}
assert ex80f["total_candidate_nodes"] == 51125648
assert ex80f["pilot_controls"] == \
    "9/9 batches open with pilot_d6 loss=false at exactly 3402 nodes"
assert len(ex80f["raw_files"]) == 12
assert CLAIM80F["confirmation_outcome"].startswith(
    "13/13 confirmation bits re-run fresh matched")
# the swept child is the census v16 selected target and its open bits
# are exactly the census v16 sweep bits
assert V16["selected_target"]["s6_hex"] == CHILD80F
assert sorted(V16["selected_target"]["sweep_bits"]) == \
    sorted(set(cands80f) - set(conf80f_bits))
assert sorted(int(c["bit"]) for c in
              V16["selected_target"]["confirmation_bits"]) == conf80f_bits
assert sorted(CLAIM80F["engine_candidate_bits"]["open_bits"]) == \
    sorted(set(cands80f) - set(conf80f_bits))

# independent re-audit of the twelve raw batch files
raw80f = {}
det80f = {}
pilot80f = 0
nodes80f = 0
v15_80f = {}
for fname, pin in RAW_PINS80F.items():
    b = (OUT / fname).read_bytes()
    assert git_blob_sha(b) == pin, fname
    target = None
    if fname.startswith("class2-lane-cost80f-det-"):
        target = det80f
    elif fname.startswith("class2-lane-cost80f-v15-"):
        target = v15_80f
    else:
        target = raw80f
    for line in b.decode().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if "control" in r:
            pilot80f += 1
            assert r["loss"] is False and r["capped"] is False
            if fname.startswith("class2-lane-cost80f-v15-"):
                assert r["nodes"] == 5949, (fname, r)
            else:
                assert r["nodes"] == 3402, (fname, r)
        else:
            assert r["bit"] not in target, (fname, r["bit"])
            assert r["andclose"] is True and r["capped"] is False
            assert r["loss"] is False, (fname, r)
            target[r["bit"]] = r
assert pilot80f == 12
assert sorted(raw80f) == cands80f
assert len(v15_80f) == 13 and sorted(v15_80f) == conf80f_bits
for b_, r in raw80f.items():
    e = perbit80f[str(b_)]
    assert r["nodes"] == e["nodes"], (b_, r["nodes"], e["nodes"])
    assert r["terminalStoneRange"] == [13, 17], b_
    nodes80f += r["nodes"]
assert nodes80f == 51125648
det1f = {}
for line in (OUT / "class2-lane-cost80f-det-batch1-20261118.jsonl") \
        .read_bytes().decode().splitlines():
    r = json.loads(line)
    if "control" not in r:
        det1f[r["bit"]] = r
det8f = {}
for line in (OUT / "class2-lane-cost80f-det-batch8-20261118.jsonl") \
        .read_bytes().decode().splitlines():
    r = json.loads(line)
    if "control" not in r:
        det8f[r["bit"]] = r
assert sorted(det1f) == AUD80F["batches"]["1"]["bits"]
assert sorted(det8f) == AUD80F["batches"]["8"]["bits"]
for b_, r in det1f.items():
    assert raw80f[b_]["nodes"] == r["nodes"], b_
    assert raw80f[b_]["loss"] == r["loss"]
    assert raw80f[b_]["terminalStoneRange"] == r["terminalStoneRange"]
for b_, r in det8f.items():
    assert raw80f[b_]["nodes"] == r["nodes"], b_
    assert raw80f[b_]["loss"] == r["loss"]
    assert raw80f[b_]["terminalStoneRange"] == r["terminalStoneRange"]



# 81 sweep completion check (0 WIN + 81 REFUTED, 0 capped)
assert AUD81["schema"] == \
    "n11-class2-lane-cost81-raw-batches-1-9-audit-20261118-v1"
assert AUD81["counts"] == {"win7_d10": 0, "refuted_d10": 81,
                            "capped": 0, "total_bits": 81}
CHILD81 = AUD81["child"]
assert CHILD81 == "00000000020000003800000080008000"
assert AUD81["total_candidate_nodes"] == 86480711
assert AUD81["open_bits_total"] == 66
assert AUD81["pilot_controls_pass"] == "9/9"
assert AUD81["confirmation_prediction_match"].startswith("15/15")
assert AUD81["confirmation_root_canons_match_census_v17_transfers"] \
    is True
assert AUD81["v15_crosscheck"]["pilot_nodes"] == 5949
assert AUD81["v15_crosscheck"]["agreement"] == \
    "15/15 loss=false (0 conflicts)"
st81, bits81 = legal_candidates(CHILD81)
cands81 = sorted(bits81)
assert len(cands81) == 81
perbit81 = AUD81["per_bit"]
assert sorted(int(k) for k in perbit81) == cands81
for b_, e in perbit81.items():
    assert e["verdict"] == "REFUTED-D10", (b_, e)
    assert e["batch"] in range(1, 10)
    assert e["terminal_stone_range"] == [13, 17], (b_, e)
    assert int(e["root_canon"], 16) == \
        canon(int(CHILD81, 16) | (1 << int(b_))), b_
conf81_bits = sorted(int(b) for b in AUD81["confirmation_bits"])
assert conf81_bits == [27, 30, 32, 35, 41, 45, 46, 74, 75, 79, 85,
                        88, 90, 93, 115]
for b_ in conf81_bits:
    assert AUD81["confirmation_outcome"][str(b_)] == "REFUTED-D10"
# census v17 overlay prediction agreement (transfers dict)
for b_, tr in CLAIM81["transfers"].items():
    assert int(b_) in conf81_bits, (b_, "transfer bit not in confirm")
    assert tr["verdict"] == "REFUTED-D10"
    assert int(tr["root_canon"], 16) == \
        int(perbit81[b_]["root_canon"], 16), b_
# claim v2 agreement
assert CLAIM81["status"].startswith("claim v2: COMPLETED")
assert CLAIM81["batches_run"] == 9
assert CLAIM81["open_bits_completed"] == 66
assert CLAIM81["open_bits_remaining"] == 0
assert CLAIM81["receipt_fold"]["status"].startswith("not needed")
ex81 = CLAIM81["actual_execution"]
assert ex81["verdicts"]["counts"] == {"win7_d10": 0,
                                       "refuted_d10": 81, "capped": 0}
assert ex81["total_candidate_nodes"] == 86480711
assert ex81["pilot_controls"] == \
    "9/9 batches open with pilot_d6 loss=false at exactly 3402 nodes"
assert len(ex81["raw_files"]) == 12
assert CLAIM81["confirmation_outcome"].startswith(
    "15/15 confirmation bits re-run fresh matched")
# the swept child is the census v17 selected target and its open bits
# are exactly the census v17 sweep bits
assert V17["selected_target"]["s6_hex"] == CHILD81
assert sorted(V17["selected_target"]["sweep_bits"]) == \
    sorted(set(cands81) - set(conf81_bits))
assert sorted(int(c["bit"]) for c in
              V17["selected_target"]["confirmation_bits"]) == conf81_bits
assert sorted(CLAIM81["engine_candidate_bits"]["open_bits"]) == \
    sorted(set(cands81) - set(conf81_bits))

# independent re-audit of the twelve raw batch files
raw81 = {}
det81 = {}
pilot81 = 0
nodes81 = 0
v15_81 = {}
for fname, pin in RAW_PINS81.items():
    b = (OUT / fname).read_bytes()
    assert git_blob_sha(b) == pin, fname
    target = None
    if fname.startswith("class2-lane-cost81-det-"):
        target = det81
    elif fname.startswith("class2-lane-cost81-v15-"):
        target = v15_81
    else:
        target = raw81
    for line in b.decode().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if "control" in r:
            pilot81 += 1
            assert r["loss"] is False and r["capped"] is False
            if fname.startswith("class2-lane-cost81-v15-"):
                assert r["nodes"] == 5949, (fname, r)
            else:
                assert r["nodes"] == 3402, (fname, r)
        else:
            assert r["bit"] not in target, (fname, r["bit"])
            assert r["andclose"] is True and r["capped"] is False
            assert r["loss"] is False, (fname, r)
            target[r["bit"]] = r
assert pilot81 == 12
assert sorted(raw81) == cands81
assert len(v15_81) == 15 and sorted(v15_81) == conf81_bits
for b_, r in raw81.items():
    e = perbit81[str(b_)]
    assert r["nodes"] == e["nodes"], (b_, r["nodes"], e["nodes"])
    assert r["terminalStoneRange"] == [13, 17], b_
    nodes81 += r["nodes"]
assert nodes81 == 86480711
det1y = {}
for line in (OUT / "class2-lane-cost81-det-batch1-20261118.jsonl") \
        .read_bytes().decode().splitlines():
    r = json.loads(line)
    if "control" not in r:
        det1y[r["bit"]] = r
det8y = {}
for line in (OUT / "class2-lane-cost81-det-batch8-20261118.jsonl") \
        .read_bytes().decode().splitlines():
    r = json.loads(line)
    if "control" not in r:
        det8y[r["bit"]] = r
assert sorted(det1y) == AUD81["batches"]["1"]["bits"]
assert sorted(det8y) == AUD81["batches"]["8"]["bits"]
for b_, r in det1y.items():
    assert raw81[b_]["nodes"] == r["nodes"], b_
    assert raw81[b_]["loss"] == r["loss"]
    assert raw81[b_]["terminalStoneRange"] == r["terminalStoneRange"]
for b_, r in det8y.items():
    assert raw81[b_]["nodes"] == r["nodes"], b_
    assert raw81[b_]["loss"] == r["loss"]
    assert raw81[b_]["terminalStoneRange"] == r["terminalStoneRange"]


# 82d sweep completion check (0 WIN + 82 REFUTED, 0 capped)
assert AUD82D["schema"] == \
    "n11-class2-lane-cost82d-raw-batches-1-9-audit-20261118-v1"
assert AUD82D["counts"] == {"win7_d10": 0, "refuted_d10": 82,
                            "capped": 0, "total_bits": 82}
CHILD82D = AUD82D["child"]
assert CHILD82D == "00000000020000003800000080000800"
assert AUD82D["total_candidate_nodes"] == 127619232
assert AUD82D["open_bits_total"] == 65
assert AUD82D["pilot_controls_pass"] == "9/9"
assert AUD82D["confirmation_prediction_match"].startswith("17/17")
assert AUD82D["confirmation_root_canons_match_census_v18_transfers"] \
    is True
assert AUD82D["v15_crosscheck"]["pilot_nodes"] == 5949
assert AUD82D["v15_crosscheck"]["agreement"] == \
    "17/17 loss=false (0 conflicts)"
st82d, bits82d = legal_candidates(CHILD82D)
cands82d = sorted(bits82d)
assert len(cands82d) == 82
perbit82d = AUD82D["per_bit"]
assert sorted(int(k) for k in perbit82d) == cands82d
for b_, e in perbit82d.items():
    assert e["verdict"] == "REFUTED-D10", (b_, e)
    assert e["batch"] in range(1, 10)
    assert e["terminal_stone_range"] == [13, 17], (b_, e)
    assert int(e["root_canon"], 16) == \
        canon(int(CHILD82D, 16) | (1 << int(b_))), b_
conf82d_bits = sorted(int(b) for b in AUD82D["confirmation_bits"])
assert conf82d_bits == [5, 15, 27, 30, 32, 35, 41, 45, 46, 74, 75,
                        79, 85, 90, 93, 105, 115]
for b_ in conf82d_bits:
    assert AUD82D["confirmation_outcome"][str(b_)] == "REFUTED-D10"
# census v18 overlay prediction agreement (transfers dict)
for b_, tr in CLAIM82D["transfers"].items():
    assert int(b_) in conf82d_bits, (b_, "transfer bit not in confirm")
    assert tr["verdict"] == "REFUTED-D10"
    assert int(tr["root_canon"], 16) == \
        int(perbit82d[b_]["root_canon"], 16), b_
# claim v2 agreement
assert CLAIM82D["status"].startswith("claim v2: COMPLETED")
assert CLAIM82D["batches_run"] == 9
assert CLAIM82D["open_bits_completed"] == 65
assert CLAIM82D["open_bits_remaining"] == 0
assert CLAIM82D["receipt_fold"]["status"].startswith("not needed")
ex82d = CLAIM82D["actual_execution"]
assert ex82d["verdicts"]["counts"] == {"win7_d10": 0,
                                       "refuted_d10": 82, "capped": 0}
assert ex82d["total_candidate_nodes"] == 127619232
assert ex82d["pilot_controls"] == \
    "9/9 batches open with pilot_d6 loss=false at exactly 3402 nodes"
assert len(ex82d["raw_files"]) == 12
assert CLAIM82D["confirmation_outcome"].startswith(
    "17/17 confirmation bits re-run fresh matched")
# the swept child is the census v18 selected target and its open bits
# are exactly the census v18 sweep bits
assert V18["selected_target"]["s6_hex"] == CHILD82D
assert sorted(V18["selected_target"]["sweep_bits"]) == \
    sorted(set(cands82d) - set(conf82d_bits))
assert sorted(int(c["bit"]) for c in
              V18["selected_target"]["confirmation_bits"]) == conf82d_bits
assert sorted(CLAIM82D["engine_candidate_bits"]["open_bits"]) == \
    sorted(set(cands82d) - set(conf82d_bits))

# independent re-audit of the twelve raw batch files
raw82d = {}
det82d = {}
pilot82d = 0
nodes82d = 0
v15_82d = {}
for fname, pin in RAW_PINS82D.items():
    b = (OUT / fname).read_bytes()
    assert git_blob_sha(b) == pin, fname
    target = None
    if fname.startswith("class2-lane-cost82d-det-"):
        target = det82d
    elif fname.startswith("class2-lane-cost82d-v15-"):
        target = v15_82d
    else:
        target = raw82d
    for line in b.decode().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if "control" in r:
            pilot82d += 1
            assert r["loss"] is False and r["capped"] is False
            if fname.startswith("class2-lane-cost82d-v15-"):
                assert r["nodes"] == 5949, (fname, r)
            else:
                assert r["nodes"] == 3402, (fname, r)
        else:
            assert r["bit"] not in target, (fname, r["bit"])
            assert r["andclose"] is True and r["capped"] is False
            assert r["loss"] is False, (fname, r)
            target[r["bit"]] = r
assert pilot82d == 12
assert sorted(raw82d) == cands82d
assert len(v15_82d) == 17 and sorted(v15_82d) == conf82d_bits
for b_, r in raw82d.items():
    e = perbit82d[str(b_)]
    assert r["nodes"] == e["nodes"], (b_, r["nodes"], e["nodes"])
    assert r["terminalStoneRange"] == [13, 17], b_
    nodes82d += r["nodes"]
assert nodes82d == 127619232
det1z = {}
for line in (OUT / "class2-lane-cost82d-det-batch1-20261118.jsonl") \
        .read_bytes().decode().splitlines():
    r = json.loads(line)
    if "control" not in r:
        det1z[r["bit"]] = r
det8z = {}
for line in (OUT / "class2-lane-cost82d-det-batch8-20261118.jsonl") \
        .read_bytes().decode().splitlines():
    r = json.loads(line)
    if "control" not in r:
        det8z[r["bit"]] = r
assert sorted(det1z) == AUD82D["batches"]["1"]["bits"]
assert sorted(det8z) == AUD82D["batches"]["8"]["bits"]
for b_, r in det1z.items():
    assert raw82d[b_]["nodes"] == r["nodes"], b_
    assert raw82d[b_]["loss"] == r["loss"]
    assert raw82d[b_]["terminalStoneRange"] == r["terminalStoneRange"]
for b_, r in det8z.items():
    assert raw82d[b_]["nodes"] == r["nodes"], b_
    assert raw82d[b_]["loss"] == r["loss"]
    assert raw82d[b_]["terminalStoneRange"] == r["terminalStoneRange"]


# the synced 79c claim now carries the full 19/19 BigInt corpus
cert79c_c = CLAIM79C["actual_execution"]["certificates"]
assert sorted(cert79c_c["bigint_full_corpus_bits"]) == \
    sorted(set(AUD79C_WIN) - {110})
assert cert79c_c["bigint_audit_blobs"] == [
    "50190347cbc31fa80bf24f9545466c0f3ad9d6f3",
    "410fb935f855881b5b5e9992b75436483d1b3ef1"]
assert AUD79C3RDB["all_pass"] is True
assert sorted(c["bit"] for c in AUD79C3RDB["certificates"]) == \
    [17, 26, 28, 29, 30, 31, 47, 58, 62, 91, 96, 100, 109, 113,
     117, 120]
for c3b in AUD79C3RDB["certificates"]:
    assert c3b["union"]["missing"] == 0
    assert c3b["union"]["extra"] == 0
assert sorted(set(c["bit"] for c in AUD79C3RDB["certificates"])
              | {1, 2, 21}) == sorted(set(AUD79C_WIN) - {110})


NEW_MAPS = {
    "cost64h": {
        "child": VM4["cost64h"]["child"],
        "win": VM4["cost64h"]["win7_d10_bits"],
        "fold": VM4["cost64h"]["fold"],
        "source": VM4["cost64h"]["source"],
    },
    "cost76c": {
        "child": VM4["cost76c"]["child"],
        "win": VM4["cost76c"]["win7_d10_bits"],
        "fold": VM4["cost76c"]["fold"],
        "source": VM4["cost76c"]["source"],
    },
    "cost66i": {
        "child": VM4["cost66i"]["child"],
        "win": VM4["cost66i"]["win7_d10_bits"],
        "fold": VM4["cost66i"]["fold"],
        "source": VM4["cost66i"]["source"],
    },
    "cost66j": {
        "child": VM4["cost66j"]["child"],
        "win": VM4["cost66j"]["win7_d10_bits"],
        "fold": VM4["cost66j"]["fold"],
        "source": VM4["cost66j"]["source"],
    },
    "cost69j": {
        "child": child69j,
        "win": AUD69J_WIN,
        "fold": ("PENDING behind the 76c/66i/66j folds; all six "
                 "certificates extracted, independently verified, "
                 "published and publication-repaired byte-exact"),
        "source": ("raw audit blob 2f6bba29 (8 sweep + 2 confirmation "
                   "batches, v17) + claim v2 + certificate manifest v1"),
    },
    "cost64a": {
        "child": RECHECK64A["target"]["s6_child"],
        "win": [],
        "fold": "LANDED coverage unchanged (STERILE row, no receipts)",
        "source": ("v17 full-row recheck 64/64 REFUTED-D10 "
                   "(64/64 v16-published agreement, verdict flips 0)"),
    },
    "cost71e": {
        "child": CHILD71E,
        "win": AUD71E_WIN,
        "fold": ("PENDING behind the 76c/66i/66j/69j folds; all 13 "
                 "certificates extracted, independently verified "
                 "engine-free and published on main"),
        "source": ("raw audit blob 9f56bdb7 (9 batches, v17) + claim v3 "
                   "(blob 3ca1c698) + certificate manifest "
                   "class2-lane-cost71e-win7-certificates-20261117.json"),
    },
    "cost72d": {
        "child": CHILD72D,
        "win": AUD72D_WIN,
        "fold": ("PENDING behind the 76c/66i/66j/69j/71e folds; all 11 "
                 "certificates extracted, independently verified "
                 "engine-free and published on main"),
        "source": ("raw audit blob 6247569a (9 batches, v17) + claim v2 "
                   "(blob c64e28fd) + certificate manifest "
                   "class2-lane-cost72d-win7-certificates-20261117.json"),
    },
    "cost73i": {
        "child": CHILD73I,
        "win": AUD73I_WIN,
        "fold": ("PENDING behind the 76c/66i/66j/69j/71e/72d folds; the "
                 "12 WIN certificates were NOT yet published on main at "
                 "census-v6 computation time (parallel-lane publication "
                 "pending); the 73i map is carried at audit strength"),
        "source": ("raw audit blob 33c8c6bb (8 sweep + 1 confirmation "
                   "batches, v17) + claim v1 (blob 4a6a17e6, in-flight)"),
    },
    "cost73j": {
        "child": CHILD73J,
        "win": AUD73J_WIN,
        "fold": ("PENDING behind the 66i/66j/69j/71e/72d/73i folds after "
                 "the landed 76c bit61 fold; all 16 certificates "
                 "extracted, independently verified engine-free and "
                 "published on main"),
        "source": ("raw audit blob 4c13cbb2 (8 sweep + 1 confirmation "
                   "batches, v17) + claim v3 (blob 74fc3417) + "
                   "certificate manifest "
                   "class2-lane-cost73j-win7-certificates-20261117.json "
                   "(blob e88710b5)"),
    },
    "cost73k": {
        "child": CHILD73K,
        "win": AUD73K_WIN,
        "fold": ("PENDING behind the 66i/66j/69j/71e/72d/73i/73j folds; "
                 "all 22 new certificates extracted, independently "
                 "verified engine-free and published on main; the 3 "
                 "confirmation WIN roots (bits 14/26/55) are covered by "
                 "the published cost73j bit 110 / cost73i bit 110 / "
                 "cost69j bit 110 certificates"),
        "source": ("raw audit blob 85f4f73f (third independent "
                   "regeneration, 8 sweep + 1 confirmation batches, "
                   "v17, 73/73 per-bit identical to the concurrent "
                   "record) + claim v3 (blob 7f654548) + certificate "
                   "manifest class2-lane-cost73k-win7-certificates-"
                   "20261117.json (blob 0892aed0)"),
    },
    "cost73l": {
        "child": CHILD73L,
        "win": AUD73L_WIN,
        "fold": ("PENDING behind the 66i/66j/69j/71e/72d/73i/73j/73k "
                 "folds; all 32 new certificates extracted, "
                 "independently verified engine-free, BigInt "
                 "third-implementation re-verified (32/32 PASS, "
                 "reverification blob 547fe617) and published on "
                 "main; the 2 confirmation WIN roots (bits 106/110) "
                 "are covered by the published cost73j bit 118 / "
                 "cost73k bit 98 certificates"),
        "source": ("raw audit blob f2ea2044 (9 sweep batches incl. 1 "
                   "confirmation batch, v17) + claim v3 (blob "
                   "39cf0f9b) + certificate manifest class2-lane-"
                   "cost73l-win7-certificates-20261117.json (blob "
                   "6e0a94ab)"),
    },
    "cost74i": {
        "child": CHILD74I,
        "win": AUD74I_WIN,
        "fold": ("NOT NEEDED: the sweep found 0 WIN7-D10 roots (74/74 "
                 "REFUTED-D10, 0 capped), so this row produces no "
                 "receipts; fully determined at audit strength"),
        "source": ("raw audit blob e5c803ed (8 sweep + 1 confirmation "
                   "batches + 2 det reruns + 2 v15 crosscheck chunks, "
                   "v17) + claim v2 (blob d915e120)"),
    },
    "cost75f": {
        "child": CHILD75F,
        "win": AUD75F_WIN,
        "fold": ("NOT NEEDED: the sweep found 0 WIN7-D10 roots (75/75 "
                 "REFUTED-D10, 0 capped), so this row produces no "
                 "receipts; fully determined at audit strength"),
        "source": ("raw audit blob 0951327a (8 sweep + 1 confirmation "
                   "batches + 2 det reruns + 2 v15 crosscheck chunks, "
                   "v17) + claim v2 (blob 6df1e54d)"),
    },
    "cost78c": {
        "child": CHILD78C,
        "win": AUD78C_WIN,
        "fold": ("PENDING behind the 66i/66j/69j/71e/72d/73i/73j/73k/73l "
                 "folds; all 11 certificates extracted, independently "
                 "verified engine-free (root-check stones=7 + loser "
                 "mobility match, all sub-roots PASS, consumed-union 0 "
                 "missing / 0 extra), determinism re-extraction "
                 "byte-identical on bits 69 and 116, and published on "
                 "main"),
        "source": ("raw audit blob 8e3ee7aa (7x9 + 1x3 open + 1x12 "
                   "confirmation batches, v17, 238,626,461 candidate "
                   "nodes, plus 2 det reruns and 2 v15 crosscheck "
                   "chunks) + claim v5 (blob 18508321, a pin-provenance "
                   "correction over v4) + certificate manifest "
                   "class2-lane-cost78c-win7-certificates-20261117.json "
                   "(blob b7fe519e); the parallel batches-1-6 audit "
                   "(blob 7460b42b, provenance-only republication of "
                   "d8e5f9b7) agrees bit-exactly on its 54 bits"),
    },
    "cost79d": {
        "child": CHILD79D,
        "win": [],
        "fold": ("NOT NEEDED: the sweep found 0 WIN7-D10 roots (79/79 "
                 "REFUTED-D10, 0 capped), so this row produces no "
                 "receipts; fully determined at audit strength (the "
                 "third fully refuted swept row after cost-74i and "
                 "cost-75f)"),
        "source": ("raw audit blob cfc6fbe3 (8x9 open + 1x7 "
                   "confirmation batches, v17, 49,103,515 candidate "
                   "nodes, plus 2 det reruns and 1 v15 crosscheck "
                   "chunk) + claim v2 (blob 8805876f); the twelve raw "
                   "batch files re-audited in this script (79/79 "
                   "per-bit verdicts, node sums and root canons "
                   "agree)"),
    },
    "cost79e": {
        "child": CHILD79E,
        "win": [],
        "fold": (
            "NOT NEEDED: the sweep found 0 WIN7-D10 roots (79/79 "
            "REFUTED-D10, 0 capped), so this row produces no "
            "receipts; fully determined at audit strength (the "
            "FOURTH fully refuted swept row after cost-74i, "
            "cost-75f and cost-79d)"),
        "source": (
            "raw audit blob 4e10e477 (8x9 open + 1x7 "
            "confirmation batches, v17, 74,450,533 candidate "
            "nodes, plus 2 det reruns and 1 v15 crosscheck "
            "chunk) + claim v2 (blob f80e6025); the twelve raw "
            "batch files re-audited in this script (79/79 "
            "per-bit verdicts, node sums and root canons "
            "agree)"),
    },
    "cost80e": {
        "child": CHILD80E,
        "win": [],
        "fold": (
            "NOT NEEDED: the sweep found 0 WIN7-D10 roots (80/80 "
            "REFUTED-D10, 0 capped), so this row produces no "
            "receipts; fully determined at audit strength (the "
            "FIFTH fully refuted swept row after cost-74i, "
            "cost-75f, cost-79d and cost-79e)"),
        "source": (
            "raw audit blob 53007edc (7x9 + 1x5 open + 1x12 "
            "confirmation batches, v17, 87,301,907 candidate "
            "nodes, plus 2 det reruns and 1 v15 crosscheck "
            "chunk) + claim v2 (blob 9190341a); the twelve raw "
            "batch files re-audited in this script (80/80 "
            "per-bit verdicts, node sums and root canons "
            "agree)"),
    },
    "cost79c": {
        "child": CHILD79C,
        "win": AUD79C_WIN,
        "fold": ("PENDING behind the 66i/66j/69j/71e/72d/73i/73j/73k/73l "
                 "folds; all 19 new certificates extracted, "
                 "independently verified engine-free (root-check "
                 "stones=7 + loser mobility match, all sub-roots PASS, "
                 "consumed-union 0 missing / 0 extra), BigInt "
                 "third-implementation PASS on bits [21,30,117,120], "
                 "determinism re-extraction byte-identical on bits 30 "
                 "and 117, and published on main; the 20th WIN bit 110 "
                 "certificate is canon-covered by the published cost73k "
                 "bit 87 certificate (canon equality re-verified in "
                 "this script); the parallel-lane BigInt general-circle "
                 "audit (blob 50190347) PASSes bits [1,2,21]"),
        "source": ("raw audit blob 133f2230 (7x9 + 1x5 open + 1x11 "
                   "confirmation batches, v17, 206,090,979 candidate "
                   "nodes, plus 2 det reruns and 2 v15 crosscheck "
                   "chunks) + claim v2 (blob d16d7b1a) + certificate "
                   "manifest class2-lane-cost79c-win7-certificates-"
                   "20261118.json (blob e904a376); the nine raw batch "
                   "files re-audited in this script (79/79 per-bit "
                   "verdicts, nodes and root canons agree)"),
    },
    "cost80f": {
        "child": CHILD80F,
        "win": [],
        "fold": (
            "NOT NEEDED: the sweep found 0 WIN7-D10 roots (80/80 "
            "REFUTED-D10, 0 capped), so this row produces no "
            "receipts; fully determined at audit strength (the "
            "SIXTH fully refuted swept row after cost-74i, "
            "cost-75f, cost-79d, cost-79e and cost-80e)"),
        "source": (
            "raw audit blob 52abb721 (7x9 + 1x4 open + 1x13 "
            "confirmation batches, v17, 51,125,648 candidate "
            "nodes, plus 2 det reruns and 1 v15 crosscheck "
            "chunk) + claim v2 (blob aed40c10, amended from "
            "e54b24a2 for the confirmation_outcome field); the "
            "twelve raw batch files re-audited in this script "
            "(80/80 per-bit verdicts, node sums and root canons "
            "agree)"),
    },
    "cost81": {
        "child": CHILD81,
        "win": [],
        "fold": (
            "NOT NEEDED: the sweep found 0 WIN7-D10 roots (81/81 "
            "REFUTED-D10, 0 capped), so this row produces no "
            "receipts; fully determined at audit strength (the "
            "SEVENTH fully refuted swept row after cost-74i, "
            "cost-75f, cost-79d, cost-79e, cost-80e and cost-80f; "
            "the first cost-81 band)"),
        "source": (
            "raw audit blob f90bdccd (7x9 + 1x3 open + 1x15 "
            "confirmation batches, v17, 86,480,711 candidate "
            "nodes, plus 2 det reruns and 1 v15 crosscheck "
            "chunk) + claim v2 (blob 5dc33107); the twelve raw "
            "batch files re-audited in this script (81/81 "
            "per-bit verdicts, node sums and root canons "
            "agree)"),
    },
    "cost82d": {
        "child": CHILD82D,
        "win": [],
        "fold": (
            "NOT NEEDED: the sweep found 0 WIN7-D10 roots (82/82 "
            "REFUTED-D10, 0 capped), so this row produces no "
            "receipts; fully determined at audit strength (the "
            "EIGHTH fully refuted swept row after cost-74i, "
            "cost-75f, cost-79d, cost-79e, cost-80e, cost-80f and "
            "cost-81; band cost82d: cost82, cost82b and cost82c "
            "are already used by earlier bands)"),
        "source": (
            "raw audit blob 14a44c8b (7x9 + 1x2 open + 1x17 "
            "confirmation batches, v17, 127,619,232 candidate "
            "nodes, plus 2 det reruns and 1 v15 crosscheck "
            "chunk) + claim v2 (blob cffeda69); the twelve raw "
            "batch files re-audited in this script (82/82 "
            "per-bit verdicts, node sums and root canons "
            "agree)"),
    },
}

new_verdict_maps = {}
new_canon = {}
new_canon_pre73k = {}      # twin without 73k/73l/74i/75f: re-derives v7 counts
new_canon_pre73l = {}      # twin without 73l/74i/75f: re-derives v8 counts
new_canon_pre74i = {}      # twin without 74i/75f: re-derives v9 counts
new_canon_pre75f = {}      # twin without the 75f map: re-derives v10 counts
new_canon_pre78c = {}      # twin without the 78c map: re-derives v11 counts
new_canon_pre79c = {}      # twin without the 79c map: re-derives v12 counts
new_canon_pre79d = {}      # twin without the 79d map: re-derives v13 counts
new_canon_pre79e = {}      # twin without the 79e map: re-derives v14 counts
new_canon_pre80e = {}      # twin without the 80e map: re-derives v15 counts
new_canon_pre80f = {}      # twin without the 80f map: re-derives v16 counts
new_canon_pre81 = {}       # twin without the 81 map: re-derives v17 counts
new_canon_pre82d = {}      # twin without the 82d map: re-derives v18 counts
for name, m in NEW_MAPS.items():
    st, bits = legal_candidates(m["child"])
    cands = sorted(bits)
    wins = sorted(m["win"])
    assert set(wins) <= set(cands), (name, wins)
    refuted = sorted(set(cands) - set(wins))
    child_v = int(m["child"], 16)
    for b_ in cands:
        c = canon(child_v | (1 << b_))
        v = "WIN7-D10" if b_ in set(wins) else "REFUTED-D10"
        e = new_canon.get(c)
        assert e is None or e[0] == v, ("new-map conflict", name, b_, e)
        new_canon[c] = (v, name, b_)
        if name not in ("cost73k", "cost73l", "cost74i", "cost75f",
                        "cost78c", "cost79c", "cost79d", "cost79e", "cost80e", "cost80f", "cost81", "cost82d"):
            new_canon_pre73k[c] = (v, name, b_)
        if name not in ("cost73l", "cost74i", "cost75f", "cost78c",
                        "cost79c", "cost79d", "cost79e", "cost80e", "cost80f", "cost81", "cost82d"):
            new_canon_pre73l[c] = (v, name, b_)
        if name not in ("cost74i", "cost75f", "cost78c", "cost79c",
                        "cost79d", "cost79e", "cost80e", "cost80f", "cost81", "cost82d"):
            new_canon_pre74i[c] = (v, name, b_)
        if name not in ("cost75f", "cost78c", "cost79c", "cost79d",
                        "cost79e", "cost80e", "cost80f", "cost81", "cost82d"):
            new_canon_pre75f[c] = (v, name, b_)
        if name not in ("cost78c", "cost79c", "cost79d", "cost79e", "cost80e", "cost80f", "cost81", "cost82d"):
            new_canon_pre78c[c] = (v, name, b_)
        if name not in ("cost79c", "cost79d", "cost79e", "cost80e", "cost80f", "cost81", "cost82d"):
            new_canon_pre79c[c] = (v, name, b_)
        if name not in ("cost79d", "cost79e", "cost80e", "cost80f", "cost81", "cost82d"):
            new_canon_pre79d[c] = (v, name, b_)
        if name not in ("cost79e", "cost80e", "cost80f", "cost81", "cost82d"):
            new_canon_pre79e[c] = (v, name, b_)
        if name not in ("cost80e", "cost80f", "cost81", "cost82d"):
            new_canon_pre80e[c] = (v, name, b_)
        if name not in ("cost80f", "cost81", "cost82d"):
            new_canon_pre80f[c] = (v, name, b_)
        if name not in ("cost81", "cost82d"):
            new_canon_pre81[c] = (v, name, b_)
        if name != "cost82d":
            new_canon_pre82d[c] = (v, name, b_)
    new_verdict_maps[name] = {
        "child": m["child"], "bits": len(cands),
        "win7_d10_bits": wins, "refuted_d10_bits": refuted,
        "capped": 0, "fold": m["fold"], "source": m["source"]}

# rebuilt-harvest vs new-maps conflict scan
agree_old_new = 0
for c, (v, name, b_) in new_canon.items():
    e = harvest.get(c)
    if e is not None:
        assert e["verdict"] == v, ("harvest/new conflict", name, b_, e)
        agree_old_new += 1
print(f"twenty-two maps: {len(new_canon)} distinct canons, 0 internal "
      f"conflicts, {agree_old_new} canons cross-agree with the rebuilt "
      f"harvest")

# ------------------------------------- 3. per-bit classification machinery
VERDICT = {}
for c, e in harvest.items():
    VERDICT[c] = (e["verdict"], "pre-64h harvest")
for c, (v, name, b_) in new_canon.items():
    VERDICT[c] = (v, name)
HCAN = set(harvest)
NCAN = set(new_canon)


def classify(child_hex, cands):
    """Per-bit {bit: (canon, verdict, source-label)}.

    Source label: map name if the canon is covered by one of the
    twenty-two fresh maps (fresh re-coverage takes display
    precedence),
    else 'pre-64h harvest', else ('open', None).  Counting of
    old-harvest vs newly covered bits must use HCAN/NCAN membership,
    not the label.
    """
    out = {}
    child_v = int(child_hex, 16)
    for b_ in cands:
        c = canon(child_v | (1 << b_))
        out[b_] = (c,) + VERDICT.get(c, ("open", None))
    return out


# 4. v1 bit-table transitions (with per-bit canon cross-check)
bit_tables = V1["bit_tables"]
transition_summary = {}
for child, table in bit_tables.items():
    st, bits = legal_candidates(child)
    cands = sorted(bits)
    assert len(cands) == table["cost"], child
    by_bit = {e["bit"]: e for e in table["bits"]}
    assert sorted(by_bit) == cands, child
    child_v = int(child, 16)
    for b_, e in by_bit.items():
        assert canon(child_v | (1 << b_)) == int(e["root_canon"], 16), \
            (child, b_)
    cls = classify(child, cands)
    for b_, e in by_bit.items():
        _, v, src = cls[b_]
        if e["status"].startswith("harvested"):
            assert v == ("WIN7-D10" if e["status"] == "harvested_win"
                         else "REFUTED-D10"), (child, b_, e, v)
        else:
            assert e["status"] == "open", (child, b_, e)
            if v != "open":
                assert src != "pre-64h harvest", (child, b_, src)
    n_open = sum(1 for c_, v, src in cls.values() if v == "open")
    n_win = sum(1 for c_, v, src in cls.values() if v == "WIN7-D10")
    n_ref = sum(1 for c_, v, src in cls.values()
                if v == "REFUTED-D10")
    transition_summary[child] = {
        "legal": len(cands), "open": n_open,
        "win7_d10": n_win, "refuted_d10": n_ref}

for child, expect in (
        ("00000000000000403800000008100000", (64, 23)),   # 64h
        ("00000000010000809002000001000000", (76, 2)),     # 76c
        ("00000000000000801226000000000000", (66, 9)),     # 66i
        ("00000000000000c09002000000001000", (66, 9)),     # 66j
        ("00000000000000403800000008000020", (69, 6)),     # 69j
        ("00000000000000801282000040000000", (64, 0))):    # 64a
    t = transition_summary[child]
    assert t["open"] == 0, (child, t)
    assert t["win7_d10"] == expect[1], (child, t)
    assert t["legal"] == expect[0], (child, t)
assert transition_summary["00000000000000403800000008000020"][
    "refuted_d10"] == 63
assert transition_summary["00000000000000801282000040000000"][
    "refuted_d10"] == 64
print("v1 bit-table children transitioned:",
      len(transition_summary), "(all root_canon checks passed)")

# ------------------------------------------ 5. families v19 (bit-exact rows)
families_v19 = {}
parent_of = {}
row_checks = []
NCAN7 = set(new_canon_pre73k)
NCAN11 = set(new_canon_pre73l)
NCAN12 = set(new_canon_pre74i)
NCAN13 = set(new_canon_pre75f)
NCAN14 = set(new_canon_pre78c)
NCAN15 = set(new_canon_pre79c)
NCAN16 = set(new_canon_pre79d)
NCAN17 = set(new_canon_pre79e)
NCAN18 = set(new_canon_pre80e)
NCAN19 = set(new_canon_pre80f)
NCAN20 = set(new_canon_pre81)
NCAN21 = set(new_canon_pre82d)
for fam, rows in V18["families_v18"].items():
    out_rows = []
    for row in rows:
        child = row["s6_hex"]
        parent_of[child] = fam
        t = bit_tables.get(child)
        if t is not None:
            assert t["parent"] == fam, (child, t["parent"], fam)
            assert t["cost"] == row["cost"], child
        st, bits = legal_candidates(child)
        cands = sorted(bits)
        assert len(cands) == row["cost"], (child, row)
        cls = classify(child, cands)
        n_open = sum(1 for c_, v, src in cls.values() if v == "open")
        v1_harv = (row["census"].get("harvested_refuted", 0)
                   + row["census"].get("harvested_win", 0)
                   + row["census"].get("receipt_win", 0))
        n_old = sum(1 for c_, v, src in cls.values() if c_ in HCAN)
        n_new = sum(1 for c_, v, src in cls.values()
                    if c_ in NCAN and c_ not in HCAN)
        n_new_v7 = sum(1 for c_, v, src in cls.values()
                       if c_ in NCAN7 and c_ not in HCAN)
        n_new_v8 = sum(1 for c_, v, src in cls.values()
                       if c_ in NCAN11 and c_ not in HCAN)
        n_new_v9 = sum(1 for c_, v, src in cls.values()
                       if c_ in NCAN12 and c_ not in HCAN)
        n_new_v10 = sum(1 for c_, v, src in cls.values()
                        if c_ in NCAN13 and c_ not in HCAN)
        n_new_v11 = sum(1 for c_, v, src in cls.values()
                       if c_ in NCAN14 and c_ not in HCAN)
        n_new_v12 = sum(1 for c_, v, src in cls.values()
                        if c_ in NCAN15 and c_ not in HCAN)
        n_new_v13 = sum(1 for c_, v, src in cls.values()
                        if c_ in NCAN16 and c_ not in HCAN)
        n_new_v14 = sum(1 for c_, v, src in cls.values()
                        if c_ in NCAN17 and c_ not in HCAN)
        n_new_v15 = sum(1 for c_, v, src in cls.values()
                        if c_ in NCAN18 and c_ not in HCAN)
        n_new_v16 = sum(1 for c_, v, src in cls.values()
                        if c_ in NCAN19 and c_ not in HCAN)
        n_new_v17 = sum(1 for c_, v, src in cls.values()
                        if c_ in NCAN20 and c_ not in HCAN)
        n_new_v18 = sum(1 for c_, v, src in cls.values()
                        if c_ in NCAN21 and c_ not in HCAN)
        n_79c = n_new - n_new_v12
        assert n_old == v1_harv, (child, n_old, v1_harv)
        assert n_new_v7 == row["newly_covered_by_ten_maps"], \
            (child, n_new_v7, row["newly_covered_by_ten_maps"])
        assert n_new_v8 == row["newly_covered_by_eleven_maps"], \
            (child, n_new_v8, row["newly_covered_by_eleven_maps"])
        assert n_new_v9 == row["newly_covered_by_twelve_maps"], \
            (child, n_new_v9, row["newly_covered_by_twelve_maps"])
        assert n_new_v10 == row["newly_covered_by_thirteen_maps"], \
            (child, n_new_v10, row["newly_covered_by_thirteen_maps"])
        assert n_new_v11 == row["newly_covered_by_fourteen_maps"], \
            (child, n_new_v11, row["newly_covered_by_fourteen_maps"])
        assert n_new_v12 == row["newly_covered_by_fifteen_maps"], \
            (child, n_new_v12, row["newly_covered_by_fifteen_maps"])
        assert n_new_v13 == row["newly_covered_by_sixteen_maps"], \
            (child, n_new_v13, row["newly_covered_by_sixteen_maps"])
        assert n_new_v14 == row["newly_covered_by_seventeen_maps"], \
            (child, n_new_v14, row["newly_covered_by_seventeen_maps"])
        assert n_new_v15 == row["newly_covered_by_eighteen_maps"], \
            (child, n_new_v15, row["newly_covered_by_eighteen_maps"])
        assert n_new_v16 == row["newly_covered_by_nineteen_maps"], \
            (child, n_new_v16, row["newly_covered_by_nineteen_maps"])
        assert n_new_v17 == row["newly_covered_by_twenty_maps"], \
            (child, n_new_v17, row["newly_covered_by_twenty_maps"])
        assert n_new_v18 == row["newly_covered_by_twenty_one_maps"], \
            (child, n_new_v18, row["newly_covered_by_twenty_one_maps"])
        n_79d = n_new - n_new_v13
        n_79e = n_new - n_new_v14
        n_80e = n_new - n_new_v15
        n_80f = n_new - n_new_v16
        n_81 = n_new - n_new_v17
        n_82d = n_new - n_new_v18
        assert n_open == len(cands) - n_old - n_new, child
        assert n_open == row["open_after_census_v18"] - n_82d, \
            (child, n_open, row["open_after_census_v18"], n_82d)
        if "excluded" not in row:
            assert n_open <= row["open_after_census_v18"], child
        new_row = dict(row)
        new_row["open_after_census_v19"] = n_open
        new_row["known_verdict_bits_v19"] = n_old + n_new
        new_row["newly_covered_by_twenty_two_maps"] = n_new
        out_rows.append(new_row)
        row_checks.append((child, n_open, n_new, n_82d))
    families_v19[fam] = out_rows

# the 73k / 73j / 76c / 64a / 73l / 74i / 75f / 78c / 79c / 79d
# / 79e / 80e exclusions are carried verbatim from the
# v13/v14/v15/v16/v17/v18 census rows; mark the newly swept
# 81/82d rows
for fam, rows in families_v19.items():
    for row in rows:
        if row["s6_hex"] == "00000000000000801206000000000400":
            assert "excluded" in row and "cost-73k complete" \
                in row["excluded"], row["excluded"][:60]
            assert row["open_after_census_v10"] == 0
        if row["s6_hex"] == "00000000000000403800000408000000":
            assert "excluded" in row and "cost-73j complete" \
                in row["excluded"], row["excluded"][:60]
        if row["s6_hex"] == "00000000010000809002000001000000":
            assert "excluded" in row and "fold LANDED" \
                in row["excluded"], row["excluded"][:60]
            assert row["open_after_census_v10"] == 0
        if row["s6_hex"] == "00000000000000c09002000000400000":
            assert "excluded" in row and "cost-73l complete" \
                in row["excluded"], row["excluded"][:60]
            assert row["open_after_census_v11"] == 0
        if row["s6_hex"] == "00000000020000003800000088000000":
            assert "excluded" in row and "cost-74i complete" \
                in row["excluded"], row["excluded"][:60]
            assert row["open_after_census_v11"] == 0
        if row["s6_hex"] == "00000000020000003800020080000000":
            assert "excluded" in row and "cost-75f complete" \
                in row["excluded"], row["excluded"][:60]
            assert row["open_after_census_v11"] == 0
        if row["s6_hex"] == "00000000000000403800000008000008":
            assert "excluded" in row and "cost-78c complete" \
                in row["excluded"], row["excluded"][:60]
            assert row["open_after_census_v12"] == 0
        if row["s6_hex"] == "00000000000000c09002000200000000":
            assert "excluded" in row and "cost-79c complete" \
                in row["excluded"], row["excluded"][:60]
            assert row["newly_covered_by_eighteen_maps"] >= 68
            assert row["open_after_census_v14"] == 0
        if row["s6_hex"] == "00000000020000003800400080000000":
            assert "excluded" in row and "cost-79d complete" \
                in row["excluded"], row["excluded"][:60]
            assert row["open_after_census_v14"] == 0
        if row["s6_hex"] == "00000000020000003800000880000000":
            assert "excluded" in row and "cost-79e complete" \
                in row["excluded"], row["excluded"][:60]
            assert row["open_after_census_v15"] == 0
        if row["s6_hex"] == "00000000020000003800000180000000":
            assert "excluded" in row and "cost-80e complete" \
                in row["excluded"], row["excluded"][:60]
            assert row["newly_covered_by_nineteen_maps"] == 76
            assert row["open_after_census_v16"] == 0
        if row["s6_hex"] == "00000000020000003800200080000000":
            assert "excluded" in row and "cost-80f complete" \
                in row["excluded"], row["excluded"][:60]
            assert row["newly_covered_by_twenty_maps"] == 76
            assert row["open_after_census_v17"] == 0
        if row["s6_hex"] == "00000000020000003800000080008000":
            assert "excluded" in row and "cost-81 complete" \
                in row["excluded"], row["excluded"][:60]
            assert row["newly_covered_by_twenty_one_maps"] == 78
            assert row["open_after_census_v18"] == 0
        if row["s6_hex"] == "00000000020000003800000080000800":
            assert "excluded" not in row
            assert row["newly_covered_by_twenty_two_maps"] == 78
            row["excluded"] = (
                "swept child (cost-82d complete: 0 WIN7-D10 + 82 "
                "REFUTED-D10, 0 capped; the EIGHTH fully refuted "
                "swept row of the presweep-1473 band after "
                "cost-74i, cost-75f, cost-79d, cost-79e, "
                "cost-80e, cost-80f and cost-81; band cost82d "
                "(cost82, cost82b and cost82c are already used "
                "by earlier bands); no WIN7-D10 certificate "
                "exists so the receipt fold is not needed; the "
                "twelve raw batch files are re-audited in this "
                "census script (82/82 verdicts, node sums, "
                "det/v15 agreements and root canons); fully "
                "determined at audit strength)")
            assert row["open_after_census_v19"] == 0
print("family rows recomputed bit-exactly:", len(row_checks))

# --------------------------------------------------- 6. ranking and selection
def sort_key(r):
    return (r["cost"], r["open_after_census_v19"], r["s6_hex"])


pool = [r for fam in families_v19.values() for r in fam
        if "excluded" not in r]
pool.sort(key=sort_key)
# the entire remaining unswept pool after the 82d sweep is 8 rows,
# all children of the single family parent
# 00000000020000003800000080000000 (the presweep-1473 frontier)
ranking = list(pool)
assert len(ranking) == 8
assert {parent_of[r["s6_hex"]] for r in ranking} == \
    {"00000000020000003800000080000000"}
v18_rank_hexes = [r["s6_hex"] for r in V18["ranking_top10"]]
swept_now = {"00000000020000003800000080000800"}
kept8 = [h for h in v18_rank_hexes if h not in swept_now]
assert len(kept8) == 8
v19_hexes = {r["s6_hex"] for r in ranking}
for h in kept8:
    assert h in v19_hexes, ("v18 ranking row fell out of v19 top10", h)

sel = ranking[0]
assert sel["cost"] == 82, sel
assert sel["s6_hex"] == "00000000020000003800000090000000", sel
assert sel["open_after_census_v19"] <= 67, sel
st, bits = legal_candidates(sel["s6_hex"])
cands = sorted(bits)
assert len(cands) == sel["cost"]
cls = classify(sel["s6_hex"], cands)
sweep_bits = [b_ for b_ in cands if cls[b_][1] == "open"]
confirmation = [{"bit": b_, "verdict": cls[b_][1],
                 "equivalent": cls[b_][2]}
                for b_ in cands if cls[b_][1] != "open"]
assert len(sweep_bits) + len(confirmation) == sel["cost"]
assert len(sweep_bits) == sel["open_after_census_v19"]
runner_up = ranking[1]

print(f"selected: {sel['s6_hex']} cost {sel['cost']} "
      f"open {len(sweep_bits)} confirm {len(confirmation)} "
      f"parent {parent_of[sel['s6_hex']]}")
for c in confirmation:
    print(f"  confirmation bit {c['bit']}: {c['verdict']} "
          f"(= {c['equivalent']})")
print(f"runner-up: {runner_up['s6_hex']} cost {runner_up['cost']} "
      f"open {runner_up['open_after_census_v19']}")
for r in ranking:
    print(f"  rank: cost {r['cost']} open {r['open_after_census_v19']} "
          f"{r['s6_hex']} parent {parent_of[r['s6_hex']]}")

# ------------------------------------------------------------- 7. output
out = {
    "schema": "n11-class2-lane-next-target-presweep-1473-v19-20261118-v1",
    "date": "2026-11-18",
    "chain_head": "1473/174/6375/504596/4648/368510",
    "baseline": {
        "v1_census_json":
            "class2-lane-next-target-presweep-1452-20261116.json "
            "(git blob 0d9a94a272de9fe45708757f17bfea60239a3c9b)",
        "v4_census_json":
            "class2-lane-next-target-presweep-1472-v4-20261117.json "
            "(git blob d70eae093e80d19660eae314bd761c21085995bb)",
        "v5_census_json":
            "class2-lane-next-target-presweep-1472-v5-20261117.json "
            "(git blob ea85c02319350b5953e0e70c3eb812fb78bbf17c)",
        "v6_census_json":
            "class2-lane-next-target-presweep-1472-v6-20261117.json "
            "(git blob c45fc0d118b7222f1e0c5d79227adc3f7ab9d1cb)",
        "v7_census_json":
            "class2-lane-next-target-presweep-1472-v7-20261117.json "
            "(git blob 68246f3263fe6cbb49ffafa866f73b49cf3c2ebb)",
        "v8_census_json":
            "class2-lane-next-target-presweep-1473-v8-20261117.json "
            "(git blob 2542914e02db14a8426a1a16ef1c2cfcd9817375)",
        "v9_census_json":
            "class2-lane-next-target-presweep-1473-v9-20261117.json "
            "(git blob af1d609490472b916eb6991e7864be98af60e9b9)",
        "v10_census_json":
            "class2-lane-next-target-presweep-1473-v10-20261117.json "
            "(git blob fc2509f0bfa49359a3053289a9af1244cafcd950)",
        "v11_census_json":
            "class2-lane-next-target-presweep-1473-v11-20261117.json "
            "(git blob 1e2b6a2b688db1a93098edea62b5793b54efaaba)",
        "v12_census_json":
            "class2-lane-next-target-presweep-1473-v12-20261118.json "
            "(git blob 8e64d55250242a557c954ad5bad8c993bacd354b)",
        "v13_census_json":
            "class2-lane-next-target-presweep-1473-v13-20261118.json "
            "(git blob fdb94e31ed2fd83ba8104f65c4f55dd2726c3bd8, "
            "commit 1306ac34)",
        "v14_census_json":
            "class2-lane-next-target-presweep-1473-v14-20261118.json "
            "(git blob 628e6d4e988ab50bc46e7f90bd4bd3c8c62830b1, "
            "commit 4584fa77)",
        "v15_census_json":
            "class2-lane-next-target-presweep-1473-v15-20261118.json "
            "(git blob dfb61db5bec195f3f98442815753ba88d9e96fff, "
            "commit 444ab1d7)",
        "v16_census_json":
            "class2-lane-next-target-presweep-1473-v16-20261118.json "
            "(git blob 972434a4ca5df21174dc1034ac35d118fca37fc1, "
            "commit 9e2732d5)",
        "v17_census_json":
            "class2-lane-next-target-presweep-1473-v17-20261118.json "
            "(git blob 22078142d6d616335bc1bc363065d91750b6ca14, "
            "commit 689c42d6)",
        "v18_census_json":
            "class2-lane-next-target-presweep-1473-v18-20261118.json "
            "(git blob 11306824f2363d5002559d4d1535d91a61509929, "
            "commit b1ba66fd)",
        "cost76c_fold_receipt":
            "class-frontier-cost76c-receipts-recompute-20261117.json "
            "(git blob 953beaea054989e8b1de33f48b1f2ebc13ae7e11; "
            "frontier_after [1473, 174, 6375, 504596, 4648, 368510])",
        "note": ("v1 head-1452 bit statuses + rebuilt harvest carried "
                 "over; v4 overlays 64h/76c/66i/66j; v5 adds 69j + the "
                 "64a STERILE correction; v6 adds the completed 71e / "
                 "72d / 73i verdict maps; v7 adds the completed 73j "
                 "verdict map; v8 adds the completed 73k verdict map, "
                 "the LANDED 76c bit61 fold (canonical head 1473) and "
                 "recomputes all family rows bit-exactly; v9 adds the "
                 "completed 73l verdict map (with its 32 published and "
                 "BigInt-re-verified certificates) and recomputes all "
                 "family rows bit-exactly at the unchanged head 1473; "
             "v10 adds the completed 74i verdict map (the first fully "
             "refuted sweep row: 0 WIN7-D10 / 74 REFUTED-D10 / 0 capped, "
             "audit strength only, no certificates and no receipt fold "
             "needed) and recomputes all family rows bit-exactly at the "
             "unchanged head 1473; v11 adds the completed 75f verdict "
             "map (the SECOND fully refuted sweep row: 0 WIN7-D10 / 75 "
             "REFUTED-D10 / 0 capped, audit strength only, no "
             "certificates and no receipt fold needed) and recomputes "
             "all family rows bit-exactly at the unchanged head 1473; "
             "v12 adds the completed 78c verdict map (the first "
             "WIN-bearing swept row of the presweep-1473 band: 11 "
             "WIN7-D10 with all 11 certificates published on main "
             "(manifest git blob b7fe519e) and independently verified "
             "engine-free, 67 REFUTED-D10, 0 capped; receipt fold "
             "pending behind the 66i/66j/69j/71e/72d/73i/73j/73k/73l "
             "folds) and recomputes all family rows bit-exactly at "
             "the unchanged head 1473; "
             "v13 adds the completed 79c verdict map (the second "
             "WIN-bearing swept row of the presweep-1473 band: 20 "
             "WIN7-D10 with all 19 new certificates published on "
             "main (manifest git blob e904a376) and independently "
             "verified engine-free plus the canon-covered bit 110, "
             "59 REFUTED-D10, 0 capped; the nine raw batch files "
             "re-audited in this script; receipt fold pending "
             "behind the 66i/66j/69j/71e/72d/73i/73j/73k/73l folds) "
             "and recomputes all family rows bit-exactly at the "
             "unchanged head 1473; "
             "v14 adds the completed 79d verdict map (the THIRD "
             "fully refuted swept row of the presweep-1473 band "
             "after cost-74i and cost-75f: 0 WIN7-D10 / 79 "
             "REFUTED-D10 / 0 capped, 49,103,515 candidate nodes, "
             "raw audit git blob cfc6fbe3, claim v2 git blob "
             "8805876f; no certificate and no receipt fold needed; "
             "the twelve raw batch files re-audited in this "
             "script) and recomputes all family rows bit-exactly "
             "at the unchanged head 1473; the synced cost-79c "
             "claim v2 (git blob ca517b73, commit 8a335959) now "
             "carries the full 19/19 BigInt general-circle "
             "third-audit corpus (blobs 50190347 + 410fb935); "
             "v15 adds the completed 79e verdict map (the FOURTH "
             "fully refuted swept row of the presweep-1473 band "
             "after cost-74i, cost-75f and cost-79d: 0 WIN7-D10 / "
             "79 REFUTED-D10 / 0 capped, 74,450,533 candidate "
             "nodes, raw audit git blob 4e10e477, claim v2 git "
             "blob f80e6025, commit 4bc11450; no certificate and "
             "no receipt fold needed; the twelve raw batch files "
             "re-audited in this script) and recomputes all "
             "family rows bit-exactly at the unchanged head 1473; "
             "v16 adds the completed 80e verdict map (the FIFTH "
             "fully refuted swept row of the presweep-1473 band "
             "after cost-74i, cost-75f, cost-79d and cost-79e: 0 "
             "WIN7-D10 / 80 REFUTED-D10 / 0 capped, 87,301,907 "
             "candidate nodes, raw audit git blob 53007edc, claim "
             "v2 git blob 9190341a, commit 72769e1e; no certificate "
             "and no receipt fold needed; the twelve raw batch "
             "files re-audited in this script) and recomputes all "
             "family rows bit-exactly at the unchanged head 1473; "
             "v17 adds the completed 80f verdict map (the SIXTH "
             "fully refuted swept row of the presweep-1473 band "
             "after cost-74i, cost-75f, cost-79d, cost-79e and "
             "cost-80e: 0 WIN7-D10 / 80 REFUTED-D10 / 0 capped, "
             "51,125,648 candidate nodes, raw audit git blob "
             "52abb721, claim v2 git blob aed40c10 (amended from "
             "e54b24a2 for the confirmation_outcome field), "
             "commits 77990039 / b2c01968; no certificate and no "
             "receipt fold needed; the twelve raw batch files "
             "re-audited in this script) and recomputes all "
             "family rows bit-exactly at the unchanged head 1473; "
             "v18 adds the completed 81 verdict map (the SEVENTH "
             "fully refuted swept row of the presweep-1473 band "
             "after cost-74i, cost-75f, cost-79d, cost-79e, "
             "cost-80e and cost-80f: 0 WIN7-D10 / 81 REFUTED-D10 / "
             "0 capped, 86,480,711 candidate nodes, raw audit git "
             "blob f90bdccd, claim v2 git blob 5dc33107, commit "
             "92e6c84d; the first cost-81 band; no certificate and "
             "no receipt fold needed; the twelve raw batch files "
             "re-audited in this script) and recomputes all "
             "family rows bit-exactly at the unchanged head 1473; "
             "v19 adds the completed 82d verdict map (the EIGHTH "
             "fully refuted swept row of the presweep-1473 band "
             "after cost-74i, cost-75f, cost-79d, cost-79e, "
             "cost-80e, cost-80f and cost-81: 0 WIN7-D10 / 82 "
             "REFUTED-D10 / 0 capped, 127,619,232 candidate nodes, "
             "raw audit git blob 14a44c8b, claim v2 git blob "
             "cffeda69, commit 775277b5; band cost82d; no "
             "certificate and no receipt fold needed; the twelve "
             "raw batch files re-audited in this script) and "
             "recomputes all family rows bit-exactly at the "
             "unchanged head 1473"),
    },
    "rebuilt_harvest": {
        "sources": harvest_sources,
        "glob_files": glob_files,
        "raw_batch_files": 20,
        "distinct_verdict_canons": harvest_n,
        "win7_d10": harvest_win,
        "refuted_d10": harvest_ref,
        "conflicts": 0,
        "pin_policy": ("77 glob-file pins carried inside the pinned v1 "
                       "census harvest.files list; 101 raw-batch pins "
                       "embedded in this script (20 76d/77e harvest "
                       "ingest + 9 cost-79c re-audit + 12 cost-79d "
                       "re-audit + 12 cost-79e re-audit + 12 cost-80e "
                       "re-audit + 12 cost-80f re-audit + 12 cost-81 "
                       "re-audit + 12 cost-82d re-audit; all "
                       "verified identical on main)"),
    },
    "new_verdict_maps": new_verdict_maps,
    "cross_checks": {
        "harvest_rebuild_matches_v1_counts": True,
        "source_candidate_lists_match_independent_enumeration": "77/77",
        "69j_win_bits_claim_audit_manifest_agreement": "6/6",
        "71e_win_bits_claim_audit_manifest_agreement": "13/13",
        "72d_win_bits_claim_audit_manifest_agreement": "11/11",
        "73i_audit_winbits_subset_of_claim_v1_open_bits": True,
        "73i_confirmation_bits_match_claim": "5/5",
        "73j_win_bits_claim_audit_manifest_agreement": "16/16",
        "73j_manifest_totals": {
            "rows": 726778, "extraction_nodes": 166238087,
            "published_bytes": 26236851, "fbt_drops_total": 0,
            "capped_per_move_total": 0},
        "73j_confirmation_bits_refuted_d10": "7/7",
        "73j_raw_batch_pins_claim_audit_agreement": "9/9",
        "73k_win_bits_claim_audit_agreement": "25/25",
        "73k_manifest_bits_are_win_minus_transfers": "22 = 25 - {14,26,55}",
        "73k_manifest_totals": {
            "rows": 966535, "extraction_nodes": 155946109,
            "published_bytes": 34933538, "fbt_drops_total": 0,
            "capped_per_move_total": 0},
        "73k_confirmation_bits_match_claim": "7/7",
        "73k_audit_per_bit_identical_to_concurrent_record":
            "73/73 (loss, nodes, capped)",
        "73l_win_bits_claim_audit_agreement": "34/34",
        "73l_manifest_bits_are_win_minus_transfers":
            "32 = 34 - {106,110}",
        "73l_manifest_totals": {
            "rows": 1693203, "extraction_nodes": 424657112,
            "published_bytes": 61171191, "fbt_drops_total": 0,
            "capped_per_move_total": 0},
        "73l_confirmation_bits_match_claim": "7/7",
        "73l_bigint_third_implementation_reverification":
            "32/32 PASS (reverification JSON git blob 547fe617; "
            "BigInt-verified certificate population now 381)",
        "73l_v15_cross_engine_win_agreement": "34/34 loss=true",
        "74i_refuted_bits_claim_audit_agreement": "74/74",
        "74i_win_bits": "0/0 (no winning 7th stone within depth 10)",
        "74i_confirmation_bits_match_claim": "5/5",
        "74i_confirmation_bits_refuted_d10": "5/5",
        "74i_v15_cross_engine_refuted_agreement": "10/10 loss=false",
        "74i_determinism_rerun":
            "field-identical on every non-ms field",
        "74i_receipt_fold": "not needed (0 win bits)",
        "74i_certificates": "not applicable (0 win bits)",
        "75f_refuted_bits_claim_audit_agreement": "75/75",
        "75f_win_bits": "0/0 (no winning 7th stone within depth 10)",
        "75f_confirmation_bits_match_claim": "4/4",
        "75f_confirmation_bits_refuted_d10": "4/4",
        "75f_v15_cross_engine_refuted_agreement": "9/9 loss=false",
        "75f_determinism_rerun":
            "field-identical on every non-ms field",
        "75f_receipt_fold": "not needed (0 win bits)",
        "75f_certificates": "not applicable (0 win bits)",
        "78c_win_bits_claim_audit_manifest_agreement": "11/11",
        "78c_manifest_roots_are_child_or_bit": True,
        "78c_manifest_totals": {
            "rows": 614003, "extraction_nodes": 77967826,
            "published_bytes": 22223603, "fbt_drops_total": 0,
            "capped_per_move_total": 0},
        "78c_confirmation_bits_match_claim": "12/12",
        "78c_confirmation_bits_refuted_d10": "12/12",
        "78c_confirmation_transfer_sources_reverified":
            "6 raw-identical + 6 canon-equal (fresh sweep verdicts "
            "match all twelve source verdicts)",
        "78c_v15_cross_engine_win_agreement":
            "17/17 (16 loss=false + 1 loss=true at WIN bit 116)",
        "78c_determinism":
            "fresh-process re-extraction byte-identical on bits "
            "[69, 116]; raw-batch det reruns field-identical",
        "78c_parallel_batches_1_6_audit_agreement":
            "54/54 per-bit verdicts agree (9 WIN / 45 REFUTED; git "
            "blob 7460b42b, the provenance-only 321ccf06 republication "
            "of the d8e5f9b7 version)",
        "78c_receipt_fold":
            "pending behind the 66i/66j/69j/71e/72d/73i/73j/73k/73l "
            "folds",
        "78c_certificates":
            "11/11 published (manifest git blob b7fe519e, band "
            "commits b359756f..97650e27) and engine-free verified",
        "79c_win_bits_claim_audit_manifest_agreement":
            "20/20 win, manifest 19 = 20 - canon-transfer bit 110",
        "79c_raw_batch_reaudit": "9 batches, 9x3402 pilot controls, "
            "79/79 per-bit verdicts + node sums + root canons agree "
            "with the published audit (git blob 133f2230)",
        "79c_manifest_roots_are_child_or_bit": True,
        "79c_manifest_totals": {
            "rows": 1106127, "extraction_nodes": 339101130,
            "published_bytes": 39877889, "fbt_drops_total": 0,
            "capped_per_move_total": 0},
        "79c_bit110_canon_covered_by_73k_bit87": True,
        "79c_confirmation_bits_match_claim": "11/11",
        "79c_confirmation_bits_outcome": "10 REFUTED-D10 + WIN bit 110 "
            "(census v12 overlay prediction matched 11/11, 0 "
            "conflicts)",
        "79c_v15_cross_engine_agreement": "14/14 (confirmation 11/11 "
            "+ heavy open chunk [116,92,117] 3/3)",
        "79c_determinism":
            "fresh-process re-extraction byte-identical on bits "
            "[30, 117]; raw-batch det reruns field-identical",
        "79c_bigint_third_implementation": "bits [21,30,117,120] "
            "PASS (record git blob ed8ec44d)",
        "79c_parallel_general_circle_third_audit":
            "bits [1,2,21] PASS (record git blob 50190347)",
        "79c_receipt_fold":
            "pending behind the 66i/66j/69j/71e/72d/73i/73j/73k/73l "
            "folds",
        "79c_certificates":
            "19/19 published (manifest git blob e904a376, band "
            "commits 462448cd..d9a9b575) and engine-free verified",
        "79c_bigint_full_corpus": "19/19 third-implementation audited "
            "(parallel bits [1,2,21] blob 50190347 + long-term-lane "
            "remaining 16 bits blob 410fb935; synced claim git blob "
            "ca517b73)",
        "79d_refuted_bits_claim_audit_agreement": "79/79",
        "79d_win_bits": "0/0 (no winning 7th stone within depth 10)",
        "79d_raw_batch_reaudit": "12 files (9 sweep + 2 det + 1 v15), "
            "9x3402 + 1x5949 pilot controls, 79/79 per-bit verdicts "
            "+ node sum 49,103,515 + root canons agree with the "
            "published audit (git blob cfc6fbe3)",
        "79d_confirmation_bits_match_claim": "7/7",
        "79d_confirmation_bits_refuted_d10": "7/7",
        "79d_confirmation_root_canons_match_census_v13_transfers": True,
        "79d_v15_cross_engine_refuted_agreement": "7/7 loss=false",
        "79d_determinism_rerun":
            "field-identical on every non-ms field (batches 1 and 8)",
        "79d_receipt_fold": "not needed (0 win bits)",
        "79d_certificates": "not applicable (0 win bits)",
        "79e_refuted_bits_claim_audit_agreement": "79/79",
        "79e_win_bits": "0/0 (no winning 7th stone within depth 10)",
        "79e_raw_batch_reaudit": "12 files (9 sweep + 2 det + 1 v15), "
            "9x3402 + 1x5949 pilot controls, 79/79 per-bit verdicts "
            "+ node sum 74,450,533 + root canons agree with the "
            "published audit (git blob 4e10e477)",
        "79e_confirmation_bits_match_claim": "7/7",
        "79e_confirmation_bits_refuted_d10": "7/7",
        "79e_confirmation_root_canons_match_census_v14_transfers": True,
        "79e_v15_cross_engine_refuted_agreement": "7/7 loss=false",
        "79e_determinism_rerun":
            "field-identical on every non-ms field (batches 1 and 8)",
        "79e_receipt_fold": "not needed (0 win bits)",
        "79e_certificates": "not applicable (0 win bits)",
        "80e_refuted_bits_claim_audit_agreement": "80/80",
        "80e_win_bits": "0/0 (no winning 7th stone within depth 10)",
        "80e_raw_batch_reaudit": "12 files (9 sweep + 2 det + 1 v15), "
            "9x3402 + 1x5949 pilot controls, 80/80 per-bit verdicts "
            "+ node sum 87,301,907 + root canons agree with the "
            "published audit (git blob 53007edc)",
        "80e_confirmation_bits_match_claim": "12/12",
        "80e_confirmation_bits_refuted_d10": "12/12",
        "80e_confirmation_root_canons_match_census_v15_transfers":
            True,
        "80e_v15_cross_engine_refuted_agreement": "12/12 loss=false",
        "80e_determinism_rerun":
            "field-identical on every non-ms field (batches 1 and 8)",
        "80e_receipt_fold": "not needed (0 win bits)",
        "80e_certificates": "not applicable (0 win bits)",
        "80f_refuted_bits_claim_audit_agreement": "80/80",
        "80f_win_bits": "0/0 (no winning 7th stone within depth 10)",
        "80f_raw_batch_reaudit": "12 files (9 sweep + 2 det + 1 v15), "
            "9x3402 + 1x5949 pilot controls, 80/80 per-bit verdicts "
            "+ node sum 51,125,648 + root canons agree with the "
            "published audit (git blob 52abb721)",
        "80f_confirmation_bits_match_claim": "13/13",
        "80f_confirmation_bits_refuted_d10": "13/13",
        "80f_confirmation_root_canons_match_census_v16_transfers":
            True,
        "80f_v15_cross_engine_refuted_agreement": "13/13 loss=false",
        "80f_determinism_rerun":
            "field-identical on every non-ms field (batches 1 and 8)",
        "80f_receipt_fold": "not needed (0 win bits)",
        "80f_certificates": "not applicable (0 win bits)",
        "81_refuted_bits_claim_audit_agreement": "81/81",
        "81_win_bits": "0/0 (no winning 7th stone within depth 10)",
        "81_raw_batch_reaudit": "12 files (9 sweep + 2 det + 1 v15), "
            "9x3402 + 1x5949 pilot controls, 81/81 per-bit verdicts "
            "+ node sum 86,480,711 + root canons agree with the "
            "published audit (git blob f90bdccd)",
        "81_confirmation_bits_match_claim": "15/15",
        "81_confirmation_bits_refuted_d10": "15/15",
        "81_confirmation_root_canons_match_census_v17_transfers":
            True,
        "81_v15_cross_engine_refuted_agreement": "15/15 loss=false",
        "81_determinism_rerun":
            "field-identical on every non-ms field (batches 1 and 8)",
        "81_receipt_fold": "not needed (0 win bits)",
        "81_certificates": "not applicable (0 win bits)",
        "82d_refuted_bits_claim_audit_agreement": "82/82",
        "82d_win_bits": "0/0 (no winning 7th stone within depth 10)",
        "82d_raw_batch_reaudit": "12 files (9 sweep + 2 det + 1 v15), "
            "9x3402 + 1x5949 pilot controls, 82/82 per-bit verdicts "
            "+ node sum 127,619,232 + root canons agree with the "
            "published audit (git blob 14a44c8b)",
        "82d_confirmation_bits_match_claim": "17/17",
        "82d_confirmation_bits_refuted_d10": "17/17",
        "82d_confirmation_root_canons_match_census_v18_transfers":
            True,
        "82d_v15_cross_engine_refuted_agreement": "17/17 loss=false",
        "82d_determinism_rerun":
            "field-identical on every non-ms field (batches 1 and 8)",
        "82d_receipt_fold": "not needed (0 win bits)",
        "82d_certificates": "not applicable (0 win bits)",
        "73i_win_certificates_published_on_main_at_v9_time": False,
        "cost76c_fold_receipt_frontier_after":
            [1473, 174, 6375, 504596, 4648, 368510],
        "64a_v19_recheck_verdicts": RC64A,
        "twenty_two_map_internal_conflicts": 0,
        "harvest_vs_twenty_two_map_conflicts": 0,
        "harvest_vs_twenty_two_map_cross_agreements": agree_old_new,
        "v1_bit_table_children_transitioned": len(bit_tables),
        "v1_bit_table_root_canon_checks": sum(
            t["cost"] for t in bit_tables.values()),
        "fully_swept_children_open_zero": 22,
        "family_rows_recomputed_bit_exactly": len(row_checks),
        "family_row_v1_harvest_count_agreement": "39/39",
        "family_row_v10_newly_covered_counts_reproduced": "39/39",
        "family_row_v11_newly_covered_counts_reproduced": "39/39",
        "family_row_open_v10_minus_75f_only_reproduced": "39/39",
        "family_row_open_v11_minus_78c_only_reproduced": "39/39",
        "family_row_open_v12_minus_79c_only_reproduced": "39/39",
        "family_row_open_v13_minus_79d_only_reproduced": "39/39",
        "family_row_v14_newly_covered_counts_reproduced": "39/39",
        "family_row_open_v14_minus_79e_only_reproduced": "39/39",
        "family_row_v15_newly_covered_counts_reproduced": "39/39",
        "family_row_open_v15_minus_80e_only_reproduced": "39/39",
        "family_row_v16_newly_covered_counts_reproduced": "39/39",
        "family_row_open_v16_minus_80f_only_reproduced": "39/39",
        "family_row_v17_newly_covered_counts_reproduced": "39/39",
        "family_row_open_v17_minus_81_only_reproduced": "39/39",
        "family_row_v18_newly_covered_counts_reproduced": "39/39",
        "family_row_open_v18_minus_82d_only_reproduced": "39/39",
        "v18_ranking_kept_rows_still_in_v19_ranking": "8/8",
        "remaining_unswept_pool_is_single_family": True,
    },
    "families_v19": families_v19,
    "ranking_top10": [
        {"s6_hex": r["s6_hex"], "parent": parent_of[r["s6_hex"]],
         "cost": r["cost"],
         "open_after_census_v19": r["open_after_census_v19"],
         "demand": r["demand"]} for r in ranking],
    "selection_policy": (
        "same policy as v4/v5/v6/v7/v8/v9/v10/v11/v12/v13/v14/v15/"
        "v16/v17/v18 (cheapest cost, then fewest open bits after "
        "the twenty-two-map overlay, then hex) over the three "
        "published families; rows closed by the landed 64h and "
        "76c folds, rows pending the 66i/66j folds, and the "
        "twenty-two swept children (64h/76c/66i/66j/69j/64a/71e/"
        "72d/73i/73j/73k/73l/74i/75f/78c/79c/79d/79e/80e/80f/81/"
        "82d) are excluded; the cheapest remaining row after the "
        "selected one is recorded as runner-up"),
    "selected_target": {
        "s6_hex": sel["s6_hex"],
        "parent": parent_of[sel["s6_hex"]],
        "cost": sel["cost"],
        "demand": sel["demand"],
        "legal_candidates": len(cands),
        "sweep_bits": sweep_bits,
        "confirmation_bits": confirmation,
        "runner_up": {"s6_hex": runner_up["s6_hex"],
                      "parent": parent_of[runner_up["s6_hex"]],
                      "cost": runner_up["cost"],
                      "open_after_census_v19":
                          runner_up["open_after_census_v19"]},
        "note": ("cheapest remaining unswept/unclaimed/unexcluded row "
                 "at head 1473 after the 82d sweep (the census v18 "
                 "runner-up); confirmation bits carry already-known "
                 "verdicts (pre-64h harvest or one of the "
                 "twenty-two maps) and will be re-run fresh in the "
                 "sweep"),
    },
    "interpretation_guard": (
        "search-plan bookkeeping only. No engine search is run here, no "
        "verdict is created, no row is closed. WIN7-D10 proves a "
        "first-player win within depth 10 from the individual 7-stone "
        "root only; REFUTED-D10 is not a LOSS proof; receipt folds are "
        "manifest-coverage bookkeeping. The 11x11 empty board, the "
        "two-stone roots {49,60} and {59,60}, S2 {59,60}, and classes "
        "1/2/4 all remain UNKNOWN."),
}

out_path = OUT / "class2-lane-next-target-presweep-1473-v19-20261118.json"
payload = json.dumps(out, indent=1, sort_keys=False,
                     ensure_ascii=True) + "\n"
out_path.write_bytes(payload.encode())
print(f"wrote {out_path} ({out_path.stat().st_size} bytes)")
