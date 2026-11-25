# 2026-11-12 n11 S2 {59,60} milestone-3 manifest（greedy証明書1–8・blocker 12個・S6 orbit 20,534・49.1%）

長期レーン。main = eb1f5ca 開始（反映直前 f6168cf まで再取得・S2 experiment pathへの
並走なし・K0753空きを items directory 実参照で確認）。K0748（milestone-2、証明書1–5・
blocker 7個・S6 orbit 10,988）を greedy順で証明書6–8（{73} → {90,96} → {23}）まで拡張し、
**milestone-3**（60 blocker中12個閉鎖）のS6 orbit worklist manifestを確定した。

## 手順（16MiB sandbox制約による分割生成）

1. **証明書6–8の新規列挙**（milestone2_worklist.ts と同一の整数外接円circle-mask幾何・
   D4 canon・78 FW oracle条件付き）: certReps=[73,90,96,23]、certBits=32,64,128,256。
   sandboxの16MiB制約で milestone-2 manifest（715,236 bytes）のfetch+全証明書再列挙は
   不可 → 証明書6–8単独のunion（fresh678）を列挙して file_system.write_file で書き出し、
   jq で milestone-2 output と merge した（merge_manifest.sh がそのまま再現手順）。
2. **jq merge**: 鍵(hex)で group_by → 共有鍵は certs bitmask を OR。cost・protocol・
   schema 文言は milestone-2 を引き継ぎ、certStats を 9 entry（{90} と {96} は別entry・
   鏡映同一集合）に拡張。

## 確定値（全て既知値と一致）

- 単独証明書S6 orbit: {73}=3,868（義務7,890 = verify_conditional_s6_cover_46.py と同規約）、
  {90}=4,232（義務8,626）・{96}=4,232（8,626）・**{90} と {96} のorbit集合は
  D4鏡映で完全同一**（全要素一致を機械検証）→ greedyの {90,96} は1証明書として
  bits 64|128 が常につく。{23}=4,416（義務8,859）。
- 証明書6–8の相互union: **11,794**（K0748 ladder測定と一致）。
- **merged union: 20,534**（41,842全体の49.1%・K0748の別実行ladder測定と完全一致）。
  内訳: milestone-2由来 10,988（うち2,248件が証明書6–8と共有でcerts拡張）+ 新規 9,546。
- **milestone-2 subset検証PASS**: 10,988鍵全件がmergedに存在、**cost不一致0件**、
  重複キー0件、s6All cost昇順単調を検証。
- S5 orbit union: 261 + 283 − 共有 → **516 / 1,447（35.7%）**（K0748と一致）。
- cost（合法S7子数）: **min 50**（milestone-2の52より低い新規帯あり）/ 中央値 78 /
  max 101 / 平均 78.117 / **合計 1,604,047 raw S7辺**（milestone-2の874,761比 +729,286）。
- manifest = **627,770 bytes**（compact形式 `n11-s2-5960-milestone3-s6-manifest-v1-compact`:
  s6All = [非ゼロパディングhex, cost, certs] 配列・cost順・certs bitmask 9 entry・
  s5Reps = [hex, certs, obligations]）。merge_manifest.sh が byte-exact 再現
  （md5 8ab21c1f… 一致を検証）。field-name形式（milestone-2互換・1,355,358 bytes）は
  merge_manifest.sh の compact 段を省略すれば同一内容で再生成できる。

## solverへの意味

- 外部solverはmilestone-3を単一バッチworklistとして消化できる
  （cost順・D4 canon・WIN/LOSS conflict検出はprotocol文言どおり）。
- 新規9,546 orbitのcost分布はmilestone-2より軽い側に広がり（min 50）、
  cost下位帯から消化することでcache暖機が早い。
- greedy 9位以降のcensus（{31}/{89,97}は追加orbit 0 = union8の部分集合）は
  本manifestを基準に次回測定する。

## 実装教訓

- github_app.get_file_contents で715KB manifestをfetchすると、tool結果の保持分で
  sandbox 16MiB制限を超過（1 operation で MemoryLimitError）。大型repo成果物は
  **fetch結果（tool-results保存ファイル）から bash+jq で抽出**して使うか、
  sandbox内で列挙だけ行い file_system.write_file で中間成果を書き出す。
- jq で group_by による鍵mergeは線形で安全だが、`index()` を使った部分集合検査は
  O(n²) で iteration limit 1000万超過 → 検査も group_by+length==2 で行う。

## 次の一手

- 外部solverでmilestone-3 manifest（20,534 S6 orbit、cost順）を消化し、
  S6 verdict蓄積 → 8証明書のS5閉鎖判定 → 12 blocker閉鎖。
- greedy 9位以降のcensus（union8基準のmarginal orbit数の全blocker測定）。
- milestone-3 manifestの消化が進んだ時点でmilestone-4（残りblockerの追加証明書）。

11×11空盤・二石root {49,60} は **UNKNOWN**。
