import copy
import importlib.util
import itertools
import json
import random
import re
import sys
import unittest
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(EXP/'scripts'))
from independent import Board, aggregate, solve_certificate, verify_dag, mask_from_key
sys.path.insert(0,str(ROOT/'research/experiments/n11-boundary-recovery-20261006/scripts'))
from fixed_player_outcome import outcome


class IndependentTests(unittest.TestCase):
    def test_all_layers_and_boolean_completions(self):
        for n in range(122):
            for size in range(4):
                for vals in itertools.product((0,1,2),repeat=size):
                    completions = itertools.product(*[(False,True) if v==0 else (v==1,) for v in vals])
                    answers = {any(c) if n%2==0 else all(c) for c in completions}
                    expected = 0 if len(answers)>1 else 1 if True in answers else 2
                    self.assertEqual(aggregate(n,vals),expected,(n,vals))
                    self.assertEqual(outcome(n,range(size),dict(enumerate(vals))),
                                     {0:'UNKNOWN',1:'WIN',2:'LOSS'}[expected])

    def test_invalid_values(self):
        for vals in [(3,),(-1,)]:
            with self.assertRaises(ValueError): aggregate(6,vals)
            with self.assertRaises(ValueError): outcome(6,[0],{0:vals[0]})

    def test_full_safe_state_dp_n1_through_n4(self):
        # Separate side-to-move Boolean recurrence, all safe masks (no D4).
        for n in range(1,5):
            b = Board(n)
            @lru_cache(None)
            def side_wins(m):
                return any(not side_wins(m|(1<<p)) for p in b.points(b.legal(m)))
            values = {}
            for m in range(b.full,-1,-1):
                try: legal=b.legal(m)
                except ValueError: continue
                expected = side_wins(m) != bool(m.bit_count()%2)
                children = [values[m|(1<<p)] for p in b.points(legal)]
                values[m]=aggregate(m.bit_count(),children)
                self.assertEqual(values[m],1 if expected else 2,(n,m))
            cert=solve_certificate(b,0,100000)
            self.assertEqual(cert['verdict'],values[0])
            self.assertEqual(verify_dag(b,cert['certificate']),values[0])

    def test_geometry_and_d4_invariance(self):
        b=Board(11)
        for pts in [(0,1,2,3),(0,5,55,60)]:
            with self.assertRaises(ValueError): b.legal(sum(1<<p for p in pts))
        for m in [-1,1<<121]:
            with self.assertRaises(ValueError): b.legal(m)
        for lo,hi in [(1<<64,0),(0,1<<57),(-1,0)]:
            with self.assertRaises(ValueError): mask_from_key(lo,hi)
        rng=random.Random(20261010)
        for _ in range(100):
            m=sum(1<<p for p in rng.sample(range(121),5))
            try: legal=b.legal(m)
            except ValueError: continue
            ch=b.children(m)
            for mapping in b.maps:
                transformed=sum(mapping[p] for p in b.points(m))
                self.assertEqual(b.canonical(transformed),b.canonical(m))
                self.assertEqual(b.children(transformed),ch)
                self.assertEqual(b.legal(transformed),sum(mapping[p] for p in b.points(legal)))
            for c in ch:
                self.assertIn(b.canonical(m),b.predecessors(c))

    def test_certificate_mutations_rejected(self):
        b=Board(4); cert=solve_certificate(b,0,100000)['certificate']
        mutants=[]
        flipped=copy.deepcopy(cert)
        flipped['nodes'][flipped['root']]['verdict']=1
        mutants.append(flipped)
        missing=copy.deepcopy(cert)
        missing['nodes'][missing['root']]['children'].pop()
        mutants.append(missing)
        cycle=copy.deepcopy(cert)
        cycle['nodes'][cycle['root']]['children']=[cycle['root']]
        mutants.append(cycle)
        duplicate=copy.deepcopy(cert)
        duplicate['nodes'][duplicate['root']]['children']*=2
        mutants.append(duplicate)
        leaf=copy.deepcopy(cert)
        leaf['nodes'][leaf['root']]={'mask':'0','verdict':2,'trusted':True}
        mutants.append(leaf)
        for mutant in mutants:
            with self.assertRaises(ValueError): verify_dag(b,mutant)

    def test_wrong_s7_polarity_mutant_fails_oracle(self):
        # The legacy mutant returns WIN for an S7 LOSS witness. A regression
        # assertion against the independent Boolean oracle demonstrably fails.
        mutant=lambda children: 1 if 2 in children else 0
        with self.assertRaises(AssertionError):
            self.assertEqual(mutant([2,0]),aggregate(6,[2,0]))
        with self.assertRaises(AssertionError):
            self.assertEqual(mutant([2,2]),aggregate(6,[2,2]))

    def test_compiled_quarantine_matches_registry(self):
        doc=json.loads((ROOT/'results/n11-s5-evidence-quarantine.json').read_text())
        expected={tuple(r['key']) for r in doc['entries'] if r['active']}
        header=(ROOT/'cpp/solvers/n11_s5_quarantine.hpp').read_text()
        compiled={tuple(map(int,m)) for m in re.findall(r'\{(\d+)ULL,(\d+)ULL\}',header)}
        self.assertEqual(compiled,expected)

    def test_production_s4_empty_boundaries(self):
        sys.path.insert(0,str(ROOT/'research/experiments/n11-boundary-recovery-20261006/scripts'))
        from verify_dual_tight_s4_win import class_status
        from verify_dual_tight_s4_win_v2 import class_status as second
        self.assertEqual(class_status({},set()),'LOSS')
        self.assertEqual(second({},set()),'LOSS')

    def test_missing_registry_fails_closed(self):
        from unittest.mock import patch
        import s5_evidence_policy
        with patch.object(s5_evidence_policy,'REGISTRY',EXP/'missing-registry.json'):
            with self.assertRaises(FileNotFoundError): s5_evidence_policy.quarantined_cache_keys()

    def test_projected_or_quarantined_raw_cannot_bypass_cache_filter(self):
        import tempfile
        from merge_exact_s5_evidence import merge
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)/'replay.csv'
            p.write_text('replay,0,5,92,0,0,1,0,0,1334191389609558016,0\n')
            with self.assertRaisesRegex(SystemExit,'positive-budget'): merge([],[str(p)])
            p.write_text('replay,0,5,90,0,100,1,50,0,1152925911243358208,536870912\n')
            with self.assertRaisesRegex(SystemExit,'active quarantine'): merge([],[str(p)])

    def test_workflow_put_functions_filter_withdrawals(self):
        import ast
        from s5_evidence_policy import quarantined_cache_keys
        for p in (ROOT/'.github/workflows').glob('n11*.yml'):
            active=False; code=[]
            for line in p.read_text().splitlines():
                if 'python' in line and '<<' in line and 'PY' in line:
                    active=True; code=[]
                elif active and line.strip()=='PY':
                    import textwrap
                    tree=ast.parse(textwrap.dedent('\n'.join(code)))
                    for f in tree.body:
                        if isinstance(f,ast.FunctionDef) and f.name=='put':
                            ns=dict(verdict={},origin={},quarantine=quarantined_cache_keys())
                            exec(compile(ast.Module(body=[f],type_ignores=[]),str(p),'exec'),ns)
                            for k in quarantined_cache_keys(): ns['put'](k,1,'historical')
                            self.assertEqual(ns['verdict'],{},p.name)
                    active=False
                elif active: code.append(line)

    def test_all_callable_cache_readers_exclude_withdrawals(self):
        # Load actual production readers, not just the central policy helper.
        folders=['n11-frontier-selection-20261005','n11-boundary-recovery-20261006','n11-strategy-redesign-20261010']
        for folder in folders: sys.path.insert(0,str(ROOT/'research/experiments'/folder/'scripts'))
        historical=ROOT/'research/experiments/n11-boundary-recovery-20261006/output/post-23b52acf-after-round3-round4-completed-merged-s5.cache'
        pairs={
            'cache_aware_reply27_cardinality':'load_cache','cache_aware_reply27_union_cover':'load_cache',
            'rank_reply27_completion_classes':'load_cache','refine_cache_aware_reply27_cover':'load_cache',
            'reply27_selected_hard_s5_s6_cover':'load_cache','derive_all_saved_s6_loss_parents':'load_current_cache',
            'verify_s7_witness_parent_win':'read_s5_cache','verify_s7_witness_parent_win_v2':'read_s5_cache',
            'collect_dual_tight_completed_probe':'read_exact_cache','collect_dual_tight_completed_probe_v2':'read_exact_cache',
            'audit_s5_raw_history':'read_cache','audit_local_s5_s6_against_saved_corpus':'read_s5_cache',
            'audit_local_s6_boundary_history':'read_s5_cache','audit_missing_s5_replay_redundancy':'read_exact_cache',
            'audit_saved_s6_targets':'read_current_cache','prepare_dual_tight_ready_subset_probe':'read_exact_cache',
            'verify_dual_tight_92_win_witness':'read_cache','verify_dual_tight_s4_win':'read_cache',
            'verify_dual_tight_s4_win_v2':'read_cache','verify_dual_tight_s4_win_from_s6':'read_s5_cache',
            'verify_post9dcb_s6_reverse_integration':'read_cache','study':'s5cache'}
        banned={(1152925911243358208,536870912),(10448351135499552768,128)}
        for name,func in pairs.items():
            with self.subTest(reader=name):
                mod=__import__(name)
                result=getattr(mod,func)(historical)
                if isinstance(result,tuple): result=result[0]
                self.assertFalse(banned.intersection(result))

if __name__=='__main__': unittest.main()
