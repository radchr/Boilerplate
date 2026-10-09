def clamp(value: int, lower: int, upper: int) -> int:
    """Return ``value`` constrained to the inclusive interval ``[lower, upper]``."""
    if lower > upper:
        raise ValueError("lower must not exceed upper")
    if value < lower:
        return lower
    if value > upper:
        return upper
    return value
