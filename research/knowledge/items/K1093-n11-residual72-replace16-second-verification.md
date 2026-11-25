---
id: K1093
title: 残余72行 代替16根 depth-10掃引の独立第二検証（幾何・記録台帳）
kind: verification
status: verified
topics: [search-methods, certificates, geometry]
aliases:
  - independent second audit of the residual72 replace16 depth10 sweep geometry and probe ledger
  - K1089 residual49 replacement16 geometry verification
relations:
- type: verifies
  target: K1089
  note: N11 K1089の代替16根・残余49行・32 probe記録を、元の掃引機械とは別の整数幾何実装で照合する
artifacts:
- path: research/experiments/n11-residual72-replace16-independent-second-verification-20261120/README.md
  role: source
  note: 対象・入力SHA-256・独立照合方法・検証境界
- path: research/experiments/n11-residual72-replace16-independent-second-verification-20261120/verify_replace16_second_20261120.py
  role: verifier
  note: D4再導入、4×4整数行列式、72行分割、49行被覆、32 probe台帳をfail-closed検査
- path: research/experiments/n11-residual72-replace16-independent-second-verification-20261120/output/audit.json
  role: data
  note: 16/16 gate、1120 root四点組・1080基底行四点組・32 probeの再照合結果
- path: research/log/2026-11-20-n11-residual72-replace16-second-verification.md
  role: log
  note: 独立監査の結果と限界
scope: >-
  K1089の残余49行を被覆する8石代替16根と、両AND順序・depth-10の32 probe記録。K1085/K1086/K1088/K1089の公開正本を固定し、根・行の幾何と記録台帳を独立照合する。DFPNエンジンの再実行、証明書抽出、receipt fold、S6行の閉鎖は対象外。
evidence: >-
  4正本のSHA-256とrunner v17 Git blobを照合。別実装のD4変換と4×4整数行列式により、16根の1120四点組と72基底行の1080四点組を再検査。K1086の23 WIN8主張行と49 REFUTED主張行はK1085の72行を分割し、K1088の残余49行とK1089の16根計画・32 probe台帳に一致する。49行は各1回だけ被覆され、全probeは未打切り・両順序整合。16/16 gate PASS。これは探索結果の二次照合であり、探索器の正しさや未収録の探索過程を証明しない。
---

## 判定範囲

WIN8-D10 candidateは証明書ではなく、REFUTED-D10はLOSS証明ではない。