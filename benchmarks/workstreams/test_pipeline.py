import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pipeline import process
from jsonstore import load

def test_pipeline_roundtrip(tmp_path):
    p = str(tmp_path / "store.json")
    r1 = process("Hello World!", "alpha bb c", p)
    assert r1["slug"] == "hello-world"
    assert r1["stats"]["avg_word_len"] == 2.67
    r2 = process("Second Entry", "one", p)
    data = load(p)
    assert set(data) == {"hello-world", "second-entry"}
