# 通常df-pnへの有限残余P/N評価の接続 (2026-10-21)

## 固定プロトコル

K0497の新規26局面と既存の深い3局面をそのまま固定して使う。今回これらを未使用holdoutとは呼ばない。
OFFと、legal閾値6・P/N quota128を比較し、設定の再調整はしない。
通常df-pnの20,000 / 100,000 work nodes、各3反復。fresh solver/TT、共有cacheなし。
各反復で設定順を回転し、同じ入力・node上限で比較する。

通常探索のwork nodeはdf-pnスタック処理の1反復、または内部exact探索の1 board nodeを各1とし、
両者の合計に上限を設ける。expansion数とは区別する。quota128は根全体の残余kernel呼出し数で別枠。
root開始時にquotaをリセットし、残量ゼロ後は通常探索へ戻る。UNKNOWNを確定TTへ格納しない。
node budgetの既定は無制限（既存動作を保持）、明示的な0はworkを許可しない。
`--node-budget`は通常df-pn専用で、exact replay/quant等との混用は拒否する。

残余評価はdf-pnフレームの初回処理時、通常expandより前に直接適用する。
`--exact-legal`を有効にしなくても使える。既存のexact handoffを明示的に併用した場合も、
同じrootの残余quotaとwork node budgetを共有する。
通常探索の既定residual gateは0で維持する。

既知26局面は独立期待値との矛盾を拒否し、UNKNOWNは別に数える。深い3局面は前回同様UNKNOWNを要求し、
新しく確定した場合は測定を停止して独立検証する。rootごとの探索時間をマイクロ秒で記録し、
初期化を含むprocess時間と分離する。1根30秒のwatchdogを併設し、node上限より先に時間が尽きた場合は
理由と消費nodesを記録して比較から隠さない。通常pushのCIに時間比較や深い探索は追加しない。

採用評価は既知局面の誤答ゼロ・UNKNOWN増加ゼロ、各予算の探索時間とnode消費、深い3局面での
費用とUNKNOWN数を併記する。固定コーパス・単一hostの観測であり、通常探索の既定ONや
11×11空盤の解決へ一般化しない。

## 通常CLIと回帰

```sh
/path/to/solver --n=11 --memo=18 --roots-csv=/path/to/roots.csv --node-budget=20000 \
  --residual-exact-legal=6 --residual-evaluator=outcome --residual-outcome-budget=128
```

rootごとの `# dfpn_root` に元の占有mask、結果、終了理由、work nodes、df-pn反復数、
exact board nodes、残余呼出し、PN使用数/残量/abort、探索時間を保存する。
`--residual-profile`を明示した場合だけ内訳時計を使い、その差分もrootごとに記録する。

cpp/tests/test_kyouen_residual_dfpn.cpp は両手番の直接handoff、quotaのrootごとのreset、
低quota UNKNOWN後の通常探索、誤った確定cacheが残らないこと、0 node上限、
exact handoffとの合計node上限、例外後の独立exact replayを通常/UBSanで検査する。
integration.py は通常CLIを実行し、既定OFF、元の4×4空盤の後手勝ち、同じrootのTT再利用、
不正node budget/modeを確認する。CIでは小さい回帰と固定資料の再検査だけを実行する。

## 完了結果

29局面 × 2設定 × 2上限 × 3反復の348根評価を完了した。全既知26局面は全設定・上限・反復で
期待値と一致し、深い3局面は全てUNKNOWN。watchdogでの打ち切りはゼロで、全UNKNOWNは
指定node上限まで処理した。根ごとのwork nodes = df-pn反復 + exact board nodesを全行で確認。
今回の比較はexact handoffを無効にしているため、exact board nodesは全て0だった。

終盤26局面の探索時間中央値合計は、2万上限で14.171→6.925 ms（51.1%短縮）、
10万上限で14.038→6.718 ms（52.1%短縮）。work nodesは両上限とも4458→1262、
expansionsは1805→243。PN呼出しは合計462、handoff内のUNKNOWN返却はゼロ。

深い3局面では2万上限664.375→687.183 ms（+3.4%）、10万上限2929.270→3095.168 ms（+5.7%）。
両上限とも残余呼出しは0で、候補のquota128は未使用だった。通常df-pnがこの予算内で選んだ
フレームに残余切替は発火していない。訪問数・expansion数もOFF/ONで一致し、UNKNOWN数は改善しない。
この差をkernel計算の費用とは呼ばず、切替条件の確認費用や測定揺らぎを含む観測として扱う。
統計的な優劣は主張しない。

したがって、予算128・閾値6は通常df-pnでも明示指定でき、今回の終盤コーパスでは有効だったが、
深いrootの改善は確認できなかった。通常探索の既定gateはOFFを維持する。
完全な表はcomparison.md、設定・binary/source hashはprotocol.jsonを参照する。

再現にはbench.pyの`--freeze --solver /path/to/solver`でsourceと入力をcommit前提で固定し、
固定ファイルをcommit後、同じbinaryで`--solver /path/to/solver`を実行する。
保存済みsummaryがある場合の再実行は拒否するため、新しい測定は別experimentへ保存する。
verify_outputs.pyは旧測定時のsource commitが利用可能ならそのblob hashを検査し、
将来の正当な実装更新を理由に歴史的測定を無効にしない。
