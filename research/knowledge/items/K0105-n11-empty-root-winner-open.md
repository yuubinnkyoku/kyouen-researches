---
id: K0105
title: 11×11の真の空盤勝敗は現在の主要未解決問題
kind: question
status: open
topics:
- square-outcomes
aliases: []
relations:
- type: depends_on
  target: K0023
  note: ''
- type: depends_on
  target: K0028
  note: ''
- type: depends_on
  target: K0312
  note: 最小極大サイズの境界は空盤勝敗と別の確定結果
- type: depends_on
  target: K0313
  note: 最大安全サイズの存在下界は空盤勝敗を決めない
- type: depends_on
  target: K0355
  note: reply27の有限証明境界の進捗。二石rootと空盤の勝敗は未確定
- type: depends_on
  target: K0372
  note: solver/cache 葉への依存の信頼境界を参照
- type: depends_on
  target: K0676
  note: 四石領域位置S4-A/B先手勝ち（空盤への鎖の決定部分）
artifacts:
- path: research/log/claim-audit/N11-DFPN-NIGHT-REPORT-2026-09-30.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/n11-search-methods/reports/N11-RESULT.md
  role: source
  note: 層0..5の厳密列挙と層6以降の資源下界
- path: research/experiments/saturation/reports/saturation-20261003.md
  role: source
  note: 8≤s_11≤10の有限完全排除と10石証人
- path: research/experiments/saturation/reports/saturation-20261003-extra.md
  role: source
  note: K_11≥21の独立検査済み安全配置
- path: research/experiments/n11-s6-terminal-loss-20261015/verify_s6_terminal.py
  role: verifier
  note: 固定先手 S6 LOSS の cache-free 終局証明; 483 S10 LOSS 葉, 1,028,621 状態; 6 S5 LOSS 親; 空盤 winner は未確定
- path: research/experiments/n11-s7-fifth-terminal-20261015/fifth_verify_standalone.py
  role: verifier
  note: S7 WIN の第5独立終局証明; 35 S8, 738 S9-S10 辺, 468 S10 葉, 93,481 状態; 空盤 winner は未確定
- path: research/experiments/n11-s9-second-target-20261015/verify.py
  role: verifier
  note: S9 葉 64 件の C++/Python 一致終局検証; 49 LOSS / 15 WIN; 7,629 状態
- path: research/experiments/n11-central-19-cover-20261031/shared58_s6_win_strategy.cert
  role: certificate
  note: 修復後46証人のうち2類を元先手WINと確定する共有七石終局戦略; 10,881選択局面・16,980到達局面・2,237終局
- path: research/experiments/n11-central-19-cover-20261031/verify_shared58_s6_win_strategy.py
  role: verifier
  note: 4x4整数幾何で全応手を再計算し、180度回転による2つ目のWIN6も独立検証
- path: research/log/2026-11-02-n11-central49-shared58-two-certified-win6-refute-1980.md
  role: log
  note: 修復後1,980七石の条件付きLOSS計画失効と証明境界
scope: 標準q=4・完全指摘・通常プレイの11×11空盤勝敗。層列挙・極大サイズ・misère勝敗とは別。
---

# 11×11の真の空盤勝敗は現在の主要未解決問題

標準通常版11×11の真の空盤勝敗はUNKNOWN。厳密な安全局面列挙は層0..5までで、層5には未計算の合法辺2,439,393,194本が残る。層5を終局にした旧DP勝敗は撤回済み。

層6の安全局面数は一般被覆評価でも3,194,106,864以上となり、既存環境での全状態DPは資源上困難。df-pn系探索の局所完了・途中統計は空盤全体の完了を意味しない。

周辺では8≤s_11≤10とK_11≥21が確定している。前者の8・9石極大の有無、後者の真の最大サイズは未確定であり、いずれも空盤勝敗とは別の問題である。

空盤の決着には真の終局まで閉じるAND/OR証明または正しい完了求解が必要。旧one-wordのK_11=11、打切りDP、proof numberを勝敗根拠にしない。

中央初手後のreply27について、保存済みexact境界の回収と現在の検証範囲は[K0355](K0355-n11-reply27-cache-recovery-frontier.md)を参照する。この局所的な進捗から二石rootや空盤の勝敗を推定しない。

[K0372の独立監査](K0372-n11-independent-exact-evidence-trust-audit.md)は上位証明の幾何・伝播とsolver/cache葉への信頼を分離した。少数のterminalまで閉じた独立minimax certificateは得られたが、空盤の証明は未完了であり、この問いのstatusはopenを維持する。

## 2026-10-17 bounded advance

New finite evidence: three local terminal certificates independently verified (all verifiers exit 0): S6 fixed-first LOSS (483 S10 LOSS leaves, 1,028,621 states, 6 S5 LOSS parents); S7 WIN (35 S8, 738 S9-S10 edges, 468 S10 leaves, 93,481 states); S9 leaves 64 (49 LOSS / 15 WIN, C++/Python agree). Saturation bounds 8<=s_11<=10 and K_11>=21 remain separate.

