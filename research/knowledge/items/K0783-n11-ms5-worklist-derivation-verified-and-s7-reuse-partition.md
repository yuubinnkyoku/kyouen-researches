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

scope: n11 S2 {59,60} milestone-5のワークリストとS7証明書再利用。局所S6と三石位置のblocker類1・2の条件付き勝敗を含むが、二石rootや空盤の勝敗は含まない。
evidence: 公開manifestの辞書順md5は0e95a438dbcb486368393de9c73fc21e。94オラクルの全744対称像を使い補完候補15072件を独立列挙。類1の新規WIN7戦略証明書13件・LOSS7証明書2件、類2のWIN7証明書54件と3六石位置の全62子・全72子・全64子のLOSS7証明書を独立検査。類1の五石位置の40六石軌道は既存記録と合わせて全て先手WIN。既存の一部証明書本体は別保管であり、公開監査記録に依存する。 2026-11-15 cost72 bit111 WIN7証明書を独立検査し、cost75b統合後の対象S5親を局所的に2軌道・費用147から1軌道・費用75へ縮小した。global frontierは未再計算。2026-11-15 warm multiband 35 WIN7 receipt後の公開frontierは解消S6 1,109・残り6,738・費用531,295・open需要5,008/395,018。35 rootを同実験の17 verified manifest（WIN7 77・LOSS7 200）、central LOSS7 parent-lift 274鍵、category-1候補396行とD4照合し、衝突0（category-1行は証明書とは数えない）。; 2026-11-15 cost69f残り4証明書(bits2/94/109/119)を別V8実行で再検査し全PASS。262,236行、検証訪問560,273局面、union 0/0、4×4行列式による根合法手数一致、8 partのGit blob SHA1・MD5/SHA256一致。cost69fの+9 S6軌道が全て証明書済み 2026-11-15 cost69f全9証明書をPython/Bareiss第三実装で再検査し9/9 PASS（第二検証のV8/BigInt 4件と共通フィールド全一致）。cost69g子の需要は二重役割S5(classes=6)のper-class計数と確定（distinct open parents=3、c1=0,c2=2,c4=2） 2026-11-15 cost72b子 00000000000000809102000002000000（cost 72・需要c1=0,c2=2,c4=0・open親2軌道）の72候補raw sweep完了。WIN7-D10 13（bits 2,11,21,30,31,36,47,66,85,95,97,100,106）・REFUTED-D10 59・打切り0・117,444,772節点。v15 cross-engine 13/13 loss=true、決定性再実行13/13 node-exact。13 rootは証明書未抽出の探索候補のためfrontier寄与0。; 2026-11-15 cost74d公開証明書bits12/66/68/118とcost72b bit85をBigInt独立検査器で5/5再生。D4親持ち上げにより証明書付きS6下限1166→1169（receipt frontier 1179とは区別）; 2026-11-15 cost72b正利得9証明書（bits 2,30,31,36,47,95,97,100,106）をBigInt独立再生9/9、13分割blobと9 whole-file Git SHA1一致。新規S6 manifest 9/9を裏付け、証明書付き下限1169→1178（receipt 1188とは区別）- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost74d-win7-certificates-20261115.json
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
