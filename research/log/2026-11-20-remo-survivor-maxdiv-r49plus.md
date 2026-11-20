# 2026-11-20 生存者列最小周期: 最大真約数帰約LEMMA REDとr=49..150 maxdiv掃引 part1（K1163）

高速レーン。単一オーナー宣言は
[remo-survivor-maxdiv-r49plus-single-owner-note](2026-11-20-remo-survivor-maxdiv-r49plus-single-owner-note.md)
（宣言commit 97b741b8・誤植訂正commit f4af3e1b）。対象はK0925定理S32
・K1145定理S48の続編。r33plusレーンが宣言ノートで招待していた
「生存者列の全称必要性」は本レーンでは閉じずOPENのまま、
その機械フラグメント（帰約補題＋拡張掃引＋構造観察）を出版した。

## 経緯

- 17:18Z: 単一オーナー宣言出版（97b741b8）。この時点の想定item番号は
  K1162（main最大K1161）。
- 検証器 verify_survivor_maxdiv_r49plus.py を完成（8チェックC0-C7・
  stdlibのみ・決定的・per-r checkpoint output/ck/・--no-cache全再計算・
  assemble二重実行byte一致assert・--no-cache隔離環境（別cwd/別HOME/
  一方はPYTHONHASHSEED=random）2回の全再計算でaudit.json・
  witness表ともbyte一致を確認）。
- 17:31Z: 並走y12 universalレーンがK1162を出版（commits
  60622f35/258cd7b0/1093e075・two-token-y12-universal-verifier-part1）。
  直前の3点確認（README grep・raw item 404・コミット一覧）で
  K1163が空きと確認できたため、AGENTS.md再採番規則に従い
  **K1163へ再採番**（main既存の番号は変更しない・参照をすべて更新）。
  検証器のitem埋め込み欄をK1163へ変更し--no-cache全再計算
  （checks:8 ok:8 all_ok:True・112.2s）で監査を再生成。
  K1162版監査とitem欄1行を除きbyte一致（diff機械確認）・
  witness表のSHA-256は不変（cdf890c1…）。
- part1出版（fetch-backはコミットSHAピンrawでbyte照合・branch refの
  fetchはCDNキャッシュ遅延があるためピンSHA参照を使う）:
  - 9fb9b796: 検証器（26,710 bytes・byte一致確認）
  - 41ea9727 → c4324730: report.md（初回pushで1箇所だけ余計な
    バッククォートがあるのを正本diffで発見し再push・byte一致確認）
  - 17fa1925: maxdiv_witness_table.txt（9,148 bytes）+
    published_run.txt（154 bytes・byte一致確認）
  - 42d00bf5: audit.json（51,077 bytes・SHA-256 d916f0a2…が
    report内ピンと一致・byte一致確認）

## 成果の要約（正本研究 log への要約にすぎない）

1. **LEMMA RED（全称・証明つき）**: m=Q(r) ⟺ 全ての素数p≤rで
   最大真約数Q(r)/pが周期でない。K0922補題DIVの系としてreport.mdに
   証明掲載。検査数がd(Q(r))−1からπ(r)へ崩壊
   （r=48: 294,911→15・r=150: 1,546,188,226,559→35）。
2. **定理S150（機械・r=2..150）**: r=49..150の全2,602 (r,p)対が
   窓[1,150]で棄却（フォールバック不使用・fail-closed）。
   witness全部≤r−1・全局最大は124（ブロック{131..136}）。
3. **等Qブロック同一性の拡張**: 40/40複数メンバーブロックで
   (p→最小witness)マップ完全一致・隣接対照47組全不一致（C6）。
4. **負の観察（C7）**: 棄却ベクトル（C∈[1,60]）レベルの同一性は
   不成立（{17,18} p=3でC=12・{37..40}/{113,120} p=13,19で相違）。
   K1145同一性は最小witnessレベルが正しい不変量。
5. **h*=1 argmaxパターンはr≤48の人工物**: r=49..150では6rのみ。
   また出版値との比較で、r∈{19,20,21,22,27,28}では全真約数側の
   witness最大値が最大真約数側より真に大きい（witness最大の約数は
   最大ですらない）ことをC3が機械記録。

## 値レベル同一性のprobe（本logにのみ記録・監査外）

reportの観察4に「same-block survivor columns differ from each other
starting just beyond the K0926 plateau; checked in the lane log」
と書いたprobeの機械記録:

```
block pair 17 18  first value-level diff at C = 18  (= r'+1)
block pair 29 30  first value-level diff at C = 30  (= r'+1)
block pair 37 40  first value-level diff at C = 38  (= r'+1)
block pair 49 52  first value-level diff at C = 50  (= r'+1)
block pair 89 90  first value-level diff at C = 90  (= r'+1)
block pair 113 120 first value-level diff at C = 114 (= r'+1)
block pair 131 136 first value-level diff at C = 132 (= r'+1)
block pair 139 148 first value-level diff at C = 140 (= r'+1)
```

（r′はブロック先頭。survivor_fastでC∈[1,400]を走査し最初の
不一致Cを記録。すべてC=r′+1。K0926 E6UプラトーC≤rでS(C,r)=P(C)
である限り列は一致し、小さいrのプラトー終端の直後に必ず相違する。
最小witness同一性（C6）は値レベルの同一性とは独立な現象である
ことがこれで確定した。）

## 次の一手（未着手）

- 等Qブロック同一性（最小witnessレベル）の統一説明の試み
  （K0928 pot縮約構造からの説明が候補）。
- 等Qブロックのwitnessマップとブロック先頭素数の関係
  （h*=1がブロック先頭素数そのものに限られる構造）。
- witness表をr=151以降に延ばす閾値調査（窓[1,150]が破れる最初の
  (r,p)がいつ現れるか・フォールバックの使用頻度）。

2026-11-20 高速レーン
