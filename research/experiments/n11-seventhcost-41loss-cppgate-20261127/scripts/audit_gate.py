#!/usr/bin/env python3
"""Part SW (seventh-cost 41 LOSS rows C++ scrutiny gate) fail-closed
machine audit (41 delegated resolved-LOSS rows + 3 calibration anchors).

EQ rev4 structure kept via the published SM/SN/SR kit audit script
template (10-capture-group REPLAY regex asserted at import; see
input/gate-rows.json for the machine-derived pins this audit derives
from). Gates: G1 raw shape (replay row + terminal replay_done +
driver headers), G2 per-row determinism (p1 == p2 except wall_s),
G3 published-raw pins (legal,budget,result,nodes), G4 gate-status
accounting, G5 input byte-clones (seventh-cost kit input/ == the
published seventh-cost kit MANIFEST-sha256.txt pins for the 41
targets; SR kit input/ == SR kit MANIFEST pins for the anchors).

Disclosed vs the SR kit transform rule: docstring + machine-generated
ROWS/RAW_PROV + part/schema strings only; the audit logic is unchanged.
Unlike SR (third-impl PRESENCE), no target row here has
third-implementation corroboration yet (seventh-cost batch
single-implementation; a third-impl Part is a separate future Part
before any adoption). No verdict is consumed: the 41 rows stay
UNCONSUMED labels (canonical head 42dbb58f keeps them absent). 11x11,
the two-stone root {60,27}, and its remaining third moves 100/108 stay
UNKNOWN throughout. k05 (WIN@50M) is NOT a row of this kit.
"""
import hashlib, json, os, re, sys

KIT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
KIT = os.path.abspath(KIT)

