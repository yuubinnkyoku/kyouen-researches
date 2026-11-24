---
id: K1310
title: "遷移窓非合同行の崩壊: T-NCW-P（非合同ペア行 = dominant 列 g*=z−2k の flip wedge 則・値 2 は g=g* と対角線 s=z の 2 直線上のみ）・T-NCW-B（非合同床行 = g*<0 全 0 / g*≥0 で r=(z−1)//2 階段 0/2/1）・L2（B-exit 一様則 [g even]・床 a=1 は 1）・C1–C5（K1309 O1′/O2 解決・OBS-NCW/OBS-BW 定理昇格・2 山面の全 k 軸未確定帯消滅・publish-then-execute・51,439 点公式監査 bad 0・4 走 byte-identical・C-descent が非合同性を保存して単一 R 強帰納で閉じる非合同 packet）"
kind: theorem
status: proved
topics: [grundy, residual-games]
aliases:
  - "THE PACKAGE: the non-congruent window row collapse (the last undetermined band of the two-heap pair/bed k-axis). Coordinates as K1309: pair k := R - 2m - g, bed k := R - 2a, window 1 <= k <= z-1, NON-congruent means k not= z (mod 2), z >= 2 (the z=2, k=1 row is the induction base; it is automatically non-congruent). T-NCW-P (universal): for every z >= 2, m >= 1, g >= 1, non-congruent k in [1, z-1], with g* := z-2k and s := 2m+g: H(2m+g+k; (m, m+g); z) = [g odd] if g* <= 0 or g > g* or s < z; 2 if 1 <= g <= g*, s >= z, and (g = g* or g = z-2m); [g even] in the remaining flip wedge {1 <= g < g*, s > z}. Claim evaluation order matters (the N-branch fires first: if g = z-2m with m < k then g > g* and the row reads [g odd]). Inside the anomaly wedge {g <= g*, s >= z} the condition m >= k is automatic (2m >= z-g >= z-g* = 2k). The 2s lie EXACTLY on the two straight lines dominant column g = g* and diagonal s = z (g = z-2m); outside the wedge the row NEVER takes a 2 (in particular the Z-DIAG g = z+1 superdiagonal 2 does not exist on non-congruent rows). T-NCW-B (universal): for every z >= 2, a >= 1, non-congruent k, with g* = z-2k, r = (z-1)//2: H(2a+k; (a, a); z) = 0 if g* < 0 (2k > z, including EVERY k = z-1 top row); a <= r: 0; a >= r+1: 1 if z odd; 2 if z even and g* = 0 (this forces z = 2 mod 4 and k = z/2 odd); z even, g* > 0: 2 at a = r+1, 1 at a >= r+2. L2 (derived from the published K0832 closed form): the m=1 non-congruent B-exit single token v(g+1, z+1, g+k+1) = (g+1) mod 2 = [g even], UNIFORM across all branches (including the g = z z==x branch tail, which also reads (z+1)%2); the bed a=1 B-exit v(1, z+1, k+1) = 1 unconditionally. C1: the z=2 base row agrees with the published K1286 z2-k1 rows (pairs all [g odd], b2(1) = 2). C2: the k = z-1 top row is always non-congruent, g* = 2-z: z >= 3 pairs all [g odd], beds all 0 — the K1308 OBS-BW observation is promoted to theorem. C3: the K1309 D10 frozen 35-row OBS-NCW value-distribution table is cellwise EXACTLY the T-NCW-P slices (machine three-way check: engine re-census, frozen-table match, claim match); the 'structured 2s of shallow rows k in {1,2,3}' are the dominant column and diagonal 2s. C4: on non-congruent rows the only window 2s are the two wedge lines and NO g = z+1 2 exists — the congruent and non-congruent window laws are mathematically distinct objects; the correct reading of the refuted parity-interleaving conjecture is 'congruent rows COPY the diagonal row's value (T-WC), non-congruent rows obey the dominant-column flip wedge law'."
  - "STRUCTURE (typed children, the single-R strong induction that the K1309 congruent packet could NOT do): every option of a non-congruent window pair cell is EXACTLY one of fall/compress (pair, g+-1, same (k, z)) / corner g=1 (bed same (k,z)) / B-exit m=1 (single token, L2 = [g even] uniform) / C (non-congruent pair at (k-1, z-1) for k >= 2 — the C-descent PRESERVES non-congruence since k-1 and z-1 flip together — or the k=0 band row on plane z-1 for k=1, read by the published K1303 band). Bed options: A -> pair gap 1, B(a=1) -> v(1, z+1, k+1) = 1, C -> non-congruent bed (k-1, z-1) or k=0 band bed. THE CLOSURE DIFFERENCE VS K1309: in the congruent packet the C-children land on congruent rows and the packet needed a joint budget argument; in the non-congruent packet the C-child (k-1, z-1) is AGAIN non-congruent, so {T-NCW-P, T-NCW-B} closes on the SINGLE budget R-1 by strong induction with L2, K0832, K1286 (z=2 base), and K1303 band as instant bases. Parity invariants (hand §2.1): s = g (mod 2), g* = z (mod 2), no s = z+1 column in the D region, F cap {m=1} = empty, z odd forces k even forces k=1 cells with no C child, bed r vs r' = (z-2)//2 half-step offset between z parities. Region tables (hand §2.4/§2.5): pair rows N (g* <= 0) / N2 / F (flip wedge) / G (dominant column g = g*) / D (diagonal band) x bed Br1..Br4 close pointwise in mex algebra; the initial hand analysis MIS-predicted sigma = 2 for the B-exit of the g=z branch of L2 and the machine follow-up (108,000 pts, z 2..60, all non-congruent k, g <= 120, bad 0) corrected it to the uniform (g+1)%2 BEFORE publication (no effect on the mex closure); recorded honestly in the note §6."
  - "MACHINE (publish-then-execute, exact chain): single-owner declaration note published FIRST at 7b992b5f (observed HEAD fdb3ceba at push time, note records start-of-work HEAD ffde117b with the Part DX batch-36 racing lane orthogonal; K1310 vacancy verified by commit search, no counter-declaration), kit e6ea44fb (13 files: README.md, verify_k1310.py, engine_block.py, explore_ncw.py, explore_ncw.out X1..X8 + L2 lemma 108,000 frozen, predry/dryrun1-4 (+.info), 4 runs byte-identical sha256 3c2eb51742c568536b0bf67738be3c2f7b59bf87ae8a1eba42e28ead11168949, ~2.5 s/run python 3.12), fetch-back byte-identical (all raw pulls 200/200 first attempt, every sha256 matched the declared pins), THEN official 4 runs from the verified bytes: same cwd x2 (PYTHONHASHSEED random/1) + isolated tree env -i x2 (PYTHONHASHSEED 99/7), all rc=0, stdout byte-identical to the declared predry sha. verify_k1310.py sha256 58fd5e46d52a5a62950b796506e08704987bdb0badfedc73ca754468824d94f3, embedded engine block startup sha gate pin bd5f22e4... (K1138/K1282..K1309 chain identical embedded bytes; standalone engine_block.py 582c93c1... identical to the K1282..K1309 kits). counts [12096, 5760, 4320, 2058, 9016, 1512, 3870, 4960, 372, 1295, 4680, 1500] total 51,439 bad 0 (D1 T-NCW-P census z3..16 m<=8 g<=24 / D2 far z{18,20,22} m<=4 g<=48 / D3 m-distance z{5,8,11,14} m<=20 g<=12 / D4 T-NCW-B census z3..16 a<=26 + far z{18,20,22} a<=14 / D5 typed self-check z2..14: children built ONLY from hand tables + published closed forms (K0832 one-token, K1303 band, K1286 base), mex == claim == engine pointwise 9,016 / D6 B-exit triple (hand L2 vs transcribed closed form vs BOTH engines) 1,512 / D7 band k=0 pair w1..15 + bed w1..15 + k=1 C-child cell gate z even 4..22 (K1303 cpsfG transcription) 3,870 / D8 published anchors (K1309 T-WC/T-WBC, K1308 Z-DIAG/T-UH/T-DU') 4,960 / D9 cross-engine 372 / D10 OBS-NCW frozen 35-row subsumption (engine re-census + frozen-table reproduction + claim match) 1,295 / D11 k=1 row stress z even 4..28 m<=12 g<=30 4,680 / D12 bed k=z-1 rows + deep tail z3..20 a<=30 + z{6,10,14,18} a<=40 all non-congruent k 1,500). Mutation battery 13/13 fail-closed exactly as pre-declared: --tamper-engine rc=2 (mutated sha 0ea47a80...), np1 [D1] 12,096 / np2 [D2] 5,760 / np3 [D3] 4,320 / bd [D4] 2,058 / ty [claim function P/Bm flip: D1+D2+D3+D4+D5+D10(1,260)+D11+D12] 40,690 / be [D6] 1,512 / cp [D7] 3,870 / ps [D8] 4,960 / xg [D9] 372 / rw [D10 claims 1,260 + one frozen '3,2' row line] 1,261 / ex [D11] 4,680 / bs [D12] 1,500, all rc=1 (D6-D9 contribute 0 under ty because those batteries compare engine-vs-engine/engine-vs-closed-form and never read the claim function — honest by design, pre-declared). Audit artifacts published at 73aa36d6 (output/audit_run1-4.out+.info, tamper 13 record files, detcheck.json OFFICIAL-PASS, MANIFEST-sha256 34 entries)."
  - "REACH and OPEN registrations (note SS5): C5 = with this package the two-heap pair/bed k-axis is FULLY closed-form on ALL of z >= 2, all k in Z, both mountains: K1303 band k <= 0 + K1309 congruent window + this non-congruent window + K1308 diagonal k = z + K1308 upper half k >= z — the undetermined band is GONE; O(1)-evaluable rows now cover the entire window (giant-lane adoption decision belongs to the giant-search owners, recorded as F2 connection only). The K1309 open registrations O1' and O2 are RESOLVED (the typed self-referential blocker is exactly what the hand proof discharges: C-descent preserves non-congruence, so the non-congruent packet {T-NCW-P, T-NCW-B} closes on single budget R-1). O-G2 (interior k >= 1 multi-mountain web surfaces, 3+ mountains) and F1 (C-SUM three-token typed generalization) remain OPEN and untouched: this package handles two-mountain pair/bed surfaces only. Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, classes 1/2/4 UNKNOWN at all times; verdicts unconsumed."
