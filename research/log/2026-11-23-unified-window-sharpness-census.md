# 統合窓セル別鋭さ census + {1}^t 全アリティ分離 実行記録（2026-11-23・高速レーン）

## 選定と着手の経緯

- 当実行の当初候補だった **y=23 全称レーンは並走実行の所有**（宣言 474ec50b・仮採番
  K1266・宣言ノートと fit log が出版済み）と判定して **譲渡**（非接触）。ただし本
  レーンで作成した独立第二ソース予測資材は有効と判断し、Knowledge に記録して
  y23 機体出版後の照合に備える:
  - y19-y22 の4出版 audit に対し **CROSSVAL ALL MATCH**（`work/predict_y23.py`）。
  - C4/C4t type machine の cand 意味論完全再現（`work/predict_c4t.py`・y22:
    clip45 違反 280/first (60,108,108)/types 797,559 まで完全一致）。
  - y23 機体出版後の照合用予測値: **clip47 violations=182・first=(60,110,110)・
    clip48 confluent violations=0・types=465,939** ほか14チェック点数値群。
- 着手レーンの選定: K1264 report 未解決 3（max(z+min(X),2) 統合窓の行ごとの鋭さの
  全称特徴付け）・4（min=1・アリティ>=3 の一般条件）と K1265 report 未解決 2 の
  **非接触残項**。対抗宣言なしを認証付きコミット一覧で機械確認（HEAD c6ae987a 時点）。

## 宣言（publish-then-execute・単一オーナー）

- 宣言ノート: `research/log/2026-11-23-unified-window-sharpness-single-owner-note.md`
  commit `cf299bdd`（先行出版・push 時 HEAD `c6ae987a` を commit message に記録）。
- スコープ: (1) T1 定理 {1}^t ∀t>=3 の (z,R)=(0,3) 分離（宣言前紙面証明を note で
  開示・段落1-3 の一様 mex 連鎖）・(2) E3 2トークン census z=0..24 × m=1..10 × d=0..60・
  (3) E4 陰性セル d<=200 拡張＋アリティ>=3 電池・(4) E5 {1}^t 行 census t=3..8 ×
  z=0..24・(5) E6 L1/L2 採引 m=11..20/11..22（事前登録予想「両線とも親2」）・
  (6) min=1・アリティ>=3 の一般全称証明は本宣言の保持範囲外。
- 宣言時点で無認証 api.github.com がレート制限中。対抗確認は認証付きコミット一覧
  ・予測可能パスの非存在確認に限られた旨を note に正直記録済み。

## 機体構築（手転写ゼロ）

- エンジンは出版 K1264 検証器 verify_min_token_staircase.py（SHA-256 108fdd65…）から
  `build_unified_verifier.py`（SHA-256 49b11350…）が **SHA ゲート付きで engine block
  （2,508 bytes・SHA-256 bd5f22e4…）を機械抽出**し、byte 比較 PROVENANCE PASS。
  provenance 鎖: K1138 再帰定義 → y22 機 K1257 → K1264 機 → 本機。
- 出版 K0832 単一トークン閉形式を対側に併用（値は同一式で計算・手転写ゼロ）。

## 実行結果（AUDIT PASS・決定性）

- 検証器 verify_unified_window_sharpness.py
  （SHA-256 0ab66665dc9990f5399a661ccb2f9c3ba75f5a010c7e915f6a44e3d4fe6d3103）。
- **総照合 273,209 比較・点数 106,921・bad 0**。E0 77,252点×2・E1 出版アンカー
  85 比較・E2 T1 アンカー 38 比較・E3(+E3b) 15,650点 62,600 比較・E4 13,818点
  55,272 比較・E5 150点 600 比較・E6 22点 110 比較。
- audit.json 正本 SHA-256
  `b74551b712efa6f8e695c62482226e709d82d68f9771e760771a79c22b5b434f`。
- 変異電池 8 種すべて捕捉（窓+1 崩壊 114・T1 親値反転 1・C手除去 44・q_odd 腐敗
  1,102・境界+1 一致主張 y=1 行 180・出版アンカー反転 1・max-token 窓 7・
  B手 z 進行除去 20）。rc=1 は未捕捉時。
- 決定性: 4 実行（同一 cwd 2回・隔離 cwd・env -i・PYTHONHASHSEED=random・別 HOME）で
  audit.json が byte-identical。

## 主要な成果

1. **T1 全称定理（証明）**: {1}^t は全 t>=3 で (z,R)=(0,3) 分離（親 0 vs 単一 1）。
   t=2 崩壊。→ K1267。
