from pathlib import Path
import csv
import sys

csv.field_size_limit(2147483647)
scripts = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(scripts))
import audit_saved_s7_s6_intersection as audit

raise SystemExit(audit.main())