Scope clarification: these are local terminal certificates only; they do not close the empty-board winner or two-stone root. 11x11 empty-board winner remains UNKNOWN; layer 5 still has 2,439,393,194 uncomputed legal edges.

Next steps: integrate first-move branches into a single empty-root KYOENC4 DAG; continue layer-5/6+ DP. Status remains open.

## 2026-10-17 bounded advance (round 2)

New finite evidence: independent audit of local S8/S9 terminal certificate chains on 11x11 standard q=4. S9: 64 terminal leaves (49 LOSS, 15 WIN), 7,629 states; S7 WIN: 35 S8 children, 738 S9-S10 edges, 468 unique S10, 93,481 states; S6 fixed-first LOSS: 483 terminal S10 LOSS leaves, 1,028,621 states; S8 targeted: 171+16 S8 WIN roots and 3 S8 LOSS roots. C++ and Python agreed; SHA-256 consistency checks passed; mutation/negative controls rejected tampered certificates; clean-room reproduction PASS. reuse_certificates.py verification.passed=true.

Scope clarification: local terminal certificates and propagation only; does not close empty-board winner, two-stone root, layer 5 (2,439,393,194 uncomputed legal edges), or saturation bounds 8 <= s_11 <= 10 / K_11 >= 21. K0105 remains open; no solve claimed.

Next steps: continue referencing K0355/K0372 for trust boundaries; optional add S8 verifier artifacts (`research/experiments/n11-targeted-terminal-lift-20261015/scripts/verify_s8_batch_cpp.cpp`, `verify_s8_batch_python.py`, `verify_s8_loss_batch_cpp.cpp`, `verify_s8_loss_batch_python.py`, and `certificates/new_s8_171_terminal.cert`, `new_s8_win_sixteen_terminal.cert`, `new_s8_loss_three_terminal.cert`). Preserve warnings about truncated DP/old win-loss claims. Status remains open.

統合監査（2026-10-20）: 上記2026-10-17の追記はローカル研究時点の報告であり、今回すべての探索・測定を再実行したものではない。再検証の範囲は `research/experiments/local-main-integration-20261020/README.md` に記す。既存の未解決性・量化の限界を維持する。

## 2026-11-02：中央49の条件付き六石LOSS計画に終局WIN反証

中央応手二石 `{49,60}` の優先四石局面から構成した46個の条件付き六石LOSS証人の一つ、`00000000000000603800000000008000` は、**元先手固定視点でWIN** と独立終局検証された。六石で元先手が点20へ置き、以後の元先手手番5,923局面に対する選択手と、相手の全合法応手を含む8,949局面・951終局の戦略証明書 `research/experiments/n11-central-19-cover-20261031/focus_s6_win_strategy_1984.cert` を保存した。別実装 `verify_focus_s6_win_strategy.py` は4×4整数Bareiss行列式から全合法手を再生成し、到達した終局がすべて奇数石（元先手WIN）であることを確認する。GitHub Actions #41351576503 成功。保存証明書SHA-256は `390554902426c5876b9742edb4219cae13648e103d6310d4f94b9d690ea4e63e`。

この結果、旧46六石証人のうち当該局面をLOSSと仮定する**選択計画は失効**する。ただし四石局面・二石rootの勝敗が反証されたわけではなく、別の六石LOSS証人による修復可能性は残る。旧1,984七石依存・57類集中配布の幾何計数は歴史的計画として保持するが、証明義務として新規配布しない。標準11×11空盤の勝敗は引き続き**UNKNOWN**。


## 2026-11-02：修復後1,980七石計画も別の六石WINで反証

上記の旧1,984類計画失効後、既知WIN6を除外した46六石証人による94五石の条件付き被覆を18回置換し、相異なる七石1,980類に圧縮していた。しかしその**修復後46証人にも、元先手WINが独立終局証明された六石局面が含まれる**。

- 六石：`00000000000000203808200000000000`（修復後46類のうち1類）。
- 元先手の合法勝ち手：点70（0始まり）。
- 終局までの戦略証明書：`research/experiments/n11-central-19-cover-20261031/shared58_s6_win_strategy.cert`（SHA-256 `10e816538fbe6cc0062e2d0dd0fe96930ef294101812701305e1595b531b21da`）。
- 元先手手番の戦略指定10,881局面、到達16,980局面、相手の全合法応手を展開して到達する終局2,237局面（13〜17石、すべて奇数石）。
- `verify_shared58_s6_win_strategy.py` が探索時の3×3差分行列式に依存せず、4×4整数Bareiss行列式で全相手応手と終局の奇数性を検査し、修復後46証人への所属も再構成する。勝敗cacheは一切参照しない。

