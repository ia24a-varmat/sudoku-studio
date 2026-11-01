import pytest
from portfolio.baselines.paradigm_examples import RowChecker, check_row_procedural, check_row_functional


@pytest.mark.parametrize('row, expected', [
    ((1, 2, 3, 0, 0, 0, 0, 0, 0), True),
    ((1, 2, 1, 0, 0, 0, 0, 0, 0), False),
    ((0, 0, 0, 0, 0, 0, 0, 0, 0), True),
])
def test_same_behavior(row, expected):
    assert RowChecker(row).is_valid() is expected
    assert check_row_procedural(row) is expected
    assert check_row_functional(row) is expected
