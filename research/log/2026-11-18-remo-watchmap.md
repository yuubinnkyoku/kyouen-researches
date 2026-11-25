# 2026-11-18 監視位置のラダー境界越え写像（WATCH-MAP・K0935）

K0934（LAD-GEN）の直接続き。高速レーン。branchなし・main直接出版。
K0935として出版。

## 発見順

1. **問題設定**: K0934で第一stretch-w法則は全称化されたが、監視位置
   （SIEVE機構の核）のストレッチ間追跡はK0933のS3/S4で手計算した
   まま一般化されていなかった。SIEVE7（spf=7・stretch-5/6・m mod 42類）
   に着手する前に、この写像を一般(w,h,n,a)の閉形式として固定する
   ことにした。
2. **censusからの読み取り**: K0934の終状態証明（3ケースのcensus）は
   新circleのsegment構造を完全に与えている。監視n−aの生存条件
   （a≠r+1・例外(0,0,2,w+1)を除く）を仮定して、各ケースで監視の
   属するsegmentとindexを数えると3ケース×2枝の閉形式が出た:
   r<hでは前segment（a≤r・未配布hot生存者群）でa2=n2−r+a・
   長segment（a≥r+2）でa2=a−r−1。r≥h・r≥1ではcold prefix側で
   a2=a+w−r（a≤r）・a2=a+w−r−1（a≥r+2）。r=h=0では
   a2=w+a−1（a=w+1は例外で死亡）。枝の隙間a=r+1はちょうど
   死亡ケースで埋まる。
3. **合成（WM-COMP）の定式化**: 写像先の位置n2−a2にLAD-GENの除去
   集合を適用すれば第二stretchの死亡判定が閉形式で出る。これは
   SIEVE7の必要とするbookkeepingの原始操作そのもの。WM2として
   シミュレーション継続と直接照合（死亡・フェーズ・保持まで）。
4. **w=4の表の計算**: K0933 S4の4族（W4・F(4,1)・F(4,2)・F(4,3)）の
   生存rごとのa2表を閉形式で生成し、watchmap()の出力と照合して
   一致を確認（report.md掲載の表）。F(4,2)とF(4,3)はa2表が同一
   （監視位置a=3が共通）なのに対しh2が1ずつずれる、という構造が
   見えた。SIEVE7はこの表にstretch-5判定（a2=r2+1・r2=n2 mod 6）を
   適用しもう1回反復するだけの有限計算になった。
5. **検証器の構成**: LAD-GEN core（シミュレータ+閉形式）はK0934の
   出版済みladder_gen_verify.pyからverbatim copy（単一ソース化より
   監査の自己完結性を優先）し、watchmap()とWM1/WM2のみ新規実装。
   stretch-2崩壊ケースの保持期待値（w2+2）を頑健化して追加
   （現在のグリッドでは該当点なしと paper で確認済みだが将来の
   グリッド拡張に備える）。

## 検証

- watchmap_verify.py: WM1 23,714検査（生存監視の新circle indexが
  n2−a2と一致）・WM2 23,713検査（合成死亡判定・フェーズ・保持照合）・
  0失敗・2回in-process実行一致。
- audit_build.py: 2回cold実行でbyte同一（file sha256
  024d86211a1a72f5c26f395b78d4e10d727594bb006190c357c10d9b1a27c36b）。
- 独立性: 検証器はK0928 Lemma Pの独立python実装（K0934と同一core）。
  閉形式は本項の定理から生成し新鮮シミュレーションと照合。

## 出版

- K0935（proved）: WATCH-MAP補題・WM-COMP系・w=4のa2表。実験
  ディレクトリ research/experiments/watchmap-20261118/（report.md・
  watchmap_verify.py・audit_build.py・output/watchmap_audit.json）。
- READMEにK0934 bullet直後にK0935 bulletを挿入。

## 次の候補

- **SIEVE7本体（次回レーンの主課題）**: w=4のa2表+n2/h2算術から
  m mod 42類の監視追跡を完了し、U側「ラベルm−1がstretch-6で死ぬ
  ⟺m≡2 (mod 7)（⟺7|2m+3）」・V側「ラベル0が死ぬ⟺m≡3 (mod 7)
  （⟺7|2m+1）」のSIEVE7-U/Vを全称証明。WATCH-MAP+LAD-GENの反復
  （WM2がその検証器）で機械検証可能。
- 素数側生存（2m+s素数なら監視生存）の一般化: WATCH-MAPで追跡が
  算術化されたので、生存帰納の形を定式化できる可能性。
- 崩壊ケースW_{w+2}(w−1)の一様状態レーン。

## 備考

- K0934と同一セッションでの継続出版。push前にitems/でK0935空き
  （max=K0934・自コミット）とREADMEのK0934 bullet到着を再確認。
- AGENTS.mdの統合前確認（uv run tools/knowledge/{check,build}.py・
  unittest）は本実行環境にrepoのcloneとuvがないため未実施。
  generated/とroot READMEは編集していない（次の統合時に再生成）。
