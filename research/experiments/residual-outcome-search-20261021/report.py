#!/usr/bin/env python3
"""Summarize frozen measurements; this does not select a default."""
import json,pathlib
HERE=pathlib.Path(__file__).resolve().parent

def main():
    s=json.loads((HERE/'summary.json').read_text())['totals']
    k=json.loads((HERE/'kernel-summary.json').read_text())['totals']
    lines=['# P/N残余探索の固定比較', '',
        f"826 kernel roots: calls {k['sg_calls']:.0f} → {k['pn_calls']:.0f} ({100*(1-k['pn_calls']/k['sg_calls']):.1f}%削減),",
        f"memo {k['sg_memo']:.0f} → {k['pn_memo']:.0f}, time {k['sg_us']/1000:.3f} → {k['pn_us']/1000:.3f} ms ({100*(1-k['pn_us']/k['sg_us']):.1f}%削減)。", '',
        'kernelは7反復の局面ごとの中央値を合計。独立subset oracle 70347状態で全826値を検査。',
        '', '盤面は3反復の局面ごとの中央値合計。初期化を除く。各根5000 board nodes、P/N quotaは100000。', '',
        '| corpus | setting | solve ms | board nodes | PN calls | aborted handoffs |',
        '|---|---|---:|---:|---:|---:|']
    for split in ('train','holdout','saved','stress'):
        for name in ('off','sg6','sg12','pn6','pn12'):
            r=s[split][name]
            lines.append(f"| {split} | {name} | {r['solve_us']/1000:.3f} | {r['nodes']} | {r['pn_nodes']} | {r['pn_aborts']} |")
    lines+=['', '全52既知局面は全設定・反復で期待値と一致。深い3局面は全設定・反復UNKNOWN。',
        'PN12の深い局面は全根でquotaを消費して通常探索へ復帰する。SG12はkernel quotaを持たないため、',
        'PN12との時間差を短絡再帰だけの効果と解釈しない。PN6の差はquota枯渇の有無を別途参照する。',
        '比較設定は事前固定し、holdoutから閾値を選ばない。既定handoffはOFF、既定evaluatorはGrundy。',
        '単一hostでの観測。根ごとの約0.5秒の初期化は別途必要で、wall時間の改善率ではない。',
        '', '## 予算境界の有限検査', '',
        '826局面それぞれで0/1/2/8/32/128/512/2048/100000呼出しを検査し、確定値は全て独立期待値に一致。',
        '各予算はfresh memo。別に同じ局面の部分memoを次の予算へ持ち越し、全826局面が最後に正しい値へ到達。',
        '512呼出しではこの826残余局面全てが確定した。これは盤面root内の全handoff合計の必要予算ではない。']
    (HERE/'comparison.md').write_text('\n'.join(lines)+'\n');print('\n'.join(lines))
if __name__=='__main__':main()
