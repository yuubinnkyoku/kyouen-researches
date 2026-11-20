# 残余23行 8根被覆判定の外部第二検証: 単一オーナー宣言ノート（2026-11-20）

- 宣言時刻: 2026-11-20T13:29:51Z
- 宣言時点の HEAD: 51bbb93880（n11: declare single owner for residual23 replace-9 depth-10 sweep (K1097 next step #1; verdict facts only)）

## 対象

コミット `b4d8b3ac52`（単一オーナー宣言 `cb31752551`・先行出版）で出版された
残余23行 8根被覆判定（K1097 interval [8,9]->[9,9] 崩壊・P‴上で最小被覆 9）の
外部第二検証。並走レーンは本検証を重複しないこと。

検証内容:

1. 出版の完全性（publication integrity）: main の byte をそのままで
   - 判定機 `research/experiments/n11-residual23-eight-root-cover-decision-20261120/scripts/eight_root_cover_decision_20261120.py`
     （SHA-256 `da51063c…`・39,301 bytes）
   - 3入力正本（K1097 `2896deb0…`・K1102 `d0b5d845…`・下界強化監査 `1310ef74…`）
   - 出版判定正本（SHA-256 `c5aaf83e…`・16,324 bytes・18 gate）
   を取得しSHA-256を検証済み（全5件一致を確認済み・2026-11-20T13:29Z）。
2. pristine 再実行: 出版機を改変せず、別環境（同一 cwd 2回 + 隔離 cwd/HOME 1回）で
   実行し、出力が出版正本と byte-identical（SHA-256 `c5aaf83e…`）であることを確認。
   出版社は成立済みの再実行（同一cwd 2回+別cwd別HOME 1回・約41秒/run）の外部反復であり、
   出版byteの輸送破損検出（本repoで複数回発生の打ち切り・輸送破損）と処理系依存の排除が目的。
3. 数え上げ証明書の外部独立チェック: 3行provider零行
   (`00000000000000003800000008002010`・`0000000000000000380000000a080000`・`00000000020000801202000000100000`)
   の provider 構造と k_min=2 > k_max=3*8-23=1 の算術を、出版正本のprovider データから
   出版機と別実装の外部チェッカで再検証（実行可能な範囲で実施し、範囲を誠実に記録する）。

## 規約

- fold26（先行レーン `e53cc60c`）、残余23行 replace-9 depth-10掃引（`a2f933c462`）、
  residual-72 36 fresh-witness掃引（`c427979aff`）には影響しない・着手しない。
- 本検証は行を1つも閉じない。被覆は候補root計画の簿記であり証明書ではない。
  REFUTED-D10はLOSS証明ではなく、nodes数・solved数を勝敗として読まない。
- 標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。
- K番号は仮番号として扱い、item push 直前に3点確認（README bullet・item 404・recent commits）で
  空きを確定する。
- first-published-priority: 同一対象の宣言が出版済みの場合は先行レーンを優先し撤退する。
