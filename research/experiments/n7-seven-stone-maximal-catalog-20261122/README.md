# 7×7の7石極大安全配置の完全カタログ: 16配置・2 D4軌道（2026-11-22）

単一オーナー宣言: [2026-11-22-n7-seven-stone-maximal-catalog-single-owner-note](../../log/2026-11-22-n7-seven-stone-maximal-catalog-single-owner-note.md)。
セッションログ: [2026-11-22-n7-seven-stone-maximal-catalog-session-log](../../log/2026-11-22-n7-seven-stone-maximal-catalog-session-log.md)。

標準共円盤（q=4、禁止四点組=同一線上または同一円上の4点）の 7×7 盤について、
**s_n ちょうど s_7=7 石の極大安全配置の完全カタログ**を作成した。
n=8 には K0032/B371 の完全カタログ（408配置・51 D4軌道・全安定化群位数1）があるが、
n=7 の7石カタログは本実験まで存在しなかった。

## 結果（有限計算・機械検証）

1. **7×7 の7石安全極大配置はちょうど16個、D4軌道はちょうど2つ**（両軌道とも
   サイズ8・安定化群位数1）。
   - 軌道O1（辞書式最小代表・石リスト昇順辞書式最小）: `[1,9,22,23,27,44,45]`
     — **K0031 の出版証人そのもの**（点番号 c = x + 7y）。
   - 軌道O2: `[3,10,22,23,30,32,38]` — 既刊に明示 witness のない軌道（新規記録）。
   - SAT符号化側の代表（指示ベクトル辞書式最小、enc_sat2 の lex-leader 規約）は
     O1: `[10,13,14,17,19,21,45]`、O2: `[18,21,22,26,31,32,38]`。
2. **本機材による s_7 = 7 の完全再導出**（K0031 の値更新ではない）:
   - 下側: k=3,4,5,6 の完全列挙がすべて found=0（最大 10,446,291 nodes @k=6）。
   - 上側: カタログの16配置（内 K0031 証人を含む）。
   - SAT側の独立再照合: n7k6 at-most-6 全解列挙 = 0モデル（UNSAT、13.4s）。
3. **最小極大 witness の軌道数の列**（類数の法則性データ、resume (b)）:

   | n | k=s_n | 総配置数 | D4軌道数 | 安定化群 | 出典 |
   |---|---|---:|---:|---|---|
   | 5 | 5 | 4 | 1 | 位数2 | K0030 出版 + 本実験再現 |
   | 6 | 6 | 8 | 1 | 位数1 | K0030 出版 + 本実験再現 |
   | 7 | 7 | 16 | 2 | 位数1×2 | **本実験（新規）** |
   | 8 | 8 | 408 | 51 | 位数1×51 | K0032/B371 出版 + 本実験で特徴検証 |
   | 10 | 10 | 不明 | ≥5類既知 | – | K1220（不全） |

   n=7→n=8 で軌道数が 2→51 に急増する（全408配置の安定化群は全て自明、もn=8側で再検証）。
4. **構造特徴**（n=8 出版カタログで意味論を検証済みの同一 feature 管線、§5）:
   - 全16配置が三点共線を少なくとも1つ持つ（B371 の n=7 版: 真）。ただし
     n=8 に24個存在する「三点共線1組のみ」の配置は n=7 には**存在しない**
     （B372 の n=7 類似は偽）。trips3 ヒストグラム {2:8, 3:8}、方向数 {2:8, 3:8}。
   - essential curve count（私人点をもつ石トリプル曲線数、出版 round10 ecc と
     同一規約・51/51一致検証済み）: n=7 {12:8, 13:8}、n=5 {8:4}、n=6 {11:8}、
     n=8（出版） {13:8, 14:8, ..., 27:8}。

## 非主張（trust boundary）

- 「16個・2軌道」の完全性は、§2 の健全性/完全性スケッチ + 有限較正全一致（§4）+
  完全に独立なSAT全解列挙との一致（§6）に基づく有限計算の主張である。
  Lean形式化でも形式的証明でもない。実装（Node/Python）/kissat UNSAT 健全性への
  信頼が trust boundary（K1220 のSAT再導出と同水準）。
- これは s_7 の値更新ではない（k≤6 排除・7石witnessは K0031 で出版済み）。
- n=9/10 への外挿は一切しない。n=9/10 のカタログは本実験では作っていない。
- 標準 11×11 空盤・二石 root・S2・class 1/2/4 は非接触（UNKNOWN のまま）。
- nodes 数・経過時間は勝敗ではない。

## 1. 禁止四点組カタログ（2系統独立生成・byte一致）

- 系統A: `pinned/census.mjs`（出版 s12-s13-sat-stabilization-20261122 機材と
  byte同一・K0057 アンカー（F_n・D/C分割）を起動毎に自己検証）。
