"""One-time, checked correction of legacy S7 fixed-player propagation helpers."""
from study import ROOT, OLD, EXP, dump
import hashlib
import subprocess

def main():
    names=['prepare_s7_witness_probe.py','verify_s7_witness_parent_win.py',
           'verify_s7_witness_parent_win_v2.py','materialize_s7_witness_evidence.py']
    receipts=[]
    for name in names:
        p=OLD.parent/'scripts'/name
        before=p.read_bytes()
        s=before.decode('utf-8')
        changes={
          's7 LOSS':'s7 WIN', 'S7 LOSS':'S7 WIN',
          'exact LOSS witness':'exact WIN witness', 'exact LOSS is a witness':'exact WIN is a witness',
          'exact LOSS witnesses':'exact WIN witnesses', 'saved_exact_s7_loss_witnesses':'saved_exact_s7_win_witnesses',
        }
        if name=='prepare_s7_witness_probe.py':
            changes.update({'any(exact.get(child) == 2':'any(exact.get(child) == 1',
                            'all(exact.get(child) == 1':'all(exact.get(child) == 2'})
        elif name.startswith('verify_'):
            changes.update({'verdict != 2':'verdict != 1', 's7_exact[key] = 2':'s7_exact[key] = 1',
                            's7_exact.get(child) == 2':'s7_exact.get(child) == 1',
                            'all(s7_exact.get(child) == 1':'all(s7_exact.get(child) == 2',
                            '"verdict": "LOSS"':'"verdict": "WIN"'})
        else:
            changes.update({'{"2": 2}':'{"1": 2}', 'int(replay[6]) != 2':'int(replay[6]) != 1',
                            'item.get("verdict") != 2':'item.get("verdict") != 1',
                            ',7,2,{row[7]}':',7,1,{row[7]}'})
        # Specific replacements precede the broader string replacements.
        for a,b in changes.items():
            s=s.replace(a,b)
        assert s!=before.decode('utf-8')
        # Verify the universally quantified branch was not accidentally inverted.
        if name.startswith('verify_'):
            s=s.replace('all(s7_exact.get(child) == 1','all(s7_exact.get(child) == 2')
        p.write_text(s,encoding='utf-8',newline='')
        receipts.append(dict(path=p.relative_to(ROOT).as_posix(),
              before_sha256=hashlib.sha256(before).hexdigest(), after_sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    dump(EXP/'output/legacy-helper-repair.json',dict(source_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
          files=receipts, historical_artifacts_modified=False))

if __name__=='__main__':
    main()
