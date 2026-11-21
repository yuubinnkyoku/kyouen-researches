# 単一オーナー宣言: 4行盤 q=6/q=7 行欠損極大 witness band/frontier レーン（2026-11-21）

- **宣言時刻**: 2026-11-21T00:45Z（実行環境時刻）。
- **レーン**: 固定幅 w=4・q点版の (4,m,q=6) m>=6 と (4,m,q=7) m>=7 の行欠損極大（deficient-maximal）witness band・frontier掃引。
- **現状確認**: 宣言時点の main に (4,*,6)/(4,*,7) の witness band 実験・item・log は存在しない（search_code で four-row/q6/q7 横断確認済み）。w=4 は q=4,5（m22教室・band extension）と q=8（解決済み）のみ。
- **作業内容**: sat2.js def-mode 完全符号化（K0810 verbatim・md5 pin 282ae832…）+ kissat 4.0.4 linux-amd64（md5 pin 3a5eba83…）による def-mode 掃引。SAT 幅は 3系統検証（sat.js verifyConfig・verify_witness.py・verify3.py 部分集合ベース第三検証器・新規）。INDET 幅は rowY 分割・--lex=H 交差符号化で再試行し、解決しなければ正直に INDET 記録（不在主張ではない）。
- **出版予定**: 実験 dir（four-row-q6-q7-frontier-20261121・records.jsonl append-only・witness・pinned scripts）→ K item（採番はpush直前3点確認）→ 研究log → knowledge README bullet。主張形は K0827/K1149 準拠: witness帯 = 有限witness下界（M_{4,q} >= m+1 形）のみ。UNSAT 幅は当該幅の欠損極大非存在の有限完全証明としてのみ記録し、M への反映は容量側存在定理が確立していないため主張しない。上界 U_{4,6}=103, U_{4,7}=81（K0318）の代入は引用値。
- **衝突プロトコル**: push前に必ず最新 main を取り直す。同一対象 (4,m,6)/(4,m,7) への先行宣言・records・item を検出した場合は即時停止・記録して次回へ回す。push競合・同時書込みが起きた場合は無理に押し進めず状况記録に留める。
- **標準11×11空盤への言及なし**（w=4 固定幅レーンは標準盤と無関係・UNKNOWN のまま）。