- 系統B: `scripts/forbidgen.py`（本実験の独立実装。C(n²,4) 全組み合わせを
  正確整数（Leibniz 4×4行列式、[x y x²+y² 1]) で直接判定。曲線列挙を使わない）。
- 正準テキスト（quartets_nN.txt: n=5/6/7、昇順・辞書式ソート）の sha256:

  | n | F（四点組総数） | sha256（両系統一致） |
  |---|---:|---|
  | 5 | 826 (=K0057 F_5) | `22d086ba612336ca3c82a874b14871154c8298c6ab24241927e625bff28faedf` |
  | 6 | 2491 (=K0057 F_6) | `6996d7720d01a46e2bf27cca8cc918069c57b3a1db8b596a96349c33804ca853` |
  | 7 | 6364 (=K0057 F_7) | `7bf555486e1fa08bd43e7c0a6b66d3d2a22956dd0ec448e1feea3b8cdf1a4bfb` |

## 2. 全列挙器 enum_catalog.mjs（方法と健全性/完全性スケッチ）

配置の列挙は、石を昇順セル番号で置く DFS で、各セル c の
`cov[c] :=`「c を含む禁止四点組のうち他3点が既に石になっているものの数」を
増分管理する:

- **安全性（soundness）**: `cov[c] > 0` の c は石にできない（禁止四点組を完成させる）。
  したがって受理された葉に禁止四点組 q={a<b<c<d} が含まれるなら、d を置いた時点で
  他3点は既に石で cov[d]>0、枝刈りされていた。よって葉は必ず safe。
- **完全性（completeness）**: 極大安全 S の石を昇順に置く経路は DFS で切断されない。
  s を置く際 cov[s]>0 なら s∈q で他3点が prefix⊆S の四点組 q⊆S が存在し S は
  unsafe、矛盾。よって S の経路は到達可能。
- **maximality判定**: u（「石でなく cov==0 のセル数」）が葉で 0 ⟺ 全空点が
  何らかの四点組で3石に攻撃されている。四点組は3石到達時にのみ「残り1点」の cov を
  +1 し、4石到達は安全性枝刈りで不可能なので計数は厳密。
- shard分割: first stone セルc=x+7y ∈ [lo,hi)（0:7 + 7:42 + 42:49）。各配置の
  最小石は一意なので分割は完全で重複しない（n=6 k=6 でshard和=全列挙のbyte一致を
  事前検証）。
- 決定性: 再実行で cfg 行 byte 一致・nodes 数 bit 一致（output/determinism.json）。

本番: 3 shard 計 **38,798,535 nodes・63.0s（run1）・found 8+8+0 = 16**。

## 3. 結果レコード

- shard_y0.jsonl（first stone 0..6・27,916,188 nodes）: 8配置を含む（K0031証人は先頭）。
- shard_mid.jsonl（7..41・10,882,338 nodes）: 8配置。shard_y6.jsonl（42..48・9 nodes）: 0。
- classify_n7.json: 16配置全リスト・軌道分類・特徴。代表: O1 `[1,9,22,23,27,44,45]`
  （8成員）、O2 `[3,10,22,23,30,32,38]`（8成員）。
- 較正（output/enum_n5_*.jsonl, enum_n6_*.jsonl, calibration-summary.json）:
  K0030 出版分布を行単位に完全再現 — n=5: k5..k8 = 4 / 1,136 / 11,280 / 4,340、
  n=6: k6..k8 = 8 / 3,952 / 115,496（7行全一致。k=8 の本体5.5MBは非刊行・sha256のみ）。
  加えて出版「5×5最小4配置=単一軌道」「6×6最小8配置=単一軌道」も軌道分類で再現
  （classify_n5.json: 1軌道 size4 安定化群位数2、classify_n6.json: 1軌道 size8 位数1）。
- 下側再導出（enum_n7_k3..k6.jsonl）: found=0 ×4 k=3..6（最大 10,446,291 nodes）。

## 4. 独立検証（多系統）

1. **verify_catalog7.py（独立幾何・Leibniz）**: 16配置すべて SAFE+MAXIMAL、
   D4軌道再構成 2軌道 [8,8] 安定化群 [1,1]、SATモデル==各軌道のvecmin、
   K0031 証人含有、一石除去で極大のままの配置なし（112/112 → 6石極大安全は
   存在しないこととの整合）、tampered 9設定全拒否（検証器の陰性対照）。
2. **pinned verify_witness.py**（出版3系統検証器とbyte同一）: 16/16 rc=0
   SAFE+MAXIMAL（output/pinned_verify_witness_n7.json）。
