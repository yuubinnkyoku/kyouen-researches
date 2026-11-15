---
id: K0783
title: n11 S2{59,60} milestone-5のS7候補監査とblocker類1・2の条件付き閉鎖
kind: proposition
status: computed
topics: [verification, certificates, provenance, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0675
  note: 94オラクル位置（78 FW + 16 SW）と14 LOSS sweep鍵が導出の全入力
- type: depends_on
  target: K0672
  note: focus2154の62証明書（27 WIN7 + 35 LOSS7）が再利用分類の入力
artifacts:
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost67c_certificates_third_independent_20261115.mjs
  role: verifier
  note: cost67cの2 WIN7証明書を有理中心分子＋共線分岐の別実装で全戦略木再生。D4親liftとS6 worklist所属も照合
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/cost67c-third-independent-certificate-audit-20261115.json
  role: data
  note: 2証明書PASS、13親軌道・7 worklist所属、共通六石子のWIN証明とfold未実施の境界を記録
- path: research/log/2026-11-15-n11-class2-cost67c-third-independent-audit.md
  role: source
  note: cost67c証明書の第三独立再生監査と親lift・frontier境界の記録
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/ms5_s7_reuse_candidates_part1.csv
  role: data
  note: 候補S7表 s7_hex,s6_hex,move,cat（1=既知LOSS子、2=プール候補）。part1..3で計8,763行
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/ms5_s7_reuse_stats.json
  role: manifest
  note: 導出anchor・md5一致・再利用分類の全計数
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/ms5_s7_reuse_analysis.ts
  role: source
  note: コメントのみで実行本体は未公開。再導出・再分類の再現器としては使用できない
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_published_candidates.py
  role: verifier
  note: 公開行の安全性・親子関係・件数を独立検査。候補の完全性や分類の正当性は検査しない
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/published-candidates-audit.json
  role: data
  note: 公開行の限定監査結果とmove座標の注意
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_candidate_completeness.py
  role: verifier
  note: 公開オラクル94位置の全対称像からS6ワークリスト上の合法な補完候補を全列挙
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_candidate_completeness_independent.py
  role: verifier
  note: 4点部分集合の逆引きと行列式による別実装で全親子対を照合
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_additional_geometry.py
  role: verifier
  note: 追加候補の安全性を独立な行列式判定で確認
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/candidate-completeness-audit.json
  role: data
  note: 全15072件と公開表に欠ける6309件の集計
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/additional-candidates.csv.gz
  role: data
  note: 追加6309件。moveは正規化されたs6の座標
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_candidate_classification.py
  role: verifier
  note: 既存の条件付きLOSS6と証明書監査記録に照らし全候補を分類
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/candidate-classification-audit.json
  role: data
  note: 条件付き先手LOSSと未確定候補の内訳
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/classified-candidates.csv.gz
  role: data
  note: 全候補の照合結果。possible_first_winは証明済み勝利ではない
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_win7_reuse.py
  role: verifier
  note: 公開WIN7監査記録を全S6ワークリストと照合
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_reused_witnesses.py
  role: verifier
  note: 抽出された勝ち子の合法性と証明書監査記録を個別照合
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/win7-reuse-audit.json
  role: data
  note: 534証人対・498親と削減後の件数・コスト
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/win7-reuse-hits.csv.gz
  role: data
  note: 各親の勝ち手・子・証明書監査記録の所在とハッシュ
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_s5_remaining.py
  role: verifier
  note: 全五石位置の合法子を再生成し、スイープとWIN7再利用を反映。幾何判定は2方式で照合
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/s5-remaining-after-reuse.json
  role: data
  note: 五石位置の残局面数と最小候補の集計
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/s5-remaining-after-reuse.csv.gz
  role: data
  note: 未解消186五石位置の残六石軌道数とコスト
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/s5-s6-remaining-incidences.csv.gz
  role: data
  note: 五石位置と未解消六石軌道の対応表
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_priority_children.py
  role: verifier
  note: class 1最小候補の13六石軌道から七石軌道を生成し、公開済み勝敗記録と照合
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/priority-s5-children-audit.json
  role: data
  note: 最小候補の七石局面の重複除去と既知結果の集計
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/priority-s5-unknown-s7.csv.gz
  role: data
  note: 新規証明書生成前の七石局面と六石親・合法手のスナップショット
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_priority_certificates.py
  role: verifier
  note: 保存した15件のWIN7・LOSS7戦略証明書を独立検査器で再検証
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/priority-certificates-verified.json
  role: manifest
  note: 先手WIN7証明書13件とLOSS7証明書2件のハッシュ・検証結果
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/priority-certificates/00000000000000803082000000000404-win7.cert.gz
  role: certificate
  note: 保存した15件の証明書の一例。他のファイルとハッシュはmanifestに列挙
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_class1_closure.py
  role: verifier
  note: 五石位置の全六石子・証明書・blocker類1への合法手を照合
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/class1-blocker-closure.md
  role: proof
  note: blocker類1の条件付き閉鎖と証明書の検査手順
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class1-closure-audit.json
  role: data
  note: 五石位置の40六石軌道とblocker 5・115への手の照合
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class1-s6-proof.csv
  role: certificate
  note: 各六石軌道の既存スイープ・監査記録・新証明書による勝ち子
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_new_certificate_reuse.py
  role: verifier
  note: 新規証明書のワークリスト全体への再利用と残件数を集計
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/new-certificate-reuse-audit.json
  role: data
  note: 類2の追加証明前のスナップショット。先手WIN六石523件、残7344件・コスト575287
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_class2_certificates.py
  role: verifier
  note: 類2候補の追加WIN7戦略証明書14件を独立検査
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-certificates-verified.json
  role: manifest
  note: 追加14件のSHA-256と独立検査結果
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-certificates/00000000000000809202000000000102-win7.cert.gz
  role: certificate
  note: 追加14件の証明書の一例。全ファイルとハッシュはmanifestに列挙
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_class2_progress.py
  role: verifier
  note: 類2候補の18六石軌道と全ワークリストへの証明書再利用を照合
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-progress-audit.json
  role: data
  note: 類2候補の17軌道解消後、最後の1軌道を判定する前のスナップショット
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_class2_last_loss.py
  role: verifier
  note: 最後の六石位置の全62七石子に対するLOSS7戦略証明書を独立検査
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-last-loss-verified.json
  role: manifest
  note: 全62件のLOSS7証明書のSHA-256と独立検査結果
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-last-loss-certificates/00000000000000809202000400000001-loss7.cert.gz
  role: certificate
  note: LOSS7証明書62件の一例。全ファイルとハッシュはmanifestに列挙
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_class2_counterexample.py
  role: verifier
  note: 62証明書による六石LOSSと3つの五石SECOND_WIN、および残ワークリストを2幾何判定で照合
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/class2-candidate-refutation.md
  role: proof
  note: 62子のLOSS7証明書による六石LOSSと3つの五石SECOND_WIN
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-counterexample-audit.json
  role: data
  note: 次の追加証明前の集計。六石LOSS・3つの五石SECOND_WIN・残六石7297件
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_class2_next_certificates.py
  role: verifier
  note: 次の類2候補で得られた4件のWIN7証明書を独立検査
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-next-certificates-verified.json
  role: manifest
  note: 追加4証明書のSHA-256と検証結果
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-next-certificates/00000000000000003800004008000802-win7.cert.gz
  role: certificate
  note: 追加4件の証明書の一例。全ファイルとハッシュはmanifestに列挙
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_class2_next_progress.py
  role: verifier
  note: 新規証明書の再利用と残ワークリストを再集計
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-next-progress-audit.json
  role: data
  note: 追加7証明前のスナップショット。残六石7288軌道と類2次候補の残27軌道
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_class2_next2_certificates.py
  role: verifier
  note: 類2次候補から得た追加7件のWIN7証明書を独立検査
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-next2-certificates-verified.json
  role: manifest
  note: 追加7証明書のSHA-256と検証結果
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-next2-certificates/00000000000000003800004208000200-win7.cert.gz
  role: certificate
  note: 追加7件の証明書の一例。全ファイルとハッシュはmanifestに列挙
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_class2_next2_progress.py
  role: verifier
  note: 追加証明書の再利用と残ワークリストを再集計
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-next2-progress-audit.json
  role: data
  note: 追加8証明前のスナップショット。残六石7278軌道と類2候補の残20軌道
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_class2_next3_certificates.py
  role: verifier
  note: 類2次候補から得た追加8件のWIN7証明書を独立検査
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-next3-certificates-verified.json
  role: manifest
  note: 追加8証明書のSHA-256と検証結果
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-next3-certificates/00000000000000801602000000200001-win7.cert.gz
  role: certificate
  note: 追加8件の証明書の一例。全ファイルとハッシュはmanifestに列挙
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_class2_next3_progress.py
  role: verifier
  note: 追加証明書の再利用と残ワークリストを再集計
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-next3-progress-audit.json
  role: data
  note: 追加7証明前のスナップショット。残六石7263軌道と類2候補の残12軌道
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_class2_next4_certificates.py
  role: verifier
  note: 類2候補から得た追加7件のWIN7証明書を独立検査
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-next4-certificates-verified.json
  role: manifest
  note: 追加7証明書のSHA-256と検証結果
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-next4-certificates/00000000000000003800004208100000-win7.cert.gz
  role: certificate
  note: 追加7件の証明書の一例。全ファイルとハッシュはmanifestに列挙
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_class2_next4_progress.py
  role: verifier
  note: 追加証明書の再利用と残ワークリストを再集計
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-next4-progress-audit.json
  role: data
  note: 次の六石LOSS検出前のスナップショット。残六石7251軌道
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_class2_next_loss.py
  role: verifier
  note: 類2次候補の六石位置の全72七石子に対するLOSS7戦略証明書を独立検査
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-next-loss-verified.json
  role: manifest
  note: 全72件のLOSS7証明書のSHA-256と独立検査結果
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-next-loss-certificates/0000000000000000380000400800000a-loss7.cert.gz
  role: certificate
  note: LOSS7証明書72件の一例。全ファイルとハッシュはmanifestに列挙
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_class2_next_counterexample.py
  role: verifier
  note: 72証明書による六石LOSSと2つの五石SECOND_WIN、残ワークリストを2幾何判定で照合
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/class2-next-candidate-refutation.md
  role: proof
  note: 72子のLOSS7証明書による六石LOSSと2つの五石SECOND_WIN
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-next-counterexample-audit.json
  role: data
  note: 追加5証明前のスナップショット。六石LOSS・2つの五石SECOND_WIN・残六石7244件
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_class2_batch5.py
  role: verifier
  note: 類2候補から得た追加5件のWIN7証明書を独立検査
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-batch5-certificates-verified.json
  role: manifest
  note: 追加5証明書のSHA-256と検証結果
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-batch5-certificates/00000000000000403800004088000000-win7.cert.gz
  role: certificate
  note: 追加5件の証明書の一例。全ファイルとハッシュはmanifestに列挙
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_class2_batch5_progress.py
  role: verifier
  note: 追加証明書の再利用と残ワークリストを再集計
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-batch5-progress-audit.json
  role: data
  note: 追加3証明前のスナップショット。残六石7235軌道と類2候補の残32軌道
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_class2_batch3.py
  role: verifier
  note: 類2候補から得た追加3件のWIN7証明書を独立検査
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-batch3-certificates-verified.json
  role: manifest
  note: 追加3証明書のSHA-256と検証結果
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-batch3-certificates/00000000000000805202000000200040-win7.cert.gz
  role: certificate
  note: 追加3件の証明書の一例。全ファイルとハッシュはmanifestに列挙
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_class2_batch3_progress.py
  role: verifier
  note: 追加証明書の再利用と残ワークリストを再集計
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-batch3-progress-audit.json
  role: data
  note: 追加2証明前のスナップショット。残六石7228軌道と類2候補の残27軌道
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_class2_batch2.py
  role: verifier
  note: 類2候補から得た追加2件のWIN7証明書を独立検査
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-batch2-certificates-verified.json
  role: manifest
  note: 追加2証明書のSHA-256と検証結果
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-batch2-certificates/00000000000000805206000000000200-win7.cert.gz
  role: certificate
  note: 追加2件の証明書の一例。全ファイルとハッシュはmanifestに列挙
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_class2_batch2_progress.py
  role: verifier
  note: 追加証明書の再利用と残ワークリストを再集計
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-batch2-progress-audit.json
  role: data
  note: 次の六石LOSS検出前のスナップショット。残六石7224軌道
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_class2_batch2b.py
  role: verifier
  note: 追加2件のWIN7証明書を独立検査
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-batch2b-certificates-verified.json
  role: manifest
  note: 追加2証明書のSHA-256と検証結果
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-batch2b-certificates/00000000000000805202000000008800-win7.cert.gz
  role: certificate
  note: 追加2件のWIN7証明書の一例
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_class2_third_loss.py
  role: verifier
  note: さらに別の六石位置の全64七石子に対するLOSS7証明書を独立検査
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-third-loss-verified.json
  role: manifest
  note: 全64件のLOSS7証明書のSHA-256と独立検査結果
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-third-loss-certificates/00000000000000805202000000002001-loss7.cert.gz
  role: certificate
  note: LOSS7証明書64件の一例。全ファイルとハッシュはmanifestに列挙
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_class2_third_counterexample.py
  role: verifier
  note: 64証明書による六石LOSSと3つの五石SECOND_WIN、残作業を2幾何判定で照合
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/class2-third-candidate-refutation.md
  role: proof
  note: 64子のLOSS7証明書による六石LOSSと3つの五石SECOND_WIN
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-third-counterexample-audit.json
  role: data
  note: 次のWIN7証明前のスナップショット。六石LOSS・3つの五石SECOND_WIN・残六石7213件
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_class2_batch1.py
  role: verifier
  note: 次の類2候補から得たWIN7証明書を独立検査
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-batch1-certificates-verified.json
  role: manifest
  note: 追加WIN7証明書のSHA-256と検証結果
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-batch1-certificates/00000000000000003802000008000006-win7.cert.gz
  role: certificate
  note: 追加WIN7終局戦略証明書
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_class2_batch1_progress.py
  role: verifier
  note: 追加証明書の再利用と残ワークリストを再集計
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-batch1-progress-audit.json
  role: data
  note: 次のWIN7証明前のスナップショット。残六石7211軌道と類2候補の残34軌道
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_class2_batch1b.py
  role: verifier
  note: 次の類2候補から得た追加WIN7証明書を独立検査
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-batch1b-certificates-verified.json
  role: manifest
  note: 追加WIN7証明書のSHA-256と検証結果
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-batch1b-certificates/00000000000000003802000009000008-win7.cert.gz
  role: certificate
  note: 追加WIN7終局戦略証明書
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_class2_batch1b_progress.py
  role: verifier
  note: 追加証明書の再利用と残ワークリストを再集計
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-batch1b-progress-audit.json
  role: data
  note: 並行レーンの追加証明前のスナップショット。残六石7208軌道
- path: research/experiments/n11-class2-blocker-closure-20261114/audit_closure.py
  role: verifier
  note: 類2候補の全六石子とWIN7監査記録、blockerからの合法手を2幾何判定で照合
- path: research/experiments/n11-class2-blocker-closure-20261114/closure-audit.json
  role: data
  note: 五石位置の41六石軌道とblocker 27・93への手の照合
- path: research/experiments/n11-class2-blocker-closure-20261114/s6-witnesses.csv
  role: certificate
  note: 各六石軌道のWIN7子・合法手・監査記録の所在
- path: research/experiments/n11-class2-blocker-closure-20261114/verify_key_certificates.py
  role: verifier
  note: cost-68の主要2証明書をPythonの整数行列式検査器で再検証
- path: research/experiments/n11-class2-blocker-closure-20261114/key-certificates-audit.json
  role: data
  note: 主要2証明書のSHA-256と独立検証結果
- path: research/experiments/n11-class2-blocker-closure-20261114/proof.md
  role: proof
  note: 類2 blocker 27・93の条件付き閉鎖と信頼範囲
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-merged-recompute-20261114.json
  role: data
  note: 並行レーンの公開監査記録を統合した残作業のスナップショット
- path: research/log/2026-11-13-n11-ms5-reproducer-source-audit.md
  role: log
  note: 再導出プログラムの実行本体が欠けることの監査
- path: research/log/2026-11-13-n11-ms5-worklist-derivation-and-s7-reuse-partition.md
  role: log
  note: 経緯と再現上の注意（メモリ上限・実装上の修正点）
- path: research/log/2026-11-14-n11-s2-incremental-reuse-source-audit.md
  role: log
  note: 23新規WIN7 rootの幾何・親子対応とK0675 baselineを独立再計算。43件の増分・cost3,275を再現。証明書本体は未再実行
- path: research/log/2026-11-14-n11-class2-lane-cost73c-raw-audit.md
  role: log
  note: cost-73cの73候補・11 raw batch・388,889,991 nodesを独立再集計。73 REFUTED-D10のみでfrontier変更なし
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost73d-certificates/README.md
  role: certificate
  note: cost-73dのbit48 WIN7 root。2分割66,680行の戦略証明書と検査範囲
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost73d-sweep-20261114.json
  role: data
  note: 73候補のsweep記録。bit48 WIN7-D10、残72 REFUTED-D10
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost73d-recompute-20261114.json
  role: data
  note: cost-73d証明書を反映した公開frontier再計算
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_cost73d_win7_certificate_independent.mjs
  role: verifier
  note: 円・直線の整数方程式を使う独立幾何実装でbit48証明書の全59 sub-rootを検査
- path: research/log/2026-11-14-n11-class2-lane-cost73d-win7.md
  role: log
  note: cost-73dのWIN7探索・証明書生成・公開frontier反映
- path: research/log/2026-11-14-n11-class2-cost73d-independent-certificate-audit.md
  role: log
  note: 66,680行証明書の別実装検査と7親D4軌道の照合
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_win7_certificate_bigint_independent.mjs
  role: verifier
  note: cost69e bit21 WIN7証明書をBigInt余因子展開で独立検査。既存のNumber Bareiss検証器とは別実装
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/cost69e-bit21-bigint-independent-verification-20261115.json
  role: data
  note: 22,261行・45/45部分木・欠落/余分0・終局石数13〜17
- path: research/log/2026-11-15-n11-class2-cost69e-bit21-bigint-independent-verification.md
  role: log
  note: bit21 WIN7証明書の独立BigInt検査記録
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost70c_raw_sweep.py
  role: verifier
  note: cost70cの70候補をBareiss整数行列式で再列挙し、13 WIN7-D10 rootの合法手数と既存記録を照合
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost70c-raw-sweep-audit-20261115.json
  role: data
  note: cost70cの13候補・節点100,935,666・mobility・既存証明書照合・mid-flight閉鎖
- path: research/log/2026-11-15-n11-class2-cost70c-raw-sweep-audit.md
  role: log
  note: cost70c raw sweepの独立監査とcost69e bit76による途中閉鎖
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost69e_20261115.py
  role: source
  note: S5親keyを文字列で一貫して扱うよう修正。receipt-unclosable S5とbest coverable S5を分離
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost69e-recompute-20261115.json
  role: data
  note: 6証明書反映後frontier 1,019/6,828/538,143と別個のreceipt-unclosable S5を記録
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost69e-20261115.csv
  role: data
  note: cost69eの7 marginal S6を除いた正しい候補表。best coverable class2は6軌道・費用443
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost72-win7-certificates-20261115.json
  role: manifest
  note: cost72 bit111のpartial WIN7 receipt。bit52は未証明として明示
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost72-certificates/bit111-root-00008000000000803202000000000200.cert
  role: certificate
  note: bit111 WIN7証明書。46,160戦略行・54/54部分木・集合差0/0
- path: research/log/2026-11-15-n11-class2-cost72-bit111-independent-audit.md
  role: log
  note: cost72 bit111証明書の独立検査とS5親の残り2子から1子への局所縮小
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost75b-recompute-20261115.json
  role: data
  note: cost75b統合後のglobal frontier 1,049/6,798/535,812/5,068/399,535。対象S5は2/147
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost75b-20261115.csv
  role: data
  note: cost72 child 000...0200とcost75 child 000...4000が対象S5の残り2子であることを確認
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost75b-sweep-20261115.json
  role: data
  note: cost75b全75候補完了、7 WIN7証明書、v15 cross-engine 7/7、決定性再実行3/3
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost75b-win7-certificates-20261115.json
  role: manifest
  note: cost75bの7 WIN7証明書。352,672行・406部分木、全件検証済み

- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost65e-bit7-independent-audit-20261115.json
  role: data
  note: cost65e bit7証明書のBigInt独立検査、D4親被覆、重複・衝突監査とfrontier差分
- path: research/log/2026-11-15-n11-class2-cost65e-bit7-independent-audit.md
  role: log
  note: bit7証明書の全56部分木検査と2つの新規S6親解消
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_bit7_win7_cert.ts
  role: verifier
  note: --certと--rootを指定して任意のWIN7証明書を独立再検査できる汎用整数Bareiss検証器

- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost65e-win7-certificates-20261114.json
  role: data
  note: cost65eのbit107・bit7のWIN7証明書receiptを統合。bit7は独立検証済みで、未証明候補一覧から除外

- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_warm_multiband_loss_conflicts_20261115.mjs
  role: verifier
  note: warm multiband 35 WIN7 rootを17 verified manifest・central LOSS7 parent-lift・knownloss候補へD4正規化で照合する衝突監査器
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/warm-multiband-loss-conflict-audit-20261115.json
  role: data
  note: 35 warm rootと既存WIN7/LOSS7・274 parent-lift・396 category-1候補のD4衝突監査
- path: research/log/2026-11-15-n11-class2-warm-multiband-loss-conflict-audit.md
  role: log
  note: 2026-11-15 warm multiband証明書の範囲限定WIN/LOSS衝突監査
- path: research/log/2026-11-15-n11-class2-cost60b-warm17-bigint-audit-and-cost71b-frontier.md
  role: log
  note: 17 warm証明書の独立検査、cost-71b frontier 1,026解消、bit22重複と未統合範囲
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost71b-recompute-20261115.json
  role: data
  note: cost-70c後からcost-71bの3 receiptを追加したmanifest-level frontier再計算
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost71b-bigint-independent-audit-20261115.json
  role: verifier
  note: cost-71b bits 109/21/105の独立BigInt検証結果
- path: research/log/2026-11-15-n11-class2-cost72-partial-batches1-5-audit.md
  role: log
  note: cost69e v2とcost70c/71bのfrontier基準差、およびcost72部分監査を記録
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost69e-recompute-20261115.json
  role: data
  note: cost69e 10 receipt・schema v2の独立再計算（merged baseline 1012から1023）
- path: research/log/2026-11-15-class2-lane-cost69e-win7.md
  role: log
  note: cost69e全11 WIN7候補の証明書化と10 receipt後のfrontier記録
- path: research/log/2026-11-15-n11-class2-cost72-batches1-9-audit.md
  role: log
  note: cost72の全72候補記録整合性、2つのWIN7-D10候補、未完了扱いの理由
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost69f-sweep-audit-20261115.json
  role: data
  note: "2026-11-15 cost69fの69候補raw sweep完了。WIN7-D10 9、REFUTED-D10 60、打切り0、112752229節点。9 WIN rootはD4軌道9個。証明書未抽出のためS6 frontierへの寄与0。 cost69f 69候補の全raw batch監査。9 WIN7-D10・60 REFUTED-D10・打切り0、D4 root照合"
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost69f-inflight-20261115.json
  role: manifest
  note: 費用69のS6 childと69合法候補の当初claim。歴史的なin-flight記録
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost69f-raw-batch1-20261115.jsonl
  role: data
  note: cost69f raw batch 1。探索記録であり証明書ではない
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost69f-raw-batch2-20261115.jsonl
  role: data
  note: cost69f raw batch 2。探索記録であり証明書ではない
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost69f-raw-batch3-20261115.jsonl
  role: data
  note: cost69f raw batch 3。探索記録であり証明書ではない
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost69f-raw-batch4-20261115.jsonl
  role: data
  note: cost69f raw batch 4。探索記録であり証明書ではない
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost69f-raw-batch5-20261115.jsonl
  role: data
  note: cost69f raw batch 5。探索記録であり証明書ではない
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost69f-raw-batch6-20261115.jsonl
  role: data
  note: cost69f raw batch 6。探索記録であり証明書ではない
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost69f-raw-batch7-20261115.jsonl
  role: data
  note: cost69f raw batch 7。探索記録であり証明書ではない
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost69f-raw-batch8-20261115.jsonl
  role: data
  note: cost69f raw batch 8。探索記録であり証明書ではない
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost69f-raw-batch9-20261115.jsonl
  role: data
  note: cost69f raw batch 9。探索記録であり証明書ではない
- path: research/log/2026-11-15-n11-class2-cost69f-sweep-complete-raw-audit.md
  role: log
  note: cost69f 69候補完了の集計、D4重複監査、証明境界
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost69f-win7-certificates-2-20261115.json
  role: manifest
  note: cost69fの9 WIN7-D10証明書を統合した現行記録。uncertified_bits_afterは空
- path: research/log/2026-11-15-n11-class2-lane-cost69f-remaining-certificates.md
  role: log
  note: cost69f残り4証明書の抽出・独立検証と9/9完了の記録
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost69f_second_independent_verification_20261115.mjs
  role: verifier
  note: split証明書の再検査、hash、4x4整数行列式、D4親被覆、証明書済みfrontierを再現
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/cost69f-second-independent-verification-20261115.json
  role: verifier
  note: bits2/94/109/119の第二独立検査結果と保存hashを記録
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost69f-certificate-backed-recompute-20261115.json
  role: data
  note: cost69fの9 receiptすべてを証明書済みとして反映したfrontier派生出力
- path: research/log/2026-11-15-n11-class2-cost69f-second-independent-verification.md
  role: log
  note: 4証明書の第二検査、根合法手数の別方式照合、frontier証拠等級更新
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost69f_win7_certs_20261115.py
  role: verifier
  note: 全9 cost69f WIN7証明書のPython第三完全独立監査。整数Bareiss 4x4行列式・repo検証器不使用・敵全合法手展開・v15 anchor照合込み
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost69f-9cert-python-independent-audit-20261115.json
  role: verifier
  note: 9/9 PASS。495,585戦略行・509 sub-root・union 0/0・終局石数13..17・records全フィールド一致
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/reconcile_cost69g_demand_20261115.py
  role: verifier
  note: cost69g子の需要不整合をmanifest+rankingからD4幾何再導出で解消。classesはbitmaskで二重役割S5(classes=6)がc2とc4の両方に需要を作る
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost69g-demand-reconciliation-20261115.json
  role: verifier
  note: 両側とも誤りなし。distinct open parents=3 と per-class demand c1=0,c2=2,c4=2 の意味論的和解とコントロール照合
- path: research/log/2026-11-15-n11-class2-lane-cost69f-python-independent-audit-and-69g-demand-reconciliation.md
  role: log
  note: Python第三監査と69g需要和解の実行記録
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost72b-sweep-20261115.json
  role: data
  note: cost72b子の72候補sweep記録。WIN7-D10 13・REFUTED-D10 59・打切り0・117,444,772 v16節点。証明書未抽出のためfrontier寄与0
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost72b-inflight-20261115.json
  role: manifest
  note: cost72b子sweepのclaim。歴史的なin-flight記録、statusは完了に更新済み
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost72b-raw-batch1-20261115.jsonl
  role: data
  note: cost72b raw batch 1。batch2..10・v15 crosscheck 4件・determinism rerunも同型の探索記録であり証明書ではない
- path: research/log/2026-11-15-n11-class2-lane-cost72b-sweep.md
  role: log
  note: cost72b子sweep完了の実行記録と交叉検査の詳細
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost72b-win7-certificates-20261115.json
  role: manifest
  note: cost72bの13 WIN7-D10証明書の全記録。636,225行・729 sub-root・抽出節点200,029,509・fbt_drops 0・独立検証13/13・19 partのblob sha
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost72b-certificates/bit2-root-00000000000000809102000002000004.cert.part1of2
  role: certificate
  note: 13証明書19ファイルの代表。bits 2/11/21/30/31/36/47/66/85/95/97/100/106、>1.75MBは2分割、全ファイルremote blob sha照合済み
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/cost72b_cert_pipeline_20261115.sh
  role: source
  note: 抽出・組み立て・検証の実ドライバ。repo-verbatim抽出器と汎用独立検証器を1 bit=1プロセスで駆動する
- path: research/log/2026-11-15-n11-class2-lane-cost72b-win7-certificates.md
  role: log
  note: 13証明書の抽出・検証・公開の実行記録
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost72b-receipts-recompute-20261115.json
  role: data
  note: cost72b 13 receipt foldのfrontier再計算。74d head 1,179へのrebase版・mim +9（すべて共有親801202の56→47）・head 1,188・2回実行byte-identical
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-s5-ranking-after-cost72b-receipts-20261115.csv
  role: data
  note: fold後のS5残存ranking。親809102は4軌道297で不変、共有親801202は47軌道3,561
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost72b-receipts-20261115.csv
  role: data
  note: fold後の次候補。親809102の残る4子（69g・74第二子・76・78）とclass4首位の明細
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost72b_receipts_20261115.py
  role: source
  note: fold実行体。74d head 1,179をrunpy鎖でbyte再現、18入力blob照合、13証明書byte検証、bit85==74d bit91のD4等価検証込み
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost72b-inflight-20261115.json
  role: manifest
  note: cost72b claim。status folded-into-chain-head-1188、foldブロック（mim内訳・D4 dedup・controls）追記済み
- path: research/log/2026-11-15-n11-class2-lane-cost72b-receipts-fold.md
  role: log
  note: 13 receipt foldの実行記録。rebase経緯・環境リセット事故・並走in-flight markerとの予測一致を含む


- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost76a_six_certificates_third_independent_20261115.mjs
  role: verifier
  note: "六つのcost-76a証明書を円の有理中心と共線分岐で第三独立再生し、親liftも監査するstandalone Node.js検査器"
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/cost76a-six-certificates-third-independent-audit-20261115.json
  role: data
  note: "6/6第三独立再生結果とhead 1188時点の局所edge被覆。global frontierは未更新"
- path: research/log/2026-11-15-n11-class2-cost76a-third-independent-certificate-audit.md
  role: log
  note: "共線判定の初期不一致と修正、6証明書の再生、3つのS5行への部分被覆を記録"

- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost74d-win7-certificates-20261115.json
  role: manifest
  note: cost74dの15 WIN7-D10候補を14本体とbit91のD4再利用で証明書化。BigInt/Number Bareissの二重独立検査15/15、19/19新規part公開と既公開bit118を含む20/20 remote Git blob SHA照合
- path: research/log/2026-11-15-n11-class2-lane-cost74d-certificate-publication-completion.md
  role: log
  note: cost74d証明書の再抽出・二重独立検査・全part公開・remote hash照合を完了した記録
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost74d_win_loss_conflicts_20261115.mjs
  role: verifier
  note: cost74dの15 WIN7-D10 rootを既存WIN7/LOSS7 manifest・中央49 LOSS7 parent-lift・category-1候補とD4照合。入力Git blob SHAを固定
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/cost74d-win-loss-conflict-audit-20261115.json
  role: data
  note: 公開済み範囲のD4衝突監査。既存LOSS7との交差0、cost72b bit85との意図した再利用1件
- path: research/log/2026-11-15-n11-class2-cost74d-win-loss-conflict-audit.md
  role: log
  note: cost74d WIN7/LOSS7の範囲限定D4衝突監査と証拠境界
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost78a-win7-certificates-20261115.json
  role: manifest
  note: cost78a WIN7証明書5/5（bits 8,20,29,36,109）のmanifest。326,698行・97,619,220 extraction nodes・311 sub-roots・31 distinct parent orbits
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost78a-certificates/bit29-root-00000000000000809102000020400000.cert.part1of2
  role: certificate
  note: 新規抽出bit29証明書のpart1。bit8/bit109も同ディレクトリに2 partずつ公開
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/assemble_cost78a_certificate_20261115.py
  role: source
  note: blind抽出rowsのsort -u・header付与・hash receipt生成
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/split_certificate_at_line_boundary_20261115.py
  role: source
  note: 1.75 MiB超証明書の行境界2分割とpart hash receipt
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/build_cost78a_certificate_manifest_20261115.py
  role: source
  note: 5/5証明書manifestの生成。whole LF blob・part blob・二独立検証結果・親orbitを記録
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost78a_receipts_20261115.py
  role: source
  note: cost78a 5 receipt fold。head 1216のbyte再現・25入力blob照合・sweep再導出・証明書bytes検証・fold・completed claim制御
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost78a-receipts-recompute-20261115.json
  role: data
  note: fold後head 1222/6625/522908/4895/386631とper-receipt marginal・親S5 after
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost78a-receipts-20261115.csv
  role: data
  note: fold後の次候補。best coverable class-2は第3 target 2行/143（69/74）
- path: research/log/2026-11-15-n11-class2-lane-cost78a-certificates-and-receipt-fold.md
  role: log
  note: 3証明書のblind抽出・二独立検証・5 receipt fold・Windows LF/CRLF再現注意
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost70e_certificates_third_independent_20261115.py
  role: verifier
  note: cost70e証明書5件の第三独立監査。part連結・LF正規化・BigInt+Number Bareiss再実行・D4親orbit再導出
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost70e-certificates-third-independent-audit-20261115.json
  role: data
  note: cost70e 5/5 PASS・236,784行・8,564,174 bytes・280 sub-roots・31 distinct parent orbits・child orbit covered
- path: research/log/2026-11-15-n11-class2-lane-cost70e-certificates-third-independent-audit.md
  role: log
  note: cost70e証明書5件の第三独立監査記録（foldは未実施・head 1227不変）
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost70f_raw_sweep_20261115.py
  role: verifier
  note: cost70f raw sweepの独立監査（stdlib Bareiss・候補70再列挙・9 batch再導出・D4重複0・一石削除6件・head-1233 CSV照合）
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost70f-sweep-audit-20261115.json
  role: data
  note: cost70f 70候補・4 WIN7-D10 bits 9/64/72/84・66 REFUTED・0 capped・81,480,831 nodes
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost70f-win7-certificates-20261115.json
  role: manifest
  note: cost70f WIN7証明書4件。155,155行・5,601,978 bytes・26,952,264 extraction nodes・214 sub-roots・25 distinct parent orbits
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost70f_receipts_20261115.py
  role: source
  note: cost70f 4 receipt fold。head 1235のbyte再現・sweep audit/証明書bytes検証・fold・completed claim制御
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost70f-receipts-recompute-20261115.json
  role: data
  note: fold後head 1239/6608/521701/4878/385424とper-receipt marginal・親S5 after
- path: research/log/2026-11-15-n11-class2-lane-cost70f-sweep-certificates-and-fold.md
  role: log
  note: cost70fのsweep・4証明書抽出・二独立検証・fold・Windows LF/CRLF再現注意


- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost70f_70g_71c_cross_lane_d4_overlap_20261115.mjs
  role: verifier
  note: cost70f/70g/71cのWIN7 rootと六石parent liftをBigInt D4正準化で横断照合。raw hexでは見えない重複root・親軌道を検出
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/cost70f-70g-71c-cross-lane-d4-overlap-20261115.json
  role: data
  note: cost70f bit84とcost70g bit29のD4同値、親lift交差8軌道、cost71cとの交差0を記録
- path: research/log/2026-11-15-n11-class2-cross-lane-d4-receipt-overlap.md
  role: source
  note: cross-lane重複の分解とfold順への含意。frontier foldではない境界を明記
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost74g_receipts_20261115.py
  role: source
  note: cost74g 10 receipt fold。head 1257のbyte再現・sweep/証明書bytes検証・fold・completed claim制御
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost74g-receipts-recompute-20261115.json
  role: data
  note: fold後head 1266/6581/519710/4851/383433とper-receipt marginal・親S5 after（第三target 1行/69）
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost74g-receipts-20261115.csv
  role: data
  note: fold後の次候補。第三targetは残り1行（cost-69）
- path: research/log/2026-11-15-n11-class2-lane-cost74g-sweep-certificates-and-fold.md
  role: log
  note: cost74gのsweep・10証明書抽出・二独立検証・fold・73g headへのrebase
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost69i_receipts_20261115.py
  role: source
  note: cost69i 4 receipt fold。head 1266のbyte再現・sweep/証明書bytes検証・第三target S5閉鎖制御・completed claim制御
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost69i-receipts-recompute-20261115.json
  role: data
  note: fold後head 1273/6574/519179/4844/382902と第三target S5の残行0・class-2 blocker条件付き閉鎖
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost69i-receipts-20261115.csv
  role: data
  note: 第三target閉鎖後の次候補。第二target 18行/1390・best class-4 18行/1460
- path: research/log/2026-11-15-n11-class2-lane-cost69i-sweep-certificates-and-fold.md
  role: log
  note: cost69iのsweep・4証明書抽出・二独立検証・第三target S5閉鎖fold
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost76b_receipts_20261115.py
  role: source
  note: cost76b 2 receipt fold。head 1277のbyte再現・sweep/証明書bytes検証・第二target 16行へのfold
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost76b-receipts-recompute-20261115.json
  role: data
  note: fold後head 1280/6567/518678/4837/382401と第二target 16行/1249
- path: research/log/2026-11-15-n11-class2-lane-cost76b-sweep-certificates-and-fold.md
  role: log
  note: cost76bのsweep・2証明書抽出・二独立検証・第二target 17→16行fold
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost77a_receipts_20261115.py
  role: source
  note: cost77a 3 receipt fold。head 1280のbyte再現・sweep/証明書bytes検証・第二target 15行へのfold
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost77a-receipts-recompute-20261115.json
  role: data
  note: fold後head 1282/6565/518522/4835/382245と第二target 15行/1172
- path: research/log/2026-11-15-n11-class2-lane-cost77a-sweep-certificates-and-fold.md
  role: log
  note: cost77aのsweep・3証明書抽出・二独立検証・第二target 16→15行fold
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost77b_receipts_20261115.py
  role: source
  note: cost77b 4 receipt fold。head 1282のbyte再現・sweep/証明書bytes検証・第二target 14行へのfold
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost77b-receipts-recompute-20261115.json
  role: data
  note: fold後head 1286/6561/518211/4831/381934と第二target 14行/1095
- path: research/log/2026-11-15-n11-class2-lane-cost77b-sweep-certificates-and-fold.md
  role: log
  note: cost77bのsweep・4証明書抽出・二独立検証・第二target 15→14行fold
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost77c_receipts_20261115.py
  role: source
  note: cost77c 8 receipt fold。head 1286のbyte再現・sweep/証明書bytes検証・第二target 13行へのfold
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost77c-receipts-recompute-20261115.json
  role: data
  note: fold後head 1290/6557/517923/4827/381646と第二target 13行/1018
- path: research/log/2026-11-15-n11-class2-lane-cost77c-sweep-certificates-and-fold.md
  role: log
  note: cost77cのsweep・8証明書抽出・二独立検証・第二target 14→13行fold
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_merged_cost75d_77d_20261115.py
  role: source
  note: 75d head 1296へのwarm-hygiene merge。bit78 root==75d bit92 rootを除外しchild closureを再主張しない
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-merged-cost75d-77d-receipts-recompute-20261115.json
  role: data
  note: merged head 1302/6545/517025/4815/380748、第2開親64行/5036→58行/4593
- path: research/log/2026-11-15-n11-class2-merged-cost75d-77d-warm-hygiene.md
  role: log
  note: 75d+77d warm-hygiene mergeとcross-lane root collision（bit78==bit92）の記録
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost79a_receipts_20261115.py
  role: source
  note: cost79a 3 receipt fold。head 1302のbyte再現・sweep/証明書bytes検証・第二target 10行へのfold
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost79a-receipts-recompute-20261115.json
  role: data
  note: fold後head 1304/6543/516873/4813/380596と第二target 10行/787
- path: research/log/2026-11-15-n11-class2-lane-cost79a-sweep-certificates-and-fold.md
  role: log
  note: cost79aのsweep・3証明書抽出・二独立検証・第二target 11→10行fold
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost80d_receipts_20261115.py
  role: source
  note: cost80d 4 receipt fold。head 1304のbyte再現・sweep/証明書bytes検証・第二target 9行へのfold
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost80d-receipts-recompute-20261115.json
  role: data
  note: fold後head 1305/6542/516793/4812/380516と第二target 9行/707（best coverable class-2）
- path: research/log/2026-11-15-n11-class2-lane-cost80d-sweep-certificates-and-fold.md
  role: log
  note: cost80dのsweep・4証明書抽出・二独立検証・第二target 10→9行fold
scope: n11 S2 {59,60} milestone-5のワークリストとS7証明書再利用。局所S6と三石位置のblocker類1・2の条件付き勝敗を含むが、二石rootや空盤の勝敗は含まない。
evidence: "公開manifestの辞書順md5は0e95a438dbcb486368393de9c73fc21e。94オラクルの全744対称像を使い補完候補15072件を独立列挙。類1の新規WIN7戦略証明書13件・LOSS7証明書2件、類2のWIN7証明書54件と3六石位置の全62子・全72子・全64子のLOSS7証明書を独立検査。類1の五石位置の40六石軌道は既存記録と合わせて全て先手WIN。既存の一部証明書本体は別保管であり、公開監査記録に依存する。 2026-11-15 cost72 bit111 WIN7証明書を独立検査し、cost75b統合後の対象S5親を局所的に2軌道・費用147から1軌道・費用75へ縮小した。global frontierは未再計算。2026-11-15 warm multiband 35 WIN7 receipt後の公開frontierは解消S6 1,109・残り6,738・費用531,295・open需要5,008/395,018。35 rootを同実験の17 verified manifest（WIN7 77・LOSS7 200）、central LOSS7 parent-lift 274鍵、category-1候補396行とD4照合し、衝突0（category-1行は証明書とは数えない）。; 2026-11-15 cost69f残り4証明書(bits2/94/109/119)を別V8実行で再検査し全PASS。262,236行、検証訪問560,273局面、union 0/0、4×4行列式による根合法手数一致、8 partのGit blob SHA1・MD5/SHA256一致。cost69fの+9 S6軌道が全て証明書済み 2026-11-15 cost69f全9証明書をPython/Bareiss第三実装で再検査し9/9 PASS（第二検証のV8/BigInt 4件と共通フィールド全一致）。cost69g子の需要は二重役割S5(classes=6)のper-class計数と確定（distinct open parents=3、c1=0,c2=2,c4=2） 2026-11-15 cost72b子 00000000000000809102000002000000（cost 72・需要c1=0,c2=2,c4=0・open親2軌道）の72候補raw sweep完了。WIN7-D10 13（bits 2,11,21,30,31,36,47,66,85,95,97,100,106）・REFUTED-D10 59・打切り0・117,444,772節点。v15 cross-engine 13/13 loss=true、決定性再実行13/13 node-exact。13 rootは証明書未抽出の探索候補のためfrontier寄与0。; 2026-11-15 cost74d公開証明書bits12/66/68/118とcost72b bit85をBigInt独立検査器で5/5再生。D4親持ち上げにより証明書付きS6下限1166→1169（receipt frontier 1179とは区別）; 2026-11-15 cost72b正利得9証明書（bits 2,30,31,36,47,95,97,100,106）をBigInt独立再生9/9、13分割blobと9 whole-file Git SHA1一致。新規S6 manifest 9/9を裏付け、証明書付き下限1169→1178（receipt 1188とは区別）; 2026-11-15 cost78a WIN7証明書5/5（bits 8,20,29,36,109）をBigInt+Number Bareissで二重独立検証し、5 receiptsをcost-67c fold後のhead 1219へfoldして新head 1225/6622/522699/4892/386422（in-manifest marginal 6・childはbit36で閉鎖・第3 class-2 target S5は2行/143）。その後並走cost-69h foldが本78a head 1225にrebaseしてcanonical head 1227/6620/522561/4890/386284を確定（head分岐解消）; 2026-11-15 cost70e WIN7証明書5件（bits 0,8,24,66,79・236,784行・280 sub-roots）をBigInt+Number Bareissの二独立検証器で5/5 PASS（union 0/0・terminal [13,17]・child orbit covered）。foldは未実施でhead 1227不変; 2026-11-15 cost70f sweep（70候補・4 WIN7-D10 bits 9/64/72/84・66 REFUTED・81,480,831 nodes）と証明書4件（155,155行・214 sub-roots）を二独立検証し、4 receiptsをhead 1235へfoldして新head 1239/6608/521701/4878/385424（in-manifest marginal 4・childはbit9で閉鎖・第2 target 24行/1836・第2開親54行/4055）; 2026-11-15 cost72c 9 WIN7 receiptsをhead 1239へfoldして1244、cost73g 8 WIN7 receiptsをhead 1244へfoldして1249、cost74g 10 WIN7 receipts（639,189行・600 sub-roots）をhead 1257へfoldして新head 1266/6581/519710/4851/383433（in-manifest marginal 9・childはbit4で閉鎖・第三target S5は残り1行/69）; 2026-11-15 cost69i 4 WIN7 receipts（bits 21,29,97,100・204,339行・216 sub-roots）をhead 1266へfoldして新head 1273/6574/519179/4844/382902（in-manifest marginal 7・childはbit21で閉鎖・第三target S5は0行/0に閉鎖しclass-2 blockerが条件付きで閉鎖）; 2026-11-15 cost65l+cost74g+cost69iの3-way mergeでcanonical head 1277/6570/518896/4840/382619、cost76b 2 WIN7 receipts（bits 72,96・118,437行・121 sub-roots）をhead 1277へfoldして新head 1280/6567/518678/4837/382401（in-manifest marginal 3・childはbit72で閉鎖・第二target S5は17行/1325→16行/1249）; 2026-11-15 cost77a 3 WIN7 receipts（bits 40,64,111・157,475行・182 sub-roots）をhead 1280へfoldして新head 1282/6565/518522/4835/382245（in-manifest marginal 2・childはbit40で閉鎖・第二target S5は16行/1249→15行/1172）; 2026-11-15 cost77b 4 WIN7 receipts（bits 9,12,59,105・190,937行・231 sub-roots）をhead 1282へfoldして新head 1286/6561/518211/4831/381934（in-manifest marginal 4・childはbit9で閉鎖・第二target S5は15行/1172→14行/1095）; 2026-11-15 cost77c 8 WIN7 receipts（bits 10,40,50,54,58,95,96,111・362,362行・457 sub-roots）をhead 1286へfoldして新head 1290/6557/517923/4827/381646（in-manifest marginal 4・childはbit10で閉鎖・第二target S5は14行/1095→13行/1018）; 2026-11-15 cost75d 4 WIN7 receiptsをhead 1290へfoldして1296、cost77d 12 WIN7 receiptsのうちbit78 root==75d bit92 rootを除外した11件をwarm-hygieneでhead 1296へfoldして新head 1302/6545/517025/4815/380748（in-manifest marginal 6・child closureは75d bit92に帰属・第2開親は64行/5036→58行/4593）; 2026-11-15 cost79a 3 WIN7 receipts（bits 9,50,64・165,209行・178 sub-roots）をhead 1302へfoldして新head 1304/6543/516873/4813/380596（in-manifest marginal 2・childはbit9で閉鎖・第二target S5は11行/866→10行/787）; 2026-11-15 cost80d 4 WIN7 receipts（bits 48,61,81,96・202,272行・243 sub-roots）をhead 1304へfoldして新head 1305/6542/516793/4812/380516（in-manifest marginal 1・childはbit48で閉鎖・第二target S5は10行/787→9行/707でbest coverable class-2に）"

---

## 主張

1. milestone-5のS6ワークリスト7,867行（鍵・classes・cost全部門）が、K0675オラクル入力からの独立再導出と全行バイト一致したと報告されている（md5 0e95a438dbcb486368393de9c73fc21e、辞書順）。ただし当該再導出の実行本体は公開されておらず、報告自体は現checkoutから再実行できない。
2. 公開ワークリストS6からのoracle補完候補S7（|O\S6|=1かつx合法）は、94オラクルの全対称像を考慮すると **15,072件**。従来公開表8,763件はこの部分集合であり、**6,309件が未掲載**。候補のある親は7,256個、ない親は611個。全列挙は公開ワークリストとオラクルを入力とする有限検査であり、ワークリスト自体の完全性や候補の勝敗分類は検査していない。
3. 既知の14個のLOSS6の合法子とfocus62監査記録から、公開8,763件中396件・追加6,309件中229件が **条件付き先手LOSS7**、残る公開8,367件・追加6,080件がスイープ上の勝ち子と照合可能な候補である。この時点の候補分類そのものは先手WIN7を意味しない。LOSS7/WIN7は元の先手の勝敗であり、七石位置の手番側から見た勝敗と区別する。
4. 公開されている3系統のWIN7証明書監査記録4,052鍵の照合で、当初 **534親子対・498親**にWIN7子を確認した。その後、類1の新規WIN7証明書13件により25親、類2の新規WIN7証明書54件によりさらに115親を解消。合計 **638親**が先手WINとなった。さらに3つの六石LOSSを持つ8つの五石位置を除いた後、この時点の残作業は **7,208六石軌道**、合法子コスト合計 **565,500**。既存証明書本体の一部は別保管で、その公開監査記録に依存する。
5. 新規証明書追加前の五石残作業は、既に第二手勝ちの10軌道を除き186軌道だった。そのうちclass 1の `00000000000000803082000000000000` は合法80手・40六石軌道の全てが先手WINであり、**この五石位置も先手WIN**。内訳は既存スイープ2軌道・既存監査記録25軌道・新規に独立検証した証明書13軌道。これにより三石位置 `{59,60,61}` のblocker手5と115は、それぞれ五石位置への手71と49により先手WINとして閉鎖される。さらに8五石軌道が第二手勝ちと判明し、この時点の五石未解消軌道は **177**。

6. 並行レーンの公開WIN7監査記録を統合すると、class 2の五石位置 `00000000000000003802000008000000` の合法82手・41六石軌道も全て先手WIN。内訳は既存スイープ1軌道、以前のWIN7監査記録4軌道、保存済み終局証明書4軌道、並行レーンのWIN7証明書32軌道。よって五石位置は先手WINで、三石位置 `{59,60,61}` のblocker手27と93は、それぞれ手49と71により**条件付きで閉鎖**される。全軌道の合法性・証明書の根・公開監査記録を照合し、重要なcost-68証明書2件はPythonの別検査器で戦略木を再検証した。その他の既存証明書の正しさは公開監査記録を前提とする。

新規証明書追加前の各blocker類で残六石軌道数が最少の候補は、class 1が13軌道・コスト859、class 2が `00000000000000809202000000000000` の18軌道・コスト1092、class 4が `00000000020000003800000080000000` の43軌道・コスト3391。これらの残数は新規証明書の反映前のスナップショットであり、探索時間の保証ではない。

類2の上記候補について、18六石軌道中17軌道は追加した14件のWIN7証明書で解消した。最後の `00000000000000809202000400000000` は合法七石子62軌道全てがLOSS7であり、全62件の独立検証済み証明書により**先手LOSS**。この六石子を選べる五石位置は上記候補を含め3軌道あり、いずれも第二手勝ち。この候補では類2 blockerを閉じられないが、別の候補によって上記6の通り閉鎖された。

類2の次候補 `00000000000000003800004008000000` は、六石子 `00000000000000003800004008000008` の合法七石子72軌道全てがLOSS7であり、自身も**第二手勝ち**と判明した。同じ六石子へ手38で移れる `00000000000000003800000008000008` も第二手勝ち。さらに類2候補 `00000000000000805202000000000000` と別の2五石位置も、六石LOSS `00000000000000805202000000002000` の全64七石子の証明書によって第二手勝ち。上記6の勝ち五石位置は以前は残32軌道だったが、その後の並行レーンの証明書により閉鎖された。

並行レーンの公開記録を統合した時点の残作業は五石176軌道・六石6,960軌道だった。ただしこれは類2を含む当時の集計で、類2閉鎖後の最小作業量ではない。類4の有力候補 `00000000020000003800000080000000` は同じ時点で残18六石軌道・合法子コスト1460。

class 1の最小候補は、13六石軌道の859合法手を対称性でまとめると727七石軌道だった。新規証明書追加前の既存記録では31軌道が先手LOSS・696軌道が未判定だったが、今回新規WIN7証明書を用いて13六石軌道を全て閉じた。

欠落例として、公開親 `0000000000000000380000000000002c` に座標51を加えた局面は合法で、オラクル `00000000000000003800800000000080` の対称像 `00000000000000003808000000000008` を含む。子の正規形 `000000000000000038008000000001a0` は元の公開表にない。

## 帰結

- 公開manifestの鍵集合・classes列・cost列の3系統一致は記録上の結果であり、独立再導出の実行本体の復元が必要。
- 既存WIN7監査記録との照合は498親、新規証明書はさらに140親を解消する。候補のうち既知の条件付きLOSS7は追加証明書生成前の時点で625件。補完候補がなかった親は611個であり、別の勝ち手の可能性を排除しない。

## 限界

- 全てのwin/loss記述はK0675オラクル（78 FW + 16 SW）の条件付き。オラクルが崩れれば本項も崩れる。
- **11x11空盤・二石root {49,60}・S2 {59,60}はいずれもUNKNOWNのまま。**類4も未解決であり、局所的な類1・2の閉鎖から盤全体の勝敗は確定しない。
- possible-win-poolは「 witness候補」であって証明済みWIN7ではない。hitしたものだけが閉鎖になる。
- CSVの `s7_hex` と `s6_hex` はそれぞれ対称性で正規化された局面だが、`move` は `s6_hex` の座標に直接対応するとは限らない。公開8,763行中7,158行は直接適用しても同じ子に到達せず、うち119行では既に石のある座標を指す。親の8個の対称像を試し、空き座標 `move` を加えた後の正規形が `s7_hex` と一致する像を選ぶこと。全行でそのような像の存在を検査した。
- 候補CSVのヘッダーはpart1にのみある。part2とpart3をそれぞれヘッダー付きCSVとして読み込むと、各パートの先頭データ行が失われる。


## 2026-11-14: incremental WIN7 reuse from the class2 lane

The original 498-parent reuse count above is the baseline from the three receipt files named in `audit_win7_reuse.py`. Four later class2-lane WIN7 manifests (cost-69c, 70b, 71, and 75) add 23 distinct seven-stone roots. All 23 roots pass an exact integer-geometry safety check; none duplicates a baseline WIN7 root or conflicts with a baseline LOSS7 receipt.

Deleting one stone from each original-first WIN7 root gives 70 parent-child incidences in the S6 milestone-5 worklist, covering 48 distinct D4-canonical S6 parents. Five were already covered by the baseline, so **43 additional S6 worklist orbits** are now closed by WIN7 reuse (class histogram: 3 class-1, 35 class-2, 5 class-3). The covered-parent count rises from 498 to 541; rows not yet closed by this WIN7-reuse mechanism fall from 7,369 to **7,326**.

The worklist contains 615,497 legal seventh-move candidates in total. After the baseline 498 parent hits, the remaining cost was 577,110; these 43 new parents remove another 3,275 candidates, leaving **573,835**. This is a worklist accounting reduction, not a game-theoretic distance or a count of unresolved game positions.

The audit rechecks D4 normalization, seven-stone occupancy, exact safety of the new roots, parent inclusion, and conflicts against the baseline LOSS7 receipts. It does **not** re-run the certificate bodies; it reuses the already-published verification receipts and logs. Reproduction: [audit script](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_incremental_class2_win7_reuse.py), [machine-readable result](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-win7-reuse-incremental-20261114.json), [run log](../../log/2026-11-14-n11-s2-class2-win7-incremental-reuse.md).

The S2 `{59,60}` root, two-stone root `{49,60}`, and empty 11×11 root remain **UNKNOWN**. These 43 S6 parent lifts do not close the 1,447-orbit S5 worklist.

### 2026-11-14 independent reproducibility audit

The large K0675 receipts were retrieved through the raw-file path after the ordinary GitHub file-fetch interface returned empty content for files above its size limit. The earlier zero-byte interpretation was a retrieval artifact, not a repository defect.

Independent recount:
- `sweep_results.json`: 3,868 S6 records; 3,854 WIN-for-mover, 14 LOSS-for-mover, 0 timeout, 29,680 attempts.
- `s6sweep/verified.json`: 4,288 receipts (3,401 WIN7 / 887 LOSS7), fails 0.
- Union of all three baseline receipt files: 4,052 WIN7 / 2,699 LOSS7, with no WIN/LOSS conflict.
- Baseline WIN7 receipts close 498 S6 worklist parents, removing cost 38,387; 7,369 parents and cost 577,110 remain.
- The four new manifests contain 23 distinct D4-canonical, seven-stone roots, all passing an independent exact integer-geometry safety check. None duplicates a baseline WIN7 root or conflicts with a baseline LOSS7 receipt.
- These roots create 70 parent-child incidences over 48 worklist parents. Five were already baseline-covered; the incremental 43 have cost 3,275 and class histogram 1:3 / 2:35 / 3:5.
- The union therefore covers 541 parents, leaving 7,326 parents and cost 573,835.

The 48 saved parent records, their child-root sets, the 43-entry `incremental_parent_hex`, and the cost/class totals match the independent recomputation.

A remaining provenance mismatch is that the checked-in `audit_incremental_class2_win7_reuse.py` writes `inputs` and `already_covered_by_baseline`, while the saved JSON uses `input` and `already_in_baseline` and additionally has `checks.worklist_unique`. The numeric and set results are independently reproduced, but the saved JSON is not byte-for-byte attributable to the current script revision. The script and output schema should be unified.

The 23 certificate bodies were not re-run. This audit independently checks the K0675 receipt sets, exact root geometry, D4 normalization, baseline conflicts, parent incidence, and worklist accounting; WIN7 strategy validity continues to rely on the published independent certificate receipts.

See [the audit log](../../log/2026-11-14-n11-s2-incremental-reuse-source-audit.md). The S2 `{59,60}` root, two-stone root `{49,60}`, and empty 11×11 root remain **UNKNOWN**; these 43 S6 parent lifts do not close the 1,447-orbit S5 worklist.

### 2026-11-14: cost-73d WIN7 root and independent certificate audit

Class-2 target S5 `00000000000000809082000000000000` のS6 child `00000000000000809082000000004000` からbit 48を加えた7石root `00000000000000809083000000004000` でWIN7-D10が1件得られた。証明書本体は66,680戦略行で、別実装の整数円・直線判定による監査を追加した。

監査結果: 親S6は安全な6石局面で合法手73、bit48は合法。7石rootは安全で相手の合法初手59。59個の8石sub-rootが全てPASSし、到達した勝者局面の和集合は証明書行と完全一致（欠落0・余分0）。終局石数は13〜17。既存の4×4 Bareiss verifierとは異なり、監査用実装は3×3整数方程式で円または直線を判定する。

7石rootから1石を除いたD4正規形は7軌道。公表frontierの3つのmanifest対象hexはこの7軌道のうち3つと一致した。公表再計算はcost-73dを7 covers・6 marginal・3 in-manifestとして反映し、after-cost73dでmanifest内解消S6=920、残S6=6,927、合法七石目コスト=545,068、open class需要=5,196軌道・408,718手、最良class-2候補=11軌道・771手と報告する。今回の独立監査は証明書と7親軌道、3 manifest keyを照合したもので、全worklist frontierの再計算ではない。

この更新はS6 worklistの被覆を増やすが、S5のclass-2 blockerを閉じない。class-2最良候補の残り11軌道、class-4の18軌道は未解決。cost-73aのbit81は証明書未公開であり、この監査に含めない。

標準11×11空盤、二石root `{49,60}`、S2 `{59,60}` は引き続き **UNKNOWN**。

## 2026-11-14: sweep-engine fbt cache saturation audit (session 11)

The canonical sweep engine's 3-stone blocked-mask cache (fbtOR, FBS=1<<17, 48-probe linear walk) silently drops queries when a probe walk finds neither the key nor an empty slot. A behavior-identical instrumented variant (fbtDrops/fbtInserts/fbtMaxProbe counters) re-solved 20 published d10 rows of this target's swept children; all 20 rows reproduced node-exact against the published raw batches.

Findings:

- All 8 audited WIN7 rows (cost-67 bits 18/34/101/118, cost-71 bits 9/70, cost-73a bit81, cost-73d bit48) have fbtDrops=0. No published certificate is affected.
- Saturation is real on 6 heaviest REFUTED rows (drops: cost-73c bit32 834,047; cost-73b bit18 646,356; cost-73c bit120 58,092; cost-74 bit70 16,034; cost-71 bit110 10,298; cost-70 bit112 9,046). Saturation onset sits between 87,159 and 90,616 total cache inserts (66.5%-69.1% of 131,072 slots); fbtMaxProbe hits the 47/48 ceiling exactly on the saturated rows.
- Every saturated verdict survived an FBS=1<<20 drop-free re-solve (fbtDrops=0 required): all remain loss=false (REFUTED-D10). No published verdict, frontier number, or certificate changes. The certificate layer was already drop-guarded (extractor: FBS=1<<20, fbt_drops=0 required per certificate).

Operational rule going forward: sweep candidates expected above ~19M nodes (~90k fbt inserts) run with the drop counter; any saturated verdict is confirmed with the FBS=1<<20 re-solve before reuse as evidence. The canonical runner stays byte-identical for raw comparability.

Artifacts: research/experiments/n11-fbt-saturation-audit-20261114/ (scripts, raw counter data, drop-free re-solves, manifest, README). The cost-73e/cost-74 remote accounting audit (26 raw files + 2 determinism reruns re-fetched and strictly re-parsed at commit 6ebceabb; candidate sets and node totals bit-exact, 0 parse failures) is recorded in research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost73e-cost74-remote-audit-20261114.json.

Provenance: session 10 ran this audit locally but lost the outputs to an environment reset before push; session 11 regenerated everything and all session-10-recorded drop counts and drop-free node counts reproduced bit-exact (determinism confirmation across independent machines). fbtInserts convention documented in the manifest: search-time inserts only, +35 for the C(7,3) root-triple pre-insertions.

Interpretation guard: REFUTED-D10 is not a child refutation. 11x11 empty board, two-stone root {49,60}, S2 {59,60}, class 2, class 4: UNKNOWN.

Follow-up (same session, 2026-11-14): the audit was extended to the whole class2 lane. All 19 published class2-lane sweep records were scanned; every raw row >= 19M nodes and every remaining WIN7 row (17 deduplicated rows) were re-solved instrumented, 17/17 node-exact vs the published raw batches. Three new saturated rows appeared (cost-69c bit110: 13,151 drops; cost-69c bit68: 208,479; cost-70 bit86: 5,703; occupancy 94,547-106,411 = 72%-81%), and all three survived the FBS=1<<20 drop-free re-solve (loss=false). WIN7 coverage is now complete class2-lane-wide: 19/19 WIN7 rows audited, all with fbtDrops=0. Combined: 37 rows audited, 9 saturated, 9/9 confirmed drop-free, 0 verdict flips. Clean heavy rows at 28.8M/24.8M/22.3M nodes with only 71k-85k occupancy confirm that occupancy (fbtInserts), not node count, predicts saturation. Details in the followup section of research/experiments/n11-fbt-saturation-audit-20261114/README.md and the followup fields of runs-manifest.json. 11x11 empty board, two-stone root {49,60}, S2 {59,60}, class 2, class 4: UNKNOWN.

Follow-up 2 (same session, 2026-11-14): the parallel lane's cost-73a sweep record (1 WIN7 bit81 + 72 REFUTED-D10, 0 capped, 383,290,602 nodes; certificate and frontier recompute published by that lane, solved 921) was audited row-wise. The two heaviest REFUTED rows and the WIN7 row reproduced node-exact: bit92 with 1,384 drops at only 87,984 total inserts (67.1%), bit23 with 1,761 drops at 97,145 (74.1%), and bit81 clean (0 drops, 55,402 occupancy). Two findings revise the audit record: the saturation-onset bracket tightens to [87,159 clean; 87,984 saturated] of 131,072 slots, and fbtMaxProbe is not a saturation indicator because dropped 48-step probe walks never update the counter (bit92 saturates with recorded maxProbe=43). The FBS=1<<20 drop-free re-solves of bits 92/23 are confirmed: the parallel lane's crosscheck (class2-lane-cost73a-runner-fbs20-crosscheck-20261114.jsonl, bits 92/23/48/81) reports fbtDrops=0 on every row with verdicts unchanged and node counts bit-exact identical to the canonical rows, so both rows are saturated-but-confirmed-surviving (combined: 11 saturated rows, 11/11 confirmed drop-free, 0 verdict flips), and no published verdict, frontier number, or certificate changes. Distinct class2-lane WIN7 rows audited remain 19/19 with fbtDrops=0 (bit81 now a third independent node-exact reproduction). The instrumented/drop-free variants are v15-derived for raw comparability; under the parallel lane's v16 memo-key repair the memo actually hits, so the v15 occupancy-onset figures must be re-measured before reuse for v16 sweeps. 11x11 empty board, two-stone root {49,60}, S2 {59,60}, class 2, class 4: UNKNOWN.


## 2026-11-14: cost-56a / cost-58b WIN7 certificates and cost-63a partial sweep

The class2 lane added two new seven-stone WIN7 strategy roots, both independently
replayed with a separate BigInt 3x3-minor determinant implementation (no solver
or repository-verifier import, no floating point, and no verdict cache).

- cost-56a root **00000000020000803202020000000000**: 27,817 strategy rows;
  43/43 sub-roots PASS; consumed-row union missing 0 / extra 0. Its seven
  one-stone deletions include three S6 worklist orbits, all three marginal.
  The full frontier recomputation moves to 927 solved-in-manifest, 6,920
  remaining S6 orbits, cost 544,617, and open-class demand 5,190 / 408,340.
  S5 **00000000000000803202000000000000** falls from 41 / 2,776 to 39 / 2,657.
- cost-58b root **00000000000000803202000000042000**: 33,459 strategy rows;
  48/48 sub-roots PASS; consumed-row union missing 0 / extra 0. Its seven
  deletions include four S6 worklist orbits. One is the cost-58 child
  **00000000000000803202000000002000**, explicitly listed under the same S5
  target at 39 / 2,657; this certificate supplies a winning move for that
  child, giving a local 38 / 2,599. The global frontier has not yet been
  recomputed after cost-58b, so the other three parent lifts are not counted
  as marginal and no global totals are changed.
- cost-63a is a separate in-flight class2 sweep on S6
  **00000000000000809102000800000000** (63 legal seventh moves). Independent
  exact geometry reproduces the full 63-bit candidate set. The first raw
  batch covers 8 candidates; bit 2 is one WIN7-D10 search candidate, with
  no certificate yet. The other seven are REFUTED-D10 only. This batch does
  not close an S6 worklist row.

Records: [cost-56a independent certificate audit](../../log/2026-11-14-n11-class2-cost56a-independent-certificate-audit.md),
[cost-58b independent certificate audit](../../log/2026-11-14-n11-class2-cost58b-independent-certificate-audit.md),
[cost-63a batch-1 audit](../../log/2026-11-14-n11-class2-cost63a-batch1-independent-audit.md).
The latest global frontier source is
[after cost-56a](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost56a-recompute-20261114.json).

These are S6 child wins and bounded seven-stone searches only. The S5 parent
blockers, S2 {59,60}, two-stone root {49,60}, and standard 11×11 empty
root remain **UNKNOWN**.


## 2026-11-15: cost69e統合後のfrontierとcost70c

cost69eでは69候補中11件がWIN7-D10、58件がREFUTED-D10、打切り0、探索節点80,172,332だった。bit21・99・87・84・76・90の6証明書を統合し、cost69e統合前の1,012解消から1,019解消へ進んだ。残りは6,828軌道、費用538,143。開いた類が必要とする六石軌道は5,098、費用401,866。

bit21の7石証明書は、BigIntの3×3余因子展開による別実装でも22,261行・45/45部分木を検査し、欠落・余分0、終局石数13〜17を確認した。探索器・判定cache・既存検証器を使わない独立検査である。

cost69eの元の六石子局面 00000000000000803202000000008000 は、cost65g warmのbit15証明書で既に閉じていた。cost69eの6証明書が追加したのは、その親以外への再利用を含む7つのS6軌道である。

cost70cは70候補のraw探索が完了し、WIN7-D10 13件、REFUTED-D10 57件、打切り0、100,935,666節点だった。Bareiss整数行列式による独立再列挙で合法候補70個が完全一致し、13個の7石rootはすべて安全、相手の合法初手数は46〜64だった。40個の既存WIN7証明書manifestに一致するrootはない。bit20だけはcost64bのbit54でもWIN7-D10だったが、証明書はまだない。

ただしcost70cの六石子局面 00000000000000803242000000000000 は、探索中にcost69e bit76証明書の親子再利用で既に閉じた。したがってcost70cのraw sweep自体ではfrontierは増えていない。13候補は他の親S6への再利用候補として保持し、v15交差検査と証明書抽出は未完了のまま扱う。

現在の最良のcoverable class2五石親 00000000000000803202000000000000 は残り6軌道・費用443。次の子は費用71、六石局面 00000000000000803202000000400000。最良class4は18軌道・費用1,460。

cost69e後のtop-candidates CSVに行が出なかった原因は、S5 keyが文字列なのに整数で辞書参照していたことだった。再計算スクリプトを文字列keyに統一し、候補表を再生成した。receipt-unclosableの別S5 00000000000000809082000000000000 は10軌道・費用698で、全て既存sweep済みだが未解消であり、best coverable class2とは別に記録した。

これらは局所S6と7石証明書の進展であり、標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60} の勝敗は引き続き UNKNOWN。


