# 2026-11-15 高速レーン: (7,10) 帯閉包 m=201..586 完走 — M_{7,10} = 19 exact

## 選定

- 開始時の未解決確認: 前回レーンで (7,10) 帯 m=111..200 完走・統合 push（c4a9341f・
  K0820/CSV/README/log）まで完了。残課題は (7,10) m=201..586 と (7,9) m=201..612 の持続性。
- 最新 main を取り直すと、並走の **q9 閉包レーンが (7,9) m=201..612 を IN FLIGHT で主張**
  （52fd92c1）し、弦対抽象円 census による新生成器 **genfast3.js** を commit（d06d8015・
  O(C(w,2)·m²·w)・m=612 で ~2s）していた。一方 **(7,10) m=201..586 は未主張**。
  genfast3 は q ≥ w+2 限定で q=10 ≥ 9 を満たすため、**同生成器を再利用した q=10 帯閉包**を
  本レーンの成果に選定。これが閉じれば K0318 substitution U=587（proved）と合わせ
  **M_{7,10} = 19 の完全決着**になる。
- (7,9) は q9 レーンが掃引中（genfast2 で m=201..237 完走済みのコミットも確認）→ 重複回避。

## 較正（genfast3 の q=10 への適用妥当性）

- 環境: API blob で genfast3.js を取得（**raw CDN は stale で最終行 module.exports 欠落版を
  返すことに注意**・API contents の md5 12c2bd9c が controls_genfast3.json と一致する版が真正）。
- **CNF byte-identity vs genfast2.js**: 7x110 def / 7x150 def / 7x200 def / 7x200 --lex=H,V,HV の
  4 サンプルで cmp 0 diff・全 MATCH（genfast2.js は m=101..200 の q10 帯で実績あり）。
- **instance-identity**: leanband3.sh（genfast3 版 leanband）m=200 再実行が band-extension レーンの
  record と bit-exact（vars 36,315 / clauses 132,264 / curves 393 / UNSAT 2,941 conflicts）。
- タイミング: 生成 m=300 0.5s / m=400 0.6s / m=586 1.0s・kissat m=300 0.5s / m=586 0.4s
  （conflicts 2,608 / 1,629）→ 全 386 幅が 3 コマンドで回せる見通し。

## 実行

- IN FLIGHT claim を先に push（0e699090・実験フォルダ + leanband3.sh/batchband3.sh）し
  スコープを確保してから掃引開始。
- **3 バッチで m=201..586 全 386 幅完走**（batch1 201..334・batch2 335..512・batch3 513..586・
  GUARD 240s・各幅 gen+solve ≤ 2s）: **全幅 UNSAT・SAT 0・INDET 0**・
  conflicts 1,324..4,623・200s cap 内。
- 交差確認: **def+lex=H,V,HV が m=201 (2,076) / m=400 (9,841) / m=586 (7,652) すべて UNSAT**。
  決定性: m=300 再生成・再解が batch 記録と bit-exact（2,608 conflicts）。
- push: records.jsonl + controls（22e9fc44）→ 生ログ 386 件を 40 件/チャンク×10 コミット
  （71178fec .. 1d3bc63c）。
- **輸送アーティファクト2件を検出・修復**（教訓）:
  (1) records.jsonl 初回 push が **328/386 行で着地** — read_file の出力が 64KB 超で
  トランケーション（was_truncated を見ていなかった）。bash cat + 末尾改行補復で再 push
  （d33529e4）し、API contents で md5 f5e5fa78・386 行の byte-exact 着地を検証。
  (2) 生ログのうち**チャンク末尾9幅**（m=240/280/320/360/400/440/480/520/586）の末尾改行が
  cat トランスポートで喪失（1 バイト・q9 レーンの 5590f225 と同一アーティファクト）→
  再 push（f31675df）し API size で全幅ローカル一致を確認。

## 統合

- K0820: title 更新（M_{7,10}=19 exact）・artifact 2 件追加（q10-closure records・controls JSON）・
  追記4 セクション。
- mwq CSV: (7,10) 行 bounds/open `{19},201..587` → **exact-threshold/proved M=19**
  （exact-threshold 8 → 9 件・bounds open 13 → 12 件）。
- fixed-width README: (7,9)/(7,10) 段落を分離し (7,10)=19 exact の閉包記述に更新・
  確定値カウント更新。実験 README に結果セクション追記。

## 結論

- **(7,10) witness-free 帯 19..586 完全閉包 + K0318 U=587（proved）により M_{7,10} = 19 exact**。
  w=7 では初・w ≥ 6 でも初の真の安定化長の完全決着。
- (7,9) は q9 閉包レーンの m=201..612 完走待ち（完了すれば M_{7,9} = 24 exact）。

## レジューム

- (1) (7,9) m=201..612 は q9 レーン所有・完了・統合を確認してから関与。
- (2) 次の高速レーン候補: (7,8)=25..651 の帯延長（K0825・7×25 rowY=3 が 250s INDET で
  残るのは難所・K0342 型 tail 評価で U=651 を下げる価値あり）、q ≤ 8 の (7,q) 帯
  （K0827 の (7,4)/(7,5)/(7,6)・(7,7) K0826 は genfast2 で m≤651 級の掃引が可能に
  なった・ただし (7,8) q=w+1 は genfast3 不可・genfast2 は O(m³) で m=600 は ~400s/幅）、
  または (8,9)/(8,10)（eight-row レーンの統合確認後）。
- (3) 輸送教訓の一般化: >64KB ファイルは read_file で読まない（bash cat + wc -c 照合）、
  cat は stdout 末尾改行を削る（末尾ファイルに "\n" 補復）→ push 後は必ず API で
  size/md5 着地検証。