3. **SAT 全解列挙（独立機材）**: pinned enc_sat2.mjs（v2.1 lex-leader・K1221規約の
   機械検査済み鎖）+ kissat 4.0.4 にブロッキング節を積み全解を列挙
   （scripts/sat_enum.mjs）。
   - n7k7（at-most-7）: 反復2回で UNSAT、**モデル2個（いずれも7石）**。モデルは
     軌道vecminと完全一致（上記）。
   - n7k6: **0モデル（初回UNSAT・13.4s）** → 下側の再照合。
   - CNF本体は非刊行（sha256 を sat_enum json に記録、決定的再生成可）。

## 5. 特徴量パイプラインの n=8 出版カタログでの検証（annotate_n8.json）

出版 round10_small_saturation.json（K0032/B371、51代表・D4閉包408・
安定化群 {1:408}）を同一 feature コードで再計算し:

- 51代表の D4 閉包は disjoint 408 configuration、全軌道サイズ8・安定化群自明
  （出版 stabilizer histogram {"1": 408} の再現）。
- essential curve count が**出版値と 51/51 一致**、全408ヒストグラムも一致
  （`{13:8, 14:8, 15:48, 16:32, 17:32, 18:96, 19:40, 20:56, 21:24, 22:24, 23:24, 24:8, 27:8}`）。
- 三点共線トリプル数ヒストグラム {1:24, 2:112, 3:176, 4:88, 5:8}、
  方向数 {1:24, 2:136, 3:176, 4:64, 5:8} — **B372 の「一方向だけの配置は24個」を
  24として再現**、B371 の「全408が三点共線を持つ」も再現。

この検証済みパイプラインを n=5/6/7 に適用した結果が上記 §結果3・4（n=7 には
「1トリプルのみ」「1方向のみ」の配置が存在しない、など）。

## 6. ファイル一覧と再現手順

```
研究.flags: すべて決定的。Node 22 / Python 3 標準ライブラリのみ。
# 禁止四点組カタログ照合
python3 scripts/forbidgen.py 7            # json (count=6364, sha256)
node    scripts/dump_quartets.mjs 7 out   # census.mjs 系統
# 全列挙（n=7 k=7 の3 shard）
node scripts/enum_catalog.mjs 7 7 out0.jsonl 0:7    # 45s
node scripts/enum_catalog.mjs 7 7 out1.jsonl 7:42   # 18s
node scripts/enum_catalog.mjs 7 7 out2.jsonl 42:49  # 即時
# 較正（出版 K0030 分布行）
node scripts/enum_catalog.mjs 5 5.. / 6 6.. 出力
# 分類・特徴
N=7 K=7 OUT=cls.json node scripts/classify.mjs out0.jsonl out1.jsonl out2.jsonl
# 独立検証
python3 scripts/verify_catalog7.py cls.json sat_enum_n7k7.json verify.json  # rc=0
# SAT 全解列挙（実験dir直下から; pinned/ を使用）
node scripts/sat_enum.mjs 7 7 work/ sat_enum_n7k7.json
# n=8 特徴照合（出版 round10.json 入力）
node scripts/annotate8.mjs <round10.json> annotate_n8.json
```

- `scripts/`: forbidgen.py / dump_quartets.mjs / enum_catalog.mjs / classify.mjs /
  sat_enum.mjs / verify_catalog7.py / annotate8.mjs
- `pinned/`: census.mjs / enc_sat2.mjs / decode_model.mjs / verify_witness.py /
  verify_witness.mjs（いずれも research/experiments/s12-s13-sat-stabilization-20261122/scripts/
  と byte 同一であることを sha256 で確認済み）。
- kissat 本体（4.0.4 official linux-amd64）は repo 規約どおりバイナリ再出版をせず、
  参照ピンで固定する: md5 `3a5eba830aa6008a604fcc9bbe99a325`・
  sha256 `21da5d984e38b74f620f14c62442f834f27b9158decdb722540d97f98aac93a1`
  （s12-s13 実験と同一 binary・同規約。実験機材の pinned dir 内でも同一 byte を確認済み）。
- `output/`: raw records 一式。MANIFEST-sha256.txt に全 file の sha256。

## 7. ライン整理

- 本実験の対象は n=7 カタログと s_7 再導出であり、並走の s_n 近傍走査レーン
  （K1223: n=11..15 witness近傍・sit-at修正監査）と対象は重複しない。
  K1222/K1223 は 2026-11-22 06:32-33Z に並走が出版（影響なし・採番は K1224 に調整済み）。
- 完了・未完の区別: 7×7 カタログと 5×5/6×6 較正は完了。n=9/n=10 カタログは
  予算外（未着手・未決着）。6×6 k=9..11 の本実験での較正は未実施
  （出版分布にまだ試みていない行。k=9=199,184・k=10=30,492・k=11=464 は今後課題）。