## 2026-11-15: cost-60b warm 17証明書の独立検査とcost-71b frontier

cost-60bのwarm rebuild証明書17件（bits 8,22,26,28,32,40,43,44,74,77,87,88,95,100,106,108,114）を、BigInt 3×3余因子展開による別実装で全件再検査した。17 rootは同一六石親 `00000000000000803202000000200000` の異なる一石追加である。全17件でroot安全性、相手合法初手、全部分木、戦略手の合法性、行の整列・一意性、消費行集合との完全一致、終局石数13〜17が通った。

合計843部分木、488,398戦略行、1,097,295訪問局面、162,754終局。戦略行の不足・余分は0/0。全詳細は監査JSONとlogを参照。これは個別WIN7証明書の独立再検査であり、17件の親被覆を現行frontierへ再計算したものではない。

cost-71bではbits 109/21/105の3証明書がBigInt独立検査済み。bit21はcost-60b warm bit22と同じroot・同一blobであり、二重計上しない。公開済みcost-71b再計算後はS6解消1,026、残り6,821、残り費用537,604、開いた類の必要S6 5,091・費用401,327。最良coverable class2五石親は残り5軌道・費用372となった。

ただし、cost-60b warm17件のうちbit22以外の16件は、このcost-71b frontierにまだ統合されていない。完全なD4親被覆を再計算し、既存receiptとの重複を除いてから追加の解消数を報告する。標準11×11空盤、二石root `{49,60}`、S2 `{59,60}`、class2・class4はいずれも引き続き **UNKNOWN**。

## 2026-11-15: cost69e v2の追加receiptとcost72の途中監査

cost69eの第二warm rebuild（bits 89/94/108/116）を含む10 receipt版の再計算が公開された。merged baseline 1,012から1,023解消へ進み、残り6,824・費用537,833、開いた類の必要S6 5,094・費用401,556。これはcost69e六receipt版ではなく10 receipt版の状態である。