この確定WIN6は、**修復後46六石すべてをLOSSと仮定する1,980七石の条件付き証明計画を失効させる**。1,980類という幾何計数自体は歴史的事実として残すが、同じ選択を証明義務として配布しない。残り45証人の勝敗や代替LOSS被覆は未確定。二石root `{49,60}` と標準11×11空盤の勝敗は引き続き**UNKNOWN**。


さらに、この六石から点70を置いた七石局面 `00000000000000603808200000000000` は、別の選択六石 `0000000000000020380c000000000000` から点75を置いた局面と**180度回転で一致**する。前者の終局戦略を180度回転し、後者の初手75に接続すると、別の六石局面についても同じ16,980到達局面・2,237終局を独立4×4整数幾何で全件検証できる。検証器はこの回転持ち上げを自前で再構成し、双方が修復後46証人に含まれることを確認する。したがって、**修復後46証人のうち少なくとも2類が元先手WINと確定**した（以前の失効計画のWIN6とは別）。残り44類はこの証明だけでは未判定。11×11空盤は引き続き**UNKNOWN**。

## 2026-11-04：条件付きLOSS計画は2,091類へ削減・三証人以下で局所最適

条件付きLOSS計画の歴史は次のとおりです（いずれも「46六石はLOSSである」という仮定への条件依存であり、勝敗の主張ではない）。

- K0646：2,301→2,154類（二証人交換10回）。全二証人交換近傍の改善0で二証人以下局所最適。
- K0668：2,154→2,098類（三証人交換1回、近傍全数列挙で改善23）。
- K0669：2,098→2,097類（三証人交換1回、改善2。ただし既知WIN6除外集合が focus1984証明書のWIN6（`…60380000000000008000`）を欠いていたため、当初2098→2094の失効交換も「最良手」と誤判定していた。除外修正により真の最良手は2,097）。
- K0670（現行）：2,097→2,091類（三証人交換1回、候補313,878組・有効282,078組・改善49件の最良を適用、2,984合法辺）。2,091出発点の近傍では改善0件であり、**三証人以下の交換近傍で厳密な局所最適**である（`audit_central49_2091_descent_three_swap_neighborhood.py`）。

現在の条件付き計画の要点：五証人等級すべてで46六石証人・94/94被覆・2,091正準七石類・2,984合法辺・終局証明済みLOSS7 6類・既知WIN6/WIN7非衝突（REFUTED込み）。

K0668〜K0670は、失効した旧2094/2093/2091/2090計画群（K0658で失効、K0659で修復）とは別の、現在の K0658 の REFUTED-aware 除外で核を確定させた系列です。失効した旧計画の16進鍵と同じ2,091数値を持つ計画ではないことに注意してください。

二石root `{49,60}` と標準11×11空盤の勝敗は引き続き **UNKNOWN**。短縮された義務は「六石LOSSが実際に46局所面から終端まで閉じることの証明」の実現作業であり、その証明自体は未実施。

## 2026-11-07：条件付きLOSS計画は方向性ごと崩壊し、先手WIN側の決定が進む

条件付き計画 lineage（K0668→K0670）の前提は崩壊し、その方向（第二手が六石LOSS証人で勝つ）は中央領域で不成立となった。経緯は次のとおりである。

- 2091 計画の focus 証人 `00000000000000203808000000000040` の全62子局面は LOSS7 35 件・WIN7 27 件と独立監査をパスし、focus_s6 は手番（先手）WIN と確定した。2091 計画の前提は崩壊した（K0672、K0670 本体へ追記）。
- focus 除外の修復三証人交換（K0673、2,140 類）の46証人集合について、全 2,140 類の実検証により **46 証人すべてが手番 WIN、LOSS は 0 件** と確定した（K0674）。修復計画の前提も崩壊し、46 証人という証人選択の方向性自体が断たれた。
- 94 五石位置の六石子全集合 3,868 について early-exit スイープで判定し、感受性証明書 4,288 件の独立監査を経て **手番 WIN 3,854 件・手番 LOSS 14 件** と確定した（K0675）。94 五石位置は **78 先手勝ち・16 第二手勝ち** に分類された。
- 94 五石子の主たる四石親として四石領域位置 S4-A（`00000000000000203800000000000000`、49五石子を含む）と S4-B（`00000000000000003800800000000000`、41五石子を含む）が同定され、各 94 合法子のうち **37 が先手勝ち五石子** であるため、四石領域位置は手番（先手）の勝ちと確定した（K0676）。

残る鎖は上流（S3・二石 root・空盤）であり、二石 root `{49,60}` と標準 11×11 空盤の勝敗は引き続き **UNKNOWN** である。方向転換の含意は、先手 WIN の証人構造（94 五石位置の先手勝ち78件への領域到達など）が残りの決定方向であることである。
