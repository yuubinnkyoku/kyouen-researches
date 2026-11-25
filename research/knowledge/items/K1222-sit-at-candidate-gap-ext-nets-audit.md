---
id: K1222
title: 近傍走査の追加候補からsit-at（未被覆セルへの直接石追加）が抜けていた穴の発見と、全セル追加による完備走査器ext_nets、K1206近傍陰性のsit-at込み監査PASS
kind: method
status: active
topics: [maximal-safe, search-methods, verification]
aliases: ["sit-at candidate gap in neighborhood scans", "ext_nets full-cell (remove m, add a) scan", "K1206 sit-at audit"]
relations:
- type: verifies
  target: K1206
  note: "K1206のwall strict局所最適性・n=12 witness周囲r2a1陰性は、候補からsit-atを抜いた走査に基づいていた。sit-at込みの全セル走査（wall r2a1-full 6,120・r2a2-full 413,100・K0320-n12 r2a1-full 7,425・W_c r2a1-full 7,425・plateau r2a1-full 8,800/r2a2-full 699,600）で再監査し、witness 0件・bestScore は seed 未満の状態なし（wall=4, plateau=6）と、公刊主張がsit-at込みでも成立することを確認した。"
- type: related
  target: K1206
  note: "hunt.mjsのlocalNets/doubleSwapCompleteは候補列挙で c!==p 条件によりsit-at追加を除外していた。State機構自体はsit-atを正当に受理する（K0031 7×7 witnessの除去→sit-at addでviol=0/uncovered=0に戻る単体検査）。"
- type: related
  target: K0312
  note: "s_11決定レーンの近傍陰性（K1223）に本走査器を提供。"
artifacts:
- path: research/experiments/minimal-maximal-neighborhood-full-nets-20261122/scripts/ext_nets.mjs
  role: verifier
  note: "全セル追加の (remove m, add a) 完備近傍走査器。full0/full1/full2、bestScore追跡、trivial自己再構成のisSeed分類、cp中断再開。列挙数は totalChecked = C(k0,m)×(a=0 ? 1 : C(n²−(k0−m),a)) を満たし、この恒等式が走査の完備性の独立検証になる。"
- path: research/experiments/minimal-maximal-neighborhood-full-nets-20261122/README.md
  role: source
  note: "sit-at穴の説明・監査表・全走査の恒等式一致・解釈規約"
- path: research/experiments/minimal-maximal-neighborhood-full-nets-20261122/records/ext_wall12_r2a2.jsonl
  role: data
  note: "wall r2a2-full 413,100構成・0 witness・bestScore 4 (=seed) = sit-at込みでもstrict局所最適"
- path: research/log/2026-11-22-minimal-maximal-neighborhood-full-nets-session-log.md
  role: log
  note: "発見順・環境リセット事故と復旧手順・出版記録"
---

# sit-at候補除外の穴・ext_nets完備走査器・K1206監査

## 命題・範囲

標準共円盤（q=4）の n×n 盤で、安全極大配置の近傍を「m石除去+a石追加」で
走査するとき、追加候補を「未被覆セルを完成するquartet完結セル」に限定する
実装（hunt.mjs の localNets・doubleSwapComplete、c!==p 条件）は、
**未被覆セルそのものへの直接石追加（sit-at）を候補から除外している**。
sit-at はState機構上合法（viol/uncovered計算に特別扱いはない）であり、
安全極大配置の（remove m, add a）近傍の任意の構成は sit-at を含みうる。
だから「追加候補完備」を主張する走査は sit-at を含める必要がある。

これを満たす走査器 ext_nets.mjs（追加候補 = 現在石でない全セル、
full0/full1/full2 = a∈{0,1,2}）を作成した。maximal でない seed（壁・plateau
状態）も走査できる。

## 現在の根拠と限界

**K1206監査PASS**: K1206が公刊した陰性（12×12 wall strict局所最適・
n=12/n=13 witness近傍）は、sit-at込みの完全走査でも同一の結論になった
（witness 0件・bestScore seed未満の状態なし）。つまりsit-at穴は
K1206の結論を変えなかった。wall r2a2-full 413,100 構成の走査で
「uncovered<4 の状態が1つもない」ことが完全列挙で確定した。

**完備性の検証**: 全25走査の totalChecked が組合せ恒等式
C(k0,m)×(a=0?1:C(n²−(k0−m),a)) と一致する（k0=seed石数）。
n=13 r2a2 では found=66 が全てtrivial自己再構成（=seed）と分類されており、
found経路とisSeed排除機構の陽性対照になっている。

**限界**: 本項は走査方法と監査の記録であり、非存在証明・値更新を含まない。
sit-at込みであっても走査は有界近傍（remove≤4・add≤2）に限る。