relations:
- type: resolves
  target: K1309
  note: "K1309 open 登録 O1′（非合同窓ペア行）・O2（非合同床行・OBS-BW 含む）を T-NCW-P/T-NCW-B で全称解決。D10 凍結表（OBS-NCW 35 行）は T-NCW-P 実例へ昇格（機体 D10 三方照合 1,295 点・凍結表分布再現 mismatch 0）。「浅い行の structured 2」の正体は dominant 列 g*=z−2k と対角線 s=z の 2 直線。blocker の構造的理由（非合同行の C 子は非合同行に落ちる自己参照）は §2.0 で逆転利用: C-descent が非合同性を保存するため packet は単一 R 強帰納で閉じる（合同 packet はclosure に joint budget が必要だった差分を §2.6 で対比）。"
- type: extends
  target: K1308
  note: "C2 により OBS-BW（床窓行 k=z−1 の全 a 0・z≥3 census 観測）を定理昇格。C4 により Z-DIAG の g=z+1 の 2 が非合同行には存在しないことを確定（T-WC との本質的相違・窓偶奇交互予想の最終整理）。"
- type: depends_on
  target: K0832
  note: "L2・床 a=1 B-exit v(1,z+1,k+1)=1 は単一トークン閉形式からの直接導出（D6 が転写閉形式・両 engine の三方照合 1,512 点）。L2 の g=z 分岐の値は初版手分析で σ=2 と誤予測したが、機械追試 108,000 点（z2..60・非合同全 k・g≤120）で (g+1)%2 一様に宣言前修正（宣言ノート §6 honest 記録）・mex 閉包への影響なし。"
