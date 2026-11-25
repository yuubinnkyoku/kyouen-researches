# Part DU 完了log (2026-11-24): batch-34 small-pocket 2キー probe 完走 — honest labels WIN 2行 (verdict不消費・11×11 UNKNOWN)

- 事前登録宣言: `research/log/2026-11-24-part-du-batch34-smallpockets-declaration.md` (commit `5ec15665`, observed HEAD-before-push `7666ae8d`)
- kit (commit `a0d40d47`): pinned runner `runbatch.sh` (`f591f8c2…`・batch-33 kitとbyte-clone) + pinned replica `jsreplay.js` (`84585617…`・byte-clone) + 新規maker `make_batch34_keys.py` (fail-closed gates G1–G6 all PASS 3回byte-identical, tamper battery pin層 5/5 + semantic層 2/2) + inputs (ag001/ag002/batch-keys-b34.json) + val-gate 8 (published batch-33 baselines)
- outputs (commit `1039a95d`): status.log 4行 (PASS 2 + WIN-HALT 2, WIN-CONTINUE は事前登録どおり) + raw 4 (2-pass fresh-cold) + val-gate fresh `.b34-host.out` 4

## 実行結果 (honest labels)

- **val-gate fresh 4/4 node-exact** (宣言後fresh実行): at2m×2 (budget 2,000,000, result 0, nodes 2,000,000) ・first-15m (budget 15,000,000, result 2, nodes 3,651,923) ・second-15m (budget 15,000,000, result 2, nodes 5,040,200)。全てpublished baselineとresult・nodes一致。
- **ag001** (serving class 23101, key `[1152921505747697664, 1032]`, legal 85, s5 745184): **WIN (result 1)・nodes 9,149,084**, 2-pass fresh-cold node-exact (48s / 47s)。
- **ag002** (serving class 1849, key `[1153485622925590528, 0]`, legal 88, s5 81011): **WIN (result 1)・nodes 4,893,014**, 2-pass fresh-cold node-exact (25s / 24s)。
- WIN-HALT (rc=45) は runbatch.sh の事前登録された挙動で、WIN-CONTINUE 規則どおり両キーのhonest labelを完走させた。determinism mismatchなし (HARD-STOP未発動)。

## verdict不消費とscrutiny owner C++ gate の現状

- 本Partはprobe完走とhonest label出版のみ。canonical chain cache `973bcd19…` (6,547行) への書込なし (両キーのexact-pair不在は宣言時G4 gateで機械確認済み)。closure表・free_now・excluded_now・unknown・update8・greedyの変化は本Partではderiveしない (adoption後のrefresh再実行+独立監査が機械導出する)。
- 採用ゲート C++第二実装 `cpp/solvers/kyouen_dfpn_root.cpp` (pin `9193f5b6…`) は**本実行環境では実行不能** (C++コンパイラ不在・パッケージ導入禁止; 2026-11-22 Part G当初の障害と同一)。よってWIN 2行の採用は引き続きscrutiny ownerが専権のまま。closure表 rank 1 (class 23101) ・rank 2 (class 1849) は採用待ちのため**本時点でもunknownのまま**。
- honest label WIN = 採用候補の記録にすぎず、WIN/LOSSの消費・クラス閉鎖・root被覆・securedの主張は本Partでは一切行わない。

## 後続 (別Partとして実施済み)

Part DU-b (declaration commit `7141772d`, 2026-11-24) で本WIN 2行の第三実装交叉検証を実施した: third = published replica = this-host replica = 1 (WIN) verdict一致 2/2, fail-closed audit ALL 117 GATES PASS×3回byte-identical, tamper battery 10/10+control。ただし第三実装一致は採用ではない (verdict不消費は不変)。

## UNKNOWN担保

**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4・class 23101・class 1849 (本batchの2キーを含む全メンバー) は本Partの実行・出版のどの時点でもUNKNOWNのまま。** nodes数・wall秒数を勝敗や距離として読まない。WIN採用はscrutiny owner C++ gate通過後の別adoption Part (pinned merger `90711961…` 専権) のみ。
