"""Integrity and generation regressions; no new mathematical searches."""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import BEGIN, END, ROOT, checked, link, load_items, solution_table, update_readme, validate, views


def item(number=1):
    return dict(id=f"K{number:04}", title="Scope-specific knowledge", kind="proposition",
                status="proved", topics=["rules"], aliases=[], relations=[],
                artifacts=[dict(path="README.md", role="source", note="Explicit premise and scope")],
                _path=f"research/knowledge/items/K{number:04}-scope-specific-knowledge.md",
                _body="A statement with explicit quantification, useful evidence and a clear verification boundary.\n")


class IntegrityTests(unittest.TestCase):
    def errors(self, items):
        return "\n".join(validate(items)[0])

    def test_content_slug_and_legacy_filename(self):
        for filename in ("K0001.md", "K0001-n11-dfpn-search-status.md"):
            with self.subTest(filename=filename):
                i=item(); i["_path"]="research/knowledge/items/"+filename
                self.assertEqual(self.errors([i]), "")

    def test_invalid_slug_or_id_prefix_is_rejected(self):
        for filename in ("K0002-n11-status.md", "K0001-.md", "K0001-N11-status.md", "K0001-n11--status.md"):
            with self.subTest(filename=filename):
                i=item(); i["_path"]="research/knowledge/items/"+filename
                self.assertIn("filename must be", self.errors([i]))

    def test_same_id_with_different_slugs_is_still_duplicate(self):
        a,b=item(),item(); b["_path"]="research/knowledge/items/K0001-other-slug.md"
        self.assertIn("duplicate id", self.errors([a,b]))

    def test_kind_specific_valid_statuses(self):
        for kind,status in (("definition","active"),("method","active"),("computation","computed"),
                            ("verification","verified"),("proposition","refuted"),("question","open")):
            with self.subTest(kind=kind,status=status):
                i=item();i.update(kind=kind,status=status)
                self.assertEqual(self.errors([i]), "")

    def test_kind_specific_invalid_statuses(self):
        for kind,status in (("definition","proved"),("method","computed"),("computation","proved"),
                            ("verification","proved"),("proposition","active"),("question","refuted")):
            with self.subTest(kind=kind,status=status):
                i=item();i.update(kind=kind,status=status)
                self.assertIn(f"status {status} is not allowed for kind {kind}", self.errors([i]))

    def test_missing_or_malformed_status_policy_fails_closed(self):
        original=yaml.safe_load((ROOT/"research/knowledge/VOCABULARY.yaml").read_text(encoding="utf-8"))
        for broken in (None, {}, {**original["status_by_kind"],"definition":None},
                       {**original["status_by_kind"],"method":["unknown-status"]}):
            with self.subTest(policy=broken),tempfile.TemporaryDirectory() as temp:
                root=Path(temp);dest=root/"research/knowledge";dest.mkdir(parents=True)
                vocab=copy.deepcopy(original);vocab["status_by_kind"]=broken
                (dest/"VOCABULARY.yaml").write_text(yaml.safe_dump(vocab),encoding="utf-8")
                (root/"README.md").write_text("source",encoding="utf-8")
                errors,_=validate([item()],root)
                self.assertTrue(any("VOCABULARY: status_by_kind" in e for e in errors))

    def test_self_reference_for_each_acyclic_relation(self):
        for relation in ("depends_on", "supersedes"):
            with self.subTest(relation=relation):
                i=item(); i["relations"]=[dict(type=relation,target="K0001")]
                self.assertIn(relation+" self-reference",self.errors([i]))

    def test_cycles_for_each_acyclic_relation(self):
        for relation in ("depends_on", "supersedes"):
            with self.subTest(relation=relation):
                items=[item(n) for n in range(1,4)]
                for i,target in zip(items,["K0002","K0003","K0001"]):
                    i["relations"]=[dict(type=relation,target=target)]
                self.assertIn(relation+" cycle: K0001 -> K0002 -> K0003 -> K0001",self.errors(items))

    def test_shared_dependency_is_not_a_cycle(self):
        items=[item(n) for n in range(1,5)]
        items[0]["relations"]=[dict(type="depends_on",target="K0002"),dict(type="depends_on",target="K0003")]
        for i in items[1:3]: i["relations"]=[dict(type="depends_on",target="K0004")]
        self.assertEqual(self.errors(items),"")

    def test_unknown_target_and_alias_collision(self):
        a,b=item(1),item(2)
        a["aliases"]=["F-A"]; b["aliases"]=["F-A"]
        a["relations"]=[dict(type="verifies",target="K9999")]
        errors=self.errors([a,b])
        self.assertIn("duplicate alias F-A",errors)
        self.assertIn("unknown relation target: K9999",errors)

    def test_artifact_path_boundaries(self):
        for path in ("../README.md","C:/private/log.txt","https://example.com/proof","not-in-repo.csv"):
            with self.subTest(path=path):
                i=item();i["artifacts"][0]["path"]=path
                self.assertTrue(self.errors([i]))

    def test_isolated_item_is_warning_not_error(self):
        i=item();i["artifacts"]=[]
        errors,warnings=validate([i])
        self.assertEqual(errors,[])
        self.assertTrue(any("isolated item" in w for w in warnings))

    def test_incoming_relation_alone_is_thin_evidence(self):
        a,b=item(1),item(2);a["artifacts"]=[]
        b["relations"]=[dict(type="supports",target="K0001")]
        errors,warnings=validate([a,b])
        self.assertEqual(errors,[])
        self.assertFalse(any("isolated item" in w for w in warnings))
        self.assertTrue(any("thin evidence" in w for w in warnings))

    def test_duplicate_yaml_keys_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);dest=root/"research/knowledge/items";dest.mkdir(parents=True)
            (dest/"K0001.md").write_text("---\nid: K0001\nid: K0002\n---\nStatement\n",encoding="utf-8")
            items,errors=load_items(root)
            self.assertEqual(items,[])
            self.assertIn("duplicate YAML key",errors[0])

    def test_strong_solution_cannot_mean_only_first_moves(self):
        i=copy.deepcopy(next(i for i in checked()[0] if i.get("solution",{}).get("level")=="strong"))
        i["solution"]["classification"]=["root","first-moves"]
        self.assertIn("strong solution requires all-safe classification",self.errors([i]))

    def test_unknown_winner_cannot_be_solved(self):
        i=copy.deepcopy(next(i for i in checked()[0] if i.get("solution")))
        i["solution"]["outcome"]="unknown";i["solution"]["level"]="weak"
        self.assertIn("unknown outcome must remain unsolved",self.errors([i]))

    def test_malformed_classification_reports_error_without_crashing(self):
        for value in (None, {"all-safe-grundy": True}, [["all-safe-grundy"]]):
            with self.subTest(value=value):
                i=copy.deepcopy(next(i for i in checked()[0] if i.get("solution",{}).get("level")=="strong"))
                i["solution"]["classification"]=value
                self.assertIn("invalid solution.classification",self.errors([i]))