- type: depends_on
  target: K1303
  note: "k=1 C 子（帯域 k=0 行・plane z−1）をペア・床両分岐で使用。D7 が K1303 cpsfG 転写照合（ペア帯域 w1..15・床帯域 w1..15・k=1 C 子 cell z 偶 4..22）3,870 点。"
- type: depends_on
  target: K1286
  note: "C1: z=2 基底行（k=1 非合同・g*=0）は K1286 の z2-k1 ペア行・b2(1)=2 と整合（窓 packet 単一 R 帰納の base・D5 が z2 を含む typed 検査 9,016 点の内側で照合）。"
- type: related
  target: K1282
  note: "engine block pin chain（埋込み bd5f22e4…・単体 582c93c1…）は K1282..K1309 kit と同一 bytes。"
- type: related
  target: K1309
  note: "C5/F2 接続: 2 山面の k 軸で未確定帯が消滅（帯域 k≤0 + 合同窓 + 非合同窓 + 対角 + 上半の和集合 = 全 z≥2 全 k）。11×11 枝刈り格子の採用判断は giant レーンオーナーに記録のみ。"
artifacts:
- path: research/log/2026-11-24-ncw-window-single-owner-note.md
  role: proof
  note: 単一オーナー宣言ノート（出版 7b992b5f・着手時 HEAD ffde117b・push 時観測 HEAD fdb3ceba・K1310 空き確認後に単一 commit）。§1 主張（T-NCW-P/T-NCW-B/C1–C5/L2）・§2 手証明全文（2.0 typed 子閉包と packet の閉性・2.1 パリティ不変量 P1–P5・2.2 L2 導出・2.3 C-descent 区域写像・2.4 T-NCW-P 区域 mex 代数〔N/N2/F/G/D〕・2.5 T-NCW-B 床区域〔Br1..Br4〕・2.6 K1309 packet との差分）・§3 宣言前探索 X1..X8 + L2 補題 108,000 凍結・§4 機体宣言（counts 51,439・変異表 13 種・predry sha 3c2eb517…）・§4.5 主張の区別・§5 open 登録 O-G2/F1/F2・§6 honest 構築経緯（L2 初回誤算と機械追試による修正・predry 初回 rc=127・D3 note 欄・`None or` 構文）。
