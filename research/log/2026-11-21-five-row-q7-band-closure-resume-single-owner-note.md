# five-row q=7 band-closure resume (m=76..): single-owner declaration

- 宣言時刻: 2026-11-21T00:08Z. HEAD `61d3f72a`（n9-ge19 lane part5 のコミット・本レーンと経路不競合）。
- **担当レーン（単一オーナー）**: 2026-11-21T00:00Z 開始の高速レーン（本ノートを出版する実行）。
- **対象**: IN FLIGHT 実験 `research/experiments/five-row-q7-band-closure-35-157-20261115/` の再開。
  現在の witness-free 幅集合は {19,...,75}（m=35..61 def-mode UNSAT・m=62..75 は rowY=0/1/2
  分割3クラス完全決着・`output/records-split.jsonl` 参照）。鋭い形は
  **M_{5,7} = 19 または M_{5,7} ≥ 77**（K0821 監査規約=highest witness-free width +2）、
  上界 158（K0332 全称証明・SAT 非依存）。本実験は残る帯 **m=76..157（82幅）** を掃引し、
  全幅 UNSAT なら **M_{5,7} = 19 exact（w=5 で初の真の安定化長の完全確定）** を目指す。
  1回の実行で帯の一部（増分的な witness-free 帯の拡大）を出版してもよく、
  その場合は本宣言をレジュームとして次回実行に引き継ぐ。
- **方法（既存の実験設計を変更しない）**: m=62 以降の事前プロトコル通り **分割ファースト**。
  各幅 genfast3.js rowfixed rowY=0/1/2（V-鏡像 y↔4-y で3クラスが全5行を被覆・K0829 と同一の
  被覆論の w=5 版）→ kissat 4.0.4（230s cap）。各幅3クラスすべて UNSAT ならその幅の
  欠損極大非存在の完全証明。meta curves は各幅で第三系全帯予測表 `ts-census-fullband.json`
  と照合（m=76 予測 775 など）。SAT クラスが出たら停止し witness を dual-verify する。
  INDET クラスが出たら正直に記録し、--lex=H,V,HV 交差符号化等で次回レジューム時に継続
  （UNSAT 不在をもって正当化しない）。小幅ごとに checkpoint push
  （records-split.jsonl 追記 + `output/raw/kissat-5x<M>-q7-rowY<y>.txt` 生ログ）し、
  環境リセット被害を最小化する。
- **環境再構築と較正（宣言前に実施済み・本ノートの根拠）**:
  - kissat 4.0.4 official linux-amd64 を GitHub release `rel-4.0.4` の同梱バイナリから取得。
    md5 `3a5eba830aa6008a604fcc9bbe99a325` は 2026-11-15/18 の五行レーン pins・
    2026-11-20 の六行レーン宣言と**同一**。
  - genfast3.js は `six-row-q8-band-closure-22-370-20261114/scripts/` の正本
    （md5 `12c2bd9cb3b24887fc3896f7ea9bcadf`）・sat.js `0cc6021a4e523a0d7f4d5ea0f5f5d40c`・
    sat2.js `282ae832efa0080127c6c153e65e1c3c`（six-row-q8-m20-class-split 実験dir のコピー
    と byte 一致）。
  - **較正**: m=62 rowfixed の3クラス CNF を再生成し meta が既刊 record と完全一致
    （vars 20883・clauses 74795・curves 541）。kissat 再実行で **UNSAT (rc=20)・
    conflicts 67,141 (rowY=2) / 461,909 (rowY=1) / 1,024,449 (rowY=0)** が
    2026-11-18T13:00Z の published records と **3/3 すべて bit-exact 一致**
    （生ログは本レーンの raw に `*-recal.txt` として保存）。以上により本環境のスタックは
    2026-11-15/18 の記録生成環境と決定的に同一。m=62,63 の2環境 bit-exact 再現も既刊
    （2026-11-18 README 同日継続3）で、今回が3環境目の再現になる。
- **並走への依頼**: 他のレーンは本実験の m=76..157 帯掃引を重複実行しないこと。
  本宣言は (5,7) の帯掃引のみに及ぶ。six-row-q8 band3（m=109..370・宣言済み resume）・
  n9-ge19 marathon・n11 検証ラティス・y12/y13 universal・K_10 lower bound・
  有限体/inversive レーンとは経路不競合。
- **管轄の限界と解釈規約**: 各幅の rowY 3クラス UNSAT はその幅の 5×m 盤における欠損極大
  安全配置の非存在の完全証明（決定論的・3インスタンス）であり、代替符号化・def-mode 掃引は
  冗長性確認であって必要性条件ではない。witness-free 帯の拡大以上の主張
  （M_{5,7}=19 の確定は全幅 76..157 の UNSAT 完了時のみ・上界 158 の改善は別課題・
  他 (w,q) への外挿はしない）を本ノートではしない。nodes/conflicts 数を勝敗として読まない。
  標準 11×11 空盤・二石 root は UNKNOWN のまま。
- K番号は成果物の push 直前に3点確認（README grep "items/KNNNN-"・item path 404・list_commits）
  で取得する。
