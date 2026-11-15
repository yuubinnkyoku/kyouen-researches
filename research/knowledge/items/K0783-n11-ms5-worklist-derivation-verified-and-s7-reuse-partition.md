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


scope: n11 S2 {59,60} milestone-5のワークリストとS7証明書再利用。局所S6と三石位置のblocker類1・2の条件付き勝敗を含むが、二石rootや空盤の勝敗は含まない。
evidence: "公開manifestの辞書順md5は0e95a438dbcb486368393de9c73fc21e。94オラクルの全744対称像を使い補完候補15072件を独立列挙。類1の新規WIN7戦略証明書13件・LOSS7証明書2件、類2のWIN7証明書54件と3六石位置の全62子・全72子・全64子のLOSS7証明書を独立検査。類1の五石位置の40六石軌道は既存記録と合わせて全て先手WIN。既存の一部証明書本体は別保管であり、公開監査記録に依存する。 2026-11-15 cost72 bit111 WIN7証明書を独立検査し、cost75b統合後の対象S5親を局所的に2軌道・費用147から1軌道・費用75へ縮小した。global frontierは未再計算。2026-11-15 warm multiband 35 WIN7 receipt後の公開frontierは解消S6 1,109・残り6,738・費用531,295・open需要5,008/395,018。35 rootを同実験の17 verified manifest（WIN7 77・LOSS7 200）、central LOSS7 parent-lift 274鍵、category-1候補396行とD4照合し、衝突0（category-1行は証明書とは数えない）。; 2026-11-15 cost69f残り4証明書(bits2/94/109/119)を別V8実行で再検査し全PASS。262,236行、検証訪問560,273局面、union 0/0、4×4行列式による根合法手数一致、8 partのGit blob SHA1・MD5/SHA256一致。cost69fの+9 S6軌道が全て証明書済み 2026-11-15 cost69f全9証明書をPython/Bareiss第三実装で再検査し9/9 PASS（第二検証のV8/BigInt 4件と共通フィールド全一致）。cost69g子の需要は二重役割S5(classes=6)のper-class計数と確定（distinct open parents=3、c1=0,c2=2,c4=2） 2026-11-15 cost72b子 00000000000000809102000002000000（cost 72・需要c1=0,c2=2,c4=0・open親2軌道）の72候補raw sweep完了。WIN7-D10 13（bits 2,11,21,30,31,36,47,66,85,95,97,100,106）・REFUTED-D10 59・打切り0・117,444,772節点。v15 cross-engine 13/13 loss=true、決定性再実行13/13 node-exact。13 rootは証明書未抽出の探索候補のためfrontier寄与0。; 2026-11-15 cost74d公開証明書bits12/66/68/118とcost72b bit85をBigInt独立検査器で5/5再生。D4親持ち上げにより証明書付きS6下限1166→1169（receipt frontier 1179とは区別）; 2026-11-15 cost72b正利得9証明書（bits 2,30,31,36,47,95,97,100,106）をBigInt独立再生9/9、13分割blobと9 whole-file Git SHA1一致。新規S6 manifest 9/9を裏付け、証明書付き下限1169→1178（receipt 1188とは区別）; 2026-11-15 cost78a WIN7証明書5/5（bits 8,20,29,36,109）をBigInt+Number Bareissで二重独立検証し、5 receiptsをcost-67c fold後のhead 1219へfoldして新head 1225/6622/522699/4892/386422（in-manifest marginal 6・childはbit36で閉鎖・第3 class-2 target S5は2行/143）。その後並走cost-69h foldが本78a head 1225にrebaseしてcanonical head 1227/6620/522561/4890/386284を確定（head分岐解消）; 2026-11-15 cost70e WIN7証明書5件（bits 0,8,24,66,79・236,784行・280 sub-roots）をBigInt+Number Bareissの二独立検証器で5/5 PASS（union 0/0・terminal [13,17]・child orbit covered）。foldは未実施でhead 1227不変"
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

