"""Stream B: text statistics. Zero cross-stream imports by design (EXP-02 S3)."""

def textstats(text: str) -> dict:
    words = text.split()
    return {
        "words": len(words),
        "chars": len(text),
        "avg_word_len": round(sum(len(w) for w in words) / len(words), 2) if words else 0.0,
        "longest": max(words, key=len) if words else "",
    }
