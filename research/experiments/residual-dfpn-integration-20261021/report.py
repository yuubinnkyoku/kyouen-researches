#!/usr/bin/env python3
"""Render the fixed normal-search comparison without choosing parameters."""
import json,pathlib
HERE=pathlib.Path(__file__).resolve().parent

def main():
    summary=json.loads((HERE/'summary.json').read_text())['totals']
    lines=['# 通常df-pnの固定比較', '',
        'legal gate=6、P/N quota=128を再調整せず、OFFと比較。3反復の局面ごとの中央値合計。',
        'work nodesはdf-pn反復 + 内部exact board nodes。P/N callsは別枠。', '',
        '| corpus | node limit | setting | UNKNOWN | solve ms | work nodes | expansions | PN calls | aborted roots | watchdog runs |',
        '|---|---:|---|---:|---:|---:|---:|---:|---:|---:|']
    for group in ('late','deep'):
        for limit in ('20000','100000'):
            for setting,r in summary[group][limit].items():
                lines.append(f"| {group} | {limit} | {setting} | {r['unknown']} | {r['solve_us']/1000:.3f} | {r['nodes']} | {r['expansions']} | {r['pn_nodes']} | {r['pn_aborts']} | {r['watchdog_runs']} |")
    lines+=['', '| corpus | node limit | ON / OFF solve time | difference |', '|---|---:|---:|---:|']
    for group in ('late','deep'):
        for limit in ('20000','100000'):
            data=summary[group][limit];off=data['off']['solve_us'];on=data['pn128-g6']['solve_us']
            lines.append(f'| {group} | {limit} | {on/off:.4f} | {100*(on/off-1):+.1f}% |')
    lines+=['', '入力はK0497の既知26局面と以前からの深い3局面。今回は新しいholdoutとは呼ばない。',
        '29 roots × 2 settings × 2 limits × 3 repeats = 348 root solves。各processはcold solver/TT。',
        '通常探索の既定gateはOFF。明示flagでのみ有効にする。既存exact handoffを併用しなくても残余評価が働く。',
        'process時間には約0.5秒/根の初期化が別途含まれる。上のsolve時間は初期化を除く。',
        'node limitはexpansion数や以前のexact replayのboard node数とは異なる指標。',
        '単一host・固定局面の観測で、時間差の統計的有意性や他の初期局面での性能は主張しない。']
    (HERE/'comparison.md').write_text('\n'.join(lines)+'\n');print('\n'.join(lines))
if __name__=='__main__':main()