前節に記したcost70c/71b後の1,026解消は、cost69e六receipt版（1,019）を基準にした別の再計算であり、cost69e第二warm batchの4 receiptを含まない。したがって1,023と1,026は別々の枝の集計で、単純加算・比較をしない。両方を重複排除して一つにまとめたfrontier再計算はまだない。

cost72は五石親 `00000000000000803202000000000000` の六石子 `00000000000000803202000000000200`（費用72、需要c1=0,c2=2,c4=0）を対象とする72候補探索。raw batch 1–5を照合し、40候補すべてがclaimのbit列と一致、重複0、候補節点43,875,519、WIN7-D10候補1件（bit52・7,498,054節点）、REFUTED-D10 39件、打切り0。5つのpilot controlは全て3,402節点で一致した。

bit52はまだ探索候補であり、証明書抽出・独立検証前。batch 6–9の32候補も未回収なのでcost72 sweepはin-flight、frontierへの寄与は0として扱う。次は残りbatchを回収し、bit52の交差検査と証明書化の有無を確認する。

標準11×11空盤、二石root `{49,60}`、S2 `{59,60}`、class2・class4はいずれも **UNKNOWN**。

## 2026-11-15: cost72 raw batch 1–9の全件記録確認

cost72の9 raw batchすべてが公開され、72/72候補のbit列はinflight claimの計画と完全一致。重複・欠落・計画外bitは0、候補節点69,563,014、WIN7-D10候補2件（bit52: 7,498,054節点、bit111: 1,872,720節点）、REFUTED-D10 70件、打切り0。pilot control 9件も全て3,402節点で一致した。

ただしinflight claimはまだ `status=in-flight`。v15交差検査、証明書抽出・独立検証、完了記録は未確認。bit52/111は探索候補であり、S6 closure・frontier改善には算入しない。詳細はcost72全件監査logとJSONを参照。

標準11×11空盤、二石root `{49,60}`、S2 `{59,60}`、class2・class4は **UNKNOWN**。

## 2026-11-15: cost72 bit111 receiptでclass2 S5親を残り1子に縮小

cost75b統合後のglobal frontierは1,049解消・残り6,798・費用535,812・open需要5,068/399,535。対象S5親 `00000000000000803202000000000000` は2軌道・費用147で、残りはcost72子 `00000000000000803202000000000200` とcost75子 `00000000000000803202000000004000`。

cost72 raw batch 1–9の72候補はclaimと完全一致。WIN7-D10はbit52/111、REFUTED-D10 70、打切り0、69,563,014節点。bit111証明書はBigInt整数幾何で独立検査し、46,160戦略行・54/54部分木・集合差0/0・終局石数13〜17を確認した。六石親 `...0002` は安全でbit111は合法。bit52は証明書なしのままなのでcost72 sweep全体はin-flightだが、bit111だけをpartial receiptとして記録した。

このreceiptを局所的に適用すると対象S5親は **2軌道・費用147 → 1軌道・費用75**。残るのは `00000000000000803202000000004000` の一子だけ。cost75bの7証明書は既にglobal 1,049へ統合済み。cost72 bit111はglobal frontierに未統合なので、global数値は据え置き、全D4親被覆を照合してから再計算する。

cost72 bit111の7親lift中manifest親は3軌道で、対象の1軌道だけが現行top-candidates表で未解消と確認できた。他2軌道は現在の解消状態を照合しておらず数えない。cost75bの7証明書も再検査し全件PASSを確認したが、既存frontierの計数を変更しない。

cost72 bit52は未証明。標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}` は引き続き **UNKNOWN**。


## 2026-11-15: cost65e bit7証明書と追加2つのS6親解消

7石root `00000000000000809102000000800080` のWIN7証明書を、BigInt 3×3小行列式による別実装で独立検査した。44,561戦略行、相手の合法初手56、56/56 sub-root PASS、行集合差0/0、終局石数13〜17。探索器・勝敗cache・浮動小数点は使っていない。

7通りの1石除去とD4正規化を6分割S6 manifest（7,867行）に照合した結果、manifest親は3軌道だった。除去bit7の親 `00000000000000809102000000800000` はcost65e bit107証明書で既に閉じている。新たに閉じるのは次の2軌道である。

- `00000000000000809102000000000080`（費用79）
- `00000000000000801202000080000008`（費用75）

公開WIN7 manifest 66件、K0675/focus2154/frontier2140の検証済みroot 6,751件、K0675のS6 sweep 3,868件、class2 LOSS7 manifest 3系列、central49 terminal LOSS7 parent-lift 274鍵を照合し、新規2親の既存被覆・WIN/LOSS衝突は見つからなかった。監査は公開receipt/cacheの照合であり、全raw証明書のbyte走査ではない。

cost75b再計算（1,049解消、残り6,798、費用535,812、open需要5,068/399,535）に2親・費用154を反映すると、解消S6は **1,051**、残り **6,796**、費用 **535,658**、open需要 **5,066/399,381**。影響するS5親は3軌道で、35/2,525→34/2,446、59/4,521→58/4,446、74/6,059→72/5,905となる。いずれも未解消のまま。

cost72 bit111の1/75という局所receiptは引き続きglobal frontierに未統合であり、今回の数値には含めない。最良class2 `00000000000000803202000000000000` はcost75b基準で2軌道・費用147のまま。S5 blockerやS2を閉じたわけではない。

詳細: [cost65e bit7監査JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost65e-bit7-independent-audit-20261115.json)、[監査log](../../log/2026-11-15-n11-class2-cost65e-bit7-independent-audit.md)。

標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}` は引き続き **UNKNOWN**。

## 2026-11-15: warm multiband 35証明書のバッチとchain head更新

coordinator計器（rank_warm_candidates_20261115.py、after-cost75b基準のmarginal_in_manifest貪欲順）が、未認証WIN7-D10候補のうち自レーンband（cost-61d/61e/61f/62a/63a/64b/65e/71b）と明示的にdeprioritize済みのcost-72 bit52から正利得35件を選んだ。4並列でrepo-verbatimのblind抽出器（FBS=1<<20、fbt_drops=0、行LC_ALL=C整列・一意化）により35証明書を生成し、BigInt独立検証器で全件再検査した。合計1,586,728戦略行・抽出節点481,639,572。全35 rootについてGitHub code searchで先行証明書の不在を確認（ヒットはsweep/inflight/audit記録とlogのみ）。27件は単一ファイル、8件（>1.75MB）はrepo慣例のpart1of2/part2of2分割で公開し、連結が全体のmd5と一致することを検査した。

並走レーンのcost-75c完了（12 receipt、第二class-2ターゲットS5 `00000000000000803202000000000000` を閉鎖、cost-72 bit111 partial receiptもfold済み）をmainから取り込み、after-cost75c基準 1,062/6,785/534,768/5,055/398,491 をrunpyでbyte-identical再現した上で、35 receiptを公開記録順にfoldした（marginalは拡大和集合から再導出）。新しいchain headは **解消S6 1,109・残り6,738・費用531,295・open需要5,008/395,018**。35 receiptの合計marginalは166、うちmanifest内は47。zero-mim receiptは5件（cost-71b bit14は既foldのcost-75c bit22と同一rootの独立再抽出でWIN7一致の正の重複照合、cost-64b bit102・cost-61e bit102・cost-61f bit102・cost-61d bit119のmanifest親は基準時点で既被覆）。

best coverable class-2五石親 `00000000000000809102000000000000` は残り35軌道・費用2,525から **17軌道・費用1,220** へ半減した。残るbottleneckはaudit-blocked class2 `00000000000000809082000000000000`（10軌道・698、receipt-unclosable）とclass4 `00000000020000003800000080000000`（18軌道・1,460）。

成果物: [warm multiband記録JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-warm-multiband-certificates-20261115.json)、[chain head再計算](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-warm-multiband-recompute-20261115.json)、[抽出・再構築・再計算スクリプト](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_warm_multiband_20261115.py)、[log](../../log/2026-11-15-n11-class2-warm-multiband.md)。

解消計数はmanifest被覆の前進であり、盤全体の勝敗ではない。標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`、class2・class4は引き続き **UNKNOWN**。


## 2026-11-15: warm multiband 35証明書のWIN/LOSS衝突監査

warm multibandの35 WIN7 rootを、同じS2再利用実験の17 verified manifest（既存WIN7 77件・LOSS7 200件）、中央49 terminal LOSS7 parent-lift 274鍵、MS5のcategory-1既知LOSS候補396行へD4正規化で照合した。35 rootは内部で35個の異なるD4軌道を持ち、既存WIN7・LOSS7・central parent-lift・knownloss候補との交差はいずれも0。既存WIN7とLOSS7の間も交差0。証明・親持ち上げ・候補表のLOSS側870 D4軌道は相互に重複しなかった。category-1候補396行は独立LOSS7証明書とは扱わない。

これは公開manifest・候補表に限った衝突監査であり、全raw cacheや非公開worker cacheを走査したものではない。warm証明書本体の戦略検証を置き換えず、S6 frontierや勝敗も変更しない。詳細は監査logと機械可読JSONを参照。

## 2026-11-15: cost-68d sweep完了（7 WIN7-D10）と7証明書、warm band hygiene、chain head 1,117

第三class-2 coverableターゲットS5 `00000000000000809102000000000000` の最安未sweep子 `00000000000000809122000000000000`（cost 68、demand c1=0,c2=2,c4=0）を、独立Bareiss 4x4列挙で68候補（公開edge cost 68とbit-exact）と確認した上でsweepした。**7 WIN7-D10（bits 18/26/29/34/47/103/108）+ 61 REFUTED + 0 capped、計61,325,518 v16 nodes**（10 pilotすべて3,402 nodesでloss=false）。batch番号の誤操作でbatch1の8候補を二重実行したが、重複分は検索結果フィールド全てで行単位完全一致（`ms`のみ相違）し、`class2-lane-cost68d-v16-determinism-rerun-20261115.jsonl` として保存、raw batchは2..9に再番号した。7 WIN7全bitについてv15 cross-engine anchorはloss=true（bit 18: 12,656,791 / 26: 9,249,234 / 29: 5,720,958 / 34: 9,724,149 / 47: 4,112,662 / 103: 4,220,738 / 108: 2,528,832 nodes）、REFUTED anchor bits 0/120/13はloss=false（5,225,527 / 1,124,734 / 16,699,066）。

7 WIN7全rootをrepo-verbatim blind抽出器（空kill table・FBS=1<<20・fbt_drops=0・行LC_ALL=C整列一意化）で証明書化し、BigInt独立検証器で全件PASS、root-absence check 0ヒット、GitHub code searchで先行証明書不在を確認した。計268,572戦略行・抽出82,180,565 nodes（bit 18は2-part分割、joined md5 8aeaf2b687bc033bbbdab2781d91471c。bit 26: 40,031行 / bit 29: 34,356 / bit 34: 49,328 / bit 47: 29,618 / bit 103: 31,183 / bit 108: 27,614行）。push済み全ファイルをremoteでgit blob sha照合した。

あわせてwarm band hygiene 6 receipt（いずれもmarginal_in_manifest 0、帳簿整備のみ）を抽出・検証した: cost-62a bits 1（55,447行）+ 89（32,471行）で **cost-62a band 11/11完了**、cost-63a bits 11（24,243行）+ 109（38,853行）で **63a 8/10**（96/97は並走レーンのclaimed）、cost-71b bit 1（42,499行）で並走remaining list [1,14,32,74,94,117] の先頭を閉鎖（71b 6/9）、cost-61d bit 22は同一rootの独立再抽出で**md5完全一致**（正の重複照合、証明書はcost-71b配下に1回のみpush）。

`recompute_frontier_cost68d_20261115.py`（runpyで1109基準をbyte-identical再現→68d membership/demand再導出→sweep raw再集計→13 receiptを公開順にfold、2回実行でbyte-identical）により、新しいchain headは **解消S6 1,117・残り6,730・費用530,739・open需要5,000/394,462**（旧 1,109/6,738/531,295/5,008/395,018、+8 solvedはすべて68d由来）。第三class-2ターゲットS5は17軌道・1,220 → **13軌道・937**。bottleneck不変: audit-blocked class2 `00000000000000809082000000000000`（10軌道・698）とclass4 `00000000020000003800000080000000`（18軌道・1,460）。並走batch-2証明書は未fold（並走レーンのfoldに委ねる）。

成果物: [sweep記録](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost68d-sweep-20261115.json)、[証明書manifest](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost68d-win7-certificates-20261115.json)、[hygiene manifest](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-warm-band-hygiene-certificates-20261115.json)、[frontier再計算](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost68d-recompute-20261115.json)、[再計算スクリプト](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost68d_20261115.py)、[log](../../log/2026-11-15-n11-class2-lane-cost68d-win7.md)。

解消計数はmanifest被覆の前進であり、盤全体の勝敗ではない。WIN7証明書は個別7石rootの深さ10以内のWINのみを証明する。標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`、class2・class4は引き続き **UNKNOWN**。

## 2026-11-15: multiband2 + cost-68d/hygiene併合再計算、chain head 1,148

1109基準で分岐していた2つの公開fold — 自レーンのcost-68d + hygiene 13 receipt（解消1,117）と並走レーンのwarm multiband 2 31 receipt（解消1,140）— を統合した。receipt集合はpublished duplicate crosscheck（31 batch-2 rootと13 cost-68d/hygiene root、54 entry、byte-exact重複のみ、WIN/LOSS衝突0）で互いに素と確認済みで、batch-2選択は自レーンのhygiene bits（62a 1/89、63a 11/109、61d bit-22=71b bit-1）を明示的にdeferredしており、fold順序で二重被覆は生じない。

`recompute_frontier_merged_after_multiband2_68dhyg_20261115.py`（commit 19bb2abc）は、並走のmultiband2スクリプトをrunpyで1,140 head（1,140/6,707/528,979/4,977/392,702）からbyte-identical再現し、1,140状態でcost-68d子 `00000000000000809122000000000000` のmembershipを文字列keyで再導出（31 batch-2 receiptは同子を被覆していない、需要c1=0,c2=2,c4=0）、9 raw batchからsweep再集計（68候補・7 WIN7-D10 + 61 REFUTED・0 capped・61,325,518 v16 nodes、determinism rerun 8 bit node-exact、v15 anchor照合）、7+6 receiptの全記録を検査（rows・sub-roots・union 0/0・md5・sha256・root==child|1<<bit）した上で、31 batch-2 receiptを既に含む拡大和集合からper-record marginalを再導出しつつ13 receiptを公開順にfoldした。cost-61d bit-22 rootはcost-71b bit-1 rootとbyte-identicalで、重複上のmarginal 0は正の重複照合である。2回実行でbyte-identical、push後のremote git blob shaでbyte-exact確認済み。

merged chain headは **解消S6 1,148・残り6,699・費用528,423・open需要4,969/392,146**（1,140基準から+8、すべて68d由来。13 receipt・marginal 56・manifest内8・zero-marginal 7 receipt）。第三class-2ターゲットS5 `00000000000000809102000000000000` は12軌道・871から **8軌道・588** へ。bottleneck不変: audit-blocked class2 `00000000000000809082000000000000`（10軌道・698、receipt-unclosable）とclass4 `00000000020000003800000080000000`（18軌道・1,460）。

並走cost-69f sweep（子 `00000000000000809102000000000008`、69候補）は完了監査済み（9 WIN7-D10・60 REFUTED・0 capped・112,752,229 nodes）だが証明書未抽出のため未fold。残る最安未sweep子は `00000000000000809102000000002000`（cost 69、需要c1=0,c2=2,c4=2）。six gain-1 cost-70c warm candidatesはこのmerged headに対して非零marginalを持ちうるが、並走bandに属するためここではfoldしない。

成果物: [merged再計算JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-merged-recompute-after-multiband2-68dhyg-20261115.json)、[ranking CSV](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-s5-ranking-after-merged-multiband2-68dhyg-20261115.csv)、[top-candidates CSV](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-merged-multiband2-68dhyg-20261115.csv)、[再計算スクリプト](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_merged_after_multiband2_68dhyg_20261115.py)、[log](../../log/2026-11-15-n11-class2-merged-recompute-multiband2-68dhyg.md)。

解消計数はmanifest被覆の前進であり、盤全体の勝敗ではない。標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`、class2・class4は引き続き **UNKNOWN**。

## 2026-11-15: class2-lane 50-receipt和解監査とcost-70c warm 6証明書、解消予測1,154 = 1,148 + 6

自レーンbatch-2 warm抽出のうち並走multiband2選択からdeferredだった **cost-70c gain-1証明書6件（bits 105/92/40/24/11/8、child `00000000000000803242000000000000`）** をblind抽出・BigInt独立検証（33,992〜52,755行、全部分木PASS、行集合差0/0、終局石数13..17）し、remote公開とサイズ照合まで完了した（md5・バイト数はaudit JSONに記録）。先行3証明書（94/20/23）と合わせ **cost-70cは13 WIN7中9件認証済み**、残りはbits 3/42/86/103（warm再構築候補）。

両batch-2レーンの独立抽出は29 rootで一致（両側byte検証、multiband2記録は first_pushed_by 自レーン18/並走13 と記録）— 正の重複照合であり衝突ではない。自レーン固有の追加は上記6件、並走固有はcost-64b bit-40とcost-61d bit-23。

**50-receipt和解監査**（[audit JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-unified-fold-reconciliation-20261115.json)、[log](../../log/2026-11-15-n11-class2-lane-unified-fold-reconciliation.md)）: 全50 receipt（68d 7 + hygiene 6 + multiband2 31 + 70c 6）の root == child | 1<<bit のBigInt検査・3-way root disjointnessが全て通過。各receiptのmarginal in-manifest hex和集合 A(8)/B(31)/C(6) は相互に非交差で、合計45。1109 + 45 = **解消予測1,154**。

同一セッション内の訂正: audit初版は1117/1140を未統合の分岐headとして記述したが、**併合再計算head 1,148（commit 19bb2abc）は既にmainに存在していた**（push前collision checkのフィルタが unified/reconcil のみで merged/recompute を見落とした）。併合foldは本監査の算術を独立に確認している: cost-68dの8 hexは1109状態と1140状態でset-identical（batch-2の31 hexと非交差であることの実証）、かつ本監査はcost-70cの6 hexが併合39 hex全てと非交差であることを再検証した。よって予測は変更なく **1,154 = 1,148 + 6** となり、未foldはcost-70cの6件のみ。次回実行のfold仕様（audit JSON記載）: `recompute_frontier_merged_after_multiband2_68dhyg_20261115.py` を拡張し1,148 endpointをbyte-identical再現→6件を貪欲順 105, 92, 40, 24, 11, 8 でfold→set-equalityと解消1,154をassert。collision checkは merged/recompute フィルタを含める運用に修正した。

環境事実: 本セッションは実行環境（bash/filesystem）が終始利用不能で、全計算をsandbox + GitHubコネクタで実施した。解消計数はmanifest被覆であり盤全体の勝敗ではない。標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`、class2・class4は引き続き **UNKNOWN**。


## 2026-11-15: unified merge fold完了 — 全50 receipt統合、chain head 1,154

和解監査のfold仕様（訂正版: merged head 1,148は44/50 receipt fold済み、予測1,154 = 1,148 + 6）に従い、`recompute_frontier_unified_merge_20261115.py`（commit 7aaa7d83）で全50 receiptの権威あるunified foldを実行した。runpyチェーンで1,109基準・1,117 endpoint・1,140 endpointをbyte-identical再現（両レーンの1,109基準集合が同一であることをassert）、6 cost-70c warm batch-2 receiptをroot恒等式・md5・rows・貪欲順 105/92/40/24/11/8 で検査、3-way root disjointness（12+31+6 root、71b bit-1 == 61d bit-22 の同一rootを含む）、各グループのmarginal-in-manifest和集合をcoversから独立再導出して公開hex list（8/31/6、union 45、pairwise空）と照合した。

foldは1,109基準から13 receipt（公開順）→ 31 multiband2 receipt（公開順）→ 6 cost-70c receipt（貪欲順）の順で、per-record marginalをすべて拡大和集合から再導出。set-equality制御: 13 receipt後 == s_1117、44 receipt後 == s_1117 ∪ s_1140（公開merged head 1,148/6,699/528,423/4,969/392,146 と一致）、50 receipt後 == s_1117 ∪ s_1140 ∪ covers(6 cost-70c)。**解消1,154をassertで確認**し、和解監査の集合和予測をfold算術に対して確定させた。2回実行でbyte-identical、push後のremote git blob shaで全4ファイルbyte-exact確認済み。

unified chain headは **解消S6 1,154・残り6,693・費用527,949・open需要4,963/391,672**（残りS5軌道175）。50 receipt・marginal 239（56+154+29）・manifest内45（8+31+6、和解監査のunionと厳密一致）・zero-marginal 7 receipt（68d bit 26 + hygiene 6）。fold戦略行合計 1,958,038。1,109基準の3分岐はmain上で完全和解した。

ランキング: 最良class-2 S5 `00000000000000809102000000000000` は **8軌道・588不変**（cost-70c receiptは同S5の行に触れない）。残る最安未sweep子は `00000000000000809102000000002000`（cost 69、需要c1=0,c2=2,c4=2）、もう一方のcost-69子（cost-69f）は並走レーンでsweep完了・証明書未抽出のため未fold。bottleneck不変: audit-blocked class2 `00000000000000809082000000000000`（10/698）とclass4 `00000000020000003800000080000000`（18/1,460）。cost-70c bandは13 WIN7中9認証・6 fold済み、残りbits 3/42/86/103。

成果物: [unified merge再計算JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-unified-merge-recompute-20261115.json)、[ranking CSV](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-s5-ranking-after-unified-merge-20261115.csv)、[top-candidates CSV](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-unified-merge-20261115.csv)、[再計算スクリプト](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_unified_merge_20261115.py)、[log](../../log/2026-11-15-n11-class2-unified-merge-50-receipts.md)。

解消計数はmanifest被覆の前進であり、盤全体の勝敗ではない。WIN7証明書は個別7石rootの深さ10以内のWINのみを証明する。標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`、class2・class4は引き続き **UNKNOWN**。


## 2026-11-15: unified mergeの二重独立実行・同一endpoint確認とcollision記録、cost-70c warm6独立検証、cost-69f raw再集計

**同時実行の記録**: 和解監査のfold仕様（訂正版）を2つの並走レーンがほぼ同時に独立実行した — 7aaa7d83（20:47:56Z、log [2026-11-15-n11-class2-unified-merge-50-receipts.md](../../log/2026-11-15-n11-class2-unified-merge-50-receipts.md)）と625b0e0c（20:51:40Z、log [2026-11-15-n11-class2-unified-merge-recompute-1154.md](../../log/2026-11-15-n11-class2-unified-merge-recompute-1154.md)）。両実装は同一の公開順fold（13 68d/hygiene → 31 multiband2 → 6 cost-70c、貪欲順 105/92/40/24/11/8）、同一のset-equality制御、同一endpoint **1,154/6,693/527,949/4,963/391,672**（残りS5軌道175）に到達し、いずれも2回実行byte-identical。2実装の一致はfold算術に対する正の交叉検証である。

**collisionの簿記**: 625b0e0cは同一パスの4ファイル（スクリプト・frontier JSON・ranking CSV・top-candidates CSV）を上書きした（push前のcollision確認listが7aaa7d83より古かった）。現行mainのライブファイルは625b0e0c版で、7aaa7d83版に加えて (a) 公開merged 1,148 head（1148/6699/528423/4969/392146）のbyte-identical再現（再生成JSONのmd5をmain値と照合）と `s_1148 == s_1117 | s_1140` のunion恒等式、(b) 31 multiband2 receiptを1,117上にfoldして1,148状態を独立再導出し集合一致をassert、(c) 6 cost-70c warm証明書の独立BigInt検証記録 [class2-lane-cost70c-warm6-bigint-independent-verification-20261115.json](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost70c-warm6-bigint-independent-verification-20261115.json)（rows 33,992〜47,165、全sub-root PASS、union 0/0、終局13..17、md5/sha256/git blob sha込み。先行manifest証明書94/20/23はmarginal-0の正の重複照合）を含む。7aaa7d83側の成果物記載はlog・K0783前節に残る。**教訓: push直前に目標パスのlistを取り直すこと（分単位で並走が動く）**。

**cost-69f raw sweep独立再集計**: 並走公開のraw batch 1–9を独立再集計しsweep-audit記録と完全一致 — 69候補、9 pilot（3,402 nodes）、WIN7-D10 9件（bits 2/20/44/68/69/94/109/118/119）、REFUTED 60、capped 0、候補節点112,752,229。child `00000000000000809102000000000008`（cost 69）は第三class-2ターゲットS5 `00000000000000809102000000000000` の最安の子（もう一方のcost-69子 `00000000000000809102000000002000` が現時点の最安未sweep子）。69f証明書は公開が始まったばかり（本セッション終了時点でbit20の1件/9件）で、全件公開後の次のunified mergeでfoldする。

**batch-2 lane-takeover crosscheck log**を出版（[2026-11-15-n11-class2-warm-multiband2-lane-takeover-crosscheck.md](../../log/2026-11-15-n11-class2-warm-multiband2-lane-takeover-crosscheck.md)）: 31証明書出版（自レーン18/並走13）、54/54 remote byte-exact、WIN/LOSS衝突0、chain break（cost65e in-place拡張、bit-107のみfold・bit-7既知重複）の独立発見・修理、frontier 1,109→1,140。

解消計数はmanifest被覆の前進であり、盤全体の勝敗ではない。標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`、class2・class4は引き続き **UNKNOWN**。

## 2026-11-15: unified merge 1154 endpointの第三の独立検証（solved set不要の帳簿法）とcost-70c warm6 marginalの親・需要構造

unified merge chain head 1,154（7aaa7d83 + 625b0e0c の二重独立実行済み）に対し、本レーンは**第三の手法**による独立検証を完了した。従来の2実装はrunpyでsolved setを再構成してfoldを再実行するが、本検証はsolved setの再構成を一切行わない帳簿法である。入力は (a) 6分割S6 manifest 7,867行、(b) merged-1148 ranking CSVの175 open S5（per-S5残数・残費用）、(c) merged-1148 top-candidates CSV（77行の子+cost+需要文字列）、(d) 和解監査の6 marginal hex のみ。175 S5×121手の子incidenceをBigInt D4正規化（8変換、bit index 11*b+a、計21,175回のcanon）で再生成した。鍵定理: 6 C hexはmerged-1148時点で未解決ゆえ h ∈ rem(X) ⟺ h ∈ children(X) が成り立ち、closing S5の残り子は全てCに含まれるため非C軌道の需要は不変、C hexのfold効果はper-S5帳簿差分で厳密に計算できる。

制御は全て通過: manifest 7,867行は検証器実装のD4 canonで全行不変・重複0、175 S5も全行canon不変、top-candidates 77行（4対象S5: 18+10+8+41行）の子hex・manifest cost・需要文字列c1/c2/c4が再生成結果と完全一致、|children(X)|>=rem(X)は175/175、closing⟺cost差分0の整合は175/175、再生child edges 14,896。

**endpoint検証結果**: 解消1,154・残りS5 175・unique 6,693・費用527,949・open需要4,963/391,672の6数値が権威unified merge JSON（625b0e0c版）と完全一致。需要ヒストグラム9バケットも完全一致（c2=2,c4=0が1,040→1,034、他不変、総和4,963）。best/next class2・class4候補ランキングも一致（best coverable 8/588・audit-blocked 10/698・best class4 18/1,460不変）。runpy fold再現とは別手法による正の交叉検証である。

**marginal 6 hexの親・需要構造**（新規の厳密な成果）: 全6 hexがmanifest所属・cost 76/80/75/80/78/85（和474）・需要すべて **c1=0,c2=2,c4=0**（open_only、バケットc2=2,c4=0）。各hexはちょうど2個のclass-2 S5に共有され、親は7個: S5 `00000000000000801242000000000000` が**全6 hexの共通親**（rem 70→64、cost 5,517→5,043、−474）。他6親は各1個減: `00000000000003800000008000002` 51→50・3,837→3,759（bit11）、`00000000000083800000008000000` 57→56・4,257→4,181（bit105）、`00000000000003800000009000000` 63→62・4,778→4,698（bit24）、`00000000000000801202010000000000` 65→64・4,708→4,633（bit40）、`00000000000000403800000080000000` 69→68・5,590→5,510（bit92）、`00000000000000801202000000000100` 71→70・5,796→5,711（bit8）。**closersなし**（remaining_s5は175のまま）、best/next候補の行は全て不変。

限界: 証明書本体の再実行ではなく公開receiptの帳簿検証であり、6 marginal hexは和解監査（BigInt独立検証済み）から引用した。需要構造はmerged-1148公開per-S5集計から導出するため、ranking CSVとfoldの両方に同種の誤りがあれば検出できない。帳簿法はsolved setを要求しないため、今後のfold予測・endpoint検証にも再利用可能。

なお、push時点で並走レーンが cost-70c warm batch-3完了（残りbits 3/42/86/103の4証明書・claim closure・gain-0予測 6751e21e）と cost-69f証明書5/9（bits 20/44/68/69/118）を公開済みであることを確認した。次回unified merge foldの材料である。解消計数はmanifest被覆の前進であり、盤全体の勝敗ではない。標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`、class2・class4は引き続き **UNKNOWN**。

成果物: [検証記録JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-unified-merge-endpoint-third-verification-20261115.json)、[log](../../log/2026-11-15-n11-class2-unified-merge-third-independent-verification.md)。

## 2026-11-15: cost-69f証明書5件公開・bit-20 truncated repush・9 receipt fold — chain head 1,163

自レーン（cost-69f sweep実行lane）が証明書5件（bits 20/44/68/69/118）を公開し、9 WIN7 receipt（bits 2/20/44/68/69/94/109/118/119）をunified merge 1,154の上にfoldした（[log](../../log/2026-11-15-n11-class2-lane-cost69f-certificates-and-receipts-fold.md)）。

**bit-20 truncated pushの修復**: 初回push（e36a6b3a）は64KB-capped reader経由で1,770行/63,965バイトのまま着地していた。全1,741,046バイト（48,171行）を再pushし、remote git blob sha `8111cff29c3f0d3d2ef66e9e64e64a8b0968c453` をlocal計算と照合した。事故は[証明書記録JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost69f-win7-certificates-20261115.json)の `incident_bit20_truncated_push` に記録した（原因・初回着地サイズ・repush確認）。

**証明書5件**: repo-verbatim抽出器・blind kill table・FBS 1<<20・全loser初手展開・LC_ALL=C行sortで、rows 35,501〜52,480・抽出節点11,305,750〜17,969,541・fbt_drops 0。BigInt独立検証を再実行し全PASS（sub-roots 56/55/58/51/54 = loser mobility = `legal_candidates.py` 独立列挙、union 0/0、terminal 13..17、行sorted-unique）。v15 anchorは9 WIN7全件 loss=true・節点数照合（bit-20は8,760,558等）、REFUTED anchor 99/112はloss=false。md5/sha256/bytes/git blob shaを記録JSONに残し、remote blob sha照合済み。残り4件（bits 2/94/109/119）は抽出未了。

**9 receipt fold**（`recompute_frontier_cost69f_receipts_20261115.py`）: baseline unified 1,154をrunpyチェーンでbyte-identical再現（head JSON blob sha `a0789eed…` 照合）、child `00000000000000809102000000000008` がbaselineで本当に残存することをassert、sweep-auditを9 raw batchから独立再導出（節点和112,752,229・batch blob sha・root恒等式）、v15/v16制御をJSONLからassert、証明書5件をbytes×md5×sha256×blob shaで検査の上、公開bit順でfold。**+9 manifest軌道**（bit 2がchild軌道+交差軌道`…80120200000000180`の2件、bit 20はmarginal-0の正の重複照合、他7件が各1件の交差軌道）。最初のreceiptがchild軌道を閉鎖したことをassertした。

**chain headは解消S6 1,163・unique残り6,684・費用527,280・open需要4,954/391,003**（残りS5軌道175、`c2=2,c4=0`は1,034→1,025）。親S5 `00000000000000809102000000000000` は7軌道・519不変。2回実行byte-identical、4ファイルのremote blob sha照合済み（初回pushの末尾余分改行1バイトを検出しbyte-exact repush）。

未fold material: cost-70c warm batch-3証明書4件（bits 3/42/86/103）、cost-65j sweep（in flight・bit-113交叉被覆の再検査必要）、69f残り4証明書。最安未sweep子は `00000000000000809102000000002000`（cost 69、c1=0,c2=2,c4=2）。

解消計数はmanifest被覆の前進であり、盤全体の勝敗ではない。WIN7証明書は個別7石rootの深さ10以内のWINのみを証明する。標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`、class2・class4は引き続き **UNKNOWN**。

成果物: [frontier JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost69f-receipts-recompute-20261115.json)、[ranking CSV](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-s5-ranking-after-cost69f-receipts-20261115.csv)、[top-candidates CSV](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost69f-receipts-20261115.csv)、[foldスクリプト](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost69f_receipts_20261115.py)、[証明書記録JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost69f-win7-certificates-20261115.json)。

## 2026-11-15: cost-70c warm batch-3証明書4件公開・band 13/13完了・gain-0 fold — chain head 1,163不変

自レーン（cost-70c warm lane）がbatch-3残り4証明書（bits 3/42/86/103）を公開してcost-70c band 13/13認証を完了し、69f recompute（30c638d5）が「次のrecomputeでfold」と明示的に委任した4 receiptのfoldを `recompute_frontier_after70cwarm3_20261115.py`（6d4ced10）で実行した（[log](../../log/2026-11-15-n11-class2-cost70c-warm-batch3-fold.md)）。

**証明書4件**: blind抽出 `warm_rebuild_pipeline2_20261115.py`（raw→行抽出、repo検証器・solver・cache不使用）、BigInt独立検証全PASS（root恒等式 child|1<<bit、sub-roots == loser mobility、union 0/0、terminal 13..17、md5/sha256/bytes）。rows 50,955/50,015/68,358/45,205、抽出節点 11,537,642/11,335,391/27,716,890/11,012,568（計61,602,491）。bit-103は別プロセス決定性再実行で節点数・md5完全一致。証明書7ファイル（bits 3/42/86は2分割push、bit 103は単一1.63MB）は全てremote git blob sha照合済み、claim `class2-lane-cost70c-warm-batch3-inflight-20261115.json` はclosure（267762ab）。

**環境事実**: foldスクリプトの初版は69f chainとunified merge chainを同一プロセスでrunpy二重再現し、実行環境の~1GB memory capでSIGKILLされた（exit 137、cost-61d制御の途中で停止）。教訓: **1プロセスにつきfull runpy chain 1本まで**。公開版は69f chain内部のunified再現（head JSON blob sha `a0789eed…` 照合込み）を `nsF['nsU']` 経由で再利用し、root-disjointness制御を保ったまま単一チェーンで完了した。

**gain-0 foldの制御**: 4 rootは49 distinct unified receipt root（12+31+6）および9 cost-69f receipt rootと互いに素。foldは公開record順（bits 3/42/86/103）、per-record marginalは拡大和集合から再導出、set-equality `s == s_1163 ∪ covers(4)` をassert。結果: covers各7、marginal **0/4/4/0**（bits 3/103は既存receiptで被覆済み、bits 42/86は非manifest軌道のみ）、**marginal-in-manifest全bit 0**（総marginal 8）。headは**不変 1,163/6,684/527,280/4,954/391,003**（残りS5軌道175）。2回実行byte-identical、push 4ファイルのremote blob sha照合済み。

**三重独立一致**: (a) 並走予測 `class2-lane-next-fold-marginal-prediction-20261115.json`（baseline 1154でper-bit marginal 0/4/4/0・mim 0）、(b) 並走の第三方法独立監査 `class2-lane-next-fold-prediction-independent-audit-20261115.json`（c10e6e9f。独立D4正規化+1石削除lift再導出、bits 42/86の非manifest lift数が厳密に4、13/13 root identity+safety、repo実装不使用）、(c) 本fold recompute（baseline 1163）。per-bit marginal値まで3導出が完全一致した。

