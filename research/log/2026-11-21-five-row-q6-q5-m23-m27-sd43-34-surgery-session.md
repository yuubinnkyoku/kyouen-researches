# 2026-11-21 五行 q6/q5 m=23/m=27 sd≤(4,3)/(3,4) 部分掃引 — session log（高速レーン）

## レーンとコミット列

- 単一オーナー宣言ノート:
  `research/log/2026-11-21-five-row-q6-q5-m23-m27-sd43-34-surgery-single-owner-note.md` = `0b2a6466`
  （宣言時 main HEAD `5c4cfca9`・受入条件6項目・in-flight species レーン `5c4cfca9` と disjoint）。
- 実験dir出版: `research/experiments/five-row-q6-q5-m23-m27-sd43-34-surgery-20261121/`
  60ファイル = `ebc712db`（HEAD-before-push `6273b13f`・fetch-back 59/59 ファイル sha256 一致 +
  manifest.json byte 一致・commit固定 raw URL）。
- csv note/source 行置換（(5,6)/(5,5) の2行）+ 本session log = この commits 直後に適用:
  HEAD-before-push `ebc712db2a83518202d29aa5f664c9989d79e8f0`・csv は 23:06Z の species レーン追記を含む
  最新版（61,934B・git blob `74494ebd398dc9d9166001ad9ec346b1d276e17a`・取得時点で不変確認済み）へ、
  (5,5)/(5,6) 行の source/note のみ追記（M/status 列変更なし・他119行 byte 不変・検証済み）し、
  `create_or_update_file`（blob sha 指定・競合時は失敗する安全な経路）で push。

## 主成果（全て陰性・局所クラス主張・不在主張ではない）

- **(5,6) 5x23**: 予算 (4,3) で 3 クラス代表（対称性クラス縮約補題・span 21 → 3類）計
  24,896,019 final-state leaves、予算 (3,4) で 96,514,929 leaves、いずれも 0 maximal / 0 witness。
- **(5,5) 5x27**: 予算 (4,3) で 8 クラス代表計 39,990,167 leaves、予算 (3,4) で 187,753,471 leaves、
  0 maximal / 0 witness。
- 合計 22 クラス代表 348,154,586 leaves（+交差検査4実行+決定論性再実行4実行 = 30実行）。
- **矩形対称性補題の予算拡張**: 各キャンペーン各予算で V@2（q6・クラス t=0）/ HV@7
  （q5・クラス t=0）交差検査が id@0 と全論理不変量一致（nP/nPpruned/nRmLeaves/nSafe/
  nMaximal/nWitness/nEmpty/nTprime）で、補題が (4,3)/(3,4) でも機械成立。代表点のみの実行は
  補題により 12/32 配置を正当化（各地1クラスメンバーで確認、他クラスメンバーは親実験で
  全配置検証済み）。
- 決定論性: 各キャンペーン各予算で id@0 を再実行して全論理値一致（elapsedMs のみ差異）。
- コントロール: census4 gates (5,12,6)=212/(5,15,5)=629/(5,23,6)=996/(5,27,5)=2355 PASS・
  シード健全性（sat_verify + safety_only + 独立Python Fractions）PASS・tamper 対照は
  3系統で UNSAFE/FAIL・not-maximal 対照は対象盤で FAIL・
  自己補完陽性対照（minus2 シード・(2,2)予算）は q6=4 witness（公開 witness 含む）/ q5=1 witness
  を再発見（親実験の対照と同値・機械が witness を見逃さないことの end-to-end 保証）。

## 増幅の実測（次段予算の判断材料）

- 第4追加点: nP は q6 125,671→2,786,101（×22.2）・q5 260,246→7,385,056（×28.4）。
  第4削除レベル: nRmLeaves は q6 5,162,142→32,446,931（×6.29）・q5 3,522,581→22,588,388（×6.41）。
- 実行時間: (4,3) 49-60s/実行・(3,4) 209-262s/実行。次段 (4,4) は2軸の積でおよそ ×6.3×(追加軸も増)
  となり単発 2,000s 超・本レーンの単発壁 (~262s) の向こう側。並走slot/chunk機構が要る。

## 正直面

- (3,4) q5 id@5 の1回目はインフラ障害（Koyeb remote command sync 失敗・ラン自体と無関係）で
  出力喪失。同一コマンドの fresh 再実行で完走し、invariant はクラス内で独立に整合。
- 全 (3,4) 実行は単発壁内に収まった（budget-limited INDETERMINATE なし）。

## repo外の知見

- 実験ツリーは最初から knowledge 配下 kit（`_frontier-sd6-surgery-kit/exp3/`・
  リセット耐性）に置く親セッションの設計を踏襲・環境リセットでの喪失ゼロ。

## 次の実行可能課題（このレーンの後継候補・宣言必要）

- (4,4)/(5,3)/(3,5) 予算: 単発壁越えのため時間分割機構（offX や add-prefix での chunk 化）の
  実装が先行条件。増幅率は本 log で定数倍評価可能。
- 陰性クラスの被覆状況: m22+m21種（q6）と m26+m25種（q5）について sd≤(3,3)∪sd≤(4,3)∪sd≤(3,4)
  が本レーン系（親+species並走+本レーン）で埋まった。次は異種構造（遠距離ジャンプ・別種）のみ。
- 対称性補題の K 昇格は bbox-grid レーン全体の方法論として次回統合時に提案のまま。

## 状態

- M_{5,6} ∈ [23,249]・M_{5,5} ∈ [27,336] 不変（M 列変更なし・note/source のみ拡張）。
- K item は作成しない（実験1回1K規約・陰性成果はCSV noteと実験READMEに記載）。
- 標準11x11空盤・二石root・S2・class 1/2/4 は本レーン非接触で UNKNOWN のまま。