# key -> (budget, expected "legal,budget,result,nodes",
#          input sha256 pin, provenance of the input pin)
ROWS = {
 "anchor-af039": [
  "30000000",
  "89,30000000,2,19234232",
  "e51a3c9de08c62a54d80547c520876af4245394d05e37bbebf01d74204f64691",
  "SR kit input/anchor-af039.input.csv (byte-clone; == EQ/EN/EO/EV/SN/SR kit input; SR kit MANIFEST-sha256.txt pin)"
 ],
 "anchor-aj001": [
  "30000000",
  "84,30000000,2,5156075",
  "2f6daea5ca3b3fe6b7713c8d450af3f3c9f203acacb8a1340255d8e8f656496c",
  "SR kit input/anchor-aj001.input.csv (byte-clone; == EQ/EN/EO/EV/SN/SR kit input; SR kit MANIFEST-sha256.txt pin)"
 ],
 "anchor-at2m": [
  "2000000",
  "98,2000000,0,2000000",
  "ecc0299b8142abde201fcc40ea9666dac7368d0888d0600abc717af66ddfe348",
  "SR kit input/anchor-at2m.input.csv (byte-clone; == EQ/EN/EO/EV/SN/SR kit input; SR kit MANIFEST-sha256.txt pin)"
 ],
 "k01": [
  "15000000",
  "86,15000000,2,2986255",
  "9b565fe5a773d8499ac0926fdde95df98eefdf94ae7c1b92cf4dc62c463ff5f5",
  "seventh-cost kit input/k01.input.csv (byte-clone of the published seventh-cost batch input of n11-seventhcost-exclusive-selection-v1; sha256 == published seventh-cost kit MANIFEST-sha256.txt pin, the input SSOT)"
 ],
 "k02": [
  "15000000",
  "80,15000000,2,3113635",
  "d5cf9b79de1b8be8e7e5bc8dfd61315f918c054b2aa1446883c1e46920cc4113",
  "seventh-cost kit input/k02.input.csv (byte-clone of the published seventh-cost batch input of n11-seventhcost-exclusive-selection-v1; sha256 == published seventh-cost kit MANIFEST-sha256.txt pin, the input SSOT)"
 ],
 "k03": [
  "15000000",
  "87,15000000,2,4803039",
  "897ba37e9c0e79207ba9546896d38c3a2f57668c3ca6895713188b7c302e85ce",
  "seventh-cost kit input/k03.input.csv (byte-clone of the published seventh-cost batch input of n11-seventhcost-exclusive-selection-v1; sha256 == published seventh-cost kit MANIFEST-sha256.txt pin, the input SSOT)"
 ],
 "k04": [
  "15000000",
  "85,15000000,2,3045320",
  "5a8ad2842da144df7815a1842cd0c189da152ea491a5223a2cc2947d6aae3ac8",
  "seventh-cost kit input/k04.input.csv (byte-clone of the published seventh-cost batch input of n11-seventhcost-exclusive-selection-v1; sha256 == published seventh-cost kit MANIFEST-sha256.txt pin, the input SSOT)"
 ],
 "k06": [
  "15000000",
  "99,15000000,2,6557441",
  "43e31705667f10802af20432f82f9d02c938d903c1751782b3dab3113e2b599d",
  "seventh-cost kit input/k06.input.csv (byte-clone of the published seventh-cost batch input of n11-seventhcost-exclusive-selection-v1; sha256 == published seventh-cost kit MANIFEST-sha256.txt pin, the input SSOT)"
 ],
 "k07": [
  "15000000",
  "95,15000000,2,4841679",
  "19bc75a6aa5892fd6abbe5e70bdfeaa0a27f92d3146c57cef93c9ebb2dd240a7",
  "seventh-cost kit input/k07.input.csv (byte-clone of the published seventh-cost batch input of n11-seventhcost-exclusive-selection-v1; sha256 == published seventh-cost kit MANIFEST-sha256.txt pin, the input SSOT)"
 ],
 "k08": [
  "15000000",
  "90,15000000,2,10134007",
  "0ce2a6d002585d16d99a3f6da6b3f762b7bb8da4f0d840436e61d81abffa4042",
  "seventh-cost kit input/k08.input.csv (byte-clone of the published seventh-cost batch input of n11-seventhcost-exclusive-selection-v1; sha256 == published seventh-cost kit MANIFEST-sha256.txt pin, the input SSOT)"
 ],
 "k09": [
  "15000000",
  "97,15000000,2,3009687",
  "2e5fefbbc234ffeb9c73173de816e49f06c3a8ba81ee1d2162b61d865bd97345",
  "seventh-cost kit input/k09.input.csv (byte-clone of the published seventh-cost batch input of n11-seventhcost-exclusive-selection-v1; sha256 == published seventh-cost kit MANIFEST-sha256.txt pin, the input SSOT)"
 ],
 "k10": [
  "15000000",
  "90,15000000,2,13100811",
  "13869737887b0e671793c494137b4ad68158d74194c956611322bc2a04b3a688",
  "seventh-cost kit input/k10.input.csv (byte-clone of the published seventh-cost batch input of n11-seventhcost-exclusive-selection-v1; sha256 == published seventh-cost kit MANIFEST-sha256.txt pin, the input SSOT)"
 ],
 "k11": [
  "15000000",
  "92,15000000,2,8175719",
  "96ca108a1d6886e4d45db50b2371ce02cb0893f400c3f8301d4b652bc49af846",
  "seventh-cost kit input/k11.input.csv (byte-clone of the published seventh-cost batch input of n11-seventhcost-exclusive-selection-v1; sha256 == published seventh-cost kit MANIFEST-sha256.txt pin, the input SSOT)"
 ],
 "k12": [
  "15000000",
  "96,15000000,2,6968873",
  "a213d3b2ec1129ec9be65aa0266190b3c191d822abd486017c7d4b219cff2dc8",
  "seventh-cost kit input/k12.input.csv (byte-clone of the published seventh-cost batch input of n11-seventhcost-exclusive-selection-v1; sha256 == published seventh-cost kit MANIFEST-sha256.txt pin, the input SSOT)"
 ],
 "k13": [
  "15000000",
  "93,15000000,2,2482316",
  "0011bfc73c1c08ab4d5a0a3c9bfefa32263a0f4a26b3a50c5dbcfce2029d252d",
  "seventh-cost kit input/k13.input.csv (byte-clone of the published seventh-cost batch input of n11-seventhcost-exclusive-selection-v1; sha256 == published seventh-cost kit MANIFEST-sha256.txt pin, the input SSOT)"
 ],
 "k14": [
  "15000000",
  "91,15000000,2,3184572",
  "0f21213527a50f626b5bf26915cfd1762d9188e62e02efdbb3dc626f3937e497",
  "seventh-cost kit input/k14.input.csv (byte-clone of the published seventh-cost batch input of n11-seventhcost-exclusive-selection-v1; sha256 == published seventh-cost kit MANIFEST-sha256.txt pin, the input SSOT)"
 ],
 "k15": [
  "15000000",
  "98,15000000,2,4499006",
  "7d44c70fd571ac1a28903d5fe10c04f7483f86229ffca7de9ca31be5cb6def0d",
  "seventh-cost kit input/k15.input.csv (byte-clone of the published seventh-cost batch input of n11-seventhcost-exclusive-selection-v1; sha256 == published seventh-cost kit MANIFEST-sha256.txt pin, the input SSOT)"
 ],
 "k16": [
  "2000000",
  "98,2000000,2,1228696",
  "908fadc540320db01234811fccf3d5c6db20aebc9733968211d7ff23a3bd8ebe",
  "seventh-cost kit input/k16.input.csv (byte-clone of the published seventh-cost batch input of n11-seventhcost-exclusive-selection-v1; sha256 == published seventh-cost kit MANIFEST-sha256.txt pin, the input SSOT)"
 ],
 "k17": [
  "2000000",
  "94,2000000,2,1831284",
  "a30a4dc4454ceb8314453c58cd805bfa35842aa7acad2a9795e8f203490a1f9a",
  "seventh-cost kit input/k17.input.csv (byte-clone of the published seventh-cost batch input of n11-seventhcost-exclusive-selection-v1; sha256 == published seventh-cost kit MANIFEST-sha256.txt pin, the input SSOT)"
 ],
 "k18": [
  "15000000",
  "90,15000000,2,2337950",
  "181d04f5bcac6402f5489fad520808d85323297f1ff49acc70ef7fc576b556a1",
  "seventh-cost kit input/k18.input.csv (byte-clone of the published seventh-cost batch input of n11-seventhcost-exclusive-selection-v1; sha256 == published seventh-cost kit MANIFEST-sha256.txt pin, the input SSOT)"
 ],
 "k19": [
  "15000000",
  "91,15000000,2,7363042",
  "a9cdab6f1605fcb8c79165e97ae38a0b878b95cf5bb5a5e47464d4d6b3972093",
  "seventh-cost kit input/k19.input.csv (byte-clone of the published seventh-cost batch input of n11-seventhcost-exclusive-selection-v1; sha256 == published seventh-cost kit MANIFEST-sha256.txt pin, the input SSOT)"
 ],
 "k20": [
  "15000000",
  "92,15000000,2,2198801",
  "d7682dbe75864e91b6001c163711857dac0341752432cae3953ed2379ba12cb7",
  "seventh-cost kit input/k20.input.csv (byte-clone of the published seventh-cost batch input of n11-seventhcost-exclusive-selection-v1; sha256 == published seventh-cost kit MANIFEST-sha256.txt pin, the input SSOT)"
 ],
 "k21": [
  "15000000",
  "98,15000000,2,6786255",
  "924d069f8b6a3c5a334aaa331b1d2701d52d34cfee4937a980325b6874a53f43",
  "seventh-cost kit input/k21.input.csv (byte-clone of the published seventh-cost batch input of n11-seventhcost-exclusive-selection-v1; sha256 == published seventh-cost kit MANIFEST-sha256.txt pin, the input SSOT)"
 ],
 "k22": [
  "15000000",
  "99,15000000,2,7990013",
  "ef4f7fb9c9037ec1e3ecc8882b49ca755382db137a1be2424815103500976e9f",
  "seventh-cost kit input/k22.input.csv (byte-clone of the published seventh-cost batch input of n11-seventhcost-exclusive-selection-v1; sha256 == published seventh-cost kit MANIFEST-sha256.txt pin, the input SSOT)"
 ],
 "k23": [
  "15000000",
  "96,15000000,2,4822824",
  "9abc314ebeef716320f91574491aa56b85d035612aa24f8e41fdbb7804d0504c",
  "seventh-cost kit input/k23.input.csv (byte-clone of the published seventh-cost batch input of n11-seventhcost-exclusive-selection-v1; sha256 == published seventh-cost kit MANIFEST-sha256.txt pin, the input SSOT)"
 ],
 "k24": [
  "15000000",
  "92,15000000,2,2960039",
  "6e55b8f94df003055cff5d7544ad4ec718e69aebe659e340f07931f2168d9c66",
  "seventh-cost kit input/k24.input.csv (byte-clone of the published seventh-cost batch input of n11-seventhcost-exclusive-selection-v1; sha256 == published seventh-cost kit MANIFEST-sha256.txt pin, the input SSOT)"
 ],
 "k25": [
  "15000000",
  "92,15000000,2,2314036",
  "50804e32ee55da2ffcf556d38f644e602d00a945e8175279b1f96783f3a3c33f",
  "seventh-cost kit input/k25.input.csv (byte-clone of the published seventh-cost batch input of n11-seventhcost-exclusive-selection-v1; sha256 == published seventh-cost kit MANIFEST-sha256.txt pin, the input SSOT)"
 ],
 "k26": [
  "15000000",
  "93,15000000,2,7170686",
  "08952c518b381a68ecb7c39039c720a0940c3ed97428b83dc2e856d88707be47",
  "seventh-cost kit input/k26.input.csv (byte-clone of the published seventh-cost batch input of n11-seventhcost-exclusive-selection-v1; sha256 == published seventh-cost kit MANIFEST-sha256.txt pin, the input SSOT)"
 ],
 "k27": [
  "15000000",
  "93,15000000,2,2535682",
  "3fb7fe2885a5eea42d5e12614fd2516f0b24ded5283ded9b4853f415a7589e49",
  "seventh-cost kit input/k27.input.csv (byte-clone of the published seventh-cost batch input of n11-seventhcost-exclusive-selection-v1; sha256 == published seventh-cost kit MANIFEST-sha256.txt pin, the input SSOT)"
 ],
 "k28": [
  "15000000",
  "98,15000000,2,3882046",
  "90438c8992092e913dfb2157793c510da6fda44b833976bba133f3182e9cce39",
  "seventh-cost kit input/k28.input.csv (byte-clone of the published seventh-cost batch input of n11-seventhcost-exclusive-selection-v1; sha256 == published seventh-cost kit MANIFEST-sha256.txt pin, the input SSOT)"
 ],
 "k29": [
  "15000000",
  "92,15000000,2,3329801",
  "09a6d82c959a8c5c2fe2ec16878896e4684fad566b0e0d5e3b9125627f5e945a",
  "seventh-cost kit input/k29.input.csv (byte-clone of the published seventh-cost batch input of n11-seventhcost-exclusive-selection-v1; sha256 == published seventh-cost kit MANIFEST-sha256.txt pin, the input SSOT)"
 ],
 "k30": [
  "15000000",
  "91,15000000,2,4837865",
  "f411687469b2a66ef8ff543b2ed95cf97ad20e2597c94b2318925c7374267e54",
  "seventh-cost kit input/k30.input.csv (byte-clone of the published seventh-cost batch input of n11-seventhcost-exclusive-selection-v1; sha256 == published seventh-cost kit MANIFEST-sha256.txt pin, the input SSOT)"
 ],
 "k31": [
  "15000000",
  "98,15000000,2,7435262",
  "e584563aae0a871a5b29f0536744f32571f27ca4b540779c26a10baad3d10077",
  "seventh-cost kit input/k31.input.csv (byte-clone of the published seventh-cost batch input of n11-seventhcost-exclusive-selection-v1; sha256 == published seventh-cost kit MANIFEST-sha256.txt pin, the input SSOT)"
 ],
 "k32": [
  "15000000",
  "97,15000000,2,3831090",
  "1b10d8c41391f6f69910c6430dc24ca6f5735b68d610aefa962b6eed1dcff604",
  "seventh-cost kit input/k32.input.csv (byte-clone of the published seventh-cost batch input of n11-seventhcost-exclusive-selection-v1; sha256 == published seventh-cost kit MANIFEST-sha256.txt pin, the input SSOT)"
 ],
 "k33": [
  "15000000",
  "103,15000000,2,2739658",
  "7b3bf9fab96c1ec23befe3afeb8444886ef0839c9fb61688318aa2bad69b15ee",
  "seventh-cost kit input/k33.input.csv (byte-clone of the published seventh-cost batch input of n11-seventhcost-exclusive-selection-v1; sha256 == published seventh-cost kit MANIFEST-sha256.txt pin, the input SSOT)"
 ],
 "k34": [
  "15000000",
  "102,15000000,2,8150456",
  "bd981d7aa7c098f5e31aac3200b78548d93ebdfcd00d75aac056ac0561636562",
  "seventh-cost kit input/k34.input.csv (byte-clone of the published seventh-cost batch input of n11-seventhcost-exclusive-selection-v1; sha256 == published seventh-cost kit MANIFEST-sha256.txt pin, the input SSOT)"
 ],
 "k35": [
  "15000000",
  "102,15000000,2,5484699",
  "bb48f792c13f8415992205521ceca0a530ee6ba7cec8e909c040703216eea5f7",
  "seventh-cost kit input/k35.input.csv (byte-clone of the published seventh-cost batch input of n11-seventhcost-exclusive-selection-v1; sha256 == published seventh-cost kit MANIFEST-sha256.txt pin, the input SSOT)"
 ],
 "k36": [
  "15000000",
  "101,15000000,2,4856132",
  "45a08e25d07e2a0e890b67c32bb18ee030ed14b7c6aa33a9471ef08f8d1ddb56",
  "seventh-cost kit input/k36.input.csv (byte-clone of the published seventh-cost batch input of n11-seventhcost-exclusive-selection-v1; sha256 == published seventh-cost kit MANIFEST-sha256.txt pin, the input SSOT)"
 ],
 "k37": [
  "15000000",
  "102,15000000,2,4695043",
  "a340b4880edce48e18060af0ec2b222db8052ac500507a2ec800b8f8fb721a05",
  "seventh-cost kit input/k37.input.csv (byte-clone of the published seventh-cost batch input of n11-seventhcost-exclusive-selection-v1; sha256 == published seventh-cost kit MANIFEST-sha256.txt pin, the input SSOT)"
 ],
 "k38": [
  "15000000",
  "103,15000000,2,6238916",
  "08fbeebf17add5dee54bf65176d497836515657e925cd51ac23da28383bc9d05",
  "seventh-cost kit input/k38.input.csv (byte-clone of the published seventh-cost batch input of n11-seventhcost-exclusive-selection-v1; sha256 == published seventh-cost kit MANIFEST-sha256.txt pin, the input SSOT)"
 ],
 "k39": [
  "15000000",
  "103,15000000,2,10652524",
  "59e6140ec0032882d8c27602b20090ddbd54298a4fc285bf659795b07a34d905",
  "seventh-cost kit input/k39.input.csv (byte-clone of the published seventh-cost batch input of n11-seventhcost-exclusive-selection-v1; sha256 == published seventh-cost kit MANIFEST-sha256.txt pin, the input SSOT)"
 ],
 "k40": [
  "15000000",
  "100,15000000,2,5235489",
  "a40e725ec2469e40dea4cb1fe734e15ccb43d5b39ded6733bb9354a258418044",
  "seventh-cost kit input/k40.input.csv (byte-clone of the published seventh-cost batch input of n11-seventhcost-exclusive-selection-v1; sha256 == published seventh-cost kit MANIFEST-sha256.txt pin, the input SSOT)"
 ],
 "k41": [
  "15000000",
  "104,15000000,2,10889302",
  "47dd5c202d5e32628f34736f06754dc25fc6a487e415cc6da47cf3ce03d41dab",
  "seventh-cost kit input/k41.input.csv (byte-clone of the published seventh-cost batch input of n11-seventhcost-exclusive-selection-v1; sha256 == published seventh-cost kit MANIFEST-sha256.txt pin, the input SSOT)"
 ],
 "k42": [
  "15000000",
  "102,15000000,2,3089468",
  "377eb6a4c1575d49db052362a138ca302acdb278071b7106dfe1934c48540832",
  "seventh-cost kit input/k42.input.csv (byte-clone of the published seventh-cost batch input of n11-seventhcost-exclusive-selection-v1; sha256 == published seventh-cost kit MANIFEST-sha256.txt pin, the input SSOT)"
 ]
}

