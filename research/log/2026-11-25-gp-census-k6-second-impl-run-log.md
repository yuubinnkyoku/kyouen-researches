# 2026-11-25 GP-census K_6 第二実装クロスチェック: 実行ログ (完了)

単一オーナー宣言: [2026-11-25-gp-census-k6-second-implementation-single-owner-note.md](2026-11-25-gp-census-k6-second-implementation-single-owner-note.md)
実験キット・成果物: [binary-cube-gp-census-k6-second-impl-20261125](../experiments/binary-cube-gp-census-k6-second-impl-20261125/README.md)

## 結果 (すべて PASS)

- **d=6 全 63 ペア**: 第二実装 census3.js の per-pair 計数が第一実装
  r6-results.jsonl と行単位で完全一致 (agg3.mjs による全行照合、perPairMismatches=0)。
- **Σ anchored テーブル**: [0,63,63,1953,39410,571340,6029142,40050850,53334038,408240,0]
  が研究メモの公開テーブル (s9=408,240 / s10=0) と完全一致。
  すなわち K0568 上界の根拠 s10=0 が素数・剰余を使わない演算核で全走査再現された。
- **battery** (battery.txt / results3.json):
  - selftest 全 PASS: B1 det vs BigInt Laplace 400 (bad 0)・B2 rank 200・
    B3 gate-identity fuzz 410 trials (60 seeds, d=3..6, fast vs 直接判定)・
    B4 9点証人 3 種 + XOR 正規化像の GP 再検証・B8 magnitude bound・
    B6 d=3/d=4 fast census 全一致。
  - brutecensus (完全独立の直接行列式全列挙): d=3 [0,1,7,21,29,5,0,...]、
    d=4 [0,1,15,105,430,940,408,0,...]、d=5 [0,1,31,465,4405,27990,104286,67606,0,...]
    すべて公開 anchored 表と一致。d=5 は第一実装 brute (サイズ6以下) より深く、
    全サイズで完走して s8=0 を全数確認した。
  - gatecheck: ペア (0,1) 先頭 600,000 child-decisions の全直接再検査 (不一致 0、
    帳簿計数も同一)、軽量 4 ペア (0,58)=28/28・(0,55)=201/201・(0,45)=19,904/19,904・
    (0,40)=75,718/75,718 の全 child-decision 再検査 (不一致 0)、
    重めの 3 ペア (0,7)/(0,13)/(0,32) 各先頭 300,000 (すべて不一致 0)。
    lexicographic-prefix バイアスは実験 README の honesty labels に明記済み。
  - determinism: ペア (0,45),(0,46),(0,47) の 2 回実行で整数ペイロード同一
    (ms は運用情報であり比較対象外、比較器も integer payload に修正)。

## 出版 chain (公開順)

1. 宣言ノート commit `09fec193`
2. キット commit `b7a6e564` (census3.js + agg3.mjs + README)
3. README 文言修正 commit (グレア訂正: 導出スケッチと「2つの大きな素数」表現)
4. census3.js ヘッダコメント修正 commit (「results lines に timing を含まない」→
   「ms は運用情報のみ、determinism 比較から除外」へ訂正。動作変更なし)
5. 公式出力 commit `f4cd9cc0` (8 ファイル: r3-results.jsonl, results3.json, battery.txt,
   census-d3/4/5.json, check-pair01.txt, determinism.txt)
6. K0568 evidence 更新 commit (blob c19d4441). same-K update・status は closed のまま。
7. 研究ログ (本ファイル) + research/knowledge/README.md bullet

