# 2026-11-15 高速レーン — (4,5,21) 掃引決着: x2 第2石完全分割で 37バケット全 UNSAT・4×21 欠損極大不在

## 選定

前回停止 (16:05Z) からの再開時点で、m=21 class-split 掃引は
73 直接 UNSAT + c0k3p0/c0k3p1 の2バケット未決 (deep cap 2400s でも INDET)。
残りを x2 スイープ (sweepp0x2.sh v2.1・cap 900s・resume skip) で掃引すれば
m=21 全体が決着し (4,5) の witness-free 幅 21 が確定するため、
情報価値最大と判断して完走させた。並走: ge20_cuts (n10・K_10∈[19,23]) は
2コア制約で排他運用 (x2 スイープと合計1コアずつ)。

## 結果

- **37/37 x2 サブバケット UNSAT・0 SAT・0 INDET** (cap 900s)。
  - c0k3p0 (row0={0,b,c}・b∈1..19): 19バケット・13,382,360 conflicts。
    最難 b1 = 1,969,663 / 185.1s。最小 b19 = 106,759 / 6.2s。
  - c0k3p1 (row0={1,b,c}・b∈2..19): 18バケット・10,930,286 conflicts。
    最難 b3 = 1,082,095 / 102.6s。
  - x2 合計 24,312,646 conflicts。
- c0k3p0 + c0k3p1 の UNSAT は分割の完全性 (b>19 は第3石の置き列なし・
  バケット互いに素) から従属するため、**75 m=21 class-split インスタンス
  すべて UNSAT** → 4×21 に行欠損極大安全配置は存在しない
  (全極大安全配置は16石・行占有 (4,4,4,4))。
- m=21 決定 110インスタンス合計 **102,380,271 conflicts**
  (73 直接 78,067,625 + 37 x2 24,312,646)。
  ※ 検証 JSON 初版は 126,692,917 と記録したが x2 分の二重計上。
  erratum を同 JSON に追記して 102,380,271 に修正した。
- **M_{4,5} = 21 または ≥ 23** (K0821-audit 鋭い形・集合形式 {21} or ≥22)。
  上界 140 (K0318) 不変。前線 4×22。知識項目 K0857。

## 第二検証

1. CNF 再生成 md5 照合 4件 (c0k3p1b7/c0k3p1b2/c0k3p0b1/c0k3p1b8) すべて
   record の cnf_md5 と一致。
2. サンプル再実行 bit-exact 2件 (c0k3p0b1=1,969,663・c0k3p1b8=721,355)。
3. 16:05Z 停止で生ログを失った c0k3p1 b2..b7 の6バケットを
   停止後に CNF 再生成から再実行し、**全6件が records と bit-exact**
   (977,786 / 1,082,095 / 1,023,149 / 810,664 / 829,408 / 752,372・全 UNSAT)。
   b2 の record 再構成事故 (records 修復と driver 追記の競合で一時消失・
   実行ログから復元) はこの独立再実行で裏付けられた。
4. **b4/b6 record md5 転記ミスを発見**: 再生成 (二重生成で冪等確認) と
   突き合わせて、c0k3p1b4/b6 の record `cnf_md5` が真の md5 の1文字
   転倒だと判明 (停止前の修復時に手再構成された行)。conflicts は
   bit-exact 再実行で無傷・再生成 md5 を権威値として検証 JSON に記録。
   停止前修復で手を入れた行は b2 だけではなかったことが判明した点も
   教訓 (修復は全行の md5 再計算を機械的に行うべき)。
4. 陽性対照: (4,20,5) class{0} k3 p1 SAT 20.0s/375,415 —
   m=20 witness の V 像を同一符号化経路で再発見 (js+py)。

## 反映

- records.jsonl 86→117行 (b2..b19 追加31行・x2 37バケット+対照/INDET行整合)。
- 検証 JSON x2-split-verification-20261115.json (第二検証+erratum)。
- sweepp0x2.sh v2.1 (comma anchor) を scripts/ へ、最難生ログ
  c0k3p0b1.txt を output/ へ (K0821 の hardest-log 規約に準拠。
  他36ログは CNF md5 記録+kissat 決定性で再現可能なため個別保管しない)。
- K0857 新設 (K0821 形式・status=computed・有限機械検証と明記)。
- K0833 追記 (witness-free at 21・M = 21 or ≥ 23)。
- CSV (4,5) 行: M 列 `"{21},23..140"`・source に K0857・note に決着記録。
- 本 README タイトル・末尾に掃引決着節を追記。

## 教訓・運用

- records.jsonl は driver 実行中 append のみ (b2 record 再構成事故の再発防止)。
- driver v2.1 の comma anchor なしには b1/b10..b19 の prefix collision で
  誤 skip が起こりえた (被覆完全性の黙った損失)。
- 検証 JSON の集計値も records からの再計算で独立に精査すべき
  (126,692,917 二重計上の発見経緯)。

## 次回

1. **4×22 掃引** (次前線): sweep21.sh の `4 21`→`4 22`・minpos 0..10 不変
   (floor(21/2)=10)・新 dir four-row-q5-m22-class-split-20261115・
   IN FLIGHT claim 付きで起動。ge20_cuts との 2コア排他運用。
   4×21 の経験上、deep cap 抵抗バケットも x2 分割で ≤ 数分/枚に落ちる見込み。
2. ge20_cuts 決着なら K_10 更新 (K0856 は n10 用に予約済み・未使用)。
3. n11 class2 レーン cost-58c (908716e1)・cost-63h (1b11089a) は着手禁止
   (IN FLIGHT)。