class GenerationTests(unittest.TestCase):
    def test_links_use_actual_path_and_relative_location(self):
        i=item();i["_path"]="research/knowledge/items/K0001-new-descriptive-slug.md"
        self.assertEqual(link(i),"[K0001](../items/K0001-new-descriptive-slug.md)")
        self.assertEqual(link(i,"."),"[K0001](research/knowledge/items/K0001-new-descriptive-slug.md)")
        for output in views([i],[]).values():
            self.assertNotIn("(../items/K0001.md)",output)

    def test_stage_column_keeps_computed_strong_solution_plain(self):
        i=copy.deepcopy(next(i for i in checked()[0] if i["id"]=="K0006"))
        table=solution_table([i])
        self.assertIn("strong; second-player-win",table)
        self.assertNotIn("要監査",table)
        self.assertEqual(i["solution"]["level"],"strong")  # display does not alter the reported metadata

    def test_human_readme_survives_with_both_newline_styles(self):
        for newline in ("\n","\r\n"):
            with self.subTest(newline=repr(newline)):
                before="# 人間の研究説明"+newline+"9×9詳細 | 10×10留保"+newline+newline
                after=newline+"11×11の未解決説明"+newline
                original=before+BEGIN+newline+"old table"+newline+END+after
                result=update_readme(original,"新しい表\n81/81\n")
                self.assertEqual(result.split(BEGIN)[0],before)
                self.assertEqual(result.split(END)[1],after)
                self.assertEqual(update_readme(result,"新しい表\n81/81\n"),result)
                if newline=="\r\n": self.assertNotIn("\n",result.replace("\r\n",""))

    def test_first_append_is_idempotent(self):
        for original in ("# 本文","# 本文\n","# 本文\r\n"):
            result=update_readme(original,"table\n")
            self.assertTrue(result.startswith(original))
            self.assertEqual(update_readme(result,"table\n"),result)

    def test_ambiguous_markers_fail_closed(self):
        for text in (BEGIN,END,END+BEGIN,BEGIN+BEGIN+END,BEGIN+END+END):
            with self.subTest(text=text):
                with self.assertRaises(ValueError):update_readme(text,"table\n")

    def test_reverse_indexes_and_markdown_escape(self):
        a,b=item(1),item(2);a["title"]="値 | 適用条件";a["aliases"]=["B548"]
        b["relations"]=[dict(type="verifies",target="K0001",note="independent check")]
        output=views([a,b],[])
        self.assertIn("値 \\| 適用条件",output["index.md"])
        self.assertIn("B548",output["aliases.md"])
        self.assertIn("K0001",output["artifacts.md"])
        self.assertIn("K0002",output["artifacts.md"])
        self.assertIn("← verifies",output["relations.md"])
        self.assertEqual(a["relations"],[])  # reverse links never mutate canon

    def test_relations_without_notes_have_no_trailing_whitespace(self):
        a,b=item(1),item(2)
        b["relations"]=[dict(type="depends_on",target="K0001")]
        output=views([a,b],[])["relations.md"]
        self.assertFalse(output.endswith("\n\n"))
        self.assertTrue(all(line==line.rstrip() for line in output.splitlines()))


class MigrationBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.items,cls.errors,cls.warnings=checked()
        cls.by_id={i["id"]:i for i in cls.items}
        cls.by_alias={a:i for i in cls.items for a in i["aliases"]}

    def test_canonical_items_validate(self):
        self.assertEqual(self.errors,[])

    def test_migrated_items_all_have_content_slugs(self):
        self.assertTrue(self.items)
        self.assertTrue(all(Path(i["_path"]).stem.startswith(i["id"]+"-") for i in self.items))

    def test_readme_table_follows_main_results_before_analysis_and_english(self):
        text=(ROOT/"README.md").read_text(encoding="utf-8")
        self.assertLess(text.index("唯一の正本"),text.index(BEGIN))
        self.assertLess(text.index(END),text.index("## 読み方"))
        self.assertLess(text.index(END),text.index("## English"))

    def test_all_adopted_originals_have_aliases(self):
        audit=json.loads((ROOT/"research/experiments/original-claims/output/round26_original_scope_index.json").read_text(encoding="utf-8"))
        rows=[r for r in audit["rows"] if r["original_status"]!="NOT_AUDITED"]
        self.assertEqual(len(rows),165)
        self.assertEqual([r["id"] for r in rows if r["id"] not in self.by_alias],[])

    def test_square_outcomes_and_evidence_boundaries(self):
        winners=["first-player-win"]*3+["second-player-win"]+["first-player-win"]*2+["second-player-win"]*2+["first-player-win","second-player-win"]
        for n,winner in enumerate(winners,1):
            self.assertTrue(any(i.get("solution",{}).get("board")==f"{n}×{n}" and i["solution"]["outcome"]==winner for i in self.items),n)
        eleven=self.by_id["K0023"]["solution"]
        self.assertEqual((eleven["level"],eleven["outcome"]),("unsolved","unknown"))
        self.assertEqual(self.by_id["K0006"]["status"],"computed")
        self.assertEqual(self.by_id["K0058"]["status"],"verified")
        self.assertEqual(self.by_id["K0289"]["status"],"computed")
        self.assertFalse(any(i["status"]=="needs-review" for i in self.items))
        self.assertIn("81/81",self.by_id["K0021"]["solution"]["coverage"])
        self.assertIn("100/100",self.by_id["K0022"]["solution"]["coverage"])
        self.assertEqual(self.by_id["K0103"]["status"],"open")


if __name__ == "__main__":
    unittest.main()