未fold material: cost-75c 12 receipt（並走。なお並走のcost-75c recomputeは別系列のcost-75b baselineで解消1,062であり、canonical 1,163 chainへのfoldは今後のrecompute）、cost-65j sweep（in flight・bit-113交叉被覆の再検査必要）、69f残り4証明書（bits 2/94/109/119、並走がraw sweep receipt+v15 anchorとしてfold済み・抽出は並走レーン担当）。最安未sweep子は `00000000000000809102000000002000`（cost 69、c1=0,c2=2,c4=2）。

解消計数はmanifest被覆の前進であり、盤全体の勝敗ではない。WIN7証明書は個別7石rootの深さ10以内のWINのみを証明する。標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`、class2・class4は引き続き **UNKNOWN**。

成果物: [fold再計算JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-after-cost70c-warm3-recompute-20261115.json)、[ranking CSV](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-s5-ranking-after-cost70c-warm3-20261115.csv)、[top-candidates CSV](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost70c-warm3-20261115.csv)、[foldスクリプト](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_after70cwarm3_20261115.py)、[batch-3 records JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost70c-warm-batch3-records-20261115.json)、[log](../../log/2026-11-15-n11-class2-cost70c-warm-batch3-fold.md)。

## 2026-11-15: cost-69f残り4証明書の公開 — band 9/9全証明書化、chain head不変

自レーンがcost-69f残り4 WIN7証明書（bits 2/94/109/119）を抽出・BigInt独立検証・公開し、**cost-69f sweepの9 WIN7-D10全件にrepo形式の独立検証済み証明書が揃った**（[log](../../log/2026-11-15-n11-class2-lane-cost69f-remaining-certificates.md)）。

- rows 53,449〜71,485・抽出節点20,795,895〜23,677,579・fbt_drops 0全件。BigInt独立検証4件全PASS（sub-roots 58/56/60/61 = loser mobility = `legal_candidates.py` 独立列挙と一致、union 0/0、terminal 13..17、行sorted-unique）。v15 anchorは4件ともloss=true・節点数照合（16,285,738 / 15,200,842 / 13,955,169 / 13,661,829）。
- 4件とも1.75MB超のためrepo慣例の2分割（行境界分割・連結md5==全体md5検証済み）とし、8 partを1コミット1 part・"(N/8)"形式で公開した。push直前のtarget dir listingで `^bit(2|94|109|119)-` 衝突0を確認した際、**前段のbit2 part1of2 push試行は着地していなかった**（dirに5ファイルのみ）ことが判明したため、(1/8)から全8件をpushし直した。push後、8 part全件のremote git blob shaをdir listingと `blob <size>\0`+内容sha1 のlocal計算で照合し **8/8一致** を確認した（target dirは13ファイル）。
- 記録JSONは5件版（並走の独立監査が参照中のため上書きせず）とは別の新規ファイル [class2-lane-cost69f-win7-certificates-2-20261115.json](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost69f-win7-certificates-2-20261115.json) に統合し、`uncertified_bits_after: []` としてsweepの被覆状況を確定させた。
- 4 rootのreceiptは既にraw sweep + v15 anchorとして9 receipt fold（chain head 1,163）に含まれているため、frontier計数は不変（解消S6 1,163・残り6,684・費用527,280・open需要4,954/391,003・残りS5軌道175）。本公開は9 receiptの証明provenanceを証明書で補完するもので、新たな軌道解消を加えない。

解消計数はmanifest被覆の前進であり、盤全体の勝敗ではない。WIN7証明書は個別7石rootの深さ10以内のWINのみを証明する。標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`、class2・class4は引き続き **UNKNOWN**。


## 2026-11-15: cost69fの4証明書を第二系統で再検査

先行レーンが公開したbits 2/94/109/119の分割証明書をGit blobから再取得し、別のV8実行でゲーム木検査を再実施した。探索器、判定cache、探索結果は使っていない。さらに、根の合法手数は4×4整数行列式の置換展開で別に列挙し、BigInt 3×3余因子展開の検査と照合した。

| bit | 証明書行 | 根の合法手 | 訪問局面 | 終局局面 | v15 anchor節点 |
|---:|---:|---:|---:|---:|---:|
| 2 | 69,879 | 58 | 142,740 | 22,921 | 16,285,738 |
| 94 | 53,449 | 56 | 120,250 | 20,161 | 15,200,842 |
| 109 | 71,485 | 60 | 153,920 | 26,397 | 13,955,169 |
| 119 | 67,423 | 61 | 143,363 | 23,779 | 13,661,829 |
| **計** | **262,236** | **235** | **560,273** | **93,258** | **59,103,578** |

4件すべてPASS。7石rootの安全性、全sub-root、strategy行の整列・一意性、union missing/extra=0/0、終局石数13〜17を確認した。根合法手数58/56/60/61は、別方式の4×4行列式でも一致した。連結後のMD5・SHA256・byte数、8個のpartのGit blob SHA1・行数・個別MD5も公開記録と一致。D4で再導出した親軌道集合も、frontier foldの新規被覆一覧と矛盾しない。

これにより、cost69fの9 WIN7-D10 receiptが増やしたS6 manifest軌道は、全9軌道とも証明書で裏付けられた。元のreceipt foldは変更せず、9件すべてを証明書済みとする派生frontierを別ファイルに保存した。

- 解消済みS6 manifest軌道: **1,163**（baseline 1,154からの+9は全て証明書済み）
- 残りS6軌道: 6,684
- 残り七石目費用: 527,280
- open class需要: 4,954軌道 / 391,003費用
- 残りS5軌道: 175
- 最良class2 S5 00000000000000809102000000000000: **7軌道 / 519費用**

bit2証明書により、S6 child 00000000000000809102000000000008 は証明書レベルで閉じた。ただし親S5には7軌道残っているため、S5自体は未解決。1,163は証明済みS6被覆数であって、11×11全体の勝敗や距離ではない。

cost65j bit113の7石rootはcost69f bit2と同じS6親軌道を1件共有するが、S7のD4軌道は別。bit2が証明済みになったため、将来bit113が証明書化されても共通親を二重計上しない。cost69gの次候補は別レーンがclaim済みなので探索を重ねていない。cost65j childも最新claimではcanonical headで既被覆とされており、再開時に最新frontierで再判定する。

再現用の検査スクリプト、第二監査JSON、証明書済みfrontierは以下に保存した。

- [第二独立検証JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/cost69f-second-independent-verification-20261115.json)
- [証明書済みfrontier](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost69f-certificate-backed-recompute-20261115.json)
- [再現スクリプト](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost69f_second_independent_verification_20261115.mjs)
- [監査ログ](../../log/2026-11-15-n11-class2-cost69f-second-independent-verification.md)

標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class2・class4は引き続き **UNKNOWN**。


## 2026-11-15: cost69f全9証明書のPython第三完全独立監査とcost69g需要不整合の解消

第二独立検証（別V8実行・BigInt 3x3余因子・未検証だった4証明書）に対し、本レーンは**言語も幾何実装も異なる第三の実装（Python、多倍長整数Bareiss 4x4行列式、浮動小数点なし）で、最初に公開された5証明書を含む全9件**を完全独立監査した。repoの検証器・engine・verdict cache・solverは一切importせず、禁止手（三石共円トリプル）マスクも盤面定義から再計算した。敵の全合法手を各局面で展開する完全な戦略リプレイを行い、sub-root分解・消費行union（0/0）・終局石数13〜17・records全フィールド照合（winner/loser states・loser reply edges・visited・terminal count・fbt_drops 0・v15 anchorのloss=trueと節点数）を確認した。

**9/9 PASS。** 合計495,585戦略行・509 sub-root・訪問1,073,872局面・終局180,983。保存照合（単一5件・2-part 4件のbytes/md5/sha256/git blob sha・行境界分割・連結ハッシュのrecords一致）も全件通過。第二検証と共通するbits 2/94/109/119の4件は全フィールドで一致した。これでcost69fは「元のBigInt検証器 → 第二独立（V8, 4件）→ 第三独立（Python/Bareiss, 9件）」の三重検証体制となった。

あわせて、第三方法監査が指摘したcost69g子の需要不整合（distinct open parents=3 vs chain需要c1=0,c2=2,c4=2の和4）を**両側とも誤りなし**と和解した。chainのclasses列はbitmask（bit0=class1, bit1=class2, bit2=class4）で、per-child需要は各open親S5をclass bitごとに数える。open親3軌道のうち00000000000000801202000000080000がclasses=6の二重役用S5でc2とc4の両方に+1するため和が4になる。claims/auditsは両方の数を併記すべき旨を再発防止として記録した。副産物として、audit-blocked S5 00000000000000809082000000000000（classes=3）の子は全てc1>=1となりopen_classes帳簿から外れることが、receipt-unclosableの構造的理由と確定した。コントロール（72子・69f子・65j子）でも幾何再導出によるper-class需要がchain公開値と全件一致。

frontier計数は不変（解消S6 1,163・残り6,684・費用527,280・open需要4,954/391,003・残りS5軌道175）。本作業は証拠確度の向上と帳簿意味論の確定であり、新規軌道解消ではない。

成果物: [Python第三監査スクリプト](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost69f_win7_certs_20261115.py)、[監査JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost69f-9cert-python-independent-audit-20261115.json)、[和解スクリプト](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/reconcile_cost69g_demand_20261115.py)、[和解JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost69g-demand-reconciliation-20261115.json)、[log](../../log/2026-11-15-n11-class2-lane-cost69f-python-independent-audit-and-69g-demand-reconciliation.md)。

標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class2・class4は引き続き **UNKNOWN**。

## 2026-11-15: cost-72b子sweep完了（13 WIN7-D10探索候補・証明書未抽出）

第三class-2 coverableターゲットS5 `00000000000000809102000000000000` の未sweep子 `00000000000000809102000002000000`（cost 72、需要c1=0,c2=2,c4=0、open親2軌道）をclaimしてsweepした。claimは `class2-lane-cost72b-inflight-20261115.json`（main 50d2773c時点で未claimを確認済み）。独立Bareiss 4x4列挙で72候補がmanifest edge cost 72とbit-exact一致し、**WIN7-D10 13件（bits 2,11,21,30,31,36,47,66,85,95,97,100,106）・REFUTED-D10 59件・打切り0、候補節点117,444,772**（repo-verbatim v16 engine、pilot d6制御3,402 nodesは10/10 batch PASS、終局石数 [13,17]）。batch構成はbit分割ミスで10 batch（7+8×8+1）になったが、72候補は重複・欠落なく1回ずつ実行済み（sweep recordのbatch_noteに正直に記録）。

交叉検査は全て通過: v15 cross-engine（別実装engine）で13 WIN bits全件 loss=true（計132,170,428節点）、REFUTEDアンカー bits 0/9/120 は loss=false、別プロセス決定性再実行13/13 node-exact、13 rootは13個すべて異なるD4軌道、GitHub code searchで13 root hexの先行公開0ヒット。

13 WIN7-D10は**探索候補**であり証明書ではない。S6 frontierへの寄与は現時点で0で、証明書抽出（repo-verbatim blind抽出器・FBS 1<<20・fbt_drops 0・行LC_ALL=C整列一意化）とfoldが次の必要作業。 2026-11-15 cost72bの13 WIN7-D10全rootにrepo形式戦略証明書を抽出・独立検証・公開した。636,225戦略行・729 sub-root・抽出節点200,029,509・fbt_drops全件0・verify_bit7_win7_cert.tsで13/13 PASS（union missing/extra 0/0、終局石数13..17、敵初手数は独立Bareiss列挙と全件一致）。19 remoteファイルのgit blob sha照合19/19。chain head 1,163へのfoldは未実施。REFUTED-D10は「深さ10以内の先手勝ち不存在」であって子の反証ではない。cost-74d（並走レーンがclaim・実行中）、cost-69g・cost-65j（いずれもin flight）は本項に含めない。

成果物: [sweep記録](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost72b-sweep-20261115.json)、[claim](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost72b-inflight-20261115.json)、[log](../../log/2026-11-15-n11-class2-lane-cost72b-sweep.md)。raw batch 1–10・v15 crosscheck 4件・determinism rerunは同output/の `class2-lane-cost72b-*`。

標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class2・class4は引き続き **UNKNOWN**。

## 2026-11-15: cost-72bの13 WIN7-D10全証明書化と公開

前節の13 WIN7-D10探索候補すべてに、repo-verbatim `class4_child1_cert_extractor_exact.ts`（FBS 1<<20・fbtDrops計数・飽和時はrowsを書き出さない自己防護付き）で戦略証明書を抽出した。敵初手は `legal_candidates.py`（独立Bareiss 4x4）による全合法手で、1 bit = 1プロセス。**13/13抽出成功・fbt_drops 0・全敵初手ok・終局石数 [13,17]**。kill tableはrepo CLI既定のKILL_BIT7 pref hints（一致する敵初手の探索順にのみ影響。verdict cache不使用。正しさは抽出の自己検査と独立検証で担保）。

汎用独立検証器 `verify_bit7_win7_cert.ts`（整数Bareiss 4x4・engine不使用・cache不使用）で**13/13 PASS**: root安全性、全sub-root（=敵初手全展開、計729）の完全戦略リプレイ、消費行union = 証明書行集合（missing 0 / extra 0 全件）、行sorted-unique、終局石数13〜17。合計 **636,225戦略行・訪問1,378,650局面（winner 889,294 + loser 264,554 + terminal 224,802・全bitで整合）・敵応答edge 1,241,817・抽出節点200,029,509**。

公開は13証明書のうち6件（bits 2/21/66/95/100/106）をrepo慣例の2分割、7件を単一ファイルとし、**19 partを1コミット1 part (1/19)..(19/19) でpush、remote git blob sha照合19/19 byte-exact**。sandbox memory limitが5件のpushプログラムをpush_files実行後にabortしたが、いずれも着地済みでremote照合で問題なし（manifestのincident_noteに記録）。claim `class2-lane-cost72b-inflight-20261115.json` は status=certificates-published-fold-pending に更新。

**S6 frontierへの寄与は当時まだ0**: 子軌道 `00000000000000809102000002000000` の被覆と交差軌道liftのfold（執筆時点ではchain head 1,163基準のrecomputeを予定）が次の必要作業とした。13 receiptはsweep記録+v15 anchorで既にfold可能な材料であり、69fと同じくfold時には子軌道の閉鎖をassertする。WIN7証明書は各7石rootの深さ10以内の先手勝ちのみを証明する。（事後記: このfoldはcost-74d foldの先着によりhead 1,179基準へのrebaseとして完了した。72b子は74d bit91の交差被覆でpre-closed、1163基準で予測していた子の閉鎖は帳簿上mimに計上されない。詳細は次々節。）

成果物: [証明書manifest](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost72b-win7-certificates-20261115.json)、[証明書ディレクトリ](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost72b-certificates/)（19ファイル）、[pipeline script](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/cost72b_cert_pipeline_20261115.sh)、[log](../../log/2026-11-15-n11-class2-lane-cost72b-win7-certificates.md)。

標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class2・class4は引き続き **UNKNOWN**。

## 2026-11-15: cost-74d子sweep・bit118証明書・15 receipt fold — chain head 1,179

自レーン（class2 lane）が第三class-2 coverableターゲットS5 `00000000000000809102000000000000` の未sweep子 `00000000000000809102020000000000`（cost 74、child == parent | 1<<41、需要c1=0,c2=2,c4=0）をclaim・sweepし、15 WIN7-D10 receiptをcost-70c warm batch-3 chain head 1,163の上にfoldした（[log](../../log/2026-11-15-n11-class2-lane-cost74d-sweep-certificates-receipts-fold.md)）。

**sweep**: 独立Bareiss 4x4列挙で74候補がmanifest edge cost 74とbit-exact一致。repo-verbatim v16 engineで**WIN7-D10 15件（bits 2,12,28,66,68,69,80,91,92,100,102,109,112,116,118）・REFUTED-D10 59件・打切り0・候補節点101,848,441**（pilot d6制御3,402 nodesは10/10 batch PASS、終局石数 [13,17]）。決定性再実行はbits 2/102/118がraw batchとnode-exact（1,887,907 / 17,056,910 / 456,245）。v15 cross-engine（別実装engine）は15 WIN bits全件 loss=true（bit2 6,793,780 / bit12 8,136,371 / … / bit118 3,163,638）、REFUTEDアンカーbits 25/103はloss=false（16,147,976 / 8,529,979）。純Python+Bareiss行列式の監査スクリプトが74候補を幾何学的に再導出しclaimと完全一致、d4正規形はcost-69f監査公表値9件で検証、15 win rootはすべて別個のd4 orbit（[sweep audit JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost74d-sweep-audit-20261115.json)）。

**bit118証明書**: root `00400000000000809102020000000000`（敵合法初手50）の戦略証明書をrepo-verbatim抽出器（FBS 1<<20・fbt_drops 0・行LC_ALL=C整列一意化）で抽出し、BigInt独立検証で**PASS**した（5,030,722抽出節点・28,719行・50/50 sub-root ok・union 0/0・終局石数 [13,17]、git blob sha `b96de16ac906721d9f7cdf82fed45bb032d57c1a`）。残り14 WIN7 bitsは証明書未抽出のままraw sweep receipt+v15 anchorとしてfoldした。

**fold**（`recompute_frontier_cost74d_receipts_20261115.py`）: 1,163 headをrunpyでbyte-identical再現（head JSON blob sha 50735896…照合）、74d子のbaseline残存assert、sweep auditの10 raw batch再導出（batch blob sha・root == child|1<<bit全件）、v15/v16制御assert、bit118証明書のbytes×md5×sha256×git blob sha検査をすべて通した上で、15 receiptを公開bit順 2,12,28,66,68,69,80,91,92,100,102,109,112,116,118 でfold。最初のreceipt（bit2）がchild軌道を閉鎖すること、fold後にchildが親のremainingから消えることをassertした。**+16 manifest軌道**（zero-mim receiptはbits 69/118 — bit118のmim 0はfold順序上の帰属であり証明書の価値を損なわない）。**chain headは解消S6 1,179・unique残り6,668・費用526,075・open需要4,938/389,798**（残りS5軌道175、c2=2,c4=0バケットは1,025→1,009）。2回実行byte-identical、push 4ファイルのremote git blob sha照合済み。

**親S5の縮小と並走レーンへの影響（重要）**: 親S5 `00000000000000809102000000000000` は**7軌道・519 → 4軌道・297**。foldは74d子（bit2のlift）に加えて、**cost-72b子 `00000000000000809102000002000000`（並走レーンがsweep・13証明書公開済み）をbit91の交差軌道liftで**、cost-76子 `00000000000000809102000000004000` をbit102のliftで閉じた。**並走cost-72b 13 receiptのfoldはこのhead 1,179へrebaseすること**（1,163基準のままfoldすると72b子の閉鎖が二重計上される。72b子はbit91 receiptで既被覆のため72b receiptのchildに対するmarginalは0になるが、各receiptの他のlift軌道は通常通りmarginalを持ちうる。fold慣行どおり拡大和集合からper-record marginalを再導出すれば帳簿は自動的に正しい）。残る4子は cost-69子 `00000000000000809102000000002000`（69g、並走in flight）・cost-74第二子 `00000000000000809142000000000000`（未claim）・cost-76子 `00000000000000809102000000000001`・cost-78子 `00000000000000809102000000400000`。

成果物: [frontier再計算JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost74d-receipts-recompute-20261115.json)、[ranking CSV](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-s5-ranking-after-cost74d-receipts-20261115.csv)、[top-candidates CSV](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost74d-receipts-20261115.csv)、[foldスクリプト](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost74d_receipts_20261115.py)、[sweep audit](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost74d-sweep-audit-20261115.json)、[bit118証明書](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost74d-certificates/bit118-root-00400000000000809102020000000000.cert)、[bit118記録JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost74d-cert-bit118-record-20261115.json)、[claim](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost74d-inflight-20261115.json)。raw batch 1–10・determinism rerun・v15 crosscheckは同output/の `class2-lane-cost74d-*`。

解消計数はmanifest被覆の前進であり、盤全体の勝敗ではない。WIN7証明書は個別7石rootの深さ10以内のWINのみを証明し、REFUTED-D10は「深さ10以内の先手勝ち不存在」であって子の反証ではない。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class2・class4は引き続き **UNKNOWN**。

## 2026-11-15: cost-72b 13 receipt fold — chain head 1,188（cost-74d head 1,179へのrebase）

前々節の13 WIN7-D10証明書をreceiptとして、cost-74d fold後のchain head 1,179の上にfoldした（[log](../../log/2026-11-15-n11-class2-lane-cost72b-receipts-fold.md)）。1163基準で実装・実行済みだったfold（総marginal 64 / mim +12・新head 1,175）は、main再取得で74d fold（head 1,179）の先着と `rebase_required` 指針を確認したため破棄し、**1179基準に全面的に書き直した**。

**D4重複の解消（重要）**: cost-72b bit85 root `00000000002000809102000002000000` と cost-74d bit91 root `00000000080000809102020000000000` は同一D4軌道（canonical `00000000000080811202000020000000`、変換 (x,y)->(x,10-y)）。chain内部の `canon()` で同一正規形をassertし、**別軌道として二重計上していない**。bit85証明書（636,225行manifestのうち40,352行）は、74d側でraw sweep receiptとしてfold済みの当該軌道の証明強化として機能する。

**fold実行体**（`recompute_frontier_cost72b_receipts_20261115.py`）のコントロール: 74d head 1,179をrunpy鎖（39 scripts）でbyte-identical再現（head JSON blob sha 06724afe…照合）、72b材料18ファイルのgit blob shaをmainと照合、子の1163基準残存を歴史制御でassert（1179では74d bit91により両open親から既にchild行消滅）、sweep記録を10 raw batchから再導出（72候補・13 WIN / 59 REFUTED・117,444,772節点・13 distinct D4 orbits）、v15 anchor・v16決定性rerun、13証明書の19 part + 13 wholeのbyte検証（manifest totals再集計: 636,225 rows / 729 sub-roots / 200,029,509 extraction nodes）、13新root vs 77個のfold済みreceipt rootのdisjointness（D4軌道等価はbit85==74d bit91の1件のみと明示）、公開bit順のfold、set-equality成立。2回実行で出力3ファイルbyte-identical。

**結果**: **marginal_in_manifest = +9**（bits 2/30/31/36/47/95/97/100/106、各+1）→ chain head **1,179 → 1,188**（unique remaining 6,668→6,659・sum cost 526,075→525,437・open需要 4,938→4,929 / 389,798→389,160、残りS5軌道175・c2=2,c4=0バケット1,009→1,000）。総marginal 57、zero-mim receiptsはbits 11/21/66（manifest内既被覆）とbit85（D4 dedup）。**+9はすべて共有open親S5 `00000000000000801202000020000000` のremaining行削減**（56軌道・4,199 → 47軌道・3,561）。親S5 `00000000000000809102000000000000` は4軌道・297で不変（72b子とbit85軌道は74d foldで既閉鎖）。

**並走実行との交叉一致**: 同じ毎時運行の別実行が同一foldのin-flight marker（`class2-lane-cost72b-fold-inflight-20261115.json`）をmainにpushし、その予測（mim +9・新head 1,188・zero-mim bits 11/21/66/85）は本foldの実測と完全一致した。独立2実装・独立実行の同一予測は交叉検査として記録する（当実行の完成push 40e03194が先着、marker側はclaim statusの更新を見てstand down可能）。

成果物: [frontier再計算JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost72b-receipts-recompute-20261115.json)、[ranking CSV](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-s5-ranking-after-cost72b-receipts-20261115.csv)、[top-candidates CSV](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost72b-receipts-20261115.csv)、[foldスクリプト](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost72b_receipts_20261115.py)、[claim更新](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost72b-inflight-20261115.json)、[log](../../log/2026-11-15-n11-class2-lane-cost72b-receipts-fold.md)。

解消計数はmanifest被覆の前進であり、盤全体の勝敗ではない。WIN7証明書は個別7石rootの深さ10以内のWINのみを証明する。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class2・class4は引き続き **UNKNOWN**。

## 2026-11-15: cost74d公開証明書の再生検査

main上のcost74d bit12・66・68・118と、D4交差利用元のcost72b bit85を、BigInt独立検査器で再生して5/5 PASS。5証明書の戦略行は計201,535行、各証明書の訪問局面数の単純和は440,820。全件でmissing/extra 0/0、終局石数13〜17。

7石rootから1石を除いた親をD4正準化し、cost74dの新規16 S6 manifest軌道と照合した結果、5証明書の和集合は6軌道を裏付ける。bit85既存分の3軌道に対し、cost74d bit12・66・68が追加で3軌道を裏付け、証明書付きS6下限は1,169。receipt frontier 1,179とは別の数値である。

bit85とcost74d bit91はD4変換 `(x,y)->(x,10-y)` で同一軌道。bit91本体は公開せず、bit85証明書を再利用する。

詳細: [監査ログ](../../log/2026-11-15-n11-class2-cost74d-published-certificate-replay.md)、[監査JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/cost74d-published-certificate-replay-20261115.json)、[再現スクリプト](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost74d_published_certificate_replay_20261115.py)。
## 2026-11-15: cost72b正利得9証明書の独立再生

cost72bの正利得9件（bits 2, 30, 31, 36, 47, 95, 97, 100, 106）をBigInt独立検査で再生して9/9 PASS。13個の公開分割blobのGit blob SHA、連結後の9証明書のwhole-file Git blob SHAとbyte数がmanifestに一致。戦略行は計458,203行、各証明書の訪問局面数の単純和は993,102。

9証明書の六石親をD4正準化し、cost72b foldの新規S6 manifest軌道と照合した結果、9/9をそれぞれ1軌道ずつ裏付けた。直前のcost74d監査で得た証明書付き下限1,169から1,178へ増加。receipt frontier 1,188とは区別する。

mainではcost74e child `00000000000000809142000000000000`（cost 74）がin-flight claim済み。二重起動しない。head 1188の最良class2 S5は4軌道・残り辺費用297。

詳細: [監査ログ](../../log/2026-11-15-n11-class2-cost72b-marginal-certificate-replay.md)、[監査JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/cost72b-marginal-certificate-replay-20261115.json)、[再現スクリプト](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost72b_marginal_certificate_replay_20261115.py)。


## 2026-11-15: cost-74d WIN7証明書出版完了 — 15/15 certified

前回の実行環境障害（Koyeb 503/DNS、2026-11-14T22:54Z〜）で3/19で中断していた出版列を、環境復旧後に完遂した。pending 10 bits（69/80/92/100/2/28/102/109/112/116）をrepo-verbatim pipeline（scripts 7件すべてmainのgit blob shaと照合済み）で再抽出し、**全件が障害前のinterim目録のmd5/sha256/git blob shaにbyte-exact一致**。キャリブレーションとして既公開のbit12/66/68/118とD4重複bit91も再抽出し、全15 bitsでbyte-identicalを確認した（bit102は単一プロセスで同一74,238行・29,752,097節点。bit80の正確なextraction_nodesは**13,115,852**と確定 — interim目録の「〜9.417M」は部分ログ由来の誤り）。

二重独立検証を全15証明書に再実行: BigInt検査器（`verify_win7_certificate_bigint_independent.mjs`）**15/15 PASS**、Number Bareiss検査器（`verify_bit7_win7_cert.ts --consumed-out`）**15/15 PASS**（sub-roots計883が敵合法初手数と全件一致、consumed union missing/extra 0/0、終局石数 [13,17]、行sorted-unique）。16ファイルを(4/19)..(19/19)の1コミット1ファイルでpushし、**remote 20ファイルのgit blob shaを全件照合（20/20 byte-exact）**。bit91は本文をpushせず、D4同一軌道のcost72b bit85証明書（blob `c99ef87964f4770e7dab365ea42ad070b8c6495d`）で裏付けた（repo precedent: cost61d bit22 = cost71b bit1）。

**最終マニフェスト** `class2-lane-cost74d-win7-certificates-20261115.json`（32,772 bytes、blob `0f6e7860796b999c6ab3b41d43931881085ad09f`、commit `5d37fab7`）: 15/15 WIN7 bits certified（14 published + bit91 D4-backed）、計723,630行・extraction nodes 186,044,401・visited 1,541,140・terminal 250,132・edges 1,380,013。claim `class2-lane-cost74d-inflight-20261115.json` をcompletedに更新（commit `7cae50e3`）。出版は15 WIN7 rootのreceipt被覆の裏付け強化であり、frontier計数は不変（74d fold 1,163→1,179、cost-72b fold→1,188はraw sweep receiptとして既に織り込み済み）。

運用記録: push_files実行**後**に16 MiB sandbox memory limitでプログラム中断が6回（bit69/80/92/100/102 part1/part2）あったが、いずれもremote blob sha照合で着地を確認してから継続し、欠損・truncationはなし。four-six-row lane（並走）とのfast-forward競合2回は同一内容retryで解決、read_file pagingとpushを同一ブロックにしない運用を確立した。

詳細: [出版完了log](../../log/2026-11-15-n11-class2-lane-cost74d-certificate-publication-completion.md)、[最終マニフェスト](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost74d-win7-certificates-20261115.json)、[interim目録](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost74d-certificate-hash-inventory-20261115.json)、[claim](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost74d-inflight-20261115.json)。証明書14本体は同output/`class2-lane-cost74d-certificates/`（bit91は`class2-lane-cost72b-certificates/bit85-root-00000000002000809102000002000000.cert`）。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class2・class4は引き続き **UNKNOWN**。


## 2026-11-15: cost74d WIN7/LOSS7 のD4衝突監査

cost74dの15 WIN7-D10 rootを、既存17 verified manifest（WIN7 77・LOSS7 200）、中央49 LOSS7 parent-lift 274軌道、category-1候補396軌道とD4照合した。既存WIN7・LOSS7・parent-lift・category-1候補との交差は全て0。category-1の396行は独立LOSS7証明書とは数えない。

cost72b WIN7証明書との交差は1件のみで、cost74d bit91 = cost72b bit85（正準形 00000000000080811202000020000000）。これは矛盾ではなく、既存証明書の意図した再利用。cost72bとの和集合に対する新規D4軌道は14。公開済み範囲のWIN/LOSS衝突は0件。

再現器は入力21ファイルのGit blob SHAを固定する。監査範囲は公開manifest・parent-lift・候補表であり、全raw cache・非公開worker cacheを走査したものではない。S6 frontierは変更していない。

詳細: [監査ログ](../../log/2026-11-15-n11-class2-cost74d-win-loss-conflict-audit.md)、[監査JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/cost74d-win-loss-conflict-audit-20261115.json)、[再現スクリプト](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost74d_win_loss_conflicts_20261115.mjs)。

標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class2・class4は引き続き **UNKNOWN**。


## 2026-11-15: cost-76a WIN7証明書出版完了 — 6/6 certified・claim closed

cost-76a child `00000000000000809102000000000001`（第三class-2 target S5 `00000000000000809102000000000000` の1<<0 lift、edge cost 76、head 1188でdemand c1=0/c2=2/c4=0）のsweep（76/76候補・131,329,581節点・6 WIN7-D10 bits 11/29/66/80/92/96・70 REFUTED・0 capped）に続く証明書工程を完遂した。

**抽出**: repo-verbatim `class4_child1_cert_extractor_exact.ts`（FBS 1<<20）を、本sessionでscripts/に公開したdriver [cert_driver76a.ts](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/cert_driver76a.ts)（blob `68336cdfe7c3eba4c0479bf79a1b309a3d32c191`）でbitごとにchunk実行。kill tableは空（pref=null）で既存判定の再利用なし、全行をextractorが自己検査つきで再証明。各bitの全loser初手（mobility 55〜62）を3〜4 chunkに分割、sort -u merge（**board移動競合は全bit 0**）、header 2行を付した。rows計279,344・extraction nodes 70,911,428・fbt_drops 0（bit96 6,642,969 / bit92 7,818,115 / bit11 13,521,724 / bit66 10,787,042 / bit80 15,010,982 / bit29 17,130,596）。

**二重独立検証**: BigInt検査器（3x3余因子展開）**6/6 PASS**、Number Bareiss検査器（--root-check・--subroots全初手・--consumed-out）**6/6 PASS**（sub-roots 351 = 敵合法初手数と全件一致、consumed union == 証明書行でcomm diff 0、missing/extra 0/0、終局石数 [13,17]、行sorted-unique）。

**出版**: bit96/bit92/bit11/bit80は単一ファイル、bit66（1,914,257 B）とbit29（2,097,005 B）は1.75 MiB = 1,835,008 bytes超につき `.part1of2`/`.part2of2` に行境界分割（連結md5 = whole md5を両bitで確認）。(1/6)..(6/6)の1コミット1ファイルでpushし、**remote 8ファイルのgit blob shaを全件照合（8/8 byte-exact）**。16 MiB sandbox memory limitがpush_files実行後に2回（bit11・bit80）プログラムを中断したが、いずれもremote listing照合で着地確認済み（欠損・truncationなし）。bit66の初回driver起動でchild hex誤指定によるfatal=2をsummary.jsonで即検出し、出力を汚さずやり直した。

**最終マニフェスト** [class2-lane-cost76a-win7-certificates-20261115.json](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost76a-win7-certificates-20261115.json)（15,810 bytes・blob `f3be0e0edfc4ddf5da327dc545de7009926407ef`・commit 33777bea）: totals 279,344 rows / 70,911,428 extraction nodes / 351 sub-roots / visited 593,146 / winner 381,849 / loser 113,633 / terminal 97,664 / edges 528,178 / v15 crosscheck sum 44,074,444。sweep auditのproof_boundary（certificate_extraction・independent_certificate_verification）を閉じ、claim [class2-lane-cost76a-inflight-20261115.json](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost76a-inflight-20261115.json) をcompletedに更新した。6 rootはD4重複なし（sweep audit d4_duplicate_scan: published 58 rootと重複0）。

**残作業**: 76aの6 receiptはまだchain head 1188にfoldされていない。fold（`class-frontier-cost76a-receipts-recompute-20261115.json`、head 1188 `1188/6659/525437/4929/389160` assert）は72b/74d/70cwarm3/unified mergeに至るrunpy鎖（39 scripts）のbyte-identical再現を要し、必要材料のfetchを含む大規模タスクとして次回に回す。第三class-2 targetの未claim最後の子はcost-78 `00000000000000809102000000400000`。

解消計数はmanifest被覆の前進であり、盤全体の勝敗ではない。WIN7証明書は各7石rootの深さ10以内の先手勝ちのみを証明する。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class2・class4は引き続き **UNKNOWN**。

詳細: [出版完了log](../../log/2026-11-15-n11-class2-lane-cost76a-certificate-publication-completion.md)。証明書6本体は同output/`class2-lane-cost76a-certificates/`。

## 2026-11-15: cost-76a six WIN7証明書の第三独立再生と部分edge被覆

cost-76aの6証明書（bits 11/29/66/80/92/96）を、既存のBigInt 3×3余因子検査器・Number Bareiss検査器をimportしない第三実装で再生した。円の中心を有理数分子/分母で表し、共線3点は整数外積で直線判定する。浮動小数点・探索器・判定cacheは使わない。6/6 PASS、279,344行、351 sub-root、訪問593,146状態、終局97,664、missing/extra=0/0、終局石数13〜17、v15 anchor全件一致。root合法手数は62/60/61/59/54/55でmanifestと一致し、6 rootのD4軌道も相互に異なる。

実装時、最初の円のみの試作はbit96 rootの合法手数を71と誤算した。K0001の規則は共円だけでなく共線4点も禁止するため、共線3点の分岐を追加して修正した。この失敗と修正は再現ログに記録した。

