import pytest
from hypothesis import given
from hypothesis import strategies as st

from boilerplate import clamp


def test_clamp_uses_each_inclusive_bound() -> None:
    assert clamp(-1, 0, 10) == 0
    assert clamp(11, 0, 10) == 10


def test_clamp_rejects_reversed_bounds() -> None:
    with pytest.raises(ValueError, match="lower must not exceed upper"):
        clamp(0, 1, 0)


@given(value=st.integers(), lower=st.integers(), upper=st.integers())
def test_clamp_result_is_within_a_valid_interval(
    value: int, lower: int, upper: int
) -> None:
    lower, upper = sorted((lower, upper))
    result = clamp(value, lower, upper)
    assert lower <= result <= upper
    if lower <= value <= upper:
        assert result == value
