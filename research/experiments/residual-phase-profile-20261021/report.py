#!/usr/bin/env python3
"""Render comparisons solely from the frozen archived measurements."""
import json,pathlib
HERE=pathlib.Path(__file__).resolve().parent

def main():
    scan=json.loads((HERE/'scan-timing-summary.json').read_text())['totals']
    indexed=json.loads((HERE/'indexed-timing-summary.json').read_text())['totals']
    lines=['# Profile OFF: per-root median sums (3 repeats)', '',
        '| corpus | gate | scan solve ms | indexed solve ms | reduction | nodes |',
        '|---|---:|---:|---:|---:|---:|']
    for corpus in ('saved','stress'):
        for gate in ('0','6','12'):
            a,b=scan[corpus][gate],indexed[corpus][gate]
            assert a['nodes']==b['nodes']
            lines.append(f"| {corpus} | {gate} | {a['solve_us']/1000:.3f} | {b['solve_us']/1000:.3f} | {100*(1-b['solve_us']/a['solve_us']):.1f}% | {a['nodes']} |")
    lines+=['', 'gate 0 はbuilderを呼ばない。同じ処理を別時間帯に測ったばらつきの参考。',
        '全52局面は独立期待値と一致、深い3局面は全設定・全反復UNKNOWN。',
        '各node予算5000。UNKNOWNの探索ノードは各3局面合計15000。',
        'setupを除いたsolve時間を比較する。各行のsolver初期化には約0.5秒が別途必要。',
        '', '# Profile ON: exclusive phase sums (1 repeat)', '',
        '| builder | corpus | gate | construction ms | structure ms | Grundy remainder ms |',
        '|---|---|---:|---:|---:|---:|']
    for label in ('scan','indexed'):
        totals=json.loads((HERE/f'{label}-profile-summary.json').read_text())['totals']
        for corpus in ('saved','stress'):
            for gate in ('6','12'):
                r=totals[corpus][gate]
                lines.append(f"| {label} | {corpus} | {gate} | {r['build_ns']/1e6:.3f} | {r['structure_ns']/1e6:.3f} | {r['grundy_ns']/1e6:.3f} |")
    (HERE/'comparison.md').write_text('\n'.join(lines)+'\n')
    print('\n'.join(lines))
if __name__=='__main__':main()
