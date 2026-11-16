# 2026-11-16: K0869 ID衝突の検出と修復（p2647 DRAT監査項目のK0871再採番）

## 発見

K0869監査JSON反映（b3cfd4ac）の着地照合中に、生成index.mdのK0869が
「p2647 サイズ1322 の3形状クラス DRAT監査」を指していることを発見した。
調査の結果、items/に id: K0869 の項目ファイルが2つ存在していた:

- research/knowledge/items/K0869-remo-k-branch-r8-boundary.md — 05:32:10Z 着地（先着）
- research/knowledge/items/K0869-p2647-size1322-three-class-drat-audit.md — 05:50:20Z 着地（後着・0ce4644c）

05:54:10Z にpushされた生成ビュー（31dcedd）は後者の作業ツリー（旧mainベース・851項目）から
構築されたため、index.mdにはp2647版のみが掲載され、先着のREMO r=8境界（定理I r=8・FATE・
ECHO・FL8/GP8/D0アンカー）が生成ビューから消えていた。また common.py の validate は
重複idを「duplicate id」エラー扱いにするため、この状態のmainで tools/knowledge/check.py は
必ず失敗する。b3cfd4ac がworkflowファイルを変更していたためCI走行中であり、
そのrunは監査ステップ完了後（約75〜90分）に check.py で失敗する見込み。

## 修復（本コミット）

repo慣例（K0866の再採番先例「作業中仮番号は並走着地に伴い再採番」）に従い、
後着側を再採番した:

1. 旧 items/K0869-p2647-size1322-three-class-drat-audit.md を削除した（前段コミット）。
2. items/K0871-p2647-size1322-three-class-drat-audit.md を新設した
   （id: K0871。スコープ・証拠・artifacts・本文は旧版と同一、本文に来歴追記）。
3. 参照を更新した:
   - K0768 本文: 「DRAT 監査済み（K0869）」→「DRAT 監査済み（K0871）」
   - K0706 本文リンク: `K0869-p2647-...` → `K0871-p2647-...`（markdownリンクをやめコードスパンで記録）
4. workflow末尾にtrigger commentを追加し、CIに生成ビューを再生成させた
   （期待: 852項目・REMO K0869復帰・K0871掲載・index/solutions/artifacts/relations/
   summary全再構築。CIのretryループが並走pushに対応する）。

検索で確認した K0869 参照一覧のうち、REMO系列（log/2026-11-16-remo-k-branch-r8-boundary.md・
README・report.md・verify_remo_k_branch_r8_sweep.py・workflow監査step）はすべて先着の
REMO K0869を指すため無変更。K0870（p2647 113 budget ladder）はREMO側が「仮番号」として
予告しただけで出版していなかったため、W-laneの取得が正当であり無変更。
REMO行列の次itemは K0872 以降の空き番号を使用すること。

## 残課題（次回実行へ引き継ぎ）

- CI再生成の成功確認（trigger comment追加により約75〜90分後に完了予定。生成ビューが
  852項目・REMO K0869掲載・K0871掲載・b3cfd4acの監査JSON artifactエントリ反映であること）。
- 走行中の旧CI run（b3cfd4acトリガー）は check.py 失敗が不可避（本修復より前にcheckout済み）。
  失敗は本修復コミット以後の run で回復する。
- 生成ビューのstale（REMO K0869欠落・851項目表記・artifacts indexの監査JSONエントリ欠落）は
  CI再生成で解消されるまで残る。

## 解釈境界

- 本修復は番号管理のみで、両項目の数学的内容には一切変更がない。
- K0869（REMO r=8境界）・K0870（p2647ラダー）・K0871（p2647 DRAT監査）の
  内容・検証状態は修復前と同一。
