from __future__ import annotations

from math import isclose

import pytest

from pycooldown.sliding_window import SlidingWindow


@pytest.mark.parametrize(["period", "capacity"], [(1, 1), (1, 2), (2, 1)])
def test_init(period: float, capacity: int) -> None:
    window = SlidingWindow(capacity, period)
    assert window.period == period
    assert window.capacity == capacity
    assert window._window == 0.0
    assert window._tokens == capacity
    assert window._last == 0.0


def test_get_tokens_before_trigger() -> None:
    window = SlidingWindow(1, 1)
    assert window.get_tokens() == 1


def test_get_tokens_after_trigger() -> None:
    window = SlidingWindow(1, 1)
    window.update_ratelimit()
    assert window.get_tokens() == 0


def test_update_ratelimit() -> None:
    window = SlidingWindow(1, 1)
    retry_after_before = window.update_ratelimit()
    retry_after_after = window.update_ratelimit()

    assert retry_after_before is None
    assert isclose(retry_after_after, 1.0, rel_tol=0.15)


def test_retry_after_equals_update_ratelimit_before_trigger() -> None:
    window = SlidingWindow(1, 1)
    retry_after_before = window.get_retry_after()
    update_ratelimit_before = window.update_ratelimit() or 0

    assert retry_after_before == update_ratelimit_before == 0


def test_retry_after_equals_update_ratelimit_after_trigger() -> None:
    window = SlidingWindow(1, 1)
    window.update_ratelimit()
    retry_after = window.get_retry_after()
    update_ratelimit = window.update_ratelimit()

    assert isclose(retry_after, update_ratelimit, rel_tol=0.15)
    assert isclose(retry_after, 1.0, rel_tol=0.15)
    assert isclose(update_ratelimit, 1.0, rel_tol=0.15)


def test_reset() -> None:
    window = SlidingWindow(1, 1)
    window.update_ratelimit()

    assert window.get_tokens() == 0

    window.reset()

    assert window.get_tokens() == 1
