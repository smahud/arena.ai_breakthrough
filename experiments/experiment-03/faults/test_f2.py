import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from f2_paginate import pages_needed
def test_exact(): assert pages_needed(10, 5) == 2
def test_remainder(): assert pages_needed(11, 5) == 3
def test_zero(): assert pages_needed(0, 5) == 0