RAW_PROV = {
 "anchor-af039": "EV/SK/SR kit raw condition (budget-ceiling baseline); == SR kit anchors block",
 "anchor-aj001": "EV/SK/SR kit raw condition (budget-ceiling baseline); == SR kit anchors block",
 "anchor-at2m": "EV/SK/SR kit raw condition (budget-ceiling baseline); == SR kit anchors block",
 "k01": "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/raw/at15m-run1-k01.out.csv (published seventh-cost replica 86,15000000,2,2986255); cold-pair node-exact vs its run2 raw; third-impl corroboration ABSENT for this row (separate future Part before any adoption)",
 "k02": "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/raw/at15m-run1-k02.out.csv (published seventh-cost replica 80,15000000,2,3113635); cold-pair node-exact vs its run2 raw; third-impl corroboration ABSENT for this row (separate future Part before any adoption)",
 "k03": "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/raw/at15m-run1-k03.out.csv (published seventh-cost replica 87,15000000,2,4803039); cold-pair node-exact vs its run2 raw; third-impl corroboration ABSENT for this row (separate future Part before any adoption)",
 "k04": "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/raw/at15m-run1-k04.out.csv (published seventh-cost replica 85,15000000,2,3045320); cold-pair node-exact vs its run2 raw; third-impl corroboration ABSENT for this row (separate future Part before any adoption)",
 "k06": "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/raw/at15m-run1-k06.out.csv (published seventh-cost replica 99,15000000,2,6557441); cold-pair node-exact vs its run2 raw; third-impl corroboration ABSENT for this row (separate future Part before any adoption)",
 "k07": "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/raw/at15m-run1-k07.out.csv (published seventh-cost replica 95,15000000,2,4841679); cold-pair node-exact vs its run2 raw; third-impl corroboration ABSENT for this row (separate future Part before any adoption)",
 "k08": "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/raw/at15m-run1-k08.out.csv (published seventh-cost replica 90,15000000,2,10134007); cold-pair node-exact vs its run2 raw; third-impl corroboration ABSENT for this row (separate future Part before any adoption)",
 "k09": "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/raw/at15m-run1-k09.out.csv (published seventh-cost replica 97,15000000,2,3009687); cold-pair node-exact vs its run2 raw; third-impl corroboration ABSENT for this row (separate future Part before any adoption)",
 "k10": "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/raw/at15m-run1-k10.out.csv (published seventh-cost replica 90,15000000,2,13100811); cold-pair node-exact vs its run2 raw; third-impl corroboration ABSENT for this row (separate future Part before any adoption)",
 "k11": "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/raw/at15m-run1-k11.out.csv (published seventh-cost replica 92,15000000,2,8175719); cold-pair node-exact vs its run2 raw; third-impl corroboration ABSENT for this row (separate future Part before any adoption)",
 "k12": "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/raw/at15m-run1-k12.out.csv (published seventh-cost replica 96,15000000,2,6968873); cold-pair node-exact vs its run2 raw; third-impl corroboration ABSENT for this row (separate future Part before any adoption)",
 "k13": "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/raw/at15m-run1-k13.out.csv (published seventh-cost replica 93,15000000,2,2482316); cold-pair node-exact vs its run2 raw; third-impl corroboration ABSENT for this row (separate future Part before any adoption)",
 "k14": "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/raw/at15m-run1-k14.out.csv (published seventh-cost replica 91,15000000,2,3184572); cold-pair node-exact vs its run2 raw; third-impl corroboration ABSENT for this row (separate future Part before any adoption)",
 "k15": "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/raw/at15m-run1-k15.out.csv (published seventh-cost replica 98,15000000,2,4499006); cold-pair node-exact vs its run2 raw; third-impl corroboration ABSENT for this row (separate future Part before any adoption)",
 "k16": "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/raw/at2m-k16.out.csv (published seventh-cost replica 98,2000000,2,1228696); cold-pair node-exact vs its run2 raw; third-impl corroboration ABSENT for this row (separate future Part before any adoption)",
 "k17": "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/raw/at2m-k17.out.csv (published seventh-cost replica 94,2000000,2,1831284); cold-pair node-exact vs its run2 raw; third-impl corroboration ABSENT for this row (separate future Part before any adoption)",
 "k18": "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/raw/at15m-run1-k18.out.csv (published seventh-cost replica 90,15000000,2,2337950); cold-pair node-exact vs its run2 raw; third-impl corroboration ABSENT for this row (separate future Part before any adoption)",
 "k19": "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/raw/at15m-run1-k19.out.csv (published seventh-cost replica 91,15000000,2,7363042); cold-pair node-exact vs its run2 raw; third-impl corroboration ABSENT for this row (separate future Part before any adoption)",
 "k20": "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/raw/at15m-run1-k20.out.csv (published seventh-cost replica 92,15000000,2,2198801); cold-pair node-exact vs its run2 raw; third-impl corroboration ABSENT for this row (separate future Part before any adoption)",
 "k21": "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/raw/at15m-run1-k21.out.csv (published seventh-cost replica 98,15000000,2,6786255); cold-pair node-exact vs its run2 raw; third-impl corroboration ABSENT for this row (separate future Part before any adoption)",
 "k22": "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/raw/at15m-run1-k22.out.csv (published seventh-cost replica 99,15000000,2,7990013); cold-pair node-exact vs its run2 raw; third-impl corroboration ABSENT for this row (separate future Part before any adoption)",
 "k23": "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/raw/at15m-run1-k23.out.csv (published seventh-cost replica 96,15000000,2,4822824); cold-pair node-exact vs its run2 raw; third-impl corroboration ABSENT for this row (separate future Part before any adoption)",
 "k24": "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/raw/at15m-run1-k24.out.csv (published seventh-cost replica 92,15000000,2,2960039); cold-pair node-exact vs its run2 raw; third-impl corroboration ABSENT for this row (separate future Part before any adoption)",
 "k25": "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/raw/at15m-run1-k25.out.csv (published seventh-cost replica 92,15000000,2,2314036); cold-pair node-exact vs its run2 raw; third-impl corroboration ABSENT for this row (separate future Part before any adoption)",
 "k26": "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/raw/at15m-run1-k26.out.csv (published seventh-cost replica 93,15000000,2,7170686); cold-pair node-exact vs its run2 raw; third-impl corroboration ABSENT for this row (separate future Part before any adoption)",
 "k27": "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/raw/at15m-run1-k27.out.csv (published seventh-cost replica 93,15000000,2,2535682); cold-pair node-exact vs its run2 raw; third-impl corroboration ABSENT for this row (separate future Part before any adoption)",
 "k28": "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/raw/at15m-run1-k28.out.csv (published seventh-cost replica 98,15000000,2,3882046); cold-pair node-exact vs its run2 raw; third-impl corroboration ABSENT for this row (separate future Part before any adoption)",
 "k29": "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/raw/at15m-run1-k29.out.csv (published seventh-cost replica 92,15000000,2,3329801); cold-pair node-exact vs its run2 raw; third-impl corroboration ABSENT for this row (separate future Part before any adoption)",
 "k30": "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/raw/at15m-run1-k30.out.csv (published seventh-cost replica 91,15000000,2,4837865); cold-pair node-exact vs its run2 raw; third-impl corroboration ABSENT for this row (separate future Part before any adoption)",
 "k31": "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/raw/at15m-run1-k31.out.csv (published seventh-cost replica 98,15000000,2,7435262); cold-pair node-exact vs its run2 raw; third-impl corroboration ABSENT for this row (separate future Part before any adoption)",
 "k32": "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/raw/at15m-run1-k32.out.csv (published seventh-cost replica 97,15000000,2,3831090); cold-pair node-exact vs its run2 raw; third-impl corroboration ABSENT for this row (separate future Part before any adoption)",
 "k33": "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/raw/at15m-run1-k33.out.csv (published seventh-cost replica 103,15000000,2,2739658); cold-pair node-exact vs its run2 raw; third-impl corroboration ABSENT for this row (separate future Part before any adoption)",
 "k34": "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/raw/at15m-run1-k34.out.csv (published seventh-cost replica 102,15000000,2,8150456); cold-pair node-exact vs its run2 raw; third-impl corroboration ABSENT for this row (separate future Part before any adoption)",
 "k35": "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/raw/at15m-run1-k35.out.csv (published seventh-cost replica 102,15000000,2,5484699); cold-pair node-exact vs its run2 raw; third-impl corroboration ABSENT for this row (separate future Part before any adoption)",
 "k36": "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/raw/at15m-run1-k36.out.csv (published seventh-cost replica 101,15000000,2,4856132); cold-pair node-exact vs its run2 raw; third-impl corroboration ABSENT for this row (separate future Part before any adoption)",
 "k37": "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/raw/at15m-run1-k37.out.csv (published seventh-cost replica 102,15000000,2,4695043); cold-pair node-exact vs its run2 raw; third-impl corroboration ABSENT for this row (separate future Part before any adoption)",
 "k38": "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/raw/at15m-run1-k38.out.csv (published seventh-cost replica 103,15000000,2,6238916); cold-pair node-exact vs its run2 raw; third-impl corroboration ABSENT for this row (separate future Part before any adoption)",
 "k39": "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/raw/at15m-run1-k39.out.csv (published seventh-cost replica 103,15000000,2,10652524); cold-pair node-exact vs its run2 raw; third-impl corroboration ABSENT for this row (separate future Part before any adoption)",
 "k40": "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/raw/at15m-run1-k40.out.csv (published seventh-cost replica 100,15000000,2,5235489); cold-pair node-exact vs its run2 raw; third-impl corroboration ABSENT for this row (separate future Part before any adoption)",
 "k41": "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/raw/at15m-run1-k41.out.csv (published seventh-cost replica 104,15000000,2,10889302); cold-pair node-exact vs its run2 raw; third-impl corroboration ABSENT for this row (separate future Part before any adoption)",
 "k42": "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126/output/raw/at15m-run1-k42.out.csv (published seventh-cost replica 102,15000000,2,3089468); cold-pair node-exact vs its run2 raw; third-impl corroboration ABSENT for this row (separate future Part before any adoption)"
}

