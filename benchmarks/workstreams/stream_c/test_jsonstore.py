import os
from jsonstore import load, save

def test_roundtrip(tmp_path):
    p = str(tmp_path / "s.json")
    save(p, {"b": 2, "a": 1})
    assert load(p) == {"a": 1, "b": 2}

def test_missing_returns_empty(tmp_path):
    assert load(str(tmp_path / "nope.json")) == {}

def test_overwrite_no_tmp_left(tmp_path):
    p = str(tmp_path / "s.json")
    save(p, {"x": 1}); save(p, {"x": 2})
    assert load(p) == {"x": 2}
    assert [f for f in os.listdir(tmp_path) if f.endswith(".tmp")] == []