2. **T2 全称定理（宣言後発見）**: {1}^t は全 t>=3 で (z,R)=(1,3) でも分離
   （親 2 vs 単一 0）。段(a)-(f) の一様 mex 連鎖を report で証明・t=3..16 機械照合。
   **宣言スコープ 6 により本 run での K 項目化はせず、report に全開示して次回の
   独立宣言に回す**（次課題 2）。
3. **前線法則（観測）**: セル (z,m) が 2トークン witness を持つ ⟺ m=1 または
   z >= z*(m) := 2m−2+(m mod 2)。266 セル（E3 250 + E3b 16）で例外 0。
   K1264 C4「y>=9 希薄化」・K1259-K1262「y=6 行 R=z+7」・Z 切片 witness 位置の
   統一説明。前線 witness は一意（偶 m: (m,m)・奇 m: (m+1,m)・親 2・単一 1/0 交互）。
4. **E6 予想の部分反証（事前登録どおり）**: L1 は奇 m のみ・L2 は偶 m のみ分離。
   単一パリティ式は 22/22。falsifiable pre-registration が機能した事例。
5. **陰性バンド 94 セル open・予想 C1**: d<=200 拡張＋アリティ電池 658 点で
   witness 0。2トークン非分離は出版 y<=22 族閉形式の引用レベル帰結。
   アリティ>=3 一般は未開拓 → 予想 C1（banded 窓拡張）を open problem として明記。
6. **K1264 C4 再集計 fail-closed 一致**: 出版値 y 毎 180/37/32/31/26/25/20/19 と完全一致。

## 誠実記録（報告書側と合わせ）

1. **宣言点数と実測のドリフト**: 宣言「139,085 比較」→ 実測 273,209 比較。理由は
   E0 の二重計上漏れ（+77,252）・E3b 追加（+1,600）・E4 の別計上（宣言どおり・
   55,272）。protocol（範囲・比較内容）はすべて宣言どおり実装。K1265 先例に従い
   本 log で訂正記録する。
2. **E3b 追加の理由**: 宣言は「C4 掃引域の分離再集計は E3 から」と述べたが、
   E3 は z<=24 で出版域（z<=26）に届かないため、再集計の完全性のため
   z=25,26 × m<=8 × d<=24 を追加した。
3. **変異電池⑦の差し替え**: 宣言⑦「アリティ電池検査省略主張」は捕捉が census
   結果依存になる設計欠陥を run 前に発見したため、決定的捕捉が保証される
   「max-token 窓主張」（出版 K1264 T6 と同一掃引・bad 7）に差し替えた。
4. **cache clear**: sandbox メモリ上限（約1.0GiB）のためセクション/行単位の
   value-transparent な cache clear を配置（宣言に明記なし）。4 実行 byte-identical
   で値透過性を検証済み。report 誠実記録にも記載。
5. **宣言前の engine 実行は 0 回**。紙面 mex 計算（T1・(2,1)@(0,3)）のみ宣言ノートに
   先行開示。T2 は宣言後に発見（宣言ノートになし・report が初出）。

## K 番号

- 本 run は **K1267**（{1}^t 全アリティ分離定理・proved）と **K1268**（統合窓
  セル別鋭さ census・observed）を使用。y23 並走レーンの仮採番 K1266 とは衝突なし。
  push 前に items の最新一覧で再確認する。

## 出版（publish-then-execute 完結）

- push 直前の最新 main 取り直しで対抗宣言・パス衝突を再確認のうえ、
  実験 dir（report・verify・build・output/audit.json）+ K1267 + K1268 + 本 log を
  一括 push。commit message に observed HEAD-before-push を記録。
- push 後、knowledge README 末尾に K1267/K1268 の bullet を追記（旧 blob sha 付き
  create_or_update_file・fetch-back 照合）。

## 未解決・次課題

1. **T2 の独立 K 昇格**: 専用の単一オーナー宣言と mex 連鎖機体で出版
   （証明は report に開発済み・アンカー済み）。z=0,1 双定理として一括でもよい。
2. **予想 C1 の検証開放**: 陰性バンド（m>=2, z<z*(m)）で R=z+m+1 の全 X 崩壊を
   証明またはアリティ>=3 witness で反証。
3. **前線法則の全称化**: z*(m)=2m−2+(m mod 2) の全 z,m 証明（m<=22 は出版 y 族
   閉形式から導出可能・m>=23 は y>=23 族レーン待ち）・前線 witness の d 一意性の証明。
4. E5 の疎パターンの一般則・(x,1) 行の witness 密度勾配（min_d が 1,3,5,… に上る観察）。
5. y23 機体出版後の照合: clip47 182 違反・(60,110,110)・clip48 0 違反・types 465,939
   （`work/predict_c4t.py` による第二ソース予測・Knowledge 記録済み）。
6. 標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は範囲外かつ
   常に UNKNOWN のまま。