REPLAY = re.compile(r"^replay,(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),([0-9.]+),(\d+),(\d+)$")
assert len(REPLAY.groupindex) == 0 and REPLAY.groups == 10, "rev4 lesson: exactly 10 capture groups"

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def main():
    gates = {}
    def g(name, ok, detail=""):
        gates[name] = {"status": "PASS" if ok else "FAIL", "detail": detail}
        return ok

    ok = True
    parsed = {}
    for key, (budget, expected, in_pin, prov) in sorted(ROWS.items()):
        rec = {"budget": budget, "expected": expected}
        # G5 input pins
        ipath = os.path.join(KIT, "input", key + ".input.csv")
        if not os.path.isfile(ipath):
            ok &= g("G5:" + key, False, "missing input file")
            continue
        ok &= g("G5:" + key, sha256(ipath) == in_pin,
                "sha256 %s %s" % (sha256(ipath), "==" if sha256(ipath) == in_pin else "!= " + in_pin))
        rows = {}
        for p in ("p1", "p2"):
            rpath = os.path.join(KIT, "output", "raw", key + "." + p + ".out")
            if not os.path.isfile(rpath):
                ok &= g("G1:" + key + ":" + p, False, "missing raw")
                rows[p] = None
                continue
            text = open(rpath).read()
            m = [REPLAY.match(l) for l in text.splitlines() if l.startswith("replay,")]
            done = "# replay_done rows=1" in text
            hdr = "# exact replay: order=0 " in text and "# exact replay: id,stones,legal,is_or,budget,result,nodes,wall_s,key_lo,key_hi" in text
            ok &= g("G1:" + key + ":" + p, bool(len(m) == 1 and done and hdr),
                    "replay_rows=%d done=%s header=%s" % (len(m), done, hdr))
            rows[p] = list(m[0].groups()) if len(m) == 1 and m[0] else None
        if rows["p1"] is None or rows["p2"] is None:
            parsed[key] = rec; continue
        # G2 determinism on all fields except wall_s (index 8)
        a = rows["p1"]; b = rows["p2"]
        det = (a[:7] == b[:7]) and (a[8:] == b[8:])
        ok &= g("G2:" + key, det, "p1=%s p2=%s" % (",".join(a), ",".join(b)))
        # G3 published pins: fields legal(2),budget(4),result(5),nodes(6) -> f3,6,7,8 of csv
        rec["observed_p1"] = ",".join([a[2], a[4], a[5], a[6]])
        ok &= g("G3:" + key, ",".join([a[2], a[4], a[5], a[6]]) == expected,
                "observed %s expected %s (%s)" % (rec["observed_p1"], expected, RAW_PROV[key]))
        parsed[key] = rec
    # G4 status accounting
    spath = os.path.join(KIT, "output", "gate-status.log")
    okp = 0; bad = []
    if os.path.isfile(spath):
        for line in open(spath):
            if " GATE-PASS " in line: okp += 1
            elif "MISMATCH" in line or "GATE-FAIL" in line or "GATE-CRASH" in line:
                bad.append(line.strip())
    ok &= g("G4", okp == len(ROWS) and not bad,
            "passes=%d/%d bad=%d" % (okp, len(ROWS), len(bad)))
    out = {"part": "SW", "schema": "n11-seventhcost-41loss-cppgate-audit-v1",
           "rows": parsed, "gates": gates,
           "overall": "PASS" if ok else "FAIL"}
    opath = os.path.join(KIT, "output", "audit_gate.json")
    with open(opath, "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
        f.write("\n")
    print("audit_gate:", out["overall"])
    for k, v in sorted(gates.items()):
        if v["status"] == "FAIL":
            print("FAIL", k, v["detail"])
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
