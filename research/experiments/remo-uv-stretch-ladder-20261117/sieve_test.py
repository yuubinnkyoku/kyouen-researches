#!/usr/bin/env python3
"""Sieve test: in V(m), when does label 0 die? In U(m), when does label m-1 die?

Conjecture under test (SIEVE):
  V: label 0 is eliminated in the pot-(p-1) stretch, where p = spf(2m+1);
     it survives the whole game iff 2m+1 is prime (then V(m)=0).
     At death it holds exactly p stones (one more than the stretch pot).
  U: label m-1 is eliminated in the pot-(p-1) stretch, p = spf(2m+3);
     survives iff prime (then U(m)=m-1).
     At death it holds exactly p-1 stones (a cold death at the stretch pot).
"""
import json
import sys


def spf(n):
    p = 2
    while p * p <= n:
        if n % p == 0:
            return p
        p += 1
    return n


def sieve_isprime(n):
    if n < 2:
        return False
    return spf(n) == n


def play_watch(m, pot0, watch_label, pins=None, idx=None):
    """Simulate; return (survivor, death_record). death_record =
    (phase_idx_1based, pot_at_death, held_at_death) or None."""
    lab = list(range(m))
    cts = [2] * m
    k = m
    ptr = 0
    pot = pot0
    ph = 0
    death = None
    while k > 1:
        ph += 1
        for i in range(pot):
            cts[(ptr + i) % k] += 1
        li = (ptr + pot) % k
        held = cts[li]
        if lab[li] == watch_label:
            death = (ph, pot, held)
        del cts[li]
        del lab[li]
        ptr = li if li < k - 1 else 0
        pot = held
        k -= 1
    return lab[0], death


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    pinmode = len(sys.argv) > 2 and sys.argv[2] == "pins"
    uv = None
    if pinmode:
        uv = json.load(open("../remo-pc-twin-laws-20261117/data/pc_uv8000.json"))
    bad_v = bad_u = bad_pin = 0
    stats_v = {}
    stats_u = {}
    for m in range(1, N + 1):
        sv, death = play_watch(m, 1, 0)
        t = 2 * m + 1
        p = spf(t)
        if pinmode and sv != uv["V"][m - 1]:
            bad_pin += 1
            print(f"V PIN mismatch m={m} sv={sv} pin={uv['V'][m-1]}")
        if p == t:  # prime
            if sv != 0 or death is not None:
                bad_v += 1
                print(f"V BAD prime m={m} t={t} sv={sv} death={death}")
        else:
            if death is None:
                bad_v += 1
                print(f"V BAD composite m={m} t={t} sv={sv} death=None")
            else:
                ph, pot_at, held = death
                if pot_at != p - 1 or held != p:
                    bad_v += 1
                    print(f"V BAD level m={m} t={t} spf={p} pot_at={pot_at} "
                          f"held={held} ph={ph}")
                stats_v[(pot_at, held - pot_at)] = stats_v.get(
                    (pot_at, held - pot_at), 0) + 1
        if m >= 2:
            sv, death = play_watch(m, 2, m - 1)
            t = 2 * m + 3
            p = spf(t)
            if pinmode and sv != uv["U"][m - 1]:
                bad_pin += 1
                print(f"U PIN mismatch m={m} sv={sv} pin={uv['U'][m-1]}")
            if p == t:
                if sv != m - 1 or death is not None:
                    bad_u += 1
                    print(f"U BAD prime m={m} t={t} sv={sv} death={death}")
            else:
                if death is None:
                    bad_u += 1
                    print(f"U BAD composite m={m} t={t} sv={sv} death=None")
                else:
                    ph, pot_at, held = death
                    if pot_at != p - 1 or held != p - 1:
                        bad_u += 1
                        print(f"U BAD level m={m} t={t} spf={p} pot_at={pot_at} "
                              f"held={held} ph={ph}")
                    stats_u[(pot_at, held - pot_at)] = stats_u.get(
                        (pot_at, held - pot_at), 0) + 1
    print(f"N={N}: V violations={bad_v}  U violations={bad_u}"
          + (f"  pin mismatches={bad_pin}" if pinmode else ""))
    top_v = sorted(stats_v.items(), key=lambda x: -x[1])[:8]
    top_u = sorted(stats_u.items(), key=lambda x: -x[1])[:8]
    print("V (pot_at, held-pot) counts:", top_v)
    print("U (pot_at, held-pot) counts:", top_u)


if __name__ == "__main__":
    main()
