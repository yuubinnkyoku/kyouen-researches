# 2026-11-14 長期レーン: cost-60 sweep 19 WIN7証明書の並走再現・独立検証・frontier再計算再現（並走競合の記録を含む・11×11はUNKNOWNのまま）

## 何をしたか

第20セッション続きの最優先レジューム項目「cost-60 sweep の19 WIN7-D10候補の証明書抽出・独立検証」を、
最新main（7d8a1c9d）を取り直してから実施した。

1. **抽出・検証（本レーン）**: repo `class4_child1_cert_extractor.ts` に export キーワードのみを追加した
   パッチ（ロジック無改変）で kill-table-first 抽出を自前実装。各候補1プロセス（pilot d6 制御
   loss=false を毎プロセス先頭で確認）、kill 表は「各loser初手mに対し lossAt(root+m+r,8)=true となる
   最初のwinner応手r」を自前計算。19根すべてで証明書抽出に成功（合計 727,822 行・抽出 39.9M nodes）。
   repo `verify_bit7_win7_cert.ts`（Bareiss 4x4・engine不使用・fs-import/argv-guard のESMパッチのみ）
   で全19件が **root-check PASS・全合法sub-root PASS・双方向union 0/0・terminal [13,17]** で独立検証された。
   bit50 は完全独立の2プロセスで抽出し byte-identical（md5 46a94444be6b3d85f10edb57c85d4852）—
   決定制御。
2. **並走競合の発生と対応**: 反映直前のmain再取得で、並走レーンが同一の19根の証明書と record・
   frontier再計算（c37852d6, e49f25cc, ab09a8c0, 060406c2, 08bd6a1a, 1c8ee665）を先に push 済みだった。
   **重複pushは全て回避**した。差分は以下の通り:
   - 並走レーンの証明書は本レーンと**異なる木**（合計 605,587 行 vs 本レーン 727,822 行）。
     両方とも valid（WIN7証明書は正準戦略を1つ要求するだけで、戦略木は非正準）。小さい方を
     main側（正本）として維持し、本レーンの19証明書はpushしていない。
   - 本レーンは main の19公開証明書を**全件独立検証**（全PASS・union 0/0・terminal [13,17]）。
     cross-lane reproduction record として1件だけ反映（child#5 の相互再現recordの前例に倣う）。
3. **frontier再計算の再現**: 本レーン独自の `recompute_frontier_cost60.py`（recompute_frontier_full.py
   論理にcost60の19根を加えた段階制御付き再実装）を公開recordの根で実行。
   baseline 638/7208/565500・batch1 657/7189/564070・batch2 665/7181/563509/5398/423516・
   batch3 690/7156/561764/5373/421771 が**公表値と完全一致（assert）**。
   cost60追加後は **solved 724（+34・sweepの推定34と完全一致）・unique remaining 7122・
   sum cost 559294・open 5339/419301**。ranking CSV は公開版と **sha-256 byte-identical**。
4. **追加反映**: main に無かった `class-frontier-top-candidates-s6-after-cost60.csv` を反映
   （batch1/2/3と同一形式。次のsweep対象選定に直結）。

## 新しい確定状況（frontier after cost-60）

- **best class-2 blocker: S5 `00000000000000003802000008000000` が 32/2206 → 17/1168 に半減**
 （cost60の19証明書がこのS5のS6需要を大きく削った）。
- best class-4 は 24/1934 不変。**レーン目標は class-2 側に切り替わる**
 （17 orbit / cost 1168 < 24 / 1934）。
- 次の最安未sweep S6 child: **cost-61 `00000000000000801a02000000080000`（c2=2,c4=2）**。
- solved_s6_in_manifest 690→724、unique_remaining 7156→7122。

## 実装上のメモ

- `verify_bit7_win7_cert.ts` / `class4_child1_cert_extractor.ts` のCLIは strip-types 下で ESM 扱いに
  なり `require('fs')` が undefined になる。main側は既に修復済み（9f86edc0, 1aa0d4aa）。
  本レーンも同一のESMパッチで対応（fs-import・argv-guardのみ・ロジック無改変）。
- sub-root列挙は「rootの空きマス全て」ではなく「rootの**合法**初手」から（禁止マスクで弾かれた空きマスを
  入れると verifier が正当に missing-row エラーを出す。bit50 の m=2 で実際に発生し判明）。
- 証明書行数の帯: bit50 17,260〜bit76 54,317（本レーン）/ bit50 15,018〜bit52 49,003（main側）。
  抽出は native Node v22 で1根あたり2〜10秒・kill表込みで3.6〜25秒（全19根を1時間未満で完了可能）。
  kill表の入手コストが支配的でないため、**証明書再構築は sweep直後に同セッション内で完走できる**
  （従来の「重い抽出」という想定は本環境では過大評価だった）。

## レジューム

1. **次は cost-61 S6 child `00000000000000801a02000000080000`（c2=2,c4=2）の sweep**
 （新 best class-2 S5 `00000000000000003802000008000000` の最安軌道・61候補）。
   sweep→WIN7証明書化→frontier再計算まで1セッションで完走可能。
2. その次の class-2 側: cost-61 `00000000000000801a02020000000000`（c2=2）。
3. 並走レーンとの競合が常態化しているため、**反映前のmain再取得は必須**。
   証明書・record・recompute出力はファイル名衝突の可能性が高い（今回はrecordのschema名まで同一だった）。

## 解釈ガード

- WIN7証明書は「対応する7石rootから深さ10以内の勝ち」の証明のみ。
- REFUTED-D10 は「深さ10以内のWIN7の否定」のみ。
- **11×11空盤・二石root {49,60}・S2 {59,60}・class 2・class 4 はいずれも UNKNOWN。**
