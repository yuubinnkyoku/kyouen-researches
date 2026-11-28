# 2026-11-28 (5,4) 5x47 前線 SAT 攻撃 — 完了 log (高速レーン・第1セッション)

宣言: 2026-11-28-five-row-q4-m47-frontier-sat-declaration.md (86eb9df6・HEAD pin b841063a)。
実験: research/experiments/five-row-q4-m47-frontier-sat-20261128/ (README + scripts/pin.js + output/records.jsonl)。

## 結果

- m=47 witness 有無は未解決のまま (全 piece INDET・不在主張なし)。M_{5,4} ∈ [47, 567] 不変。csv 変更なし。
- 初の m=47 SAT 攻撃として rowY=0/1/2 (lex=H,V,HV / lex 無し) と rowY=1 krow=1:2 minpos p=0..6 (+lex=H p=0) を実行。全て UNKNOWN・ほぼ一様抵抗 (~9-14k conflicts @210-270s caps)。
- 較正: 5x39 rowY=1 lex=H,V,HV SAT 21,147 conflicts = 出版値 bit-exact。5x39 lex 無し 13,787 conflicts は環境リセット跨ぎ bit-exact。
- pin.js (krow/minpos 後段ピン層) を新規実装し対照電池で検証 (既知 witness への unit pin SAT 0・unsafe 点で UNSAT 0・H-image + krow chain + minpos SAT 0・ピン付き witness 発見の実演)。初版自作 counter の符号化バグは対照で即検出し sat3s counter() verbatim に差し替え (開示済み・偽値は不採用)。
- 硬さ較正: m=46 rowY=1 lex 無し @225s UNKNOWN (11,316) — 既知 SAT の幅でも 225s 級 cap では witness を発見できない。この幅の掃引には 600s+ の cap か別符号化が必要。

## 運用メモ

- bash 境界越えで環境リセット 1回 (既知 file-loss モード)・作業 tree 消滅 → CNF md5 が pre/post で同一 (cal39 5e59b097・m47r1nolex 3b9e42f3) であることで cross-reset 決定性を確認し再構築。
- セッション末に実行環境が不安定化し post-reset raw log (.out) の手元到達・出版ができず。conflicts 値はすべて records.jsonl に保存。CNF は md5 pin 済みで再生成可能。
- 並走レーン (n11 系・AG/PG q=7 blocking) とは非衝突。push 競合なし。

## 次回候補 (着手前に必ず最新 main 再取得・hourly 並走注意)

- (a) k=2 minpos p=7..23・k=1 p=0..23・k=0 の継続掃引 (音分解は p ∈ 0..23)。
- (b) 深 cap (600-1200s) が使える環境での再実行 (m=46 較正が示す通り 225s 級では決着不能)。
- (c) m=46 既知 witness を種にした bounded surgery budget ≥4。
- 標準 11x11 空盤・19 central-reply roots・二石 root {60,27}・第三手 {100,108}・全 closure class は全時点 UNKNOWN・verdict 不消費。
