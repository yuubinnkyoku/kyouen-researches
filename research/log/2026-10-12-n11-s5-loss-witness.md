# 2026-10-12: S5 LOSS witness budget benchmark

最新main `49f28e6a1da2e5f77d0d5c8ec7af2edb3c8f5ab9` を基準にした。K0375/K0378から最新候補S4由来3根と前候補S4由来3根を固定した。source raw、両terminal-only proof bundle、独立検査receipt、6根integration auditをSHA拘束で一致確認した。探索中のsolver processはなく、他担当の現行S4 UNKNOWN対象は調べずに保持した。

実験前に候補表を作り、各親S5の直接法/分割法とも250,000 nodeを上限とした。分割法は固定順で5子を各50,000 nodeまで調査した。測定したA–Eはすべて各方式合計1,500,000 nodes、direct6根UNKNOWN、S6 30行UNKNOWNで、S6 LOSS witnessは0だった。legal-count orderの効果と7石層共有のヒットは観測されなかった。共有TT方式はfresh-TTのS6 batchよりwallが短いが、node数は同じでdirect方式との時間差も小さいため、計算量改善とは判定しなかった。高予算追試・現行unknown S5探索は行わなかった。

solverには既定offの `--exact-replay-stop-on-loss` を追加した。4×4独立fixtureでLOSS後だけ停止し、UNKNOWN後は処理を続けること、flagなしの結果列が保たれることを確認した。fixture開発・再現時の試行はnode合計149として独立監査JSONに残した。solver-trusted値は独立証明へ取り込んでいない。
