# 2026-10-15: n11 S6/S8終局証明パッケージの独立検証と計画反映（要求S5和集合31,771）

## 経緯

- 上流確認: origin/main は `ebcd4cbb`。ローカルmainは他セッションの統合commit `d2fe5ce5`（Q48/N11統合・427 items）が未pushで先行していた。
- 統合ゲートで `tools/knowledge/tests` の `test_square_outcomes_and_evidence_boundaries` が失敗: K0426が `status: needs-review` のままで、このstatusは最終状態として許容されない。
- 原因: K0426は「パッケージ取り込みのみ・検査器は未実行」として needs-review で残されていた。検証を実施して確定させるのが正しい解。

## 実施（WSL2: bash + sha256sum + g++ 15.2 + python3、2026-10-15夜）

対象: `research/experiments/n11-s6-terminal-loss-20261015/` と `research/experiments/n11-targeted-terminal-lift-20261015/`。

1. `verify_s6_terminal.py` → PASS。483終局S10葉、1,028,621メモ化状態。証明書非圧縮SHA-256一致（cb2e73c2...）。
2. `verify_s8_loss_cpp.cpp`（g++ -O3 -std=c++20）→ 同一の29根・1,046義務・483葉・1,028,621状態で一致PASS。
3. `audit_joint_plan.py` → PASS。6個のS5 LOSS親のうち3個が選択S4クラス16397の8第三手群に一致（初手24/26/48）、要求S5和集合31,774→31,771。S4選択は固定。
4. `reproduce.sh` フル再現（4m30s）→ `PASS full clean-room reproduction`。SHA256SUMS照合、S8 WIN 171+16、S8 LOSS 3、407件のS10 C++/Python一致（WIN 364・LOSS 43・378,648状態・衝突0）、merge 51,164+407=51,571（重複0）、差分監査・偽近LOSS除外・高被覆475件全分類・負例対照すべてPASS。

## 判断

- K0426: `needs-review` → `verified`。evidence・artifact noteを実行記録に合わせて更新。
- K0417: 上界31,774 → **31,771**（S4選択固定・下界6,585不変・層別13・除外S4 17・WIN側値不変）。update6計画JSONは凍結基準として上書きしない（S6 READMEの「将来の計画改訂時は要再監査」に従う）。
- K0424: 夜間記録の31,774はそのまま。K0426検証による31,771への縮小を追記しK0417を参照。

## 次の一手

- d2fe5ce5＋本検証のコミットをpush。
- N11の次候補（未着手・新規指示待ち）: S6再順位付けの次根 `00000000000040001000044400010000`（51子中23 LOSS・28 UNKNOWN）、10M NODE_LIMIT据え置きの144019・144692・193768、block外221294。新規探索は明示指示があるまで起動しない。
