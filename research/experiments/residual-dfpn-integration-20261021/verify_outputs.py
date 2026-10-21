#!/usr/bin/env python3
"""Recheck frozen ordinary-search inputs and archived per-root counters."""
import hashlib,json,pathlib,subprocess
import bench
HERE=pathlib.Path(__file__).resolve().parent

def main():
    p=json.loads((HERE/'protocol.json').read_text());data=json.loads((HERE/'fixtures.json').read_text())
    assert data==bench.fixtures()
    assert p['limits']==[20000,100000] and p['settings']==['off','pn128-g6'] and p['repeats']==3
    assert p['quota']==128 and p['gate']==6 and p['memo_power']==18 and p['wall_guard_seconds']==30
    assert p['late_sha256']==bench.digest(bench.LATE) and p['deep_sha256']==bench.digest(bench.DEEP)
    assert p['fixtures_sha256']==bench.digest(HERE/'fixtures.json')
    assert set(p['roots_sha256'])=={f'{i:02}.csv' for i in range(29)}
    for name,value in p['roots_sha256'].items():assert bench.digest(HERE/'roots'/name)==value
    assert len(p['source_commit'])==40
    assert set(p['source_hashes'])=={'cpp/solvers/kyouen_dfpn_root.cpp','cpp/solvers/kyouen_residual_micro.hpp'}
    available=subprocess.run(['git','cat-file','-e',p['source_commit']+'^{commit}'],cwd=bench.ROOT,capture_output=True).returncode==0
    for path,value in p['source_hashes'].items():
        assert len(value)==64
        if available:
            blob=subprocess.check_output(['git','show',f'{p["source_commit"]}:{path}'],cwd=bench.ROOT)
            assert hashlib.sha256(blob).hexdigest()==value
    count=0
    if (HERE/'summary.json').exists():
        records=json.loads((HERE/'records.json').read_text());assert len(records)==348
        keys=set()
        for row in records:
            key=(row['setting'],row['limit'],row['repeat'],row['id']);assert key not in keys;keys.add(key)
            assert row['setting'] in bench.SETTINGS and row['limit'] in bench.LIMITS and row['repeat'] in (0,1,2)
            prefix=f'{row["setting"]}-n{row["limit"]}-r{row["repeat"]}-id{row["id"]:02}'
            actual=bench.parse_root((HERE/'raw'/f'{prefix}.csv').read_text(),data[row['id']],row['setting'],row['limit'],row['repeat'])
            assert actual=={k:v for k,v in row.items() if k!='process_us'}
            assert row['process_us']>=row['solve_us']
        summary=json.loads((HERE/'summary.json').read_text())
        assert summary['protocol_sha256']==bench.digest(HERE/'protocol.json')
        assert summary['totals']==bench.aggregate(records)
        count=len(records)
    print(f'VERIFIED ordinary df-pn frozen roots=29, work-node/PN budget accounting, archived rows={count}')
if __name__=='__main__':main()
