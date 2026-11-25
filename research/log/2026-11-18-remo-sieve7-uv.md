# 2026-11-18 SIEVE7-U/Vの全称証明と双子法則mod 210全解決（K0936）

K0935（WATCH-MAP）の直接続き。高速レーン。branchなし・main直接出版。
K0936として出版。

## 発見順

1. **着手判断**: K0935のreport/logが「SIEVE7本体（spf=7・stretch-5/6・
   m mod 42類）は次回レーン」と明言しており、remo系で最高情報価値。
   合成定理（STR2/S3/S4/LAD-GEN/WATCH-MAP）がすべて出版済みなので、
   残るは反復bookkeepingの有限計算+紙上の全称化と判断した。
2. **合成の構成**: m=30j+cと置くと反復がアフィン軌道になることが
   手計算で見えた。n4=15j+c4（S3閉形式の帰結）・n2=n4−t4−[r4≥h4]
   =12j+c2・n3=10j+c3と傾きが15→12→10と強制され、WATCH-MAPの出力
   a2/h2・a3/h3はすべてクラス定数。唯一のj依存分岐は
   r6=(3j+c3) mod 7で、これが死亡をただ一つの剰余類j≡ρ (mod 7)に
   局在させる。手計算でV-A1・V-A2・U A-I・A-IIの4類のρと死亡型
   （V: a3≤h3のhot最終死・保持7・U: a3=h3+1の冷死・保持6・
   フェーズはn3//7）を厳密確認してから検証器に移った。
3. **N=7退化形の特定**: stretch-6死亡⟺7|NはN=7（Vのm=3・Uのm=2）で
   破れる（ゲームが監視生存のまま終了・N=7は素数なのでSIEVEとは矛盾
   しない）ことに気づき、主張を「7|N かつ N>7」（= spf(N)=7の合成数）
   に修正。SV7EDGEの有限検査でm<60のdomain 62対・8死亡
   （V: 24,38,45,59・U: 23,37,44,58）を確認。
4. **双子法則の閉じ方**: 57類の素数インスタンスはC∈{3,5,7}
   （LAW2は{2,4,6}）ちょうどに有限ピンできる（類の定義が3,5,7|Cなので
   素数ならC自身が3,5,7）。合成数側はSIEVE-COMPOSITEで即死むので、
   LAW1/LAW2のmod 210類が**全称定理として閉じる**（予想からの昇格）。
   新規はspf=7の8+8類。これはK0929の予想を3つ目の素数まで推し進めた
   ことになる。
5. **検証器の構成**: LAD-GEN core（ladder_gen・watch_dies・watchmap）
   はK0934/K0935検証器からverbatim copy。play()はK0928 Lemma Pの
   位相規則（K0932/K0933と同一）をストレッチ記録付きで再実装し、
   ピン表1,400ゲームと完全一致でengine健全性を確認。track()が合成の
   実装。メモリ制限のため全ゲーム記録を保持せずCANON/TRKをシミュ
   レーションループ内でインライン検証+コンパクト記録にした。
6. **32行クラステーブル**: 全32類（両側16類）でアフィン形式・定数・
   剰余類一意性・K0935表との整合・engine一致（j=2..16）が0失敗で
   確定。audit JSONに表を全文埋め込み、report.mdに転記。

## 検証

- sieve7_verify.py: 12チェック全合格（PIN/REDRECON/FRESHPIN/CANON/TRK/
  S3REG/K935TBL/SV7EDGE/SV7/CLASS/TWIN210/SIEVEOBS）。
  m=1..700両側1,400ゲーム。SV7: 合成領域684対・死亡98・生存586・
  0失敗。TWIN210: 57+57類・4,343数・0違反。
- audit_build.py: 2回in-process実行一致・2回cold実行でbyte同一
  （file sha256
  5a0fa03a4a36faf1277bc026a3e4652b2541bbef85c0f3769639e9e3aa3c8ac2）。
- 独立性: 検証器のengineはK0928 Lemma Pの独立python実装で、閉形式
  （tracker）は本項の定理から生成し新鮮シミュレーションと照合。

## 出版

- K0936（proved）: 定理SIEVE7-U/V・系SIEVE-COMPOSITE・系LAW1/LAW2
  mod 210・32行クラステーブル。実験ディレクトリ
  research/experiments/remo-sieve7-uv-20261118/（report.md・
  sieve7_verify.py・audit_build.py・output/sieve7_uv_audit.json）。
- READMEにK0935 bullet直後にK0936 bulletを挿入。

## 次の候補

- **SIEVE予想の一般化の形**: 合成領域の証明構造（クラス定数分岐+
  剰余類一意性+アフィン下界）はspf=7までで尽くすわけではなく、
  「spf=pの合成数側はストレッチp−1での死亡」が同型の有限計算で
  進めうるかをspf=11（stretch-8/9・m mod 30×11類）で試すのが次の
  自然なステップ。ただし類数・表の大きさが線形に増え、ad hoc計算の
  限界が近いので、一般pへの帰納構造（分岐パラメータのクラス定数性
  の不変量論証）を先に定式化する方が情報価値が高い可能性がある。
- 素数側生存の一般化: WATCH-MAPで追跡が算術化されたので、生存帰納
  （7∤Nかつ5∤Nかつ3∤Nでの全ストレッチ生存）の帰納法の形を探す。
- 双子法則の残りmod 210類（spf≥11依存）はSIEVEの一般化が必要。
- 崩壊ケースW_{w+2}(w−1)の一様状態レーン（K0935ログから継続）。

## 備考

- K0935と同一セッション系統の継続出版。push前に最新main HEAD
  （72769e1e・n11レーンのcost80e sweep）を再取得し、items/でK0936
  空き（max=K0935）とREADMEのK0935 bullet到着を確認してから出版。
- AGENTS.mdの統合前確認（uv run tools/knowledge/{check,build}.py・
  unittest）は本実行環境にrepoのcloneとuvがないため未実施。
  generated/とroot READMEは編集していない（次の統合時に再生成）。
