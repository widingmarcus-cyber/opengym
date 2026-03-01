import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from processor import process_amounts, calculate_total

def test_process_amounts():
    amounts = [10.555, 20.444, 30.999]
    result = process_amounts(amounts)
    # Should round properly, not floor
    assert result == [10.56, 20.44, 31.0]

def test_calculate_total():
    amounts = [10.555, 20.444, 30.999]
    total = calculate_total(amounts)
    assert abs(total - 62.0) < 0.01

def test_single_amount():
    result = process_amounts([99.999])
    assert result == [100.0]

def test_exact_amounts():
    result = process_amounts([10.00, 20.00])
    assert result == [10.0, 20.0]

def test_negative_amounts():
    result = process_amounts([-5.555])
    assert result == [-5.56]