- path: research/experiments/ncw-window-20261124/
  role: machine
  note: 実験キット一式（出版 e6ea44fb・成果物 73aa36d6）: README.md・verify_k1310.py (sha 58fd5e46…・engine pin bd5f22e4… startup ゲート内蔵)・engine_block.py (582c93c1…・K1282..K1309 chain と同一 bytes)・explore_ncw.py/.out (5d9b41b8…/3f44deff…・X1..X8+L2 108,000 凍結: X1 16,128 / X2 2,080 / X3 2 の完全局在 offband 0 / X4 5,616 / X5 297 / X6 1,260 / X7 840 / X8 4,264)・predry/dryrun1-4 (+.info・byte-identical 3c2eb517…) + 公式監査成果物（output/audit_run1-4.out+.info・tamper レコード 13・detcheck.json OFFICIAL-PASS・MANIFEST-sha256 34 entries）。fetch-back 全ファイル sha 一致（初回 raw 404 なし）。
- path: research/log/2026-11-24-noncongruent-window-collapse.md
  role: report
  note: 実行 log（出版 chain 7b992b5f→e6ea44fb→73aa36d6 の記録・公式 4 走・変異電池 13 種の実測表・受入判定・§4.5 の主張区分の再掲・次課題 O-G2/F1）。

## 概要

K1309 が O1′/O2 として残した**非合同窓行**（1 ≤ k ≤ z−1・k ≢ z mod 2）の
ペア・床の真の法則を 2 本の全称定理で確定し、2 山面の k 軸の未確定帯を消滅させた:

- **T-NCW-P**: 非合同ペア行は dominant 列 g*=z−2k の flip wedge 則に従う。
  値 2 は楔 {g≤g*, s≥z} 内の 2 直線（g=g* と s=z）上のみ。Z-DIAG の
  g=z+1 の 2 は非合同行には存在しない。
- **T-NCW-B**: 非合同床行は g*<0（k=z−1 頂行を含む全行）で 0、
  g*≥0 で r=(z−1)//2 を境に 0/1/2 の階段。

