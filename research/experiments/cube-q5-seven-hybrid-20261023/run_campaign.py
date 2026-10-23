#!/usr/bin/env python3
"""Explicitly launched multi-stage search; save, freeze deltas and retain PN work."""
from pathlib import Path
import argparse
import fcntl
import gzip
import hashlib
import json
import os
import shutil
import signal
import subprocess
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('engine', type=Path)
    parser.add_argument('verifier', type=Path)
    parser.add_argument('workspace', type=Path)
    parser.add_argument('reports', type=Path)
    parser.add_argument('roots', type=Path)
    parser.add_argument('base', type=Path)
    parser.add_argument('base_index', type=Path)
    parser.add_argument('sealed', type=Path)
    parser.add_argument('--stages', type=int, default=10)
    parser.add_argument('--epochs', type=int, default=8)
    args = parser.parse_args()
    pause_requested = False
    def request_pause(_signum, _frame):
        nonlocal pause_requested
        pause_requested = True
    signal.signal(signal.SIGTERM, request_pause)
    signal.signal(signal.SIGINT, request_pause)
    args.workspace.mkdir(parents=True, exist_ok=True)
    lock = (args.workspace/'.campaign.lock').open('w')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    bases = [str(args.base), str(args.sealed)]
    indices = [str(args.base_index), str(args.sealed)+'.idx']
    state_path = args.workspace/'run-state.json'
    def write(state):
        tmp = state_path.with_suffix('.new');tmp.write_text(json.dumps(state, indent=2)+'\n');tmp.replace(state_path)
    start_stage = 2
    if state_path.exists():
        previous = json.loads(state_path.read_text())
        if previous['status'] == 'verified-result':return
        bases = previous['bases']; indices = previous['indices']
        if previous['status'] in ['stage-budget-completed', 'blocked-storage']:
            start_stage = previous['last_completed_stage']+1
        elif previous['status'] == 'stage-saved':
            start_stage = previous['stage']+1
            if bases[-1] != previous['sealed']:
                bases.append(previous['sealed']);indices.append(previous['sealed']+'.idx')
        else:
            start_stage = previous['stage']
            proc = Path('/proc')/str(previous.get('pid', -1))/'cmdline'
            if proc.exists() and proc.read_bytes().startswith(os.fsencode(args.engine)+b'\0'):
                raise RuntimeError('the recorded worker is still running')
            sealed = args.workspace/f'layer-{start_stage}.hyb'
            if sealed.exists() and not Path(previous['checkpoint']).exists():
                bases.append(str(sealed));indices.append(str(sealed)+'.idx');start_stage += 1
    end_stage = start_stage+args.stages
    for stage in range(start_stage, end_stage):
        if shutil.disk_usage(args.workspace).free < 3*1024**3:
            write({'status': 'blocked-storage', 'bases': bases, 'indices': indices, 'last_completed_stage': stage-1})
            return
        checkpoint = args.workspace/f'active-{stage}.hyb'
        report = args.reports/f'stage-{stage}.jsonl'
        if report.exists() and report.stat().st_size:
            attempt = 1
            while report.with_suffix(f'.attempt-{attempt}.jsonl').exists():attempt += 1
            report.replace(report.with_suffix(f'.attempt-{attempt}.jsonl'))
        log = args.workspace/f'stage-{stage}.log'
        prefix = args.workspace/f'proof-{stage}'
        command = [str(args.engine), '7', ','.join(bases), ','.join(indices), str(checkpoint),
                   str(args.roots), '1000000', str(args.epochs), '4', '1500000', '9', str(prefix)]
        if not checkpoint.exists():command.append('--promote')
        state = {'status': 'running', 'stage': stage, 'bases': bases.copy(), 'indices': indices.copy(),
                 'checkpoint': str(checkpoint), 'report': str(report), 'log': str(log), 'command': command}
        with report.open('w') as out, log.open('w') as err:
            process = subprocess.Popen(command, stdout=out, stderr=err)
            state['pid'] = process.pid;write(state)
            resource_stop = None
            while process.poll() is None:
                if pause_requested:
                    resource_stop = 'pause';process.terminate();break
                if shutil.disk_usage(args.workspace).free < 2*1024**3:
                    resource_stop = 'storage';process.terminate();break
                try:
                    values = dict(line.split() for line in Path('/sys/fs/cgroup/memory.stat').read_text().splitlines())
                    if int(values['anon']) > 7*1024**3:
                        resource_stop = 'memory';process.terminate();break
                except (FileNotFoundError, KeyError):pass
                time.sleep(5)
            code = process.wait()
        if code:
            state.update(status='failed', returncode=code);write(state);return
        records = [json.loads(line) for line in report.read_text().splitlines()]
        if not records:
            state.update(status='failed-empty-report');write(state);return
        last = records[-1];state['last_record'] = last
        if last['outcome'] != 'UNKNOWN':
            state.update(status='verifying');write(state)
            certificates = list(args.workspace.glob(prefix.name+'-*.cert'))
            assert len(certificates) == 1
            proof = certificates[0];verification = args.reports/f'stage-{stage}-verified.json'
            with verification.open('w') as out:
                checked = subprocess.run([str(args.verifier), str(proof)], stdout=out, stderr=subprocess.PIPE, text=True)
            if checked.returncode:
                state.update(status='verification-failed', error=checked.stderr);write(state);return
            assert json.loads(verification.read_text())['verified']
            compressed = args.reports/f'stage-{stage}.cert.gz'
            with proof.open('rb') as inp, compressed.open('wb') as out:
                with gzip.GzipFile(fileobj=out, mode='wb', filename='', mtime=0) as zipped:shutil.copyfileobj(inp, zipped)
            with compressed.open('rb') as file:digest=hashlib.file_digest(file,'sha256').hexdigest()
            state.update(status='verified-result', certificate=str(compressed), sha256=digest, verification=str(verification))
            write(state);return
        if resource_stop == 'pause' or pause_requested:
            state.update(status='paused', resource_stop='pause');write(state);return
        sealed = args.workspace/f'layer-{stage}.hyb'
        if sealed.exists():raise RuntimeError('refusing to overwrite an immutable layer')
        checkpoint.replace(sealed);bases.append(str(sealed));indices.append(str(sealed)+'.idx')
        state.update(status='stage-saved', sealed=str(sealed), bases=bases.copy(), indices=indices.copy(), resource_stop=resource_stop);write(state)
        if resource_stop == 'storage':return
    write({'status': 'stage-budget-completed', 'bases': bases, 'indices': indices,
           'last_completed_stage': end_stage-1})


if __name__ == '__main__':
    main()
