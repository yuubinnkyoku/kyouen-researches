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
  role: data 2026-11-15 cost69fの69候補raw sweep完了。WIN7-D10 9、REFUTED-D10 60、打切り0、112752229節点。9 WIN rootはD4軌道9個。証明書未抽出のためS6 frontierへの寄与0。
  note: cost69f 69候補の全raw batch監査。9 WIN7-D10・60 REFUTED-D10・打切り0、D4 root照合
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
scope: n11 S2 {59,60} milestone-5のワークリストとS7証明書再利用。局所S6と三石位置のblocker類1・2の条件付き勝敗を含むが、二石rootや空盤の勝敗は含まない。
evidence: 公開manifestの辞書順md5は0e95a438dbcb486368393de9c73fc21e。94オラクルの全744対称像を使い補完候補15072件を独立列挙。類1の新規WIN7戦略証明書13件・LOSS7証明書2件、類2のWIN7証明書54件と3六石位置の全62子・全72子・全64子のLOSS7証明書を独立検査。類1の五石位置の40六石軌道は既存記録と合わせて全て先手WIN。既存の一部証明書本体は別保管であり、公開監査記録に依存する。 2026-11-15 cost72 bit111 WIN7証明書を独立検査し、cost75b統合後の対象S5親を局所的に2軌道・費用147から1軌道・費用75へ縮小した。global frontierは未再計算。2026-11-15 warm multiband 35 WIN7 receipt後の公開frontierは解消S6 1,109・残り6,738・費用531,295・open需要5,008/395,018。35 rootを同実験の17 verified manifest（WIN7 77・LOSS7 200）、central LOSS7 parent-lift 274鍵、category-1候補396行とD4照合し、衝突0（category-1行は証明書とは数えない）。
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
