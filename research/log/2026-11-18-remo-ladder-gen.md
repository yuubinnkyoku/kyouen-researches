# 2026-11-18 制限ラダーF(w,h;n)第一stretch-w法則の全称決定（LAD-GEN）

K0933（SIEVE5-U/V・S4・mod 30双子法則）の直接続き。高速レーン。
branchなし・main直接出版。K0934として出版。

## 発見順

1. **問題設定**: K0931の制限ラダーは「h=0全r、h≥1でr=0またはr≥h」の
   終状態則が4グリッド8,282検査のみ（無証明）で、h≥2・1≤r<hは
   open classだった。K0933でw=4の3インスタンスが証明済みになった
   だけだった。目標を一般wの全称決定とし、(a) block構造(b) breaking
   (c) 終状態(d) 除去集合(e) 監視条件を閉形式で導くことにした。
2. **block帰納の一般化**: K0933のL3/S4で手でやったblock帰納を一般
   (w,h,n)に定式化。鍵は2つのフレーム事実: 「元位置x ≥ (j−1)(w+1)−1
   の短縮indexはx−(j−1)」「pop後のptrはL mod (k−1)で元位置j(w+1)を
   指す」。これでフェーズjの配りが(j−1)(w+1)..j(w+1)−2・敗者が
   j(w+1)−1（保持w）と機械的に従い、Jの切り替わり（j(w+1)−1が
   hot tail n−h..n−1に触れるか）がJ = t ⟺ r≥h を直接与える。
3. **breakingの2+2ケース**: r<h（ptr=(t−1)(w+1)・配りはwrapなし・
   敗者n−r−1 hot）とr≥h（wrap込み・敗者w−r…r=0のみ敗者w+1）を
   剰余算術で導出。r=0・h=0のbreakingはptr=0に巻き戻る特別形
   （pop後tw mod wt = 0）。ここで一時的にptr算術を誤り
   （k=n−tをwt+r+1と勘違いして敗者がw−r−1に出た）、シミュレータ
   との突き合わせでk=wt+rであることを確認して修正。
4. **崩壊ケースの発見**: (t,r,h)=(1,0,0)はn=w+1・全員coldで、
   block-1後にk=wとなりbreakingでq=1・全員w+2・一様状態
   W_{w+2}(w−1)に落ちる。ラダーの正規経路（w→w+1）から外れる
   ジャンプケースとして定理に明示的に組み込んだ。K0931のLAD-h0
   にも同じ行があった（回帰で確認）。
5. **終状態censusの厳密化**: 終stateをmultisetでなくptr順の厳密
   list [w+1]^(n2−h2)+[w+2]^h2として証明。r<hでは監視側hot群が
   「配られたw+2群（n−h..n−r−2）」と「配られていないw+1群
   （n−r..n−1）」に割れること、r≥hではhot tail全員がbreakingで
   1回配られw+2になること、r≥hのwrapで0..w−r−1が二重配り
   （w→w+2）になることがcensusの本体。h2=(h−1−r) mod (w+1)の
   統一形はここから出る。
6. **監視条件と例外の導出**: 除去集合の要素のうちn−aに一致するのは
   (i) block敗者t(w+1)−1 ⟺ a=r+1（r≥h・冷死）(ii) r<hのbreaking
   敗者n−r−1 ⟺ a=r+1（hot最終死）(iii) r≥hのbreaking敗者
   （元位置w−r/w+1）はa=(w+1)t+2r−w resp. (w+1)(t−1)で、
   t≥2では監視範囲外になるのは (w+1)(t−1)≤w+1 ⟺ t=2 の1点のみ:
   例外(h,r,t,a)=(0,0,2,w+1)（監視=breaking敗者w+1・phase 3 hot）。
   n≥2w+2の仮定がt=1のwrap衝突を排除する役もこれで明確になった。
7. **LG8（2ストレッチhandoff）の設計**: 終状態主張は「次のstretchが
   F(w+1,h2;n2)としてLAD-GENの閉形式に従う」ことまで検証する
   設計にした（終circleのptrフレーム位置→label写像でstretch-2の
   block/breaking敗者を照合）。h2>w+1のケースはF族の定義域外
   （w+2保持者がf=間隔を超える）なので、handoff検証はh2≤w+1に
   限ることをLimitationsに明記。

## 検証

- ladder_gen_verify.py: LG1-LG8全合格。4,949ゲーム・68,411 block・
  4,949 breaking・4,949終状態・4,949除去集合・28,470監視（例外1点
  を含む全パターン）・903 LAD-h0回帰・580 S4回帰（死亡表・冷死/
  hot別・block・長さ式(n−a)//5+1）・1,503 stretch-2 handoff
  （8,924 stretch-2 block検査）。0失敗・2回in-process実行一致。
  実行2回で約40秒。
- audit_build.py: 2回cold実行でbyte同一（sha256
  52cbab9aa98095044e254b6d9355d340e68840e6fc51a809a6e4c9e95fa01d36）。
- 独立性: 検証器はK0928 Lemma Pの独立python実装。閉形式は定理から
  生成し新鮮シミュレーションと照合。紙上証明（block帰納・breaking
  場合分け・census・監視条件導出・例外の一意性）はreport.mdに
  完全記載。

## 出版

- K0934（proved）: LAD-GEN (a)-(e)・系（LAD-h0回帰・open class
  完全解決・K0931制限ラダー則の全称証明化・S4回帰・ラダー再帰）。
  実験ディレクトリ research/experiments/ladder-gen-20261118/
  （report.md・ladder_gen_verify.py・audit_build.py・
  output/ladder_gen_audit.json）。
- K0931 itemのOPEN記述を更新（open class全称解決・制限ラダー則の
  証明済み化を反映）。K0933 itemの「一般wはOPENのまま」を更新。
- READMEにK0933 bullet直後にK0934 bulletを挿入。

## 次の候補

- SIEVE7（spf=7・stretch-5/6）: 本項でper-stretch法則が全称化され
  たので、S3終状態からW5/F(5,h;·)族のstretch-5・6追跡は有限
  bookkeeping（m mod 42類）に帰着した。死亡条件は6|2m+s系の剰余類
  に写像。次回レーンの主課題。
- 監視位置のストレッチ間写像の一般式: 監視n−aが新circleのどの
  位置に落ちるか（K0933のS3/S4で手計算したもの）をLAD-GENの
  censusから導くとSIEVE7のbookkeepingが自動化できる。
- 崩壊ケースW_{w+2}(w−1)の一様状態レーンでの扱い（w→w+2ジャンプ）。

## 備考

- 並走レーンとの衝突なし（push前にitems/のK0934空き・README/K0931/
  K0933のbaseを再取得して確認）。
- AGENTS.mdの統合前確認（uv run tools/knowledge/{check,build}.py・
  unittest）は本実行環境にrepoのcloneとuvがないため未実施。
  generated/とroot READMEは編集していない（次の統合時に再生成）。
