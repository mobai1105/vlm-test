#!/usr/bin/env python3
"""Validate local JSONL/CSV experiment manifests without printing prompt contents."""
import argparse
import csv
import json
from pathlib import Path

REQUIRED = {"sample_id", "source_intent_id", "language", "condition", "image_path",
            "prompt_ref", "split", "label_source", "license"}
CONDITIONS = {"text_only", "image_only", "image_text", "benign_control"}
SPLITS = {"pilot", "dev", "test"}

def load_records(path):
    path = Path(path)
    if path.suffix.lower() == ".jsonl":
        records = []
        with path.open(encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                if not line.strip():
                    continue
                try:
                    records.append((line_no, json.loads(line)))
                except json.JSONDecodeError:
                    records.append((line_no, None))
        return records
    if path.suffix.lower() == ".csv":
        with path.open(encoding="utf-8-sig", newline="") as f:
            return [(i + 2, row) for i, row in enumerate(csv.DictReader(f))]
    raise ValueError("Input must be .jsonl or .csv")

def validate(path, check_images=True):
    path = Path(path)
    issues, seen = [], set()
    try:
        records = load_records(path)
    except Exception as exc:
        return [{"line": 0, "code": "read_error", "detail": type(exc).__name__}], 0
    valid = 0
    for line_no, row in records:
        if not isinstance(row, dict):
            issues.append({"line": line_no, "code": "invalid_json_or_record", "detail": "record is not a JSON object"})
            continue
        missing = sorted(k for k in REQUIRED if k not in row)
        if missing:
            issues.append({"line": line_no, "code": "missing_fields", "detail": ",".join(missing)})
            continue
        sid = str(row.get("sample_id", "")).strip()
        if not sid:
            issues.append({"line": line_no, "code": "empty_sample_id", "detail": "sample_id is empty"})
        elif sid in seen:
            issues.append({"line": line_no, "code": "duplicate_sample_id", "detail": "sample_id duplicated"})
        seen.add(sid)
        if row.get("condition") not in CONDITIONS:
            issues.append({"line": line_no, "code": "invalid_condition", "detail": "condition not in allowed set"})
        if row.get("split") not in SPLITS:
            issues.append({"line": line_no, "code": "invalid_split", "detail": "split not in allowed set"})
        image_path = row.get("image_path")
        if row.get("condition") in {"image_only", "image_text"} and not image_path:
            issues.append({"line": line_no, "code": "image_required", "detail": "image condition requires image_path"})
        if check_images and image_path:
            p = Path(image_path)
            if not p.is_absolute():
                p = path.parent / p
            if not p.is_file():
                issues.append({"line": line_no, "code": "image_missing", "detail": "local image path does not exist"})
        if not str(row.get("source_intent_id", "")).strip():
            issues.append({"line": line_no, "code": "empty_source_intent_id", "detail": "source_intent_id is empty"})
        else:
            valid += 1
    return issues, valid

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest")
    parser.add_argument("--no-image-check", action="store_true")
    parser.add_argument("--report", help="Optional JSON report path")
    args = parser.parse_args()
    issues, valid = validate(args.manifest, check_images=not args.no_image_check)
    report = {"manifest": Path(args.manifest).name, "valid_records": valid, "issue_count": len(issues), "issues": issues}
    output = json.dumps(report, indent=2, ensure_ascii=False)
    print(output)
    if args.report:
        target = Path(args.report)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(output + "\n", encoding="utf-8")
    raise SystemExit(1 if issues else 0)

if __name__ == "__main__":
    main()