42件の7石root親liftは37個のD4正準S6親軌道、42個の親・着手辺にまとまる。既知のopen S6軌道2個について7辺を新たに証明:
- S6 `00000000000000809102000000000001`: 76辺中6辺（bits 11/29/66/80/92/96）を被覆、残り70。これを共有するS5 `00000000000000809102000000000000` は4軌道・297から局所291へ、S5 `00000000000000801202000000000400` は77軌道・6296から局所6290へ。
- S6 `00000000000000801202000000200400`: 81辺中1辺（bit64）を被覆、残り80。S5 `00000000000000801202000000200000` は41軌道・3058から局所3057へ。

S5ごとの費用減少の合計は13だが、一意なS6→S7辺は7件。最初の6辺が2つの異なるS5親に共有されるためであり、独立した13辺ではない。既知のS6親はいずれも未閉鎖。37親軌道のうち35軌道は今回のshortlistで状態未分類。**global frontierは再計算しておらず、head 1188/6659/525437/4929/389160は変更しない。**

詳細: [第三独立監査ログ](../../log/2026-11-15-n11-class2-cost76a-third-independent-certificate-audit.md)、[監査JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/cost76a-six-certificates-third-independent-audit-20261115.json)、[再現スクリプト](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost76a_six_certificates_third_independent_20261115.mjs)。

6証明書は各7石rootの勝ちを示すだけで、76合法手のS6親を閉じない。REFUTED-D10はLOSS証明ではない。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、類2・類4は引き続き **UNKNOWN**。


## 2026-11-15: cost-76a receipts fold 完成 — chain head 1188→1195

cost-76a sweep の証明書付きWIN7-D10 receipts 6件（bits 11/29/66/80/92/96）を head 1188 にfoldし、新chain head **1195/6652/524884/4922/388607**（remaining S5 orbits 175）を確定した。head JSON は `class-frontier-cost76a-receipts-recompute-20261115.json`（blob `efd83f2637f83c0e1c5c477dcb0cc42162cda534`）、fold script は `recompute_frontier_cost76a_receipts_20261115.py`（blob `9090e4c86795f96864c0d83bd66db18b35ea88e2`）。

- total marginal 31 / marginal_in_manifest +7。bit11 receipt が子軌道 `00000000000000809102000000000001` 本体と交差被覆 `00000000000000801202000000200400` を閉鎖し、bits 29/66/80/92/96 が各1軌道（`00000000000000801202000002000400`, `00000000000000849002000000000001`, `00000000000100809002000000000001`, `00000000100000809002000000000001`, `00000000040000801202000000000400`）を閉鎖。zero-mim receipt なし。4回実行すべてbyte-identical。
- 第三class-2 target S5 `00000000000000809102000000000000` は残り4行（69/74/76/78 = 297）→3行（221）。残る69（cost-69g）・74（cost-74e）・78（cost-78a）はすべて並走レーンでin flight。
- 統制: 1188 head のrunpy鎖 end-to-end 再現（head JSON・両CSVがmain掲載版とbyte-identical）、16入力ファイルのgit blob SHA照合、sweep audit のraw 10 batchからの再導出（76候補・131,329,581節点・6 WIN7-D10 / 70 REFUTED / 0 capped）、v15 anchor のnode一致、証明書6件のbytes再検証（md5×sha256×git blob、8 parts + 6 wholes、union 0/0、終局石数13〜17）、第三独立audit JSONの全項目一致、root disjointness（既fold 90 roots、raw + D4両方）。set-equality `s_after == s_1188 ∪ covers(6 roots)` 成立。

事前作業として `recompute_frontier_cost72b_receipts_20261115.py` の透明修復（commit b4d655f9）を行った。公開後のclaim closure追記でclaimファイルのblob shaが変わり、公開済みchainが再実行不能になっていた。現行blob `b1c135c539e20c0ae94cdc2e66d769911af5eb7d` に差し替え、算術は無変更で1188 headをbyte-identical再現した。以後のfold script はclosure後のclaim blobをassertする（76a script は `7922a02aa7a84fa12c03ea04be9b1006468ea596` をassertし、無期限に再実行可能）。

自claim c1f3028f の約1分後に並走実行が同fold claim（c4767883）をstale-fetchで上書きしたが、c00b4543 で自版を復元し、衝突をclaim closureの `concurrent_claim_note` に記録した。並走が独立にfoldを公開した場合は同一算術の相互検証を行う（cost-72b collision protocol）。

cost-78a receipts fold（並走、証明書公開中）は**新head 1195 へのrebaseが必須**。以後のrecompute・claimはこのheadをassertして拡張する。

解消計数はmanifest被覆の前進であり、盤全体の勝敗ではない。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class2・class4は引き続き **UNKNOWN**。

詳細: [fold log](../../log/2026-11-15-n11-class2-lane-cost76a-receipts-fold.md)、[head JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost76a-receipts-recompute-20261115.json)、[fold script](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost76a_receipts_20261115.py)。


## 2026-11-15: cost78a公開証明書の独立再生監査 — bit20・bit36 PASS・frontier不変1195

並走cost-78aレーンがmainに公開したWIN7証明書のうち、掲載済み2件（bit20・bit36）をBigInt独立検証で再生監査した。bit20は2 partを行境界で再連結（2,039,074 B・md5 `348871fd605dedeb34b5a4c4ad6f518c` == claimの `joined_md5_equals_whole_md5`）、bit36は単一ファイル（1,833,561 B）。BigInt検査器（3×3余因子展開・engine不使用）で**2/2 PASS**: bit20は64 sub-roots == loser mobility == sweep `opponent_legal_replies`・56,452行sorted-unique、bit36は59 sub-roots・50,711行。計107,163戦略行・consumed union 0/0・終局石数[13,17]・claim記載のrows・md5・v15 anchor nodes（9,116,968/6,829,497）・v16 sweep nodes（2,523,199/1,435,988）と全件一致。

入力6ファイル（sweep audit・v15 crosscheck・claim・bit20両part・bit36）のgit blob SHAをmainと照合しbyte-exact。root == child|1<<bit のbit検算、D4正準形がsweep audit `d4_canonical_hex` と一致、親lift再導出で両rootの6親のD4正準軌道にchild `00000000000000809102000000400000` が含まれることを確認した。

head-1195 tie-in: 第3class-2 target S5 `00000000000000809102000000000000` の残り行は{69,74,78}=221で、child（cost 78）は依然remaining。よって本監査はfrontier計数を一切変更しない（`s6_frontier_contribution: 0`）。bits 8/29/109は並走が公開中のため監査対象外。**cost-78a receipt foldは並走担当・新head 1195へのrebase必須**（1188基準のままfoldしないこと）。

WIN7証明書は各7石rootから深さ10以内の先手勝ちのみを証明し、78合法手の6石親は閉じない。REFUTED-D10はLOSS証明ではない。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class2・class4は引き続き **UNKNOWN**。

詳細: [監査log](../../log/2026-11-15-n11-class2-cost78a-published-certificate-replay.md)、[監査JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/cost78a-published-certificate-replay-20261115.json)、[再現スクリプト](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost78a_published_certificate_replay_20261115.py)。


## 2026-11-15: cost-63f sweep・WIN7証明書2件出版 — 第2 class-2 target最安行・frontier不変1195

第3class-2 target S5 `00000000000000809102000000000000` の残り3行（69/74/78）がすべて並走in flightのため、head-1195で大域最安の未sweep行 **cost-63 child `00000000000080809002000000000800`** をcost-63fとして取得した（IN FLIGHT claim commit 30d2dd47を先行push）。子は第2 coverable class-2 target S5 `00000000000000801202000000200000`（40 orbits/2977）のD4一石lift（stone 79削除で一致）でもう1個のopen親はclass-2 S5 `00000000000000801202020000000000`（52/3551・stone 11）・demand c1=0,c2=2,c4=0・`legal_candidates.py` 63候補がmanifest edge cost 63とbit-exact。

**sweep（v16・depth 10・cap 1e9・andclose 1・8バッチ・pilot 3402×8）**: 63/63候補・**WIN7-D10 2件（bits 85, 91）**・61 REFUTED・0 capped・44,140,211 nodes（76aの131M比34%）。統制: batch-6 determinism rerun一致・v15交差エンジンでbits 85/91はloss=true（10,145,295/3,920,892 nodes）・refutedアンカーbits 1/7/109はloss=false・pilot 5949×3。独立監査 [audit_cost63f_raw_sweep_20261115.py](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost63f_raw_sweep_20261115.py)（標準ライブラリのみ・Bareiss再実装）が10 rawファイルから全件再導出（候補63 bit-exact・各bit 1回・terminal [13,17]全件・root == child|1<<bit・D4 canonical重複0・published 149 roots比較）。

**証明書2件（二重独立検証 2/2 PASS）**: repo-verbatim driverで全loser初手をchunk抽出・sort -u merge。bit85 root `00000000002080809002000000000800`: 40,154行・51/51 sub-roots・extraction 17,491,560 nodes・1,449,311 B単一ファイル。bit91 root `00000000080080809002000000000800`: 29,305行・49/49 sub-roots・6,973,105 nodes・1,058,527 B。BigInt 3×3余因子検査とNumber Bareiss（--root-check --subroots全初手 --consumed-out）の双方でPASS（consumed union == 証明書行・missing/extra 0/0・終局石数[13,17]・fbt_drops 0）。manifest [class2-lane-cost63f-win7-certificates-20261115.json](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost63f-win7-certificates-20261115.json): 計69,459行・24,464,665 nodes・sub-roots 100。claimをcompletedに更新（fold pending）。15ファイル全remote blob sha byte-exact照合済み。

**2 receiptのfoldは未実施・canonical chain head 1195/6652/524884/4922/388607は不変**（foldはhead 1195へのrebase必須）。兄弟cost-63行 `00000000080000801202000000200000` は未claimのまま別レーン候補。WIN7証明書は各7石rootから深さ10以内の先手勝ちのみを証明し、63合法手のS6親は閉じない。REFUTED-D10はLOSS証明ではない。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class2・class4は引き続き **UNKNOWN**。

詳細: [log](../../log/2026-11-15-n11-class2-lane-cost63f-sweep-and-certificates.md)、[sweep audit](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost63f-sweep-audit-20261115.json)。証明書2本体は同output/`class2-lane-cost63f-certificates/`。

## 2026-11-15: cost-63f receipts fold 完成 — chain head 1195→1199

cost-63f sweepの証明書付きWIN7-D10 receipts 2件（bits 85/91）をhead 1195にfoldし、新chain head **1199/6648/524616/4918/388339**（remaining S5 orbits 175）を確定した。head JSONは `class-frontier-cost63f-receipts-recompute-20261115.json`（blob `e1e72b12ca39769f2c4a298d91833b612c97afeb`）、fold scriptは `recompute_frontier_cost63f_receipts_20261115.py`（blob `f9a02900ab13c0dc5c201d7f22ac9b39ff90471d`）。fold claim（claim df33461d → 本体push 3333d4f9・closure版blob `4c1d2e14231961cc4874ab9cc869177747851294`）はclosure後のclaim blob shaをscriptがassertし、無期限に再実行可能（cost-72b修復の教訓を適用）。

- total marginal 12 / marginal_in_manifest +4。bit85 receipt（root `00000000002080809002000000000800`）が子軌道 `00000000000080809002000000000800` 本体＋交差被覆 `00000000000080801202000000200000`・`00000000000000801202020800000000` を閉鎖し、bit91 receipt（root `00000000080080809002000000000800`）が `00000000000000801202020020000000` を閉鎖。zero-mim receiptなし。3回実行すべてbyte-identical。
- 第2 coverable class-2 target S5 `00000000000000801202000000200000` は残り40行/2977 → **38行/2837**。第2 open parent（class-2 S5 `00000000000000801202020000000000`）は52行/3551 → **49行/3360**。両open parentからchild行が落ちたことをbit-exactで検証。childのD4一石lift関係（stone 79削除→parent1・stone 11削除→parent2）をchain-internal canon()で再導出。
- 統制: 1195 headのrunpy全再現（76a fold script経由で1188から再現・head JSON `efd83f26…`・両CSVがmain掲載版とbyte-identical）、14入力ファイルのgit blob SHA照合、sweep auditをraw 8 batchから再導出（63候補==claim列挙 bit-exact・2 WIN7-D10 / 61 REFUTED / 0 capped・44,140,211 nodes・batch-6 determinism rerun node-exact）、v15 anchor（2 WIN node一致・refuted bits 1/7/109・pilot 5949×3）、証明書2件のbytes再検証（md5×sha256×git blob・sub-roots 51/49 == loser mobility == sweep root mobility・union 0/0・terminal 13..17・manifest totals再集計: 69,459行 / 100 sub-roots / 24,464,665抽出nodes）、root disjointness（96既fold roots = 90 pre-76a + 6 cost-76a・raw + D4両方）。set-equality `s_after == s_1195 ∪ covers(2 roots)` 成立。
- 着手直前の最新main確認で、兄弟cost-63行 `00000000080000801202000000200000` は並走がcost-63gとしてIN FLIGHT claim済み（commit 69a8f4ad）であることを確認し、触れていない。並走が同セッション中にcost-63f証明書の第三独立監査（rational-geometry replay・CI・D4 root manifest照合）をpushしているのも確認した（commits 6728ba9d/bdc35e32/71464062/77daf4cf）。

**cost-63g fold（並走・sweep in flight）とcost-78a fold（並走・証明書公開中）は新head 1199へのrebase必須**。以後のrecompute・claimはこのheadをassertして拡張する。69g/65j/74eも並走in flight。

解消計数はmanifest被覆の前進であり、盤全体の勝敗ではない。WIN7証明書は各7石rootの深さ10以内の先手勝ちのみを証明する。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class2・class4は引き続き **UNKNOWN**。

詳細: [fold log](../../log/2026-11-15-n11-class2-lane-cost63f-receipts-fold.md)、[head JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost63f-receipts-recompute-20261115.json)、[fold script](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost63f_receipts_20261115.py)。

## 2026-11-15: cost-65k sterile sweep — 65 REFUTED-D10・WIN7-D10不在・frontier不変1199

head-1199のtop-candidatesで未sweepだった cost-65 child `00000000020000801202000000200000`（第2 coverable class-2 target S5 `00000000000000801202000000200000` のS6行・stones [21, 49, 57, 60, 71, 89]・lift stone 89・開親2個ともclass 2: parent1 38行/2837〔stone 89削除〕・`00000000000000003800000008002000` 53行/3698〔stone 21削除〕）をcost-65kとしてsweepした（cost-65b–65jは他行で使用済み）。**65/65候補・WIN7-D10 0件・65 REFUTED-D10・0 capped・総nodes 32,457,462**（v16 engine・depth 10・cap 1e9・andclose 1・8バッチ・pilot 3402×8全PASS）。STERILE: receiptが存在しないためfold材料なし・証明書抽出対象なし。

- terminal stone rangeは64候補 [13,17]、bit 9のみ [13,15]（全ライン早期終端・63fとは異なる正当値。監査assertは固定値比較から深さ10境界検査〔[0]≥7・[1]≤17〕に修正し `distinct_terminal_ranges` を記録）。batch 6（bits 74,75,76,77,79,83,84,86）determinism rerunはnode-exact一致、v15交差エンジン（`class4_child1_runner.ts`）でアンカーbits 7/86/118はloss=false（nodes 125301/2037455/5749144・pilot 5949）。
- 独立監査 `audit_cost65k_raw_sweep_20261115.py`（Python標準ライブラリのみ・Bareiss再実装・repo engine不使用）が10 rawファイルから全件再導出: 候補65==claim列挙 bit-exact・各bit 1回ずつ・pilot 3402×8・D4 canonical重複0（published manifest roots 151個との比較込み・59 manifest走査）。監査JSON `class2-lane-cost65k-sweep-audit-20261115.json`・2回実行byte-identical。
- 出版はbase64一括転写2回失敗を受け、整数compact-table（bit, nodes, ms, terminal range）からのJSONL行再生方式に切替（ローカルでbyte-exact検証後にpush・remote 13ファイル全部cmp一致・blob sha照合済み）。
- 並走: cost-63g sweep 63/63・証明書14/14出版済み（commit `1b814444` 時点）・foldは並走担当。78a/69g/65j/74eも並走in flight。

**child `00000000020000801202000000200000` はparent1の未解決S6行のまま（38行/2837）**。この行を反証で閉じるには深さ>10の証拠（65個の7石root各々への深さ>10の反証または不変量）が必要で、parent1の他の子行からのWIN7 receipt foldでの閉鎖も可能。REFUTED-D10はLOSS証明ではない。canonical chain head **1199/6648/524616/4918/388339 は不変**。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class2・class4は引き続き **UNKNOWN**。

詳細: [sweep log](../../log/2026-11-15-n11-class2-lane-cost65k-sterile-sweep.md)、[completed claim](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost65k-inflight-20261115.json)、[sweep audit](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost65k-sweep-audit-20261115.json)、[audit script](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost65k_raw_sweep_20261115.py)。

## 2026-11-15: cost-63g receipts fold 完成 — chain head 1199→1216

cost-63g sweepの証明書付きWIN7-D10 receipts 14件（bits 0,9,12,50,54,58,62,64,72,94,96,99,105,113）をhead 1199にfoldし、新chain head **1216/6631/523382/4901/387105**（remaining S5 orbits 175）を確定した。head JSONは `class-frontier-cost63g-receipts-recompute-20261115.json`（blob `e311e24346adad570e42f145f9190fe8427ae921`）、fold scriptは `recompute_frontier_cost63g_receipts_20261115.py`（最終blob `8f24511c815ec716f62f93587678ffc6b704ae57`）。claim v3 retire（blob `1844f9d25f15dbc6717b13178cb18459894fdade`）はfold記録・出力blobを記載し、scriptはclaim v2/v3両blobを受け入れ、retired claim controlが再実行時にfold数値とhead JSON byte同一性を再assertする（cost-72b修復の教訓どおり無期限再実行可能）。

- total marginal 73 / marginal_in_manifest +17、zero-mim receiptはbit58・bit64。子軌道 `00000000080000801202000000200000` はbit0 receipt（root `00000000080000801202000000200001`）で閉鎖（全14 rootが自身の追加石削除で子を被覆するため公開順最初のreceiptで閉じる）。set-equality `s_after == s_1199 ∪ covers(14 roots)` 成立。
- 第2 coverable class-2 target S5 `00000000000000801202000000200000` は38行/2837 → **33行/2470**（parent-lift影響監査 `cost63g-parent-lift-frontier-impact-20261115.json` の予測とbit-exact一致・5行喪失）。もう一方のopen parent（class-2 S5 `00000000000000003800000808000000`）は71行/5281 → **58行/4351**（13行喪失・子を含む）。両S5 parentとも未解決のまま。fold後のbest coverable class-2は `00000000000000809102000000000000`（3行/221）。
- 統制: 1199 headのrunpy全再現（63f fold script経由・head JSON `e1e72b12…`・両CSVがmain掲載版とbyte-identical）、14入力ファイルのgit blob SHA照合、sweep auditをraw 8 batchから再導出（63候補==claim列挙 bit-exact・14 WIN7-D10 / 49 REFUTED / 0 capped・75,637,935 nodes・WIN合計15,742,818・batch-5 determinism rerun 8/8 node-exact・pilot 3402×8）、v15 anchor（14 WIN node一致 合計31,368,332・refuted bits 1/32/116・pilot 5949×5）、証明書14件のbytes再検証（md5×sha256×git blob・bit113は2 parts結合がwholeと一致・sub-roots == loser mobility == len(loser_first_moves)・terminal 13..17・fbt_drops 0・d4_canonical_hex == canon(root)・d4_parent_orbitsが全てcanon不変かつ各々が子を含む・manifest totals再集計: 419,398行 / 15,142,573 bytes / 54,670,850抽出nodes / 667 sub-roots）、root disjointness（98既fold roots = 96 pre-63f + 2 cost-63f・raw + D4両方・14個の異なるD4軌道）。3回実行（claim v2時2回・v3 retire後1回）すべてbyte-identical。
- 訂正: claim記載のextraction_nodes 54,670,950はmanifest再合計 **54,670,850** に置き換え（claim v3 retireのcorrection欄に明記。fold scriptのcontrolsも`claim_extraction_nodes_superseded`として記録）。
- 運用事実: fold実行中に並走cost65l raw artifacts着地（commit 1d08a5fc）に伴い、top-candidates CSVの初回pushが一度だけ409競合した。最新mainを取り直して再pushし解決（中身不変・blob 77c12f79）。cost65l（2 WIN7-D10 bits 21/48のsweep完了・foldは未）・cost78a証明書・69g/65j/74eレーンは本foldに含めない。

**以後のfold（cost65l・cost78a・69g/65j/74e）は新head 1216/6631/523382/4901/387105へのrebase必須**。解消計数はmanifest被覆の前進であり、盤全体の勝敗ではない。WIN7証明書は各7石rootの深さ10以内の先手勝ちのみを証明する。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class2・class4は引き続き **UNKNOWN**。

詳細: [fold log](../../log/2026-11-15-n11-class2-cost63g-receipt-fold.md)、[head JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost63g-receipts-recompute-20261115.json)、[fold script](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost63g_receipts_20261115.py)、[retired claim](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost63g-inflight-20261115.json)。

## 2026-11-15: cost-67c sweep・WIN7証明書2件出版 — 混合需要c2+c4の子・foldは次回

子S6 `00000000000000801202000000202000`（石 13,21,49,57,60,71、edge cost 67）は需要 c1=0,c2=1,c4=1 の混合行で、第2 coverable class-2 S5 `00000000000000801202000000200000`（33/2470・lift石13）と open class-4 S5 `00000000000000801002000000080800`（76/5703・lift石57）の両方に効く。head 1216時点でparent1の最安未sweep子（重複claim無しをcode searchで確認済み）。

- sweep（v16 runner・depth 10・cap 1e9・andclose 1）: 67候補（legal_candidates.py独立列挙とbit-exact一致）、**WIN7-D10 2件（bits 64, 96）**、65 REFUTED-D10、0 capped、41,942,979 nodes（WIN合計 2,368,197: bit64 1,393,667 / bit96 974,530）。全terminal範囲 [13,17]。pilot 3402×9 PASS、batch-5 determinism rerun 8/8 node-exact、v15交差検証はWIN 2/2 loss=true（bit64 5,068,403 / bit96 2,436,013 nodes・pilot 5949×5）・refutedアンカー bits 1/32/116 loss=false・raw判定完全一致。raw batch 1..9・sweep audit・determinism rerun・v15 crosscheckをすべてpush、raw取得でbyte-exact確認済み。
- WIN7証明書2件（`cert_driver63g.ts`・kill table空・fbt_drops 0）: bit64 root `00000000000000811202000000202000`（34,583行 / 1,249,941 bytes / 抽出7,018,550 nodes / sub-roots 53・D4正準形 `00000000000000809102000000080800`）、bit96 root `00000001000000801202000000202000`（35,897行 / 1,296,064 bytes / 4,536,424 nodes / 53・D4正準形 `00000000040000809002000000080800`）。BigInt独立検証器 2/2 PASS（union conflict 0/0・terminal [13,17]。bit64: visited 72,383 / winner 46,475 / loser 14,045 / loser-reply edges 65,414 / terminal 11,863。bit96: visited 75,928 / winner 48,819 / loser 14,516 / reply edges 67,109 / terminal 12,593）＋第二独立検証（perm-det4 Bareiss 整数4×4行列式）2/2 PASS（root loser mobility 53 = sub_roots_total = len(loser_first_moves)、per-node mobility一致、子がrootのd4 parent orbits（各7軌道）に含まれる）。rows sorted-unique。両rootとも既存公開rootとraw hex・D4正準形の両方でdisjoint（code search 0 hits）。
- 公開: 両証明書とも1MB超のためbit113と同じ2分割方式（part1of2/part2of2・結合がwholeとmd5一致）。4 partファイルのremote git blob shaは全件byte-exact照合済み。manifest `class2-lane-cost67c-win7-certificates-20261115.json`（totals: 2証明書 / 70,480行 / 2,546,005 bytes / 抽出11,554,974 nodes / sub-roots 106 / v15 crosscheck合計 7,504,416 / v16 WIN合計 2,368,197）。claim v2（status `sweep_and_certificates_complete_fold_pending`・remote blob `0b98e003fae000bb663e8b5a4d7f6ad5954cedc3`）はsweep_results・win7_certificates・rebase_target・next_actionを記載。
- 運用事故と復旧: 4 partファイルを最初に誤ってrepo直下 `output/class2-lane-cost67c-certificates/` へpushしてしまった（正しくは `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/` 配下）。正パスへ再pushした上で誤配置4件を削除コミットで除去、誤パスのディレクトリはmainから消滅（削除直後のraw 200応答はCDNキャッシュ）。manifestの `controls.misplaced_path_cleanup` に記録。
- foldは次回実行: 並走cost-65l fold（bits 21/48・証明書公開済み）が先にheadを進める可能性が高いため、cost-67c fold（`recompute_frontier_cost67c_receipts_20261115.py`・63g版がtemplate）はfold時点の最新canonical headをassertしてからrebaseして行う。証明書の公開だけではfrontier計数は不変（head 1216/6631/523382/4901/387105のまま）。

REFUTED-D10はWIN7-D10の不在のみを証明し勝敗判定ではない。解消計数はmanifest被覆の前進であり、盤全体の勝敗ではない。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class2・class4は引き続き **UNKNOWN**。

詳細: [sweep log](../../log/2026-11-15-n11-class2-cost67c-sweep-certificates.md)、[certificates manifest](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost67c-win7-certificates-20261115.json)、[claim v2](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost67c-inflight-20261115.json)。

## 2026-11-15: cost-67cの第三独立証明書再生監査

cost-67cの2本のWIN7証明書を、既存のBigInt検査器・perm-det4 Bareiss検査器とは別の実装で再生した。円は有理中心分子の整数等式、共線三点は直線上の整数外積で判定し、浮動小数点・探索器・共有cacheは使っていない。

- **2/2 PASS**。bit64 rootは34,583戦略行、bit96 rootは35,897行。各rootの相手側初手53通りをすべて展開し、戦略行の不足・余分は両方0。全終局は13〜17石。
- 全証明木を複数初手間で共有するDAGとして再走査した一意局面数は52,739 + 54,785 = **107,524**。勝ち側70,480局面、負け側21,490局面、負け側応手辺102,248、終局15,554。これは今回の検査器での全root合併後の一意数であり、既存検査器のsub-rootごとの訪問数とは集計方法が異なる。
- 2証明書から得る六石親への持ち上げは14 incidence、D4軌道は**13個**。共通親は子S6 `00000000000000801202000000202000`。13軌道中7軌道が7,867行のS6 worklistに存在する。ただし、worklist membershipは現在の未解決membershipを意味しない。
- 共通の子S6は、bit64とbit96の2つの異なる合法手で、それぞれ第二手番が負ける7石rootへ進めるため、**この六石局面自体はWINと証明された**。現行headのtop-candidates CSVにはclass2親からの残り行として1件が直接掲載される。もう一つのclass4親もopen S5だが、その親に対する子行はtop-candidatesの掲載範囲外であり、この監査では残りincidenceを独立再生成していない。claimは両親で残り行と記録している。
- 証明書のreceipt foldは未実施。親lift全体と未解決S6集合の交差を確定していないため、公式frontierは **1216/6631/523382/4901/387105** のまま。S5は175軌道。未foldの証明を公式solved数へ先取りしない。

