import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_manifest import validate

def record(sample_id="s1", condition="text_only", image_path=None):
    return {
        "sample_id": sample_id,
        "source_intent_id": "intent-1",
        "language": "en",
        "condition": condition,
        "image_path": image_path,
        "prompt_ref": "opaque-1",
        "split": "pilot",
        "label_source": "synthetic-test",
        "license": "test-only",
    }

def test_valid_text_record(tmp_path):
    f = tmp_path / "manifest.jsonl"
    f.write_text(json.dumps(record()) + "\n", encoding="utf-8")
    issues, valid = validate(f)
    assert issues == []
    assert valid == 1

def test_missing_fields(tmp_path):
    row = record()
    del row["language"]
    f = tmp_path / "manifest.jsonl"
    f.write_text(json.dumps(row) + "\n", encoding="utf-8")
    issues, valid = validate(f)
    assert valid == 0
    assert issues[0]["code"] == "missing_fields"

def test_invalid_condition(tmp_path):
    row = record(condition="not-a-condition")
    f = tmp_path / "manifest.jsonl"
    f.write_text(json.dumps(row) + "\n", encoding="utf-8")
    issues, _ = validate(f)
    assert any(i["code"] == "invalid_condition" for i in issues)

def test_duplicate_sample_id(tmp_path):
    f = tmp_path / "manifest.jsonl"
    f.write_text(json.dumps(record()) + "\n" + json.dumps(record()) + "\n", encoding="utf-8")
    issues, _ = validate(f)
    assert any(i["code"] == "duplicate_sample_id" for i in issues)

def test_image_condition_requires_path(tmp_path):
    f = tmp_path / "manifest.jsonl"
    f.write_text(json.dumps(record(condition="image_text")) + "\n", encoding="utf-8")
    issues, _ = validate(f)
    assert any(i["code"] == "image_required" for i in issues)

def test_missing_image_path(tmp_path):
    row = record(condition="image_text", image_path="missing.png")
    f = tmp_path / "manifest.jsonl"
    f.write_text(json.dumps(row) + "\n", encoding="utf-8")
    issues, _ = validate(f)
    assert any(i["code"] == "image_missing" for i in issues)
