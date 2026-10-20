#!/usr/bin/env python3
"""Compile independent C++ and compare every state to the Python reference."""
from pathlib import Path
import subprocess
import tempfile
from verify import CASES, solve

ROOT = Path(__file__).resolve().parent
with tempfile.TemporaryDirectory() as tmp:
    exe = Path(tmp) / 'independent'
    subprocess.run(['g++', '-std=c++17', '-O2', '-Wall', '-Wextra', '-pedantic',
                    str(ROOT / 'independent.cpp'), '-o', str(exe)], check=True)
    lines = subprocess.check_output([str(exe)], text=True).splitlines()
    assert len(lines) == 2 * len(CASES)
    for idx, (name, case) in enumerate(CASES.items()):
        assert lines[2 * idx].startswith(name + ' ')
        cpp = list(map(int, lines[2 * idx + 1].split(',')))
        _, py = solve(**case)
        assert cpp == py, f'{name}: independent state vectors differ'
        print(f'{name}: {len(py)} occupied masks independently matched')
print('ALL EXACTLY MATCHED')