標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`、class2・class4の勝敗は引き続き **UNKNOWN**。

再現スクリプト: [audit_cost67c_certificates_third_independent_20261115.mjs](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost67c_certificates_third_independent_20261115.mjs)  
監査結果: [cost67c-third-independent-certificate-audit-20261115.json](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/cost67c-third-independent-certificate-audit-20261115.json)

## 2026-11-15: cost-73f sterile sweep — class-4 frontier行の初sweep・73 REFUTED-D10・frontier不変1216

head-1216（cost-63g fold後のcanonical chain head 1216/6631/523382/4901/387105）のtop-candidatesで、**best class-4 blocker S5 `00000000020000003800000080000000`（18 orbits/1460・head-1045以来不変のclass-4 bottleneck）の最安未sweep行 cost-73 child `000000000200000038000000c0000000`**（stones [30,31,59,60,61,89]）をcost-73fとしてsweepした（cost-73a..73eはaudit-blocked class-2 S5の別行で使用済み）。**class-4 frontier行への初のsweep着手**（近年のレーンはすべてclass-2 target行）。

- **claim前検証（head 1216基準）**: exact-integer D4正準化で子の6個の一石削除を照合し、開親3個がすべてclass-4（best blocker 18/1460〔stone 30削除〕・`00000000020000003800000040000000` 85/6497〔stone 31削除〕・`00000000000000003800000001800000` 77/5548〔stone 89削除〕・残り3削除はhead-1216 ranking CSVに不在の閉行）→ c1=0,c2=0,c4=3（head-1216 top-candidates CSVと一致）。IN FLIGHT claim（commit f391d736・blob ecfc38be…）を先行pushして着手。
- **sweep結果（v16 d10・cap 1e9・andclose 1・10バッチ・pilot 3402×10全PASS）**: **73/73候補・WIN7-D10 0件・73 REFUTED-D10・0 capped・総nodes 51,522,112**。terminal rangeは71候補 [13,17]・bits 40/66が [11,17]（深さ10境界検査〔[0]≥7・[1]≤17〕で合格・distinct_terminal_rangesに記録）。batch-6 determinism rerun node-exact・v15交差エンジンでアンカーbits 3/32/116はloss=false（nodes 7881598/1751024/1696566・pilot 5949）。
- **独立監査**: `audit_cost73f_raw_sweep_20261115.py`（Python標準ライブラリのみ・Bareiss再実装・repo engine不使用）が12 rawファイルから全件再導出（候補73==claim列挙 bit-exact・各bit 1回・pilot 3402×10・batch-6一致・v15アンカー一致）し2回実行byte-identical（md5 d7bdc565…）。出版訂正1件: 初版監査に65k雛形の記述残骸（"65"表記2箇所・"ten raw artifacts"ヘッダ）が残っていたのを検出即修（assert・集計値は初版から正しく記述フィールドのみ・訂正コミットfb9a609bでclaim/logに記録）。
- **STERILE（負の実験事実）**: WIN7-D10 receiptが存在しないためfold材料なし・証明書抽出対象なし・**canonical chain head 1216/6631/523382/4901/387105は不変**。childは3開親（すべてclass-4）の未解決S6行のまま（best blockerは18行/1460不変）。REFUTED-D10はLOSS証明ではなく、この行を反証で閉じるには深さ>10の証拠が必要。class-4 frontierの次候補は同S5のcost-74行 `00000000020000003800000080000020`（c1=2,c2=0,c4=3）ほか。
- 並走（着手時点）: cost-65l（bits 21/48証明書出版中）・cost-67c（bits 64/96・証明書出版済みでfold待ち）・cost-78a（bits 8/29/109）・69g/65j/74eはin flightで本sweepと衝突なし。それらのfoldはfold時点のcanonical headへのrebase必須。

解消計数はmanifest被覆の前進であり、盤全体の勝敗ではない。WIN7証明書は個別7石rootの深さ10以内の先手勝ちのみを証明する。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class2・class4は引き続き **UNKNOWN**。

詳細: [sweep log](../../log/2026-11-15-n11-class2-lane-cost73f-sterile-sweep.md)、[sweep audit](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost73f-sweep-audit-20261115.json)、[completed claim](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost73f-inflight-20261115.json)。

## 2026-11-15: cost-74f sterile sweep — best class-4 blocker S5の最安2行が連続STERILE・74 REFUTED-D10・frontier不変1216

head-1216（canonical chain head 1216/6631/523382/4901/387105不変）のtop-candidatesで、cost-73fに続く**class-4 frontier 2度目のsweep**: best class-4 blocker S5 `00000000020000003800000080000000`（18 orbits/1460）の最安未sweep行 cost-74 child `00000000020000003800000080000020`（stones [5,31,59,60,61,89]・cost-74a–74eは他行で使用済み）をcost-74fとしてsweepした。

- **claim前検証（head 1216基準）**: exact-integer D4正準化（8要素二面体群）で子の6個の一石削除を照合 → 開親3個（lift 5: best blocker 18/1460〔mask 4〕・lift 31: `00000000000000801082000000080000` 79/6036〔**mask 5 = class-1+4混合**〕・lift 89: `00000000000000003800000000800020` 69/5346〔mask 5〕・lift 59/60/61は閉行）→ maskビットごと需要 c1=2, c2=0, c4=3（head-1216 top-candidates CSVと一致）。**73f（純粋class-4需要3）と対照的に、本行は2個のmask-5開親を通じてclass-1需要も同時に運ぶ**。IN FLIGHT claim先行push（commit 4bc32165）後に着手。
- **sweep結果（v16 d10・cap 1e9・andclose 1・10バッチ・pilot 3402×10全PASS）**: **74/74候補・WIN7-D10 0件・74 REFUTED-D10・0 capped・総nodes 59,017,987**（74候補==独立Bareiss列挙 bit-exact）。terminal rangeは**全74候補 [13,17]**（73fにあった早期終端行はなし）。batch-6 determinism rerun node-exact、v15交差エンジンのアンカーbits 3/53/118はloss=false（nodes 4013034/4710260/1989273・pilot 5949）。
- **独立監査**: `audit_cost74f_raw_sweep_20261115.py`（stdlibのみ・Bareiss再実装）が12 rawファイルから全件再導出（候補74==claim列挙・各bit 1回・batch-6一致・v15一致・深さ10境界検査合格）に加え、**一石削除D4正準化6件を監査内で独立再導出**（lift 5/31/89の開親・lift 59/60/61の閉行を全件照合）。2回実行byte-identical（md5 d697aa06…・remote blob 9911a5cc…照合済み）。raw 12ファイルもremote git blob sha全件byte-exact照合済み。
- **STERILE（負の実験事実）**: WIN7-D10 receiptなし・fold材料なし・**canonical chain head 1216/6631/523382/4901/387105は不変**。childは3開親（best blocker〔mask 4〕と2個のmask-5行）の未解決S6行のまま。REFUTED-D10はLOSS証明ではなく、この行の反証閉鎖には深さ>10の証拠が必要。
- **class-4 frontierで2行連続STERILE**: best class-4 blocker S5の最安2行（cost-73・cost-74行・計147候補・約1.1億nodes）がともに深さ10以内の先手勝ち候補ゼロ。「class-4 frontier行では深さ10以内のWIN7材料が稀」という作業仮説が強化され、class-4 blocker閉鎖には深さ>10探索か構造的議論が必要になる可能性が高い（観測ベースの仮説・結論ではない）。次候補は同S5の2番目のcost-74行 `00000000020000003800000088000000`（c1=0,c2=1,c4=2）とcost-75行 `00000000020000003800020080000000`（c1=0,c2=0,c4=3）。
- **出版過程の記録**: 監査JSON・claimとも初回pushは手書きtemplate形式だったため、監査JSONを公開監査スクリプトが生成する形式（byte再現可能・md5 d697aa06…）に標準化して再pushした（JSONセマンティクス不変・レイアウトのみの訂正・73f監査訂正と同じ透明性基準）。標準化後のclaimはremote blob `c3f8d9fe…`（全数値・全記述を再取得して検証済み）。
- 並走（着手時点）: cost-65l（bits 21/48証明書出版済み・foldは未）・cost-67c（bits 64/96証明書出版済み・foldは未）・cost-78a・69g/65j/74eはin flightで本sweepと衝突なし。fold時はfold時点のcanonical headへのrebase必須。

解消計数はmanifest被覆の前進であり、盤全体の勝敗ではない。WIN7証明書は個別7石rootの深さ10以内の先手勝ちのみを証明する。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class2・class4は引き続き **UNKNOWN**。

詳細: [sweep log](../../log/2026-11-15-n11-class2-lane-cost74f-sterile-sweep.md)、[sweep audit](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost74f-sweep-audit-20261115.json)、[completed claim](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost74f-inflight-20261115.json)。

## 2026-11-15: cost-67c receipts fold 完成 — canonical chain head 1216→1219

cost-67c sweep（67候補・WIN7-D10 bits 64/96・65 REFUTED・41,942,979 nodes）の証明書付きreceipts 2件を、cost-63g fold後のcanonical chain head **1216/6631/523382/4901/387105** にfoldした。着手前に最新main・AGENTS.md・README・並走レーン（65l/78a/69g/65j/74e）を再確認し、新規fold着地なしを確認（rebase不要）。

- **新canonical chain head: 1219/6628/523173/4898/386896**（`class-frontier-cost67c-receipts-recompute-20261115.json`・remote blob `6d187f48420a9b66d527c3c0fb2764ad5f63235a`・9,323 bytes）。remaining S5 orbits 175不変。total marginal 9 / marginal_in_manifest +3。
- fold script `recompute_frontier_cost67c_receipts_20261115.py`（42,661 bytes）は63g版と同じrunpy chainで1216 headをbyte-identical再現（chain内部で1199 headも再現）し、14入力ファイル＋claimのgit blob sha byte-exact照合、sweep auditをraw 9 batchから再導出（67候補==claim列挙・batch-5 determinism rerun node-exact）、v15 cross-engine anchors（2 WIN sum 7,504,416・3 REFUTED anchors・pilots 5949×5）、証明書2件のbytes再検証（4 parts join-whole md5一致・md5×sha256×git blob・rows 70,480 / bytes 2,546,005 / extraction 11,554,974 / sub-roots 106・terminal 13..17・sub-roots==loser mobility==53）、第三独立監査JSON全項目一致（13 covered orbits・worklist parents・proven_win [64,96]）、root disjointness（112既fold roots・raw+D4両方・2 distinct D4 orbits）をすべて管理。2回実行byte-identical。
- **child軌道 `00000000000000801202000000202000`（混合demand c1=0,c2=1,c4=1・両開親の残行）はbit-64 receipt（公開順最初・covers 7 / marginal 4 / in-manifest 1）で閉鎖**。bit-96 receiptはcovers 7 / marginal 5 / in-manifest 2。set-equality管理 `s_after == s_1216 ∪ covers(2 roots)` 成立。
- **両開親の行喪失をbit-exact検証**: 第二coverable class-2 target S5 `00000000000000801202000000200000` 33行/2470→**32行/2403**（child行のみ）。開class-4 S5 `00000000000000801002000000080800` 76行/5703→**74行/5560**（child行＋`00000000020000003800000040000002`）。bit-96 receiptの交差被覆はさらにclass-2 S5 `00000000000000801202000040000000` 45/3119→44・class-4 S5 `00000000020000003800000040000000` 85/6497→84を削減（`00000000040000003800000088000000`閉鎖）。
- **claim retire v4**: `class2-lane-cost67c-inflight-20261115.json` をstatus `completed`（fold record: chain_head_after・total_marginal 9・total_marginal_in_manifest 3・child_orbit_closed_by_bit 64・parents_after 32行/2403・74行/5560・receipts_folded [64,96]・output blob shas・head_json_bytes 9323）にretire（remote blob `728f929d999fba6d0bed8e037b573d528f99616e`）。fold scriptはcost-76a基準（cost-72b再実行不能事故の教訓）に従いretire後のclaim v4 blobをassertする形で差し替え再push（`01d3ceabd9487e1e3a8da440c08dafea018b55df`）し、retired claimのfold record全項目一致・head JSON byte-identicalを含む再実行を確認済み。以後このscriptはclaim修正なしに恒久的に再実行可能。
- 出力: ranking CSV blob `fa04928a15c62d56fcceae3ce1ef5d670d5365a1`（7,580 bytes）、top-candidates CSV blob `52872558ff4e1d5a0d972a840fedc776fcba460c`（6,039 bytes）。
- **次への指示**: 65l/78a/69g/65j/74eの各foldは新head 1219/6628/523173/4898/386896へのrebase必須。第三target class-2 S5 `00000000000000809102000000000000`（3行/221）の69/74/78行は並走担当。第二coverable target（32行/2403）の次の最安未sweep行は公開済みsterile・in-flightとの照合の上で選定する。best class-4 blocker S5 18行/1460は不変（73f/74fで連続STERILE済み）。

解消計数はmanifest被覆の前進であり、盤全体の勝敗ではない。WIN7証明書は個別7石rootの深さ10以内の先手勝ちのみを証明し、child軌道の閉鎖は両開親の残行を減らすがどちらのS5親も解決しない。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class2・class4は引き続き **UNKNOWN**。

詳細: [fold log](../../log/2026-11-15-n11-class2-lane-cost67c-receipts-fold.md)、[head JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost67c-receipts-recompute-20261115.json)、[retired claim v4](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost67c-inflight-20261115.json)。

## 2026-11-15: cost-78a WIN7証明書5/5出版とreceipt fold — cost-67c head 1219→1225

cost-78a（第3 coverable class-2 target S5 `00000000000000809102000000000000` のcost-78 child `00000000000000809102000000400000`・需要 c1=0,c2=2,c4=0）のsweepで得た5 WIN7-D10 root（bits 8,20,29,36,109）について、既公開2件（bit36/bit20）に加えて残り3件（bit29/bit8/bit109）をblind抽出（空kill table・repo-verbatim v16抽出器）し、BigInt 3x3とNumber Bareiss 4x4の二独立検証器で**5/5 PASS**（sub-roots 59/64/58/62/68・union missing/extra 0/0・terminal [13,17]・fbt_drops 0）。3件の抽出は56,463/75,033/88,039行、16,395,724/25,476,207/27,863,969 nodes。manifest `class2-lane-cost78a-win7-certificates-20261115.json`（blob `b0737084…`）は**326,698行・11,806,510 bytes・97,619,220 extraction nodes・311 sub-roots・31 distinct parent-lift orbits**を記録。

5 receiptsをcost-67c fold後のcanonical head 1219/6628/523173/4898/386896にfoldし、新canonical head **`1225/6622/522699/4892/386422`**（solved 1219→1225・in-manifest marginal 6・raw marginal 26・zero-mimなし）。childは**bit36**で閉鎖。第3 target S5は**3行/221 → 2行/143**（残り69/74）、第2開親 `00000000000000801202000100000000` は**79行/6539 → 73行/6065**（child+5親orbit喪失）。best class-4 blocker S5 `00000000020000003800000080000000` は**18行/1460不変**。best class-2は第3 target（2行/143）で、残る69はcost-69g・74はcost-74eが並走担当。両行がWIN7 receiptで閉じれば第3 target S5が先手WINとなりclass-2 blockerが条件付きで閉鎖されるが、現時点では未fold。**その後、並走cost-69h foldが本78a head 1225にrebaseして1227/6620/522561/4890/386284を確定し、head分岐は解消済み**（cost-69h節参照）。

fold scriptはrunpyでcost-67c chain head 1219をbyte-identicalに再現し（chain内部でcost-63g 1216 headも再現・assert）、25入力+claimのgit blob sha、sweep audit再導出（78候補・5 WIN7/73 REFUTED/0 capped・184,253,822 nodes・pilots 3402×10・determinism rerun node-exact・v15 5/5 WIN+3/3 refuted anchors sum 64,742,220）、manifest totals再合計、114 folded rootsとのraw/D4 disjointness、set等式 `s_after == s_1219 ∪ covers(5 roots)` をassertする。completed claim後の再実行で3出力（head JSON `3938bb16…`・ranking `5579258e…`・top-candidates `f22888a2…`）のbyte-identityとfold数値を再assertする制御付き。この1225 headがcost-69h rebaseの入力としてmainに併存する。

解消計数はmanifest被覆の前進であり、盤全体の勝敗ではない。WIN7証明書は個別7石rootの深さ10以内の先手勝ちのみを証明する。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class2・class4は引き続き **UNKNOWN**。

詳細: [log](../../log/2026-11-15-n11-class2-lane-cost78a-certificates-and-receipt-fold.md)、[certificate manifest](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost78a-win7-certificates-20261115.json)、[fold head JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost78a-receipts-recompute-20261115.json)、[completed claim](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost78a-inflight-20261115.json)。


## 2026-11-15: cost-70d sterile sweep — 第二coverable targetの最安未sweep行・frontier不変・head分岐の指摘

第二coverable class-2 target S5 `00000000000000801202000000200000` の最安未sweep行 cost-70 child `00000000000000801282000000200000`（stones [21,49,55,57,60,71]・5本あるcost-70行で唯一のclass-1需要 c1=1,c2=1,c4=0）をcost-70dとしてsweepした。claim前検証: legal 70 = manifest edge cost 70 bit-exact・D4正準化で開親2個（lift 55 = 第二coverable S5・lift 57 = class-1 S5 `00000000000000801082000000200000` 75/5971）・残り4削除は閉行。**70/70 REFUTED-D10・WIN7-D10 0件・0 capped・総nodes 53,890,941・全候補 terminal [13,17]・pilot 3402×9 PASS**。STERILE: fold材料なし・frontier不変。統制: batch5 determinism rerun node-exact・v15交差エンジン（pilot 5949）でアンカーbits 4/92/114一致（loss=false）。独立監査 `audit_cost70d_raw_sweep_20261115.py`（stdlib Bareiss・repo engine不使用）全assert合格・2回実行byte-identical（md5 `a1739c77…`）・D4重複走査は公開win7 manifest 56ファイル138 canonical rootsと重複0。一石削除D4正準化6件を監査内で独立再導出。

**訂正（cost-74fのK0783追記の次候補記述）**: 74f追記は「class-4 frontierの次候補は同S5の2番目のcost-74行 `00000000020000003800000088000000` とcost-75行 `00000000020000003800020080000000`」と書いたが、この2行は並走により既にSTERILE確定済みだった（cost-74c = `class4-lane-cost74c-sweep` 2026-11-14・cost-75 = `class2-lane-cost75-sterile` 相当・いずれも74/75 REFUTED-D10・0 WIN7）。さらにcost-79行2本 `00000000020000003800000880000000` `00000000020000003800400080000000` も並走cost-79/79bとしてSTERILE確定済み（270,231,378 / 223,708,504 nodes・全REFUTED-D10）。best class-4 blocker S5 `00000000020000003800000080000000` のsweep済み行は73f/74f（自レーン）+74c/75/79/79b（並走）の6行・すべてSTERILE。次の未sweep行はcost-80行2本（`00000000020000003800000180000000` c4=2・`00000000020000003800200080000000` c4=1）。

**head分岐の指摘**: 本claim（head参照1221/6626/523035/4896/386758・commit `bb44940e`）の時点で、並走cost-78a fold head `1225/6622/522699/4892/386422`（commit `1691d9bb`）が既にmainに存在していた。78a foldと69h fold（1219→1221・commit `3d2faf3b`）は**同一baseline head 1219から並行着地**しており、canonical chainが分岐したまま（両head JSONがmainに併存）。70dはSTERILEでfold材料を持たずどちらのchainとも交差しない（70d child行は両chainで開行・2開親は78a foldの影響を受けない）。**次のfold実行者は78a（1225）と69h（1221）のマージrecompute（両fold receiptsを単一chainに再適用）が必須**。

REFUTED-D10はLOSS証明ではない。解消計数はmanifest被覆の前進であり、盤全体の勝敗ではない。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4は引き続き **UNKNOWN**。

詳細: [sweep log](../../log/2026-11-15-n11-class2-lane-cost70d-sterile-sweep.md)、[sweep audit](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost70d-sweep-audit-20261115.json)、[completed claim](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost70d-inflight-20261115.json)。


## 2026-11-15: cost-69h receipts fold と78a headへのrebase — canonical head 1227・head fork解消

cost-69の69候補をcost-69hとしてsweepした（2 WIN7-D10 / 67 REFUTED / 0 capped・総nodes 83,542,525・pilots 3402×9・batch-5 determinism rerun node-exact・v15交差エンジン 2 WIN anchors node一致 sum 7,553,969 + 3 REFUTED anchors bits 64/117/22・pilot 5949）。証明書付きWIN7-D10 receipts 2件（bits 58/96）をcost-67c head 1219へfoldし1219→**1221**（total marginal 10 / in-manifest 2・child `0000000000000080120a000000200000` はbit-58 receiptで閉鎖・第二coverable class-2 S5 `00000000000000801202000000200000` 32行/2403→31行/2334・開class-2 S5 `0000000000000080120a000000000000` 49行/3593→47行/3455（bit-96証明書の交差被覆で2行目も閉鎖））としたが、このfoldは並走cost-78a fold（5 WIN7 receipts bits 36/20/29/8/109・marginal 26/6・head **1225**・第三target S5 `00000000000000809102000000000000` 3行/221→2行/143）と**同一baseline head 1219から並行着地**しており、cost-70d追記の指摘どおりcanonical chainが分岐した。

本レーンは78a laneがcost-67c時と同じrebase手順で本foldを78a head 1225へrebaseし、forkを解消した。**新canonical chain head: `1227/6620/522561/4890/386284`**（= 1225+2・set等式 `s_1227 == s_1219 ∪ covers(5×78a roots) ∪ covers(2×69h roots)`）。total marginal 10（78a分5 + 69h分5）/ in-manifest 2・child閉鎖bit58・parents_after（31行/2334・47行/3455）はすべて1219→1221 foldと同一で、78a coversと69h coversの被覆重なりは0。rebase版fold scriptは78a公開4ファイル（head JSON・両CSV・completed claim）のgit blob sha byte-exact照合の後、78a foldを純幾何（covers()/canon()のみ・repo engine不使用）で再導出し（per-receipt marginal counts・marginal hex lists全一致・summary/parents/両CSV byte-identical再生成）、69h入力の全面検証（sweep audit再導出・証明書2件parts-join-whole bytes・第三独立監査）、119 folded roots（98+14+2+5）と69h 2 rootsのraw/D4双方でのdisjointness、1225上のfoldを実行する。78a証明書bytes（約12MB）は実行環境cgroup 1GB制限のため再検証せず、78a lane自script検証済みである旨をmethod文字列に明記した。claimはv4としてretire（chain_head_before `1225/…`・chain_head_after `1227/…`・head JSON remote blob `d25eb3a0…` 11,295 bytes）、v3（1221歴史fold record・output blobsは定数保存）は歴史controlとしてscriptに残し、CLAIM_BLOBS_RETIREDへ両blobを登録したdual controlで恒久再実行可能化した。retire後再実行でhead JSON byte-identical含む全control PASS、3出力の2回実行byte-identical。

fold後frontier: best coverable class-2 = 第三target S5 `00000000000000809102000000000000` **2行/143**（残り69行はcost-69g・74行はcost-74eが並走担当）・第二coverable 31行/2334（次の最安未sweep行はclaim列挙による重複排除を最初に実施して選定）・audit-blocked class-2 S5 `00000000000000809082000000000000` 10行/698・best class-4 blocker S5 `00000000020000003800000080000000` 18行/1460（73f/74f/74c/75/79/79b/70dすべてSTERILE）。**以後のrecompute/claim（65l/69g/65j/74e等の未着地foldを含む）は新head `1227/6620/522561/4890/386284` をassertして拡張すること**。

REFUTED-D10はLOSS証明ではない。解消計数はmanifest被覆の前進であり、盤全体の勝敗ではない。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class2・class4は引き続き **UNKNOWN**。

詳細: [log](../../log/2026-11-15-n11-class2-lane-cost69h-receipts-fold.md)、[fold head JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost69h-receipts-recompute-20261115.json)、[completed claim](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost69h-inflight-20261115.json)。

## 2026-11-15: 78a+69h merged headの第三独立検証 — fold順可換・二重被覆0・CSV byte-identical第三一致

cost-70d追記の指摘した78a head 1225と69h head 1221のforkは、前節のとおり並走rebase（69h foldを78a headに適用しcanonical head 1227/6620/522561/4890/386284）で解消済み。本レーンはこのmerged headを**並走rebase手法と独立の第三手法**で再構成・検証した。merge script `recompute_frontier_merged_cost78a_69h_20261115.py`は、cost-67c chain head 1219をrunpy 1回でbyte-identical再現（blob `6d187f48…` assert）した後、両branch head JSON（78a `3938bb16…`・69h rebase v2 `d25eb3a0…`）をgit blob shaで検証し、7 receipt roots（78a bits 36/20/29/8/109 + 69h bits 58/96）をcovers()で再計算、fork 1219から単一順でreplayする。全検証PASS: per-bit marginals published一致・child閉鎖 bit36/bit58・addA=26/addB=10・raw overlap 0・**covers overlap 0（二重被覆なし）**・set等式 `s_merged == sA∪sB == sF∪cov7`・**逆順replay（69h→78a）も同一結果（fold順可換）**・**merged head数値 == 並走rebase head数値 1227/6620/522561/4890/386284（第三一致）**。

さらに本scriptが再生成した**ranking CSV（md5 `f248573f9afd378dc3142bb36e488119`）とtop-candidates CSV（md5 `43ceb46eecd84e9fc1c29407d34115ce`）は、並走rebase v2版の両CSVとbyte-identical**（第三一致を数値一致から出力byte一致に格上げ）。3回実行すべてbyte-identical（merged head JSON md5 `bea292d0fed96c67fb707eb4c2165730`・git blob `294c4ed3…`）。**環境知見**: 両fold scriptを同一プロセスでrunpy実行するとcgroup 1GB制限でOOMする（exit 137・78a証明書bytes検証がメモリピーク）ため、blob検証済みhead JSON 2件からrootsを再取得してfork 1219からcovers()で再構成する方式を取った（1回約10秒で完走）。以後のfold（65l/69g/65j/74e等）は引き続き新head 1227をassertして拡張すること。

REFUTED-D10はLOSS証明ではない。解消計数はmanifest被覆の前進であり、盤全体の勝敗ではない。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4は引き続き **UNKNOWN**。

詳細: [log](../../log/2026-11-15-n11-merged-frontier-78a-69h-independent-verification.md)、[merged head JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-merged-cost78a-69h-recompute-20261115.json)。

## 2026-11-15: cost-70e raw sweep第三独立監査 — WIN7-D10 5 roots・D4重複0・証明書待ち

cost-70e（第二coverable class-2 target S5 `00000000000000801202000000200000` の最安未sweep cost-70 child `00000000000000801202000000200004`・stones [2,21,49,57,60,71]・需要 c1=0,c2=2,c4=0・両開親class-2・head 1227でclaim `14970683`）の並走raw sweep（batch1-9・v16 determinism rerun・v15 crosscheck・総nodes 83,656,928）について、第三独立監査 `audit_cost70e_raw_sweep_20261115.py`（stdlib Bareiss・70d監査geometry流用+70e用新規実装・repo engine不使用）を実施した。**全assert合格**: 独立legal再列挙70がclaimとbit-exact・batch bits 1-9がengine計画と一致・pilot 3402×9・**WIN7-D10 bits [0,8,24,66,79]（nodes 4,596,984/1,333,433/2,197,162/1,763,979/1,765,453）・REFUTED 65・capped 0**・全候補 terminal [13,17]・determinism rerun（batch5）node-exact一致・v15交差エンジン 5/5 WIN loss=true + 3 REFUTEDアンカー（bits 113/75/86）loss=false一致・**WIN 5 rootsのD4正準形は互いにdistinct、かつ公開win7証明書manifest 58ファイル・canonical roots 145個と重複0（すべて新規fold材料候補**・bit0 `00000000000000801202000000200005`・bit8 `00000000000000801202000000200104`・bit24 `00000000000000801202000001200004`・bit66 `00000000000000841202000000200004`・bit79 `00000000000080801202000000200004`）。一石削除D4正準化6件を独立再導出（del-2 = parent1 bit-exact 31行/2334・del-21 = class-2 S5 `00000000000000003800000008400000` 49行/3625・del-49/57/60/71 はhead-1227 ranking CSV（175 open）に不在の閉行）・head-1227 top-candidates CSVのchild行 demand c1=0,c2=2,c4=0・edge cost 70照合。監査2回実行byte-identical（md5 `a75a4dcc306b3a9fa17224fe1265cb05`）。

**証明書待ち**: 5 WIN rootsはfold材料候補だが、foldには blind抽出・独立検証済みWIN7証明書manifestの出版が先決（78a/69hと同じ手順）。出版までhead 1227/6620/522561/4890/386284不変。REFUTED-D10 65件はLOSS証明ではなく、child行は両開親の未解決行のまま。解消計数はmanifest被覆の前進であり、盤全体の勝敗ではない。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4は引き続き **UNKNOWN**。

詳細: [log](../../log/2026-11-15-n11-class2-lane-cost70e-raw-sweep-audit.md)、[sweep audit](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost70e-sweep-audit-20261115.json)。

## 2026-11-15: cost-82b sterile sweep — blocker S5連続STERILE 14行目・70d追記の次候補訂正

**訂正（cost-70d追記の次候補記述）**: 70d追記は「best class-4 blocker S5 `00000000020000003800000080000000` の次の未sweep行はcost-80行2本（`00000000020000003800000180000000` c4=2・`00000000020000003800200080000000` c4=1）」と書いたが、この2行は2026-11-14に並走により既にsweep済みSTERILEだった（cost-80: 80 REFUTED-D10・290,092,122 nodes・cost-80c: 80 REFUTED・220,291,094 nodes）。さらにcost-81（child `00000000020000003800000080008000`・325,836,995 nodes）・cost-82（child `00000000020000003800000080000800`・335,027,684 nodes）・cost-86a/b/c（children `...80000100`/`...80004000`/`...0280000000`・373,903,515/344,931,733/301,085,672 nodes）も同日STERILE確定済みで、18行のうち13行までがsweep済みだった。74f追記の訂正（74c/75/79/79b既にSTERILE）に続き、**次候補記述は公開sweep JSON（`class4-lane-cost{N}-sweep-20261114.json`）との突合を要する**。

実際の最安未sweep行 cost-82行2本目 **`00000000020000003800000090000000`**（stones [28,31,59,60,61,89]・需要 c1=0,c2=0,c4=3・3開親すべてclass-4: blocker S5 18行/1460・`00000000000000901002000000080000` 88行/6966・`00000000000000003800000004800000` 87行/6833）をcost-82bとしてsweepした（claim `5e1427b6`・IN FLIGHT先行push・head 1227基準・cost-82の名前は`...80000800`行の2026-11-14 STERILE sweepが使用済みのため82b）。claim前検証: legal 82 = manifest edge cost 82 bit-exact・D4一石削除で開親3個（mask 4×3）・残り3削除（59/60/61）はhead-1227 ranking CSV上の閉行。**82/82 REFUTED-D10・WIN7-D10 0件・0 capped・総nodes 68,922,913・全候補 terminal [13,17]・pilot 3402×11 PASS**。STERILE: fold材料なし・frontier不変（head 1227不変）。統制: batch5 determinism rerun node-exact・v15交差エンジン（pilot 5949）で最重REFUTEDアンカー bits 118/7/2 一致（loss=false・nodes 5,796,536/11,259,120/9,262,419）。独立監査 `audit_cost82b_raw_sweep_20261115.py`（stdlib Bareiss・70d/70e監査geometry流用・repo engine不使用）全assert合格・2回実行byte-identical（md5 `e2c64baf…`）・一石削除D4正準化6件を監査内で独立再導出・head-1227両CSVとparent行・需要行照合。

blocker S5の連続STERILE記録は**14行目**（73f/74f/74c/75/79/79b/80/80c/81/82/86a/86b/86c/82b）。未sweepは4行: cost-84 `00000000020000003800000080000400`（c4=3）・cost-86 `00000000020000003800100080000000`（c4=3）・cost-86 `00000000020000003840000080000000`（c4=3）・cost-87 `00000000020000003800000080000004`（c4=3）。**次の最安未sweep行はcost-84行**。18行すべてがSTERILEでもblocker S5自体は解決しない（各行の反証には深さ>10の証拠が必要）が、depth-10負の実験事実の蓄積はblocker閉鎖探索の指針となる。

REFUTED-D10はLOSS証明ではない。解消計数はmanifest被覆の前進であり、盤全体の勝敗ではない。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4は引き続き **UNKNOWN**。

詳細: [sweep log](../../log/2026-11-15-n11-class4-lane-cost82b-sterile-sweep.md)、[sweep audit](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class4-lane-cost82b-sweep-audit-20261115.json)、[completed claim](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class4-lane-cost82b-inflight-20261115.json)。
## 2026-11-15: cost-70e WIN7証明書5件出版 — bit8/bit0決定論的再生成・第三独立監査PASS・foldは次回

cost-70e（child `00000000000000801202000000200004`・両開class-2親・head 1227）のsweepで得られた5 WIN7-D10 roots（bits 0/8/24/66/79）のn11-terminal-strategy-v1証明書5件を出版した。**rows合計 236,784**（bit0 67,895 / bit8 47,877 / bit24 46,324 / bit66 36,897 / bit79 37,791）・bytes 8,564,174・extraction nodes 20,246,025（blind・空kill table・fbt_drops 0・sub-roots 280）。manifest `class2-lane-cost70e-win7-certificates-20261115.json`（remote blob `9f8e5a93…`・20,309 bytes）にper-cert全hashes（whole md5/sha256/git blob・10 parts {path,bytes,md5,git_blob_sha}）・loser_first_moves（60/63/56/49/52）・d4_parent_orbits（各7）・v15 anchor nodes（9,207,684/2,959,509/5,448,943/4,399,834/5,230,712）を記録。

抽出sessionでbit24/66/79の6 partは着地済みだったが、bit8/bit0の4 partはsandbox resetでローカル成果物を喪失していたため、**repo-verbatim `class4_child1_cert_extractor_exact_v16.ts`（remote blob `5518d375…`）+ 独立実装の合法loser初手列挙（5 rootすべてsweep auditのmobilityと一致）+ 新driver `cert_driver70e.ts`で5証明書すべてを一から再生成**した。bit8 47,877行/2,317,958 nodes・bit0 67,895行/7,777,721 nodesは前セッション記録値とnode数まで完全一致（v16 extractor特定の根拠: `class4_child1_cert_extractor_exact.ts` ではbit66が7,266,956 nodesとなり記録値3,142,163と不一致）。bit24/66/79も再抽出して公開済みparts join全体とbyte-exact一致し、5/5でpipeline再現性を実証。split規約（part1 = header 2行 + ceil(rows/2)行）を既知3証明書のpart blob shaから特定し、bit8/bit0の4 partが期待git blob sha `04d7ddbb`/`c45d058d`/`38dc49aa`/`1ca00ce2` と完全一致のうえ着地。

**検証3層**: (1) `verify_win7_certificate_bigint_independent.mjs` 5/5 PASS（subroots 60/63/56/49/52・union 0/0・terminal [13,17]）。(2) 第三独立監査 `audit_cost70e_certificates_third_independent_20261115.mjs`（remote blob `0b4b9a50…`・69h版の5証明書拡張・BigInt有理中心分子＋共線分岐・入力7ファイル+S6 manifest 6 partsをgit blob sha pin）**全check合格**: DAG replay union 0/0・terminal [13,17]・parent orbits 31（incidences 35・共有はchild S6 orbitのみ・worklist 11/20）・child manifest cost 70/classes "2"・開親2個（parent1 `00000000000000801202000000200000` 31行/2334・parent2 `00000000000000003800000008400000` 49行/3625）・top-candidates child行照合・claim snapshot照合（出力 remote blob `6727eb65…`）。(3) sweep audit `47d38c00…`（並走監査版）のwin7_d10_bits・root mobility・D4正準形との一致を監査内で再確認。

claim `class2-lane-cost70e-inflight-20261115.json` はv2としてretire（remote blob `b857b635…`・status completed・sweep_results + win7_certificates追記）。**foldは未実施**: 5 receiptsはparent1・parent2両開frontierのfold材料だが、fold実行時は最新main再取得・canonical head再assert・rebaseが必須（並走65l/class4-84等の着地可能性）。5 rootsは既fold 121 roots（98 pre-63g + 14 cost-63g + 2 cost-67c + 5 cost-78a + 2 cost-69h）とraw・D4正準形双方でdisjoint。**head 1227/6620/522561/4890/386284不変**（第三target 2行/143・第二coverable 31行/2334・parent2 49行/3625・audit-blocked 10行/698・class-4 blocker 18行/1460）。5 WIN7は個別7石rootのdepth-10 first-player winのみを証明し、どのS5/S6行も解決しない。REFUTED-D10 65件はWIN7-D10不在のみを意味する。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4は引き続き **UNKNOWN**。

詳細: [log](../../log/2026-11-15-n11-class2-lane-cost70e-win7-certificates.md)、[manifest](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost70e-win7-certificates-20261115.json)、[第三独立監査](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/cost70e-third-independent-certificate-audit-20261115.json)。

## 2026-11-15: cost-84 sterile sweep — blocker S5連続STERILE 15行目・残り3行

best class-4 blocker S5 `00000000020000003800000080000000`（head 1227で18行/1460）のcost-82b完了後の最安未sweep行 cost-84 **`00000000020000003800000080000400`**（stones [10,31,59,60,61,89]・需要 c1=0,c2=0,c4=3・3開親すべてclass-4: blocker S5 18行/1460・`00000000020000003800000000000400` 88行/7388・`00000000000000003800000000800001` 85行/7023）をsweepした（claim `3c08ca67`・IN FLIGHT先行push・head 1227基準）。claim前検証: legal 84 = manifest edge cost 84 bit-exact・D4一石削除で開親3個（mask 4×3・del 10 = blocker S5 bit-exact）・残り3削除（59/60/61）はhead-1227 ranking CSV上の閉行。**84/84 REFUTED-D10・WIN7-D10 0件・0 capped・総nodes 108,689,432・全候補 terminal [13,17]・pilot 3402×11 PASS**。STERILE: fold材料なし・frontier不変（head 1227不変）。統制: batch5 determinism rerun node-exact・v15交差エンジン（pilot 5949）で最重REFUTEDアンカー bits 66/34/86 一致（loss=false・nodes 4,040,549/9,695,280/5,532,140）。独立監査 `audit_cost84_raw_sweep_20261115.py`（stdlib Bareiss・82b監査流用・repo engine不使用）全assert合格・2回実行byte-identical（md5 `ba408eef…`）・一石削除D4正準化6件を監査内で独立再導出・head-1227両CSVとparent行・需要行照合（commit `aafd0602`・raw 11バッチ+rerun+crosscheck+claim+audit+logの17ファイル一括push）。

blocker S5の連続STERILE記録は**15行目**（73f/74f/74c/75/79/79b/80/80c/81/82/86a/86b/86c/82b/84）。未sweepは3行: cost-86 `00000000020000003800100080000000`（c4=3）・cost-86 `00000000020000003840000080000000`（c4=3）・cost-87 `00000000020000003800000080000004`（c4=3）。いずれもc4=3需要。18行すべてがSTERILEでもblocker S5自体は解決しない（各行の反証には深さ>10の証拠が必要）が、depth-10負の実験事実の蓄積はblocker閉鎖探索の指針となる。

REFUTED-D10はLOSS証明ではない。解消計数はmanifest被覆の前進であり、盤全体の勝敗ではない。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4は引き続き **UNKNOWN**。

詳細: [sweep log](../../log/2026-11-15-n11-class4-lane-cost84-sterile-sweep.md)、[sweep audit](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class4-lane-cost84-sweep-audit-20261115.json)、[completed claim](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class4-lane-cost84-inflight-20261115.json)。

## 2026-11-15: cost-70e WIN7証明書5件の検証器レベル独立監査 — 5/5 PASS・fold待ち

第二coverable class-2 target S5 `00000000000000801202000000200000` のcost-70 child `00000000000000801202000000200004`（edge cost 70・需要 c1=0,c2=2,c4=0）のsweepが得た5 WIN7-D10 roots（bits 0,8,24,66,79）の証明書5件（各2 part）を、公開partの行境界連結・CRLF→LF正規化の上で**BigInt 3x3余因子**と**Number Bareiss 4x4**の二独立検証器により再検証した。**5/5 PASS**（sub-roots 60/63/56/49/52・union missing/extra 0/0・terminal [13,17]・consumed union == 証明書行集合 0/0）。合計**236,784行・8,564,174 bytes・280 sub-roots・31 distinct parent-lift orbits**、5 rootのD4 canonicalはdistinct、child orbitは全証明書に含まれる。上記の並走第三独立監査（DAG replay版）とは別実装の検証器レベル監査であり、両監査の数値は一致する。

本監査はfoldの代わりではない。canonical head 1227/6620/522561/4890/386284は不変で、childは両開親の未解決S6行のまま。cost-70eのreceipt foldはfold時点のcanonical headへのrebaseが必須。REFUTED-D10はLOSS証明ではなく、WIN7証明書は個別7石rootの深さ10以内の先手勝ちのみを証明する。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4は引き続き **UNKNOWN**。

詳細: [audit log](../../log/2026-11-15-n11-class2-lane-cost70e-certificates-third-independent-audit.md)、[audit JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost70e-certificates-third-independent-audit-20261115.json)、[audit script](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost70e_certificates_third_independent_20261115.py)。

## 2026-11-15: cost-70e receipts fold 完成 — chain head 1227 → 1233・claim v3 retire・baseline 1227の純幾何独立再構成

cost-70e（child `00000000000000801202000000200004`）の5 WIN7-D10 receipts（bits 0/8/24/66/79）をcanonical head 1227/6620/522561/4890/386284にfoldした。fold script `recompute_frontier_cost70e_receipts_20261115.py`（remote blob `df5be7fefce1f28e5798a5903660799575c86b66`）。**新canonical chain head: 1233/6614/522131/4884/385854**（head JSON remote blob `a0171d4bb839aeb813d231c7d879d6a89452359f`・ranking CSV `33fe27c1e2664ac7644a1eff00df649cb38efe1c`・top-candidates CSV `4561af13ce0dd743051e5f3485ea040438a3d908`）。

- publication order [0, 8, 24, 66, 79]・total marginal 26（in-manifest 6）・per-bit marginal 5/5/6/6/4・in-manifest 1/1/2/2/0。**bit0 receiptがchild orbit本体を閉鎖**。
- parent1 `00000000000000801202000000200000` は31行/2334 → **28行/2119**、parent2 `00000000000000003800000008400000` は49行/3625 → **45行/3340**。両開親からchild行が落ちたことをbit-exact検証。solved 1227 → 1233・hist c2=2,c4=0 は965 → 959。
- fold実行前にbaseline 1227を**52個の公開head JSON（402 chain roots）から純幾何（covers()/canon()）で独立再構成**し、両CSV byte-identical再現（staged controls 638/657/665/814 PASS・merged head `294c4ed3`込み）。以後のfold検証はrunpy再帰鎖に依存せず、入力git blob sha照合＋純幾何だけで完結する。
- 統制: 117入力のgit blob sha照合、sweep再導出（70候補・5 WIN7-D10 / 65 REFUTED / 0 capped・nodes 83,656,928）、det rerun batch5 node-exact、v15 cross-engine anchors（win sum 27,246,682・refuted 75/86/113・pilots 5949×2）、証明書5件parts-join-whole再検証（md5×sha256×git blob・236,784行・280 sub-roots・d4 parent orbits == covers() 7軌道each・BigInt union 0/0）、第三独立監査PASS cross-check、root disjointness（5 roots vs 492既fold roots）、set-equality + reverse-order replay PASS。
- fold後frontier: best coverable class-2 は第3target `00000000000000809102000000000000`（2行/143）、second はparent1（28行/2119）。best class-4 blocker 18行/1460・audit-blocked 10行/698 は不変。
- claim `class2-lane-cost70e-inflight-20261115.json` はv3としてretire（remote blob `9c27cff582e84159aace369b60cfe4543e788bbf`・schema v3・top-level `fold`レコード追記・win7_certificates.fold PENDING→COMPLETED）。
- 並走cost-65l fold-in-flight（bits 21/48・head 1227ベース）が着地すると1227ベースforkとなるため、**次回のfold/mergeは最新main再取得後に78a+69hと同じ統合rebase手順が必要**。cost-86d（class4）も並走in flight。

REFUTED-D10はLOSS証明ではない。解消計数はmanifest被覆の前進であり、盤全体の勝敗ではない。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4は引き続き **UNKNOWN**。

詳細: [fold log](../../log/2026-11-15-n11-class2-lane-cost70e-receipts-fold.md)、[head JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost70e-receipts-recompute-20261115.json)、[claim v3](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost70e-inflight-20261115.json)。

## 2026-11-15: cost-70g sweep 完成 — 8 WIN7-D10 / 62 REFUTED・v15交差11/11・全8証明書のblind抽出・独立検証・byte-exact push（fold待ち）

第二coverable class-2 target S5 `00000000000000801202000000200000`（head 1233で28行/2119）の第2未sweep cost-70 child `00000000000100809002000000000800`（stones [11,49,60,63,71,80]・edge cost 70・需要 c1=0,c2=2,c4=0・第2開親 `00000000000000801202010000000000` 60行/4342）をsweepした（claim `class2-lane-cost70g-inflight-20261115.json`・head 1233基準・cost-70シリーズ7番目の別child）。claim前検証はhead 1233の純幾何再導出の上、6一石削除のD4正準化で開親2個のみ（80削除=parent1 bit-exact・11削除=第2親に正準化、49/60/63/71削除は閉行）、legal 70 = manifest edge cost 70 bit-exact。

**8 WIN7-D10（bits 9/20/29/34/62/70/76/119）・62 REFUTED・0 capped・総nodes 63,592,195（win sum 15,922,270）・全候補 terminal [13,17]・pilot 3402×9 PASS**。統制: batch5 determinism rerun node-exact（WIN bit62込み）・v15交差エンジン（repo blob `8744fc65…`・pilot 5949×11 PASS）で**8 WIN bitsすべてloss=true、最重REFUTED 3アンカー（bits 6/86/98）もloss=false、11/11判定一致**（v15総nodes 92,419,285・`class2-lane-cost70g-v15-crosscheck-20261115.jsonl`）。8 WIN7 rootのGitHub code search は**8/8で0 hits（新規coverage）**。

**全8 rootのn11-terminal-strategy-v1証明書をblind抽出**（repo-verbatim extractor blob `5518d375…` + `cert_driver70g.ts`＝70e driverのimport行差分・空kill table・FBS 1<<20・fbt_drops 0・fatalなし）。**rows合計 302,270**（bit9 51,456 / bit20 16,902 / bit29 44,195 / bit34 56,345 / bit62 26,591 / bit70 19,456 / bit76 45,917 / bit119 41,408）・extraction nodes 31,812,232・loser初手 60/46/54/63/51/49/55/56（BigInt独立列挙）。検証: `verify_win7_certificate_bigint_independent.mjs`（blob `62b5d941…`）で**8/8 PASS**（root stones=7+safe・mobility一致・全sub-roots PASS・union 0/0・rows sorted unique・terminal [13,17]）。pushは `class2-lane-cost70g-certificates/` に8件、**全remote blob shaがローカルgit hash-objectとbyte-exact一致**。manifest `class2-lane-cost70g-win7-certificates-20261115.json` にper-cert詳細。

**foldは未実施（PENDING）**: 並走cost-70f（raw batches着地済み・sweep record待ち）とhead-1227ベースcost-65l fold-in-flightの着地を待つ。fold時は最新main再取得・canonical head再assert・（65l着地済みなら）78a+69h流の統合rebaseが必須。receiptsは両開class-2親（parent1 28行/2119・第2親60行/4342）を同時に進める材料。sweep record `class2-lane-cost70g-sweep-20261115.json`（v2）・claim v3（sweep+certificates completed）で反映済み。

REFUTED-D10はLOSS証明ではない。8証明書は個別7石rootのdepth-10先手勝ちのみを証明し、fold前はどのfrontier数も変えない。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4は引き続き **UNKNOWN**。

詳細: [sweep log](../../log/2026-11-15-n11-class2-lane-cost70g-sweep-certificates.md)、[sweep record](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost70g-sweep-20261115.json)、[certificate manifest](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost70g-win7-certificates-20261115.json)、[claim v3](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost70g-inflight-20261115.json)。

## 2026-11-15: cost-71c sweep 完成 — 2 WIN7-D10 / 69 REFUTED・両証明書の二重独立検証・byte-exact push（fold待ち）

第二coverable class-2 target S5 `00000000000000801202000000200000`（head 1233で28行/2119）の最安未sweep cost-71 child `00000000000000801202000080200000`（stones [21,31,49,57,60,71]・edge cost 71・需要 c1=0,c2=2,c4=0・両開親ともclass-2: del31=parent1 bit-exact、del21→第2開親 `00000000000000801202000080000000` 43行/3268）をsweepした（claim `class2-lane-cost71c-inflight-20261115.json`・head 1233基準）。

**2 WIN7-D10（bits 24/112）・69 REFUTED・0 capped・総nodes 94,128,613（win sum 4,442,926）・pilot 3402×9 PASS**。統制: batch5 determinism rerun node-exact、v15交差エンジン（bits 24/112 loss=true 2,695,796/14,334,967・最重REFUTEDアンカー75/113/116 loss=false・pilot 5949）、独立監査 `class2-lane-cost71c-sweep-audit-20261115.json`（71候補bit-exact・aggregate再導出・batch計画一致・D4重複scan 49 manifests/126 roots 0重複・head-1233 ranking/top-candidates CSV cross-check・一石削除lift検証）。

**両WIN rootのn11-terminal-strategy-v1証明書をblind抽出**（repo-verbatim extractor blob `52bcaf509ea12fad4c936501d30d26b5b66c0085`・driver `cert_driver71c.ts`・空kill table・FBS 1<<20・fbt_drops 0）: bit24 root `00000000000000801202000081200000` 22,196行（md5 `9e63e160ba08a7edc827b81dbf9067a5`）・bit112 root `00010000000000801202000080200000` 60,406行（md5 `e38d80cfd89ccc8e48264c36a9e7701a5`）・総82,602行・extraction nodes 24,639,331。**二重独立検証PASS**: BigInt余因子検証器（blob `62b5d941…`・47/56 sub-roots・union 0/0・terminal [13,17]）とPython/Bareiss再プレイ検証器 `verify_cost71c_win7_bareiss_independent.py`（全loser応手展開・インクリメンタル forbidden mask・戦略行集合厳密閉包・union 0/0・terminal {13,15,17}）。環境リセット越えで再抽出が同一md5（determinism control）。pushはbit24単一ファイル（804,827B）・bit112は行境界2分割（part md5 `8ae38925…`/`832120f7…`・join==whole md5確認）、全着地をmd5照合。manifest `class2-lane-cost71c-win7-certificates-20261115.json` にper-cert詳細。

**foldは未実施（PENDING）**: 最新main再取得・canonical head 1233再assert・（並走65l/70f/70g fold着地済みなら）78a+69h流の統合rebaseが必須。receiptsは両開class-2親（parent1 28行/2119・第2親43行/3268）を同時に進める材料。claim v2（sweep+certificates completed・fold pending）で反映済み。

REFUTED-D10はLOSS証明ではない。2証明書は個別7石rootのdepth-10先手勝ちのみを証明し、fold前はどのfrontier数も変えない。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4は引き続き **UNKNOWN**。

詳細: [sweep log](../../log/2026-11-15-n11-class2-lane-cost71c-sweep-certificates.md)、[sweep audit](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost71c-sweep-audit-20261115.json)、[certificate manifest](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost71c-win7-certificates-20261115.json)、[claim v2](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost71c-inflight-20261115.json)。

## 2026-11-15: cost-71c receipts fold — head 1233→1235（2 receipts・総marginal 10・child orbit closure）とbit112 md5誤記の検出・訂正

`recompute_frontier_cost71c_receipts_20261115.py`（122公開入力をgit blob shaでbyte-exact検証・純幾何baseline再構成）でcost-71c receipts foldを実施した。baselineはhead 1233（70e fold head・blob `a0171d4b`）。統制: 52 pre-70e head JSONsから402 chain rootsで1227 merged headを再構成しstaged controlsとmerged CSV byte-identical再生成、**70e fold（bits [0,8,24,66,79]）をaddition recordsとper-record marginal完全一致で再導出**して1233に到達し70e head CSVもbyte-identical再生成、71c child（`00000000000000801202000080200000`・cost 71・c1=0,c2=2,c4=0）の両開親での残存（parent1 28行/2119・第2親 43行/3268・holderはこの2親のみ・del31/del21 D4 lift・残り4削除は閉行）、9 raw batchesからのsweep再導出（**2 WIN7-D10 bits 24/112・69 REFUTED・0 capped・94,128,613 nodes**・pilot 3402×9・batch5 determinism node-exact・v15 cross-engine 2,695,796/14,334,967・アンカー75/113/116 loss=false・D4 duplicate scan 126 roots 0重複）、両証明書の検証（bit24単一ファイル・bit112 2分割join・rows sorted-unique・sub-roots==mobility 47/56・BigInt/Bareiss verify記録union 0/0・root−追加石→child）、2新root vs **497 fold済みroot**のraw+D4 disjointness、公開順 [24,112] fold（bit24 marginal 5/in-manifest 1〔child〕・bit112 marginal 5/in-manifest 1〔`00000000210000003800000000000200`〕）。

**fold後 head: solved 1235 / unique 6612 / cost 521,988 / open 4,882 / open_cost 385,711（hist c2=2,c4=0=957）**。parent1 26行/1976・第2親42行/3197。head JSON [class-frontier-cost71c-receipts-recompute-20261115.json](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost71c-receipts-recompute-20261115.json)・ranking/top-candidates CSVs・fold scriptをpush、claim v3（fold record込み）で反映。

**bit112全体md5誤記を検出**: 公開6文書（manifest・claim v2・sweep audit・certificates README・前log・前節）のbit112全体md5が末尾に余分な`5`の付いた33文字 `e38d80cfd89ccc8e48264c36a9e7701a5` だった。真値は32-hex `e38d80cfd89ccc8e48264c36a9e7701a`（join bytesから再導出・sha256 `314c456b…`・fold scriptがassert）。part md5・join・証明書バイト・両独立検証PASS・fold算術には影響なし。履歴文書はbyte-unmodifiedのまま[md5 erratum](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost71c-md5-erratum-20261115.json)とclaim v3で訂正。**教訓: 記録するmd5は計算値を直接機械転記し、文字数（32/40/64）を検証すること**。

REFUTED-D10はLOSS証明ではない。2証明書は個別7石rootのdepth-10先手勝ちのみを証明する。solved 1235はmanifest被覆の簿記であり盤全体の勝敗ではない。**標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4は引き続きUNKNOWN**。次のfold baselineはhead 1235。未fold: cost-65l（bits 21/48・証明書本体未push）・cost-70f（fold未）等。

詳細: [fold log](../../log/2026-11-15-n11-class2-lane-cost71c-receipts-fold.md)。

## 2026-11-15: cost70f / cost70g / cost71c cross-lane D4 receipt overlap — one duplicate root, eight shared parent orbits

3つのcertificate manifestを、11×11 D4の8変換をBigInt 121-bit boardへ適用して横断照合した。cost70fの公開 `parent_lift_orbits` は削除一石から再計算した全一覧と一致。cost70g・cost71cはmanifestに親一覧がないためrootから独立導出した。

- cost70f: 4 root軌道・28親lift incidence・25一意親軌道
- cost70g: 8 root軌道・56 incidence・49一意親軌道
- cost71c: 2 root軌道・14 incidence・13一意親軌道

**cost70f bit84 と cost70g bit29 は同一D4 root**（正準形 `00000000000100809002000020000800`）。raw bitboardは異なるため、raw hex検索だけでは検出できない。cost70gはcost70fとの間でroot 1軌道、六石親lift 8軌道が重複する。親liftの8軌道は、重複rootの7親と、追加の `00000000000000c09002000000000800`（cost70f bit72 / cost70g bit70）に分解される。

cost71cのroot・親liftはcost70f/70gのいずれとも交差しない。3 laneの親lift和集合は79軌道、root和集合は13軌道。

**fold順への含意**: cost70fを先にfoldすると、cost70g child `00000000000100809002000000000800` はcost70f bit84の親liftとして既に被覆される。後続cost70g foldではこれを二重計上しない。cost70gの追加分はcost70fとの差としてroot 7軌道・親lift 41軌道だが、41はhead 1235の新規manifest coverageではない。実際のmarginalはcanonical headの全被覆集合とfold scriptで再計算する必要がある。

この監査はmanifestのD4集合関係であり、certificate payloadの再検証やfrontier foldではない。solved数・open class数・勝敗statusは変更しない。

詳細: [cross-lane D4 audit](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/cost70f-70g-71c-cross-lane-d4-overlap-20261115.json)、[reproduction script](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost70f_70g_71c_cross_lane_d4_overlap_20261115.mjs)、[log](../../log/2026-11-15-n11-class2-cross-lane-d4-receipt-overlap.md)。

## 2026-11-15: cost-70f sweep・WIN7証明書4件・receipt fold — head 1235→1239

第二coverable class-2 target S5 `00000000000000801202000000200000` のcost-70 child `00000000000000801202000002200000`（stones [21,25,49,57,60,71]・需要 c1=0,c2=2,c4=0）をcost-70fとしてsweepした。**70/70候補・WIN7-D10 4件（bits 9,64,72,84）・66 REFUTED-D10・0 capped・81,480,831 nodes**、pilot 3402×9・batch-5 determinism rerun node-exact・v15交差エンジン4 WIN+3 refuted anchors一致。独立監査 `audit_cost70f_raw_sweep_20261115.py` が9 raw batchから全件再導出（候補70 bit-exact・D4重複0・一石削除6件・head-1233 CSV照合）。

4 WIN rootsをblind抽出（空kill table・repo-verbatim v16抽出器）し、**BigInt 3x3 + Number Bareiss 4x4の二独立検証器で4/4 PASS**（sub-roots 57/48/55/54・union 0/0・terminal [13,17]・fbt_drops 0）。manifest `class2-lane-cost70f-win7-certificates-20261115.json` は**155,155行・5,601,978 bytes・26,952,264 extraction nodes・214 sub-roots・25 distinct parent orbits**、child orbit covered。

4 receiptsをhead 1235/6612/521988/4882/385711（cost-71c fold後）にfoldし、新canonical head **`1239/6608/521701/4878/385424`**（solved 1235→1239・in-manifest marginal 4・raw marginal 20・zero-mim bits 64/72）。childは**bit9**で閉鎖。第2 target S5は**26行/1976 → 24行/1836**、第2開親 `00000000000000003800000808000000` は**57行/4272 → 54行/4055**。set等式・499 folded rootsとのraw/D4 disjointness・sweep audit再導出・manifest totals再合計をassertし、completed claim後の再実行で3出力blobのbyte-identityを再assertする制御付き。

REFUTED-D10はLOSS証明ではなく、WIN7証明書は個別7石rootの深さ10以内の先手勝ちのみを証明する。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4は引き続き **UNKNOWN**。次のfold baselineはhead 1239。未fold: cost-72c（raw着地済み）・cost-70g（証明書8件）・cost-65l（fold in flight）等。

詳細: [lane log](../../log/2026-11-15-n11-class2-lane-cost70f-sweep-certificates-and-fold.md)、[sweep audit](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost70f-sweep-audit-20261115.json)、[certificate manifest](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost70f-win7-certificates-20261115.json)、[fold head JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost70f-receipts-recompute-20261115.json)、[completed claim](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost70f-inflight-20261115.json)。

## 2026-11-15: cost-72c receipts fold — head 1239→1244（9 receipts・総marginal 43・child orbit closure bit1）とclaim blob pinning廃止

第二coverable class-2 target S5 `00000000000000801202000000200000` のcost-72 child `00000000000000801202000000220000`（stones [17,21,49,57,60,71]・需要 c1=0,c2=2,c4=0・両開親ともclass-2: del17=parent1 bit-exact・del21→第2開親 `00000000000000083800000008000000`）の9 WIN7-D10 receipts（bits [1,7,24,39,59,64,67,72,96]・証明書321,781行/11,604,178 bytes/41,346,462 extraction nodes）をhead 1239にfoldした。

`recompute_frontier_cost72c_receipts_20261115.py`: runpyで70f fold scriptから1239/6608/521701/4878/385424 head（head JSON + 両CSV blob-identical）を再現、37の公開72c入力（sweep audit・certificate manifest・9 raw batches・determinism rerun・3 v15 crosschecks・18 per-bit verify records・3 scripts・certificates README）をgit blob shaでbyte-exact検証、childの両開親での残存（parent1 24行/1836・parent2 55行/4111・lift stones 17/21・残り4削除は閉行）、9 raw batchesからsweep再導出（72候補・**9 WIN7-D10/63 REFUTED/0 capped・61,297,942 nodes**・pilot 3402×9・batch5 determinism node-exact・v15 9 WIN + 3 refuted anchors node-matched）、9証明書18パートをpart bytesで直接検証（part md5/blob→join == whole md5/blob・per-bit BigInt/Bareiss verify記録再読込・union 0/0・manifest totals再総和）、9新root vs **503 folded roots**のraw+D4 disjointness、公開順 [1,7,24,39,59,64,67,72,96] fold（**総marginal 43・in-manifest 5・zero-mim [39,59,64,72,96]**）・child orbit closure bit1（公開順最初）・set等式 `s_after == s_1239 UNION covers(9 roots)`・3回連続実行byte-identical。

**fold後 head: solved 1244 / unique 6603 / cost 521,339 / open 4,873 / open_cost 385,062**。parent1（第2 target S5）**21行/1615**（child + `00000000000000801202000000200002` + `00000000000000881202000000200000` を喪失）・parent2 **52行/3898**（child + `00000000000000083800000009000000` + `00000000000000801202000000020080` を喪失）。head JSON [class-frontier-cost72c-receipts-recompute-20261115.json](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost72c-receipts-recompute-20261115.json)・ranking/top-candidates CSVs・fold scriptをpush、claim v4（fold record込み）で反映。

**運用変更: claim blob pinning廃止** — fold scriptがclaimをblob-pinすると、claim closure updateでscriptのblob参照が壊れ再実行不能になる循環（cost-72b repairの教訓）が生じる。claimは内容検証のみ（70f方式に統一）とし、closure後のscript再実行可能性を優先した。head JSONの `published_inputs_byte_exact_vs_main` は37（claim分を除く）となり、claim側foldレコードがscript blob `144b41c6…` を明記して相互参照を担保する。

**cost-70f head JSONのbaseline_main prose誤記を記録**: 70f head JSONのbaseline_main文がcost-70eのhead数字（1235/6614/522131/4884/385854）と70e head blob（`a0171d4b…`）を引用している（実際にassertしているのは71c head 1235/6612/521988/4882/385711・blob `61af2eb3…`）。prose-onlyのcopy-paste誤記で、70f fold scriptのassertは正しく、いかなる公開数値にも影響しない。履歴はbyte-unmodifiedのまま、本fold head JSONの `baseline_erratum_note` に記録した（71c bit112 md5誤記と同じ運用）。

REFUTED-D10はLOSS証明ではなく、9 WIN7証明書は個別7石rootの深さ10以内の先手勝ちのみを証明する。solved 1244はmanifest被覆の簿記であり盤全体の勝敗ではない。**標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4は引き続きUNKNOWN**。次のfold baselineはhead 1244。未fold: cost-70g（証明書8件・並走lane）とcost-65l（bits 21/48・fold in flight）は**本head 1244へのrebaseが必須**。

詳細: [fold log](../../log/2026-11-15-n11-class2-lane-cost72c-receipts-fold.md)、[ranking CSV](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-s5-ranking-after-cost72c-receipts-20261115.csv)、[top-candidates CSV](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost72c-receipts-20261115.csv)、[claim v4](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost72c-inflight-20261115.json)。

## 2026-11-15: cost-73g sweep・WIN7証明書8件 — 第2target S5のcost 73行（foldは次回）

第2coverable class-2 target S5 `00000000000000801202000000200000`（head 1244で21行/1615）の最安未sweep行 child `00000000000000849002000000000800`（edge cost 73・需要 c1=0,c2=2,c4=0・stones [11,49,60,63,66,71]）をcost-73gとしてsweepした。**73/73候補・WIN7-D10 8件（bits [31,54,56,62,69,81,89,113]）・65 REFUTED-D10・0 capped・91,357,592 nodes**、pilot 3402×10・batch-5 determinism rerun node-exact・v15交差エンジン8 WIN + 3 refuted anchors（0/100/117）一致。独立監査 `audit_cost73g_raw_sweep_20261115.py`（純Python・完全整数Bareiss）が全assert PASS: 73候補再列挙bit-exact・集計再導出・一石削除で両開親再現（del66=parent1 bit-exact・del11→第2開親 `00000000000000801242000000000000` 59行/4656・残り4削除は閉行）・8 WIN rootのD4 orbitが公開15 manifest・25 canonical rootと無重複。

8 WIN rootsをblind抽出（空kill table・repo-verbatim extractor blob `52bcaf50`・fbt_drops 0）し、**BigInt検証器（blob `62b5d941`）とBareiss検証器（`verify_cost73g_win7_bareiss_independent.py`）の二独立検証で8/8 PASS**（union 0/0・rows sorted-unique・terminal [13,17]）。**343,092 strategy rows / 94,100,994 extraction nodes**。manifest `class2-lane-cost73g-win7-certificates-20261115.json`・16行境界パート（join md5 == whole md5全16件）・per-bit verify records 16件・certificates READMEを公開済み（全ファイルremote md5照合）。

receipts foldは次回以降: fold前に最新mainを再取得しhead 1244（blob `42dbb92e`）を再assertすること。並走のcost-70g/65l foldが先に着地した場合はrebase必須。兄弟行 `00000000220000083800000000000200`（cost 73・第2開親67行/5182）は未着手のまま残置。

REFUTED-D10はLOSS証明ではなく、8証明書は個別7石rootの深さ10以内の先手勝ちのみを証明する。solved 1244はmanifest被覆の簿記であり盤全体の勝敗ではない。**標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4は引き続きUNKNOWN**。

詳細: [lane log](../../log/2026-11-15-n11-class2-lane-cost73g-sweep-certificates.md)、[sweep audit](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost73g-sweep-audit-20261115.json)、[certificate manifest](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost73g-win7-certificates-20261115.json)、[claim v2](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost73g-inflight-20261115.json)。

## 2026-11-15: cost-73g receipts fold — canonical head 1244 → 1249

直前のcost-73g sweep・証明書セッション（上記）に続く同一セッションで、8 WIN7-D10 receipts [31, 54, 56, 62, 69, 81, 89, 113]をcanonical head 1244（blob `42dbb92e`）にfoldした。claim v3（fold IN FLIGHT fence）を先頭にpushして並走をfenceし、fold成果物のpush前に最新mainを再取得してfive-row-q7レーンの新コミットが本チェーンに無影響であることを確認した（72c head JSON不変）。

`recompute_frontier_cost73g_receipts_20261115.py`を書いて3回連続実行、すべてbyte-identical（head JSON md5 `4f36b505`）を確認した上でpushした。統制はcost-72c foldの方式を踏襲:

- **baseline再構成**: 72c fold scriptをrunpy鎖（72c→70f→71c→前期鎖全体）で再現し、1244/6603/521339/4873/385062 head（72c head JSON blob `42dbb92e`・両CSVともblob-identical）を再生成。fold済みroot集合は**512個**（499 through cost-71c + 4 cost-70f + 9 cost-72c）。
- **childの残存確認**: parent1 `00000000000000801202000000200000` 21行/1615・parent2 `00000000000000801242000000000000` 59行/4656がchild `00000000000000849002000000000800`（edge cost 73・需要 c1=0,c2=2,c4=0）を行として持ち、開親はこの2つのみ。D4 lift: del66=parent1 bit-exact・del11=parent2 bit-exact・残り4削除は閉行。
- **sweep再導出**: 10 raw batch JSONLsから73候補を一度ずつ（claim列挙と一致）・8 WIN7-D10・65 REFUTED-D10・0 capped・総nodes 91,357,592・pilot 3402×10・batch5 determinism rerun node-exact・v15交差エンジン（8 WIN node-matched・アンカー0/100/117 loss=false・pilot 5949×4）・8 distinct D4 win orbits。
- **証明書検証**: 8証明書16パートすべてpart bytesで直接検証（part bytes/md5/blob sha → join == whole md5・whole blob sha）・rows sorted-unique・sub-roots == loser mobility（合計450）・terminal 13..17（BigInt）/ 13,15,17（Bareiss）・per-bit verify記録16件の再読込・union 0/0・manifest totals再総和（**343,092 rows / 12,392,797 bytes / 94,100,994 extraction nodes**）。
- **root disjointness**: 8新root vs 512 fold済みrootをraw-hex・D4両方で確認。
- **fold**: 公開順 [31, 54, 56, 62, 69, 81, 89, 113]でper-record marginalを拡張unionから再導出。**総marginal 39・in-manifest 5**・zero-mim receipts [56, 62, 69, 81, 113]・child orbit closureはbit31（公開順最初）・set等式 `s_after == s_1244 UNION covers(8 roots)`。

**fold後 head: solved 1249 / unique 6598 / cost 520,956 / open 4,868 / open_cost 384,679**。parent1（第2 target S5）**19行/1463**（child + `00000000020000809002000000000800` を喪失）・parent2 **55行/4352**（child + `00000000000000801242000080000000` + `00000000000000841242000000000000` + `00000000000000849002000080000000` を喪失）。foldはin-manifest 5行を閉じた（child + 4行）が、どちらのS5親も解決していない。head JSON [class-frontier-cost73g-receipts-recompute-20261115.json](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost73g-receipts-recompute-20261115.json)・ranking・top-candidates CSVs・fold script・claim v4（fold record込み・`published_inputs_byte_exact_vs_main` 37）をpush、全remote blob/md5照合済み。

claimは内容検証のみ（blob pinning廃止の運用継続）。claim v4のfold recordがscript blob `386b0666…` と出力3 blob shaを明記し、fold scriptのsection 9がclaim v4と再計算の一致を再assertする（実行確認済み）。

REFUTED-D10はLOSS証明ではなく、8証明書は個別7石rootの深さ10以内の先手勝ちのみを証明する。solved 1249はmanifest被覆の簿記であり盤全体の勝敗ではない。**標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4は引き続きUNKNOWN**。次のfold baselineはhead 1249。未fold: cost-70g（証明書8件）とcost-65l（bits 21/48）は**本head 1249へのrebaseが必須**。兄弟行 `00000000220000083800000000000200`（cost 73・第2開親67行/5182）は未着手のまま残置。

詳細: [fold log](../../log/2026-11-15-n11-class2-lane-cost73g-receipts-fold.md)、[ranking CSV](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-s5-ranking-after-cost73g-receipts-20261115.csv)、[top-candidates CSV](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost73g-receipts-20261115.csv)、[claim v4](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost73g-inflight-20261115.json)。

## 2026-11-15: cost-74g sweep・WIN7証明書10件・receipt fold — head 1257→1266（第三target S5が残り1行）

第三coverable class-2 target S5 `00000000000000809102000000000000` のcost-74 child `00000000000000809142000000000000`（stones [49,54,56,60,63,71]・需要 c1=0,c2=2,c4=0）をcost-74gとしてsweepした（staleなcost-74e claimはhead 1188・planのみでartifactsなしのため実行上stale扱い、名前衝突回避）。**74/74候補・WIN7-D10 10件（bits 4,11,20,44,69,95,100,108,109,116）・64 REFUTED-D10・0 capped・179,966,455 nodes**、pilot 3402×10・batch-5 determinism rerun node-exact・v15 10 WIN+3 refuted anchors一致。

10 WIN rootsをblind抽出（空kill table・repo-verbatim v16抽出器）し、**BigInt 3x3 + Number Bareiss 4x4の二独立検証器で10/10 PASS**（union 0/0・terminal [13,17]・consumed union == 証明書行集合 0/0）。合計**639,189行・23,085,545 bytes・241,387,497 extraction nodes・600 sub-roots**（bit44のみ単一ファイル、他9件は2分割）。

10 receiptsをhead 1257/6590/520380/4860/384103（cost-70g/73h fold後）にfoldし、新canonical head **`1266/6581/519710/4851/383433`**（solved 1257→1266・in-manifest marginal 9・raw marginal 49・zero-mim bits 11/20）。childは**bit4**で閉鎖。**第三target S5は2行/143 → 1行/69**（残るはcost-69 row `00000000000000809102000000002000` のみ）、第2開親 `00000000000000003800000008000010` は**64行/4813 → 55行/4143**。set等式・532 folded rootsとのraw/D4 disjointness・sweep再導出・証明書bytes検証をassertし、completed claim後の再実行で3出力blobのbyte-identityを再assertする制御付き。

REFUTED-D10はLOSS証明ではなく、WIN7証明書は個別7石rootの深さ10以内の先手勝ちのみを証明する。**第三target S5は残り1行**で、これがWIN7 receiptで閉じれば第三target S5が先手WINとなりclass-2 blockerが条件付きで閉鎖される。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4は引き続き **UNKNOWN**。次のfold baselineはhead 1266。未fold: cost-70g（証明書8件）・cost-65l（fold in flight）等。

詳細: [lane log](../../log/2026-11-15-n11-class2-lane-cost74g-sweep-certificates-and-fold.md)、[fold head JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost74g-receipts-recompute-20261115.json)、[top-candidates CSV](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost74g-receipts-20261115.csv)、[completed claim](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost74g-inflight-20261115.json)。

## 2026-11-15: cost-69i sweep・WIN7証明書4件・receipt fold — 第三class-2 target S5が閉鎖（head 1266→1273）

第三coverable class-2 target S5 `00000000000000809102000000000000` の**最後の残行** cost-69 child `00000000000000809102000000002000`（stones [13,49,56,60,63,71]・需要 c1=0,c2=2,c4=2）をcost-69iとしてsweepした（staleな69g claimと、別childを扱う既存69h laneとの名前衝突を回避）。**69/69候補・WIN7-D10 4件（bits 21,29,97,100）・65 REFUTED-D10・0 capped・62,994,015 nodes**、pilot 3402×9・batch-5 determinism rerun node-exact・v15 4 WIN+3 refuted anchors一致。

4 WIN rootsをblind抽出し、**BigInt 3x3 + Number Bareiss 4x4の二独立検証器で4/4 PASS**（union 0/0・terminal [13,17]）。合計**204,339行・7,379,919 bytes・76,747,485 extraction nodes・216 sub-roots**。

4 receiptsをhead 1266/6581/519710/4851/383433（cost-74g fold後）にfoldし、新canonical head **`1273/6574/519179/4844/382902`**（solved 1266→1273・in-manifest marginal 7・raw marginal 19）。childは**bit21**で閉鎖。**第三target S5は1行/69 → 0行/0（閉鎖）**: このS5の6石の子はすべて先手WINとなったため、S5自体が先手WINとなり、**class-2 blockerが条件付きで閉鎖**される。第2開親 `00000000000000801202000000080000` は**72行/5477 → 69行/5265**、class-4開親 `00000000000000003800000000810000` は**84行/6815 → 79行/6427**。set等式・542 folded rootsとのraw/D4 disjointness・sweep再導出・証明書bytes検証・第三target残行0制御をassertし、completed claim後の再実行で3出力blobのbyte-identityを再assertする制御付き。

REFUTED-D10はLOSS証明ではなく、WIN7証明書は個別7石rootの深さ10以内の先手勝ちのみを証明する。第三target S5の閉鎖はmanifest被覆（全6石子が先手WIN）に基づく条件付きclosureであり、blocker全体の独立証明ではない。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}は引き続き **UNKNOWN**。次のfold baselineはhead 1273。cost-65l fold（head 1261）は本headへのrebase・mergeが必須。

詳細: [lane log](../../log/2026-11-15-n11-class2-lane-cost69i-sweep-certificates-and-fold.md)、[fold head JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost69i-receipts-recompute-20261115.json)、[top-candidates CSV](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost69i-receipts-20261115.csv)、[completed claim](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost69i-inflight-20261115.json)。

## 2026-11-15: cost-74h sterile sweep — 第二coverable class-2 target S5の最安未sweep行・74候補exactly-once・WIN7-D10 0件・74 REFUTED-D10・0 capped・総nodes 72,720,136（head不変）

2-way merged canonical head 1270（`class-frontier-merged-cost65l-74g-recompute-20261115.json`・blob `02109530`）基準で、**第二coverable class-2 target S5 `00000000000000801202000000200000`**（17行/1325）の cost-74 行child `00000000000000889002000000000800`（stones [11,49,60,63,67,71]・両開親とも純class-2需要 c1=0, c2=2, c4=0: `00000000000000801222000000000000` 75/5705 と第二target 17/1325）をclass2-laneとしてsweepした（cost-65兄弟2行はcost-65k sterile/cost-65l fold済み・cost-70兄弟はcost-70d sterile済みの最安未sweep行）。**74候補をexactly-onceで列挙・探索**（pilot 3402×10・総nodes **72,720,136**・全terminal range [13,17]）し、判定は**WIN7-D10 0件・74 REFUTED-D10・0 capped** — **sterile**（head不変）。raw batches 1-10をpushし、determinism rerun（batch5を同一分割で再実行・node-exact一致）と**v15 crosscheck**を実施。v15アンカーは当初74gのアンカー0/1/2と混同してbit 1を含めていたが、**bit 1は74h childではBareiss-unsafeかつclaim列挙に不含**のため、合法アンカー [0,2,62,86,87] に修正して実行した（refutedアンカー [0,2,62,86,87]・全loss=false・pilot 5949×3・anchor合法性はaudit script内でclaim列挙への所属としてassert）。audit script `audit_cost74h_raw_sweep_20261115.py` は全統制PASS・2回実行byte-identical（sweep audit JSON `class2-lane-cost74h-sweep-audit-20261115.json`・md5 `acd1b1c86daab4096bc4d079bbad26df`）。claim `class2-lane-cost74h-inflight-20261115.json` は **completed (STERILE)** へretire済み（commit `6fac1e3e`・15ファイル）。

重要な副次記録: sweep実行中に**実行sandboxの環境リセットが発生しローカルmirrorが全消滅**した（未pushのraw 12ファイルを含む）。10バッチ+determinism rerunを同一分割で再生成し、消失前の集計（nodes・terminal range・判定別件数・pilot件数）と全件一致を確認した。同一コード・同一分割が**環境をまたいで一致して再現する**ことが実験事実として確定した。REFUTED-D10はLOSS証明ではない。sterile行は当該6石child配下の7石rootsの深さ10以内の先手勝ち証明が存在しないことのみを意味する。headはこのsweepでは不変。

詳細: [sweep log](../../log/2026-11-15-n11-class2-lane-cost74h-sterile-sweep.md)、[sweep audit JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost74h-sweep-audit-20261115.json)、[retired claim](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost74h-inflight-20261115.json)。

## 2026-11-15: cost-65l/74g/69i 3-way merged fold — fork 1257解消・canonical head 1277/6570/518896/4840/382619（第三target S5 0/0閉鎖を維持）

fork 1257（cost-73h）から着地していた**3本の並走fold**（65l→head 1261・74g→head 1266・69i→head 1273・69iは1266ベースで着地し65l receiptsを含まない）を**3-way mergeで統合解消**した。上の69iセクション末尾の「cost-65l fold（head 1261）は本headへのrebase・mergeが必須」は本foldで**解消済み**。merge script `recompute_frontier_merged_cost65l_74g_69i_20261115.py`（commit `dde42161`）は:

- fork 1257をrunpyでbyte-identical再現し、出版4 head JSON blobをgit blob shaで検証（65l `0b523e70`・74g `fce4ce77`・69i `8692a7a6`・2-way merged-AB `02109530`）。
- **16 receipt roots（2+10+4）の相互disjointness raw+D4**。**65l-vs-69i・74g-vs-69iは初検証**（69i laneの出版検証は542-root baseline＝532+74g分のみで65l rootsを含まない）。全ペアraw・D4とも重複なし。
- pairwise covers overlap: A-B 0・A-C 0・**B-C 3**（`00000000000000809102000000001000`・`00000000000000809102000000200000`・`00000000000000809102000020000000`）。3行とも74g foldで既にsolved済みで69iのpublished marginalsには元々不含 — **chain-C marginal deltas vs published: none**。
- 統合逐次replay（65l→74g→69i）: total marginal 78（10+49+19）・in-manifest 20（4+9+7）・child closures 3つ各1回（65l bit21・74g bit4・69i bit21）・set等式・**逆順replay（69i先）同一集合**。
- **統合head `1277/6570/518896/4840/382619`**（solved 1257+20）。per-parent: 第二target 17/1325・class-4 lift親 75/5519・**第三target 0/0（CLOSED・維持）**・74g第2親 55/4143・69i第2親 69/5265・69i第3親 79/6427。
- **3回連続実行で全出力byte-identical**。

branch head 3個（1261・1266・1273）と2-way merged head 1270は1257 forkの有効な独立foldとして残るが、**正準継続は1277のみ**。以後のfoldは1277 baselineをassertしてから行う。次のsweep targetは第二coverable class-2 target S5 `00000000000000801202000000200000`（17行/1325）の次行cost-75 `00000000000040801202000000200000`、およびclass-4 blocker S5（18行/1460）のcost-80行2本。第三target S5の0/0閉鎖はeven-OR/odd-AND規約下の**条件付きclosure**であり、solved 1277はmanifest被覆の簿記であり勝敗ではない。

詳細: [merge log](../../log/2026-11-15-n11-merged-fold-cost65l-74g-69i-fork-resolution.md)、[merged head JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-merged-cost65l-74g-69i-recompute-20261115.json)、[top-candidates CSV](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-merged-cost65l-74g-69i-20261115.csv)、[merge script](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_merged_cost65l_74g_69i_20261115.py)。

## 2026-11-15: cost-76b sweep・WIN7証明書2件・receipt fold — 第二class-2 target S5が17→16行（head 1277→1280）

第二coverable class-2 target S5 `00000000000000801202000000200000` のcost-76 child `00000000000000801302000000200000`（stones [21,49,56,57,60,71]・需要 c1=0,c2=1,c4=0・開親は第二targetのみ）をcost-76bとしてsweepした（76aは別child）。**76/76候補・WIN7-D10 2件（bits 72,96）・74 REFUTED-D10・0 capped・107,961,863 nodes**、pilot 3402×10・determinism rerun node-exact・v15 2 WIN+3 refuted anchors一致。

2 WIN rootsをblind抽出し、**BigInt 3x3 + Number Bareiss 4x4で2/2 PASS**（union 0/0・terminal [13,17]）。合計**118,437行・4,272,471 bytes・121 sub-roots**。2 receiptsをhead 1277にfoldし、新canonical head **`1280/6567/518678/4837/382401`**（solved 1277→1280・in-manifest marginal 3・raw marginal 11）。childは**bit72**で閉鎖、**第二target S5は17行/1325 → 16行/1249**。set等式・548 folded rootsとのraw/D4 disjointness・sweep再導出・証明書bytes検証をassertし、completed claim後の再実行で3出力blobのbyte-identityを再assertする制御付き。

REFUTED-D10はLOSS証明ではなく、WIN7証明書は個別7石rootの深さ10以内の先手勝ちのみを証明する。第二target S5は残り16行で未解決、best class-2はaudit-blocked S5（10行/698）、best class-4 blocker S5は18行/1460。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}は引き続き **UNKNOWN**。次のfold baselineはhead 1280。

詳細: [lane log](../../log/2026-11-15-n11-class2-lane-cost76b-sweep-certificates-and-fold.md)、[fold head JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost76b-receipts-recompute-20261115.json)、[top-candidates CSV](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost76b-receipts-20261115.csv)、[completed claim](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost76b-inflight-20261115.json)。

## 2026-11-15: cost-77a sweep・WIN7証明書3件・receipt fold — 第二class-2 target S5が16→15行（head 1280→1282）

第二coverable class-2 target S5 `00000000000000801202000000200000` のcost-77 child `00000000000000801202000000204000`（stones [14,21,49,57,60,71]・需要 c1=0,c2=2,c4=0・開親は第二targetとclass-2 S5 `00000000000000003800000408000000`）をcost-77aとしてsweepした。**77/77候補・WIN7-D10 3件（bits 40,64,111）・74 REFUTED-D10・0 capped・103,356,793 nodes**、pilot 3402×10・determinism rerun node-exact・v15 3 WIN+3 refuted anchors一致。

3 WIN rootsをblind抽出し、**BigInt 3x3 + Number Bareiss 4x4で3/3 PASS**（union 0/0・terminal [13,17]）。合計**157,475行・5,671,984 bytes・182 sub-roots**。3 receiptsをhead 1280にfoldし、新canonical head **`1282/6565/518522/4835/382245`**（solved 1280→1282・in-manifest marginal 2・raw marginal 14・zero-mim bits 64/111）。childは**bit40**で閉鎖、**第二target S5は16行/1249 → 15行/1172**、第2開親は62行/5092 → 60行/4936。set等式・550 folded rootsとのraw/D4 disjointness・sweep再導出・証明書bytes検証をassertし、completed claim後の再実行で3出力blobのbyte-identityを再assertする制御付き。

REFUTED-D10はLOSS証明ではなく、WIN7証明書は個別7石rootの深さ10以内の先手勝ちのみを証明する。第二target S5は残り15行で未解決、best class-2はaudit-blocked S5（10行/698）、best class-4 blocker S5は18行/1460。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}は引き続き **UNKNOWN**。次のfold baselineはhead 1282。

詳細: [lane log](../../log/2026-11-15-n11-class2-lane-cost77a-sweep-certificates-and-fold.md)、[fold head JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost77a-receipts-recompute-20261115.json)、[top-candidates CSV](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost77a-receipts-20261115.csv)、[completed claim](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost77a-inflight-20261115.json)。

## 2026-11-15: cost-77b sweep・WIN7証明書4件・receipt fold — 第二class-2 target S5が15→14行（head 1282→1286）

第二coverable class-2 target S5 `00000000000000801202000000200000` のcost-77 child `00000000000000801202000200200000`（stones [21,33,49,57,60,71]・需要 c1=0,c2=1,c4=0・開親は第二targetのみ）をcost-77bとしてsweepした（77aは別child）。**77/77候補・WIN7-D10 4件（bits 9,12,59,105）・73 REFUTED-D10・0 capped・153,463,195 nodes**、pilot 3402×10・determinism rerun node-exact・v15 4 WIN+3 refuted anchors一致。

4 WIN rootsをblind抽出し、**BigInt 3x3 + Number Bareiss 4x4で4/4 PASS**（union 0/0・terminal [13,17]）。合計**190,937行・6,904,467 bytes・231 sub-roots**。4 receiptsをhead 1282にfoldし、新canonical head **`1286/6561/518211/4831/381934`**（solved 1282→1286・in-manifest marginal 4・raw marginal 20・zero-mim bit59）。childは**bit9**で閉鎖、**第二target S5は15行/1172 → 14行/1095**。set等式・553 folded rootsとのraw/D4 disjointness・sweep再導出・証明書bytes検証をassertし、completed claim後の再実行で3出力blobのbyte-identityを再assertする制御付き。

REFUTED-D10はLOSS証明ではなく、WIN7証明書は個別7石rootの深さ10以内の先手勝ちのみを証明する。第二target S5は残り14行で未解決、best class-2はaudit-blocked S5（10行/698）、best class-4 blocker S5は18行/1460。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}は引き続き **UNKNOWN**。次のfold baselineはhead 1286。

詳細: [lane log](../../log/2026-11-15-n11-class2-lane-cost77b-sweep-certificates-and-fold.md)、[fold head JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost77b-receipts-recompute-20261115.json)、[top-candidates CSV](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost77b-receipts-20261115.csv)、[completed claim](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost77b-inflight-20261115.json)。

## 2026-11-15: cost-77c sweep・WIN7証明書8件・receipt fold — 第二class-2 target S5が14→13行（head 1286→1290）

第二coverable class-2 target S5 `00000000000000801202000000200000` のcost-77 child `00000000040000801202000000200000`（stones [21,49,57,60,71,90]・需要 c1=0,c2=2,c4=0・開親は第二targetとclass-2 S5 `00000000000000003800000009000000`）をcost-77cとしてsweepした。**77/77候補・WIN7-D10 8件（bits 10,40,50,54,58,95,96,111）・69 REFUTED-D10・0 capped・98,545,191 nodes**、pilot 3402×10・determinism rerun node-exact・v15 8 WIN+3 refuted anchors一致。

8 WIN rootsをblind抽出し、**BigInt 3x3 + Number Bareiss 4x4で8/8 PASS**（union 0/0・terminal [13,17]）。合計**362,362行・13,055,390 bytes・457 sub-roots**。8 receiptsをhead 1286にfoldし、新canonical head **`1290/6557/517923/4827/381646`**（solved 1286→1290・in-manifest marginal 4・raw marginal 36・zero-mim bits 50/58/95/111）。childは**bit10**で閉鎖、**第二target S5は14行/1095 → 13行/1018**、第2開親は57行/4337 → 53行/4049。set等式・557 folded rootsとのraw/D4 disjointness・sweep再導出・証明書bytes検証をassertし、completed claim後の再実行で3出力blobのbyte-identityを再assertする制御付き。

REFUTED-D10はLOSS証明ではなく、WIN7証明書は個別7石rootの深さ10以内の先手勝ちのみを証明する。第二target S5は残り13行で未解決、best class-2はaudit-blocked S5（10行/698）、best class-4 blocker S5は18行/1460。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}は引き続き **UNKNOWN**。次のfold baselineはhead 1290。

詳細: [lane log](../../log/2026-11-15-n11-class2-lane-cost77c-sweep-certificates-and-fold.md)、[fold head JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost77c-receipts-recompute-20261115.json)、[top-candidates CSV](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost77c-receipts-20261115.csv)、[completed claim](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost77c-inflight-20261115.json)。
## 2026-11-15: cost-75d receipts fold — 延期foldのhead 1290 rebase完走 — 第二class-2 target S5が13→11行（head 1290→1296）・bit-92 cross-coverが並走77d行も閉鎖

実行環境outageでsweep・証明書4件公開後にfoldだけ延期されていたcost-75d（第二coverable class-2 target S5 `00000000000000801202000000200000` のcost-75 child `00000000000040801202000000200000`・stones [21,49,57,60,71,78]・需要 c1=0,c2=1,c4=0・単一開lift親）を、deferral noteのrebase条項に従いhead 1290へrebaseしてfoldした（77a/77b/77c/78a foldが延期中に着地）。`recompute_frontier_cost75d_receipts_20261115.py`は77c fold scriptをrunpy再実行してhead 1290/6557/517923/4827/381646と3出力をbyte-identical assertし、claim検証・head 1290でchild genuinely remaining（第二target 13行/1018・lift 78・他5削除軌道は閉鎖維持）・sweep再導出（75候補・WIN7-D10 4件 [12,40,92,111]・71 REFUTED・0 capped・143,552,593 nodes・pilot 3402×10・det rerun node-exact・v15 pinned record一致）・証明書bytes検証（part join == whole・split manifests・BigInt+Bareiss 4/4・239,868行・8,654,219 bytes・242 sub-roots）・4 root vs 565 folded rootsのraw/D4 disjointnessを統制してから4 receiptsを公開順 [12,40,92,111] でfoldした。childは**bit12**で閉鎖・総marginal 22・in-manifest marginal 6・zero-mimなし・set等式 PASS・3回連続実行byte-identical。

新canonical head **`1296/6551/517468/4821/381191`**。**第二target S5は13行/1018 → 11行/866**。喪失2行のうち1行はchild行、もう1行は**bit-92 receiptのcross-coverが閉じたcost-77行 `00000000100000801202000000200000`**（並走cost-77d sweepがIN FLIGHT claim中のchild行）で、77d foldはcost-70g先例のwarm-hygiene統制（child既閉鎖assert・拡張unionからのmarginal再導出）が必須。

REFUTED-D10はLOSS証明ではなく、WIN7証明書は個別7石rootの深さ10以内の先手勝ちのみを証明する。第二target S5は残り11行で未解決、best class-2はaudit-blocked S5（10行/698）、best class-4 blocker S5は18行/1460。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}は引き続き **UNKNOWN**。次のfold baselineはhead 1296。

詳細: [lane log](../../log/2026-11-15-n11-class2-lane-cost75d-receipts-fold.md)、[fold head JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost75d-receipts-recompute-20261115.json)、[top-candidates CSV](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost75d-receipts-20261115.csv)、[completed claim](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost75d-inflight-20261115.json)。

## 2026-11-15: 全published fold chain監査のv3拡張（77b/77c/75dまで）+ cost63cd malformed hex erratum記録

同一監査レーンで、v2監査（1233→1282・553 roots・88 pins byte-exact）を着地済みの77b/77c/75d headまで拡張した。純stdlib・publishedファイルのみ・過去の監査状態は一切再利用しない。**全統制PASS・2回実行byte-identical**（schema v3・86,060 bytes・md5 `77d3b34952c46f16d074692b468eeb66`）。

- **pins 88→95**: v2のpin提案4件（71c `61af2eb3…`・70f `4d0f130e…`・73g `e4fb98dc…`・70g `73890fe3…`）をpin tableに反映し、77b `b648ed06…`（77c headのbaseline_main quoteから）・77c `7f2badce…`（77d claimのchain_head_at_claimから）・75d `c801e605…`（completed 75d claimのoutput_blob_shasから）を追加。post-70e headは全件pinnedとなった。
- **root在庫 553→569**（557@77b・565@77c・569@75d・branch-aware own-line lineage一致）。新16 receipt rootsは16新D4 orbitで**twin pair増加なし**（558 orbits / 569 roots / 11 twins）——77b/77c/75d fold scriptのraw+D4 disjointness主張を先行在庫全体に対して独立確認し、特に**deferred後にrebaseされた75d receiptsがどこでも未計数だった**ことも確認。
- **head arithmetic 66→69 heads・anomaly 0**: 77b/77c/75dともsequential-fold-union（delta 4/4/6・sum_mim == union_mim == delta・77cのraw marginal 36・75dのraw marginal 22のうちin-manifestは4/6）。3 baseline quoteはpublished状態と5数値完全一致（77b→77a・77c→77b・75d→77c frontier状態）。quote erratumは既知の70fのみ・pointer-differsは74gのみ。
- **canonical-line hex-level exactly-once 1233→1296**: 正準鎖に77a→77b→77c→75dを追加し、63 manifest hexes（49+4+4+6）が各々ちょうど1つのreceipt recordからmarginal主張される（total mim 63 == distinct 63 == 1296−1233・multi-claim 0）。75dのbit-92 cross-coverによる77d child行の閉鎖もこのhex集合に正確に1回だけ計上。
- **endpoint 77a/77b/77c/75d**: 4件のcompleted claim fold recordがpublished head JSONとbyte-exact（blob sha a2ba7235…/b648ed06…/7f2badce…/c801e605…・7554/8073/10558/8992 bytes）・head遷移 1280→1282→1286→1290→1296 成立。

**cost63cd malformed hex erratum（本項目に記録・履歴文書はbyte-unmodified）**: `class2-lane-cost63cd-frontier-recompute-20261114.json` の `cost63b_addition` の `marginal_manifest_hexes` に35文字のmalformed hex `00000000000010000003800000000100020` が混入（残り7件は正常）。`marginal_in_manifest`=8は計数整合で**fold算術・被覆計数には無影響**。1〜4文字削除でもLevenshtein-4修復でも未掲載covers候補から一意に修復できず、published corpus単独では当該1エントリのhex同一性は回復不能。v2監査で発見・v3監査でも単一のpublished hex erratumとして再確認。

cost-77d（並走IN FLIGHT・sweepは77c head基準で実行中）はfold head未存在のため本監査対象外。77d fold着地時はhead 1296へのrebaseと、75d bit-92 cross-coverでchild行が既に閉じたことに伴うwarm-hygiene統制（cost-70g先例）が必要。solved 1296はmanifest被覆の簿記であり勝敗ではない。REFUTED-D10はLOSS証明ではない。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4は引き続き **UNKNOWN**。

詳細: [監査log](../../log/2026-11-15-n11-published-fold-chain-roots-independent-audit.md)、[audit JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-published-chain-roots-independent-audit-20261115.json)、[audit script](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_published_chain_roots_independent_20261115.py)。

## 2026-11-15: v3監査拡張の第二独立検証 — 独立拡張実装との全統制一致 + v3 fresh mirror再現byte-exact

並走のv3監査着地（前項・`b9d6b7c6`）と同一のv1 baselineから、並走の着地を待たず独立に導出していた第二実装（`audit_published_chain_roots_second_independent_20261115.py`・blob `794c027c`・55,423B・91 pins版）で同75d endpoint拡張をもう一度実装・実行した。**両実装は全substantive controlで完全一致**: cumulative root在庫497→569全17 head（own-branch lineage含む）・D4 orbit構造（569 roots / 558 orbits / 11 twin pairs・twin provenance）・head arithmetic 69 heads 0 anomalies（分類・quote status・70f erratum/74g pointer-differsも同一）・canonical-line hex-level exactly-once 63 hexes 1233→1296（total mim 63 == distinct 63 == 1296−1233・per-head内訳も同一）・child closure 24 heads・convention-external 1件・per-record geometry 434 receipt + 40 group records 0 anomalies（cost63cd erratum同一）・75d endpoint・interpretation guard、すべて一致。v3 scriptはfresh mirror（tarball再構築+本レーン75d成果物）で再実行し**pushed blob `9ae57954`と2回連続byte-identical**。

第二実装は91 pins版としてv2 pin提案4件（71c/70f/73g/70g）を独立再計算しており、その値がv3のpin tableと完全一致（`61af2eb3`/`4d0f130e`/`e4fb98dc`/`73890fe3`・pinの二重確認）。また第二実装は75d claimの`parents_lost_rows`（cost-75行 `00000000000040801202000000200000` に加えcost-77行 `00000000100000801202000000200000` のbit-92 cross-cover・`parents_after` 11行/866）を追加assertしており、**77d foldに課されるwarm-hygiene要件（child行はhead 1296で既閉鎖・cost-70g先例の統制）を独立再確認**した。

衝突規則に従い、着地済みv3ファイル（v1 scriptパス・正準audit JSONファイル名）は一切変更せず、第二実装は別ファイル名で公開: script blob `794c027c`、出力v2 audit JSON blob `db0916c0`（85,324B・md5 `d067ab29`・schema v2・**6回連続byte-identical**）。77d fold着地時は両audit scriptを機械的にv4へ拡張（PINS/ORDER・own_claim・own_baseline・CANONICAL_LINE・endpointの各1エントリ）し二重検証を維持すること。solved 1296はmanifest被覆の簿記であり勝敗ではない。REFUTED-D10はLOSS証明ではない。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4は引き続き **UNKNOWN**。

詳細: [第二検証log](../../log/2026-11-15-n11-published-fold-chain-audit-second-independent-verification.md)、[第二実装script](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_published_chain_roots_second_independent_20261115.py)、[v2 audit JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-published-chain-roots-independent-audit-v2-20261115.json)。

**第二実装出力JSONの`v1_supersession`欄erratum（本項目に記録・published blobは変更せず）**: v2 audit JSON（blob `db0916c0`）の`v1_supersession`フィールドは「v1 audit JSONが`class2-lane-published-chain-roots-independent-audit-20261115.json`としてpublished unchangedのまま残る」と記載しているが、この記載はv3着地（`b9d6b7c6`）前の想定で書かれたもので、実際には同ファイル名はv3監査（blob `9ae57954`）で上書きされた。v1の元blob `79cab641`（80,309B）はgit履歴上は不変だが現行mainの当該パスには存在しない。proseのみの誤記で、v2 JSONの監査統制・計数・pin検証のいずれにも影響なし（同フィールドは非規範的な経路説明）。第二実装scriptのdocstringと第二検証logは正確なv3関係を記載済み。

## 2026-11-15: cost-75d + cost-77d のwarm-hygiene merge — canonical head 1302

cost-77d laneのlane-local fold（1290→1299）実行中に、並走のcost-75d foldがhead **1296/6551/517468/4821/381191** で着地していた。75dのbit92 receiptが77d child `00000000100000801202000000200000` を**cross-coverで既に閉鎖**しているため、77d foldを1296 baselineへrebaseし、warm-hygiene統制（child closureを二重計上しない）を適用した。

- 1296 baselineで77d childはsolved済みで、両開親のremaining rowsに不在（第二target 11行/866、第2開親64行/5036）。
- 77dの12 WIN rootsのうち**bit78 root `00000000100040801202000000200000` は75d bit92 rootと完全一致**（cross-lane root collision）のためfoldから除外。
- 残り11 receiptsをfoldし、child closureは主張しない。新canonical head **`1302/6545/517025/4815/380748`**（in-manifest marginal 6・raw marginal 51・zero-mim bits 7/39/58/64/108）。
- 第二target S5は11行/866で不変、第2開親は**64行/5036 → 58行/4593**。best class-2はaudit-blocked S5（10行/698）、best class-4 blocker S5は18行/1460。
- 出力: head JSON blob `97130384…`・ranking `aba88980…`・top-candidates `49b7f378…`。以後のfoldはhead 1302へのrebaseが必須。

warm-hygiene mergeは公開receiptの帳簿更新であり、child closureの帰属は75d bit92にある。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}は引き続き **UNKNOWN**。

詳細: [merge log](../../log/2026-11-15-n11-class2-merged-cost75d-77d-warm-hygiene.md)、[merged head JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-merged-cost75d-77d-receipts-recompute-20261115.json)、[merge script](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_merged_cost75d_77d_20261115.py)。

## 2026-11-15: cost-79a sweep・WIN7証明書3件・receipt fold — 第二class-2 target S5が11→10行（head 1302→1304）

第二coverable class-2 target S5 `00000000000000801202000000200000` のcost-79 child `00000000000000801212000000200000`（stones [21,49,52,57,60,71]・需要 c1=0,c2=2,c4=0・開親は第二targetとclass-2 S5 `00000000000000801212000000000000`）をcost-79aとしてsweepした。**79/79候補・WIN7-D10 3件（bits 9,50,64）・76 REFUTED-D10・0 capped・131,934,659 nodes**、pilot 3402×10・determinism rerun node-exact・v15 3 WIN+3 refuted anchors一致。

3 WIN rootsをblind抽出し、**BigInt 3x3 + Number Bareiss 4x4で3/3 PASS**（union 0/0・terminal [13,17]）。合計**165,209行・5,977,942 bytes・178 sub-roots**。3 receiptsをhead 1302にfoldし、新canonical head **`1304/6543/516873/4813/380596`**（solved 1302→1304・in-manifest marginal 2・raw marginal 14・zero-mim bit64）。childは**bit9**で閉鎖、**第二target S5は11行/866 → 10行/787**、第2開親は73行/5750 → 71行/5598。set等式・580 folded rootsとのraw/D4 disjointness・sweep再導出・証明書bytes検証をassertし、completed claim後の再実行で3出力blobのbyte-identityを再assertする制御付き。

REFUTED-D10はLOSS証明ではなく、WIN7証明書は個別7石rootの深さ10以内の先手勝ちのみを証明する。第二target S5は残り10行で未解決、best class-2はaudit-blocked S5（10行/698）、best class-4 blocker S5は18行/1460。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}は引き続き **UNKNOWN**。次のfold baselineはhead 1304。

詳細: [lane log](../../log/2026-11-15-n11-class2-lane-cost79a-sweep-certificates-and-fold.md)、[fold head JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost79a-receipts-recompute-20261115.json)、[top-candidates CSV](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost79a-receipts-20261115.csv)、[completed claim](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost79a-inflight-20261115.json)。

## 2026-11-15: cost-80d sweep・WIN7証明書4件・receipt fold — 第二class-2 target S5が10→9行（head 1304→1305）

第二coverable class-2 target S5 `00000000000000801202000000200000` のcost-80 child `00000008000000809002000000000400`（stones [10,49,60,63,71,99]・需要 c1=0,c2=2,c4=0・開親は第二targetとclass-2 S5 `00000000000000003800000008000001`）をcost-80dとしてsweepした。**80/80候補・WIN7-D10 4件（bits 48,61,81,96）・76 REFUTED-D10・0 capped・131,430,976 nodes**、pilot 3402×10・determinism rerun node-exact・v15 4 WIN+3 refuted anchors一致。

4 WIN rootsをblind抽出し、**BigInt 3x3 + Number Bareiss 4x4で4/4 PASS**（union 0/0・terminal [13,17]）。合計**202,272行・7,309,967 bytes・243 sub-roots**。4 receiptsをhead 1304にfoldし、新canonical head **`1305/6542/516793/4812/380516`**（solved 1304→1305・in-manifest marginal 1・raw marginal 18・zero-mim bits 61/81/96）。childは**bit48**で閉鎖、**第二target S5は10行/787 → 9行/707**（これで第二targetがbest coverable class-2に）、第2開親は55行/4417 → 54行/4337。set等式・583 folded rootsとのraw/D4 disjointness・sweep再導出・証明書bytes検証をassertし、completed claim後の再実行で3出力blobのbyte-identityを再assertする制御付き。

REFUTED-D10はLOSS証明ではなく、WIN7証明書は個別7石rootの深さ10以内の先手勝ちのみを証明する。第二target S5は残り9行で未解決、best class-2は第二target（9行/707）、best class-4 blocker S5は18行/1460。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}は引き続き **UNKNOWN**。次のfold baselineはhead 1305。

詳細: [lane log](../../log/2026-11-15-n11-class2-lane-cost80d-sweep-certificates-and-fold.md)、[fold head JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost80d-receipts-recompute-20261115.json)、[top-candidates CSV](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost80d-receipts-20261115.csv)、[completed claim](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost80d-inflight-20261115.json)。


## 2026-11-15: cost-77d fold事前予測brief — 着地merged foldとの全数値一致・bit-78重複root同一性の独立確認

当レーンがfold前に公開した予測brief（`class2-lane-cost77d-fold-prediction-20261115.json`・blob `97db3dec…`・script `4808dd64…`）を、着地後のmerged cost-75d+77d warm-hygiene fold（head 1296→1302）と全数値照合した。**head 5数値 1302/6545/517025/4815/380748・union marginal 51 / in-manifest 6・per-bit 11/11（各bitのmarginal・in-manifest数・marginal hex集合まで完全一致）・parent effects（第二target 11/866不変・第2開親64→58は同じ6行喪失）すべて一致**。zero-mim規約のみ差があり、予測[7,39,58,64,78,108]（bit-78をzero-marginal receiptとして計上）に対し着地[7,39,58,64,108]（bit-78を除外済み重複rootとして非計上）で、bit-78の寄与は0のため意味は同一。予測の`already_folded_root_duplicate`フラグ（bit-78 = true）は着地扱いと整合。

あわせて**bit-78重複rootの同一性を独立確認**（merged fold scriptにはcommentのみでassertがなかった統制）: 77d bit-78 root `00000000100040801202000000200000` は75d bit-92 receipt rootとraw-hex完全一致（1296 inventory内）、独立D4実装による7つのdeletion orbitは**すべてhead 1296で既解決（zero marginal）**。11-receipt set等式と仮想12-receipt版が一致し、除外は算術的に正当。

詳細: [prediction brief](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost77d-fold-prediction-20261115.json)。

## 2026-11-15: cost-77d / merged 75d+77d / cost-79a / cost-80d の4 fold第二独立検証 — 全統制PASS・12成果物byte-identical

codeload tarballから再構築した隔離mirror（80d成果物50ファイルはmainからfetchしgit blob sha照合・着地セッションの状態は一切不使用）で、4つのpublished fold scriptを**それぞれ独立の短命サブプロセスで2回ずつend-to-end再実行**し、全統制PASS・12成果物（各foldのhead JSON + ranking CSV + top-candidates CSV）がmainのgit blobとbyte-identical・2回の実行状態一致を確認した。runpy鎖はdel+gcでもプロセス内に状態が残り、同一インタプリタで4 script×2回を実行すると1回目全PASS後に2回目の途中でcgroup約1GB上限を超えてOOM kill（RC=137）することを実測、プロセス分離で解決した（各scriptのピークRSS約150-200 MB）。

追加統制: **独立8要素D4群**で19新root（77d 12 + 79a 3 + 80d 4）を再正準化し565/569/580/583-rootの各baseline inventoryとraw+D4 disjoint・全root==child|1<<bit・popcount 7。**独立Bareiss候補列挙**で77d/79a/80d childのlegal候補77/79/80件がclaimとbit-equal。**独立marginal算術**で11 merged receipts・3 79a receipts・4 80d receiptsのper-bit covers/marginalsがpublished recordsとhex集合単位で一致し、unionが1302・1304・1305状態を正確に再現。80d foldはchild genuinely remaining（両開親 10/787・55/4417）・sweep再導出（80候補・4 WIN7-D10 bits 48/61/81/96・76 REFUTED・131,430,976 nodes）・証明書4件 202,272行/7,309,967 bytes/243 sub-roots・4 root vs 583 folded roots disjoint・child閉鎖bit48・head 1305/6542/516793/4812/380516を再確認。

erratum 2件を記録（published blobは不変・算術無影響・proseのみ）: (1) merged fold scriptのprose「the 12 roots asserted disjoint … the 12 receipts folded in publication order」「set_equality_after_12」はcodeがfoldする11 receipts（bit-78除外）と食い違い、正しくは11。(2) 同scriptのprint「CONTROL 12 published certificates asserted … 11/11 PASS」も11 certificatesが正。

次のfold baselineはhead **1305**（`class-frontier-cost80d-receipts-recompute-20261115.json`・blob `289c9337…`）。solved 1305はmanifest被覆の簿記であり、REFUTED-D10はLOSS証明ではない。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1、class2、class4は引き続き **UNKNOWN**。

詳細: [検証log](../../log/2026-11-15-n11-class2-lane-cost77d-merged75d77d-79a-folds-second-verification.md)、[検証script](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_cost77d_merged_79a_folds_second_independent_20261115.py)、[検証JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost77d-merged75d77d-79a-folds-second-verification-20261115.json)。

## 2026-11-15: published fold-chain全root監査の双実装80d追従完了 — v1系(第一実装)も80d endpointまで拡張・両実装の全統制一致

第二独立実装v4(80d endpoint・95 pins・587 roots・全統制PASS)に続き、**第一実装(v1系・`audit_published_chain_roots_independent_20261115.py`)もcost-80d/1305 endpointまで機械追従**させ、published fold-chain全root監査の双実装相互検証体制が80dで完成した。

v1系の拡張内容: git blob pins **95→99**(77d `d19c96b7`・merged `97130384`・79a `7dea99ff`・80d `289c9337`の4 headをPOST70E_PINS/ORDERに追加・26+52+21)・root inventory **569→587**(own_claimに77d lane-local 577=565+12・merged 580=569+11・79a 583・80d 587、own_baselineに77d→77c・merged→75d・79a→merged・80d→79a)・D4 orbit **587 roots/576 orbits/11 twins**・CANONICAL_LINE +3エントリ(merged key `cost77d_addition`・79a・80d)で**canonical line 1233..1305・mim 72 = distinct 72・multi 0(exactly-once)**・**bit-78重複rootのexactly-once簿記統制を新設**(root同一性・両child軌道covers・逐次marginal規約・canonical line上のclaim源は75d bit-92/bit-12の各1回・inventory単一計上・merged receipts 11 == 77d receipts minus bit-78)・ENDPOINT_CHECKS 4→**8**(77d 1299/…/receipts 12・79a 1304/…/3・80d 1305/…/4の各completed claimとbyte-exact照合、**merged 75d+77d headは77d claimの`merged_fold`レコード経由でcrosscheck** — before 1296→after 1302・excluded bit-78・`97130384` + 12,460 bytes)。

**両実装の数値は全統制で一致**: 587 roots/576 orbits/11 twins・receipt records 464 anomalies 0・arith 73 heads anomalies 0・canonical line 72/72/multi 0・bit-78 root `00000000100040801202000000200000`・convention-external 1(既知75c)。pin数の差(第一実装99・第二実装95)はv3時点のpin範囲の違い(第一実装は77b/77c/75dをv3で先行pin)によるもので、監査corpusのendpoint(80d)は同一。第一実装はschema v4出力を**新ファイル** `class2-lane-published-chain-roots-independent-audit-v4-20261115.json` に書き、v3出力JSONはpublishedのまま無傷(raw CDN照合済み)・`supersedes`フィールドで関係を明記。2回実行byte-identical(md5 `1156db7d…`・95,881 bytes)。

次のfold baselineはhead **1305**。80d以降のfold(並走laneのcost-82c等)にも同じ拡張パターン(pins追加・own_claim/own_baseline・CANONICAL_LINE・ENDPOINT_CHECKS)で両系統を同時に機械追従できる。solved 1305はmanifest被覆の簿記であり、REFUTED-D10はLOSS証明ではない。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1、class2、class4は引き続き **UNKNOWN**。

詳細: [第一実装v4 log](../../log/2026-11-15-n11-class2-lane-published-chain-roots-audit-v4-first-implementation.md)、[第一実装拡張script](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_published_chain_roots_independent_20261115.py)、[第一実装v4出力JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-published-chain-roots-independent-audit-v4-20261115.json)、[第二実装v4 log(同日)](../../log/2026-11-15-n11-class2-lane-published-chain-roots-audit-v4-second-independent.md)。

## 2026-11-15: 双実装監査一致の機械照合(第三script) — 75d/80d両endpointで全統制一致・bit-78 root同一性を機械固定

双実装一致を人手の表ではなく第三の照合scriptで機械固定した: `audit_dual_implementation_agreement_20261115.py` が4つのpublished audit JSON(v3 `9ae57954`・v2 `db0916c0`・v4first `c3df2d1e`・v4second `e3a0b7da`・blob pin)を再読込し、両endpoint pair(75d: v3 vs v2・80d: v4first vs v4second)で**cumulative per-head bookkeeping(75d 17 heads・80d 21 heads・全フィールド)**・D4 orbit構造・per-record geometry・head arithmetic(69/73 heads・classification/quote counts)・canonical line exactly-once(1296 mim 63・1305 mim 72)・convention-external receipts・child-closure(24/28 heads・全record)・base/chain/baseline inventory・endpoint head records・**bit-78 root hex `00000000100040801202000000200000`**の一致をassert。pin数差(post70e 17 vs 13・21 vs 17)は第一実装のみpinするv2 pin proposals(71c/70f/73g/70g)4件と正確に一致することもassert。**AGREEMENT CONFIRMED**・2回実行byte-identical(md5 `d8878a85…`・8,900 bytes)。75d pairのcumulative 17行の完全一致は今回初の機械確認。fork topology(77d lane-local・bit-78重複・merged rebase)を独立に書いた2実装が同一に導出していることが全行単位で確認された。以後のfold追従では両実装拡張後に本照合scriptのpin差替で一致確認が再実行できる。

cost-82cは並走laneがIN FLIGHT(`class2-lane-cost82c-inflight-20261115.json`・fold: null・claim時head 1305)でsweep実行中。着地後は両監査実装の82c追従と本照合scriptの拡張を次回実行で行う。solved 1305はmanifest被覆の簿記であり、REFUTED-D10はLOSS証明ではない。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1、class2、class4は引き続き **UNKNOWN**。

詳細: [機械照合log](../../log/2026-11-15-n11-published-fold-chain-dual-implementation-agreement.md)、[照合script](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_dual_implementation_agreement_20261115.py)、[agreement JSON](../../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-published-fold-chain-dual-implementation-agreement-20261115.json)。
