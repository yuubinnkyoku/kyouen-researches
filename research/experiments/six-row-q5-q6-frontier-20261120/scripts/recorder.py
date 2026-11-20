#!/usr/bin/env python3
import json, os

def vali(s):
    try: return int(s)
    except Exception: return None

rec = {
    'w': int(os.environ['R_W']), 'm': int(os.environ['R_M']), 'q': int(os.environ['R_Q']),
    'mode': os.environ['R_MODE'], 'rowY': None if os.environ['R_ROWY'] == 'null' else vali(os.environ['R_ROWY']),
    'generator': 'sat2.js-md5-282ae832efa0080127c6c153e65e1c3c',
    'vars': vali(os.environ['R_VARS']), 'clauses': vali(os.environ['R_CLAUSES']), 'curves': vali(os.environ['R_CURVES']),
    'cnf_md5': os.environ['R_CNFMD5'],
    'gen_sec': round(float(os.environ['R_G1']) - float(os.environ['R_G0']), 2),
    'kissat': {
        'result': os.environ['R_RESULT'], 'rc': int(os.environ['R_RC']),
        'conflicts': vali(os.environ['R_CONFLICTS']), 'sec_cap': int(os.environ['R_CAP']),
        'sec': round(float(os.environ['R_T1']) - float(os.environ['R_T0']), 2),
    },
    'ts': os.environ.get('R_TS', ''),
    'gen_extra': os.environ.get('R_EXTRA_LABEL',''), 'solver_cfg': os.environ.get('R_KCFG_LABEL',''),
}
if os.environ.get('R_RESULT') == 'SATISFIABLE' and os.environ.get('R_WIT'):
    wit = json.load(open(os.environ['R_WIT']))
    def jok(s):
        try: return json.loads(s[s.index('{'):s.rindex('}') + 1]).get('ok') is True
        except Exception: return False
    def tpass(s):
        try: return json.loads(s[s.index('{'):s.rindex('}') + 1]).get('pass') is True
        except Exception: return False
    js, py, ts = os.environ.get('R_VJS', ''), os.environ.get('R_VPY', ''), os.environ.get('R_VTS', '')
    rows = {}
    for x, y in wit['stones']:
        rows[y] = rows.get(y, 0) + 1
    rec['witness'] = {
        'nStones': wit['nStones'],
        'rows': [rows.get(y, 0) for y in range(int(os.environ['R_W']))],
        'js_ok': jok(js), 'py_ok': jok(py), 'ts_pass': tpass(ts),
        'js_rc': vali(os.environ.get('R_VJSRC')), 'py_rc': vali(os.environ.get('R_VPYRC')), 'ts_rc': vali(os.environ.get('R_VTSRC')),
        'satjs_verifyconfig_ok': (wit.get('verify') or {}).get('ok') is True,
    }
    # mirror witness + verify outputs into the record for publication (small)
    rec['witness']['stones'] = wit['stones']
    rec['witness']['verify_outputs'] = {'js': js, 'py': py, 'ts': ts}
else:
    rec['witness'] = None
    if os.environ['R_RESULT'] not in ('SATISFIABLE', 'UNSATISFIABLE'):
        rec['cnf_deleted'] = True

with open(os.environ['R_RECORDS'], 'a') as f:
    f.write(json.dumps(rec, separators=(',', ':')) + '\n')
# resilience mirror to workspace root (survives env resets)
try:
    import shutil
    shutil.copy(os.environ['R_RECORDS'], '/home/user/kr65-records-mirror.jsonl')
except Exception:
    pass
print(json.dumps({'m': rec['m'], 'q': rec['q'], 'mode': rec['mode'], 'rowY': rec['rowY'],
                  'kissat': rec['kissat'], 'witness': {k: rec['witness'][k] for k in ('nStones', 'rows', 'js_ok', 'py_ok', 'ts_pass')} if rec['witness'] else None}))
