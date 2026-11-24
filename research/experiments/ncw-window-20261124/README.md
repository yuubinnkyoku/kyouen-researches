# ncw-window-20261124 — 遷移窓非合同行パッケージ機体（K1310）

publish-then-execute: 単一オーナー宣言ノート
`research/log/2026-11-24-ncw-window-single-owner-note.md` が先に出版
されており、本キットはその §4 機体宣言の実体。定理・証明・非主張の区別はすべて
宣言ノート参照（この README は重複正本としない）。

## 主張の要約（詳細は宣言ノート §1/§4.5）

- **T-NCW-P**: ∀ z≥2, m≥1, g≥0, k∈[1,z−1]（k ≢ z mod 2）:
  g*:=z−2k, s:=2m+g として H(2m+g+k; (m,m+g); z) =
  [g odd]（g*≤0 or g>g* or s<z）/ 2（g≤g*, s≥z, g=g* or g=z−2m）/
  [g even]（その他の flip wedge）。claim 評価順序は宣言ノート §1（N 枝が先）。
  値 2 は dominant 列 g=g* と対角線 s=z の 2 直線上のみ。
- **T-NCW-B**: 床 H(2a+k−1…; (a,a); z) 型全非合同行:
  g*<0 → 全 0 / g*≥0: a≤r → 0、z 奇 → a≥r+1 で 1、z 偶 g*=0
  （z≡2 mod 4）→ a≥r+1 で 2、z 偶 g*>0 → a=r+1 で 2・a≥r+2 で 1。
  r:=(z−1)//2。k=z−1 頂行（OBS-BW）を含む。
- **L2**（導出）: m=1 NCW pair の B-exit σ(g+1,z+1,g+k+1)=(g+1)%2=[g even]
  が全分岐で一様。床 a=1 の B-exit は常に 1。
- **C1**（z=2 基底行 ↔ K1286 整合・b2(1)=2）/ **C2**（k=z−1 頂行 = OBS-BW 解決）/
  **C3**（OBS-NCW 35 行凍結表の定理昇格）/ **C4**（2 の局在・T-WC との本質的相違）/
  **C5**（2 山面の全 k 軸確定: K1303 帯域 + K1309 合同窓 + 本項非合同窓 + Z-DIAG +
  T-UH/T-DU′ で未確定帯消滅）。K1309 O1′/O2 解決。
- 規約上: verdict 不消費・11×11 巨大探索への影響は literary（構造補題の接続は
  giant レーンオーナーの判断）。

## ファイル（sha256）

| file | sha256 |
|---|---|
| verify_k1310.py | `58fd5e46d52a5a62950b796506e08704987bdb0badfedc73ca754468824d94f3` |
| engine_block.py | `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`（K1282..K1309 chain と同一 bytes） |
| explore_ncw.py | `5d9b41b8d6c756ffd8932275bbb651b605ced2847930af9cea2067f682bbe3d8` |
| explore_ncw.out | `3f44deffe77ed2f2d69dd67cec20ce0b5bbef8e10685a6b6b08329cdb4f78e75`（宣言前探索・凍結・X1–X8 + L2 補題 108,000 の正本） |
| predry/dryrun1-4.out | 4 走とも `3c2eb51742c568536b0bf67738be3c2f7b59bf87ae8a1eba42e28ead11168949`（byte-identical） |

埋込み engine block の起動 sha gate: pin
`bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92`
（verify_k1310.py 内蔵・不一致なら即時 abort）。

## 電池（宣言ノート §4・総計 51,439 点・期待 overall_bad = 0）

D1 T-NCW-P pair census 12,096 / D2 far stress 5,760 / D3 m 距離 stress 4,320 /
D4 T-NCW-B census 2,058 / D5 typed self-check（手申立+K0832/K1303 閉形式のみで
子構成・mex==申立==engine 三点一致）9,016 / D6 B-exit triple 1,512 /
D7 帯域+C 子 cell gate（K1303 cpsfG 転写込み）3,870 / D8 公刊アンカー
（K1309 T-WC/T-WBC・K1308 Z-DIAG/T-UH/T-DU′）4,960 / D9 cross-engine 372 /
D10 OBS-NCW 凍結表サブサンプション 1,295 / D11 k=1 行 stress 4,680 /
D12 床 k=z−1 行 + 深 tail stress 1,500。

## 変異電池（fail-closed・事前宣言）

- `--tamper-engine` → rc=2（変異 sha `0ea47a80…` ≠ pin）
- `--tamper=np1` → rc=1, bad 12,096 / `np2` → 5,760 / `np3` → 4,320 /
  `bd` → 2,058 / `ty` → 40,690（D1..D5+D10 主張部分+D11+D12; D6–D9=0 は
  申立を参照しない電池故の honest 値）/ `be` → 1,512 / `cp` → 3,870 /
  `ps` → 4,960 / `xg` → 372 / `rw` → 1,261（申立 1,260+凍結表 '3,2' 行 1）/
  `ex` → 4,680 / `bs` → 1,500

## 公式監査（本キット出版後に fetch-back bytes から実行・成果物は output/ に追記出版）

1. fetch-back: 全ファイル size+sha256 byte 照合（API 側・全ファイル）
2. 公式 4 走: 同一 cwd ×2（PYTHONHASHSEED=random/1）+ 隔離 tree/env -i ×2
   （PYTHONHASHSEED=99/7）→ 全走 rc=0・stdout byte-identical
   （predry と同一 sha `3c2eb517…` を確認）・総計 51,439・overall_bad=0
3. 変異電池 13 種 → 上表 bad count・rc で全 fail-closed 確認
4. output/audit_run1-4.out/.info・tamper レコード・detcheck.json・MANIFEST-sha256 出版

## 規約

verdict 不消費・11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4
は全時点 UNKNOWN。engine は K1138 転写（sha pin 実装）・census は照合であって
証明の代替ではない。証明は宣言ノート §2（手証明全文）。
