# 11×11 cert {73}: bit51 重複数の監査修正（2026-11-12）

基準 main: `39cc9b2fa9bab0cd0f20f7564c8c80ebbc187034`。`AGENTS.md`、知識索引、K0762、cert73 再利用検査スクリプトを確認した。

## 発見と修正

`cert73_reuse_check.py` の旧 `bit51 = sum(1 for k in c73_s6_keys if k & (1 << 51))` は、**局面鍵の第51ビット**を数えており、証明書の**所属マスク第51ビット**を数えていなかった。したがって K0762 と既存集計の「421 orbit が bit51 に属する」は、その計算からは支持されない。421を確定した共有cache被覆数として使用しないこと。

修正後は `c73_s6` の各行の `r[2]`（所属マスク）を用いて数える。さらに S5集合一致・義務算術・S6集合/数・LOSS包含・全証明書宣言数の検査が失敗したら、結果を書き出す前に例外で停止するようにした。

## 未完・再開条件

修正版スクリプトによる完全manifestとK0675データの再実行は今回未実施。正しい bit51 重複数は**未確認**であり、K0762 の421という値は要訂正。K0762本文・生成索引の正式更新は、再実行と `tools/knowledge/check.py` / `build.py` 等の回帰を通した後に行う。S6 verdict 3,868件の再利用可否や11×11勝敗に新たな認定を与えるものではない。

標準11×11空盤と対象二石rootは UNKNOWN。

## 再実行完了（2026-11-12・長期レーン）

修正版検査の完全manifest再実行は本文取得経路の制約（open_urlは~32KBで打ち切り、part1個が
594,201 bytesでrange分割取得も不可）により実行できないため、**等価かつmanifest非依存のTS再実行**
（scripts/cert73_regen_audit.ts）で確定した:

- cert {73}のS5/S6集合をrepo生成機関（milestone4_worklist.tsと同一のfwHex/swHex・
  整数外接円幾何・D4 canon・78 FW oracle条件）から再生成。制御全一致:
  S5 94・rawObligations 7,890・S6 3,868・sum_cost 281,121（summary.jsonと全一致）。
- K0675 s5_verdicts.json（raw取得）と照合: 94位置universe key一致94/94・
  7,813+77=7,890・loss_s6_covers 14/14包含 PASS。
- **bit51確定**: 所属マスク第51ビットは全証明書ビット割当て（最大2^49）に存在しないため
  membership読みは恒等的に**0**。旧421は**位置鍵第51ビット（セル51占有）の計数**であり、
  独立再生成で**421として正確に再現**。K0762本文・summary.jsonを両計数の区別明記で更新。
- 残りworklist 39,507 orbit・3,196,057 cost辺（3,477,178−281,121）も再現。
- python版cert73_reuse_check.pyの全manifest再実行は引き続き未実施（本TS再実行は
  bit51問題にはmanifest非依存で十分強いが、manifest行レベルの照合を行う場合は
  環境制約のない実行系で実施すること）。

実装教訓（本監査）:

- **open_urlの本文は~32,793文字で打ち切り**。GitHub rawの数百KBファイルは分割取得も不可
  （range非対応）→ 大型成果物の検証は生成機関からの独立再生成が実用的。
- **open_urlはJSON文字列リテラル内に改行を混入することがある**（例: "FIRST"改行"_WIN"）。
  パース失敗positionの制御文字を1字ずつ除去して復元可能（s5_verdicts.jsonで複数件）。
- **BigIntのString()は10進**。Setに格納した鍵とhex列を比較する際は
  k.toString(16)への変換を忘れると包含判定が偽陰性になる
  （本監査で1件・修正後にloss 14/14）。

S6 verdict 3,868件の再利用可否はK0762の通り（K0675で全件認定済み）。
標準11×11空盤と対象二石rootは **UNKNOWN**。