sha256 (成果物):
- r3-results.jsonl `0a6b43920215aed4119a15ab7abc51e99bdb06a81c4821846e6315d449c6270f`
- results3.json `40bc64d685878461da221e6dd389a363bea89ee5e2c1f666d9b17b11ccde9e87`
- battery.txt `101138dd5e66dcd49096a0ed3ab0732185ee714a5d34d25fda37a6f47220a680` (計算時点)
- census-d3.json `a35e55b6929e98544612c6cf3f859e34f7999f20b2799e1931695b979b0af20f`
- census-d4.json `6c274d60dac295241940d7e25f290ad19e0c2c7597672aee6fd0a34658f298c3`
- census-d5.json `d9186f7fcc1a72bc80a1933511c9297d3b8cefbe22373f0128892dfe4fc65fa9`
- determinism.txt `f2ae091b95ae13a6424f1ff55f0d3e6969124f1b2f3137165c6eff82e625e2fe` (軽量ペア分)
- check-pair01.txt `914a954507c411fc666bc7dcdb9c6350da2e35adf4d4c422dc60516ba5b57b94`

## honest incidents (開発・実行中の失敗の全記録)

1. **実装バグ 2 件 (宣言前のデバッグ段階で検出・修正、公式実行前に解消)**:
   - (a) rankExact が引数行列を破壊するのに scan が S 行を再利用し、
     候補 2 つ目以降の rank 判定を汚染していた (d=3 で 12 個の size-4 GP 集合のうち
     10 個しか数えない等の過小計数)。各候補で fresh copy を渡すように修正。
   - (b) fastDecide の γ̃ 計算が scratch に MB 全体を写さず行 i だけを書いており、
     γ̃ が常にゼロ側に壊れた。BigInt Laplace による γ̃ の ground truth 突き合わせで
     特定し修正。
   - 教訓として、B3 fuzz (410 trials) はこれらを拾えず、小次元 census 全一致
     (d=3/d=4) が決定的な検出器だった。selftest に B6 (d3/d4 census 全一致) を追加。
2. **背景実行の死没**: nohup+background の battery/determinism チェーンが実行中に
   消滅 (奇数/偶数 worker は完走したが、後段チェーンが途中停止)。
   残り (brutecensus 5・census d3/4/5・heavy gatecheck 3) はフォアグラウンド再実行で
   完走。出力は再生成後のものを push。
3. **even worker の初回起動失敗**: シェル演算子の結合順位で 2 つ目の nohup が動かず、
   約 5 分後に気づいて再起動 (r3-even.jsonl のタイムスタンプが証拠)。
4. **determinism 初回比較の偽 FAIL**: byte 比較に ms 実行時間を含めてしまい FAIL
   扱いとして誤検出していた。整数ペイロード比較に修正し PASS。kit のヘッダコメントも同時に訂正。
5. **README の文字化け**: キット README の数行でエスケープシーケンス混入
   (u8126… 等)。直後に修正 commit。数値主張への影響なし。

## 意味と限界 (実験 README の honesty labels と同じ内容)

- 本研究は第一実装の有限計算の独立再現であり、数学的な新規主張は行わない。
- 両実装は同じ列挙規約 (頂点0アンカ・63ペア分割・昇順正準木) を採るため、
  一致は「演算核の独立性を経由した計数レベルの二重確認」である。
  個々の GP 集合の同一性検証ではなく、その担い手は第一実装の独立 brute
  ゲート再照合と本実装の gatecheck (prefix + 軽量ペア全件) だが全網羅ではない。
- 全中間値の float64 厳密性は battery B8 (実測 max |det| = 907 未満と B1 maxabs 実測)
  と理論値 (Hadamard 907 / |g|<=1512 / 4x4 < 1.26e14 < 2^53) で保持。

## レジューム (次回の着眼点)

- (a) 同レーンの追加検証候補: gatecheck の対象ペア拡大 (重いペアの prefix 長を
  引き上げる、top-1 ペア (0,1) の trial 全件は brute 換算で重いので費用対効果注意)。
- (b) K0568 に残る別軸: Grundy 値、misère 版 (census でも直接には扱わない)。
- (c) 11x11 レーンへの接続: 本レーンの成果は K0568 の二重化のみで、11x11 構造には
  直接寄与しない (接続不要・独立)。