C1（z=2 基底行・K1286 整合）・C2（OBS-BW 定理昇格）・C3（OBS-NCW 35 行凍結表が
T-NCW-P の cellwise 実例）・C4（合同/非合同の法則の本質的相違の確定）・
C5（全 k 軸確定）が corollary。L2（B-exit 一様則・g=z 分岐も含めて
(g+1)%2・床 a=1 は 1）は K0832 から直接導出。

構造の鍵は **C-descent が非合同性を保存する**（k−1 ≢ z−1）ことで、
K1309 の合同 packet では相互再帰のために joint budget が必要だったのに対し、
非合同 packet {T-NCW-P, T-NCW-B} は C 子が自分自身の packet に落ちるため
**単一予算 R の強帰納**で閉じる。これが O1′ blocker の解除機構。

## 主張の区分（過大主張の防止）

- 定理（全称証明・宣言ノート §2 に証明全文）: T-NCW-P・T-NCW-B。
- 導出補題（published からの直接導出）: L2・C1・C2・C3・C4・C5。
- census は証明ではない: 51,439 点は定理・手表の実機照合（bad 0）であり、
  定理の全称性は手証明によって成立する。
- D10 は観測表のサブサンプション（観測→定理実例の昇格確認）であり
  新規法則主張ではない。OBS-NCW/OBS-BW の昇格済み要素は以後 K1310 を引用。
- O-G2（3 山以上の窓面・multi-c web）と F1（C-SUM 3 トークン）は未解決のまま。

## 公式監査（publish-then-execute）

- 宣言 7b992b5f（着手時 HEAD ffde117b・push 時観測 HEAD fdb3ceba・K1310 空き・
  Part DX batch-36 レーンと直交・対抗宣言なし）→ 機体 e6ea44fb（13 ファイル）→
  fetch-back byte 一致（全 sha256 が宣言 pin と一致・全ファイル初回 200）→
  公式 4 走（同一 cwd×2 PYTHONHASHSEED=random/1 + 隔離 tree/env -i×2 99/7）
  すべて rc=0・stdout byte-identical sha256 3c2eb517…（宣言・predry と同一）。
  約 2.5 秒/走。
- counts `[12096, 5760, 4320, 2058, 9016, 1512, 3870, 4960, 372, 1295, 4680, 1500]`・
  総計 51,439 点・bad 0・engine_gate PASS。D5 typed（z2..14・手表+
  published 閉形式のみで子構成・mex == 申立 == engine 三点一致）・D6 L2 三方照合・
  D7 K1303 cpsfG 転写ゲート・D8 公刊アンカー 4,960・D10 凍結表サブサンプション・
  D11/D12 k=1 行・床頂行 stress。
- 変異電池 13/13 検出・宣言どおり: engine rc=2（0ea47a80…）・np1 12,096・
  np2 5,760・np3 4,320・bd 2,058・ty 40,690（D6–D9=0 は申立関数を参照しない
  engine 照合電池故の honest 値）・be 1,512・cp 3,870・ps 4,960・xg 372・
  rw 1,261〔申立 1,260+凍結表 '3,2' 行 1〕・ex 4,680・bs 1,500（rc=1）。
- 成果物出版 73aa36d6（audit_run1-4.out+.info・tamper レコード 13・
  detcheck.json OFFICIAL-PASS・MANIFEST-sha256 34 entries）。

## 11×11・規約への接続

- verdict 不消費・11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4 は全時点 UNKNOWN。
- 2 山面（ペア・床）の k 軸は全 z≥2・全 k∈Z で閉形式確定（C5）。
  O(1) 即値格子の全窓拡大を giant レーンオーナーに記録するのみ
  （採用判断はオーナー側）。

## 次課題（単一オーナー候補）

1. **O-G2**: 内面 k≥1 の multi-c web（3 山以上の窓面）。2 山 packet の閉性が
   単一 R 帰納できた点が typed 化の足がかりになるか。
2. **F1**: C-SUM 3 トークン typed 化（K1308/K1309 から不変）。
3. **L2 の一般化**: B-exit 一様則の m>1 版・r 人対戦版の成立可能性の探索
   （本項では m=1 と床 a=1 のみ確定）。
