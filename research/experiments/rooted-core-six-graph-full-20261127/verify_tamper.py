#!/usr/bin/env python3
"""Fail-closed tamper battery for the audit of the 6-vertex graph core family.

Each case runs verify_independent.py on a scratch tampered copy and requires
verdict FAIL (rc != 0). Cases are run one at a time from the shell to respect
sandbox wall limits; this driver takes the case name as argv[1] and prints a
one-line result. The official audit.json is never modified.

T1_value_flip      : flip one Grundy value inside a record prefix (length 700)
T2_phantom_record  : append a record with a 3-point edge mask (provably outside
                     the pure-two-edge family) and bump new_closure_states
T3_certified_flip  : jointly_certified true -> false
T4_window_flip     : joint_start_candidate 500 -> 400 (needed adjusted)
control            : untouched copy must PASS
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
VER = HERE / 'verify_independent.py'


def run_on(audit_dict, tmp):
    p = tmp / 'audit_tampered.json'
    p.write_text(json.dumps(audit_dict))
    r = subprocess.run([sys.executable, str(VER), str(p)],
                       capture_output=True, text=True)
    try:
        out = json.loads(r.stdout)
        verdict = out.get('verdict')
    except Exception:
        verdict = 'CRASH'
    return verdict, r.returncode


def main(argv):
    case = argv[1]
    base = json.loads((HERE / 'output' / 'audit.json').read_text())
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        if case == 'control':
            t = base
        elif case == 'T1_value_flip':
            t = json.loads(json.dumps(base))
            t['records'][7]['prefix'][700] = (t['records'][7]['prefix'][700] + 1) % 40
        elif case == 'T2_phantom_record':
            t = json.loads(json.dumps(base))
            phantom = dict(t['records'][0])
            phantom['n'] = 6
            phantom['forbidden'] = [7]  # 3-point mask: outside the family
            t['records'].append(phantom)
            t['new_closure_states'] += 1
        elif case == 'T3_certified_flip':
            t = json.loads(json.dumps(base))
            t['jointly_certified'] = False
        elif case == 'T4_window_flip':
            t = json.loads(json.dumps(base))
            t['joint_start_candidate'] = 400
            t['values_needed_through'] = 2 * 400 + 69
        else:
            print('unknown case', case)
            return 2
        v, rc = run_on(t, tmp)
    ok = (v == 'PASS' and rc == 0) if case == 'control' else (v != 'PASS' and rc != 0)
    print(json.dumps(dict(case=case, verdict=v, rc=rc,
                          fail_closed_ok=bool(ok))))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
