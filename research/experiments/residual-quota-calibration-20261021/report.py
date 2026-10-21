#!/usr/bin/env python3
"""Render the locked training choice and prospective confirmation."""
import json,pathlib
HERE=pathlib.Path(__file__).resolve().parent

def main():
    choice=json.loads((HERE/'selection.json').read_text());summary=json.loads((HERE/'summary.json').read_text())
    candidate=choice['candidate'];name=candidate['name']
    lines=['# 小quotaの事前選択と新規確認', '',
        f"固定候補: quota={candidate['quota']}, legal gate={candidate['gate']}。選択commit: `{summary['selection_commit']}`。", '',
        '## 調整用26局面（3反復の局面ごとの中央値合計）', '',
        '| setting | UNKNOWN | solve ms | board nodes | PN calls | aborted roots |',
        '|---|---:|---:|---:|---:|---:|']
    for config,r in choice['training_totals'].items():
        lines.append(f"| {config} | {r['unknown']} | {r['solve_us']/1000:.3f} | {r['nodes']} | {r['pn_nodes']} | {r['pn_aborts']} |")
    lines+=['', 'UNKNOWN数、探索時間、quota、閾値の順に6つのPN候補から選択し、OFFは対照として保持した。',
        '閾値6の3予算は全て259 calls・枯渇ゼロで同じ仕事量。予算間の時間差には測定揺らぎも含む。',
        '', '## commit後の確認（3反復の局面ごとの中央値合計）', '',
        '| corpus | setting | UNKNOWN | solve ms | board nodes | PN calls | aborted roots |',
        '|---|---|---:|---:|---:|---:|---:|']
    for split in ('new','stress'):
        for config,r in summary['totals'][split].items():
            lines.append(f"| {split} | {config} | {r['unknown']} | {r['solve_us']/1000:.3f} | {r['nodes']} | {r['pn_nodes']} | {r['pn_aborts']} |")
    for split in ('new','stress'):
        off=summary['totals'][split]['off']['solve_us'];pn=summary['totals'][split][name]['solve_us']
        lines+=['',f'{split}: OFFに対する探索時間比 {pn/off:.4f}、差 {100*(pn/off-1):+.1f}%。']
    lines+=['', f"事前の採用条件を全て満たしたか: {'YES' if summary['passed'] else 'NO'}。", '',
        '入力・設定を固定してtrain546回、新規確認156回、深い3局面18回、計720根評価。',
        '新規確認は既存826局面とD4非重複、1 trial 1局面、独立subset-mex 5150状態で期待値を検証。',
        '全結果から候補を再選択しない。quotaとboard nodesは別枠であり、node数だけを時間短縮と解釈しない。',
        '探索時間は初期化を除く。単一host・固定コーパスの観測で、時間差の統計的有意性や全入力への一般化は主張しない。']
    (HERE/'comparison.md').write_text('\n'.join(lines)+'\n');print('\n'.join(lines))
if __name__=='__main__':main()
