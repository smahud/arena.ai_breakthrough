from textstats import textstats

def test_simple():
    s = textstats("alpha bb c")
    assert s == {"words": 3, "chars": 10, "avg_word_len": 2.67, "longest": "alpha"}
def test_empty():
    assert textstats("") == {"words": 0, "chars": 0, "avg_word_len": 0.0, "longest": ""}
def test_whitespace():
    assert textstats("   ")["words"] == 0
