from slugutil import slugify

def test_basic(): assert slugify("Hello World") == "hello-world"
def test_punct(): assert slugify("Hi, there! 42 ok?") == "hi-there-42-ok"
def test_collapse(): assert slugify("a---b   c") == "a-b-c"
def test_trim(): assert slugify("--edge--") == "edge"
def test_empty(): assert slugify("!!!") == ""
