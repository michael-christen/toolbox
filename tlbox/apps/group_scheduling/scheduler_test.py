from datetime import datetime, timedelta

import pytest

from tlbox.apps.group_scheduling.scheduler import (
    TimeSlot,
    find_common_slots,
    get_availability,
    propose_meeting,
)

# ---------------------------------------------------------------------------
# TimeSlot
# ---------------------------------------------------------------------------


def _ts(start_h: int, end_h: int, day: int = 0) -> TimeSlot:
    base = datetime(2026, 5, 4) + timedelta(days=day)  # arbitrary Monday
    return TimeSlot(base + timedelta(hours=start_h), base + timedelta(hours=end_h))


def test_timeslot_duration():
    assert _ts(9, 11).duration_hours() == 2.0


def test_timeslot_overlaps_true():
    assert _ts(9, 11).overlaps(_ts(10, 12))


def test_timeslot_overlaps_false():
    assert not _ts(9, 10).overlaps(_ts(10, 12))


def test_timeslot_intersection_exists():
    result = _ts(9, 12).intersection(_ts(10, 14))
    assert result is not None
    assert result.duration_hours() == 2.0


def test_timeslot_intersection_none():
    assert _ts(9, 10).intersection(_ts(10, 12)) is None


def test_timeslot_intersection_contained():
    result = _ts(9, 14).intersection(_ts(10, 12))
    assert result is not None
    assert result.duration_hours() == 2.0


# ---------------------------------------------------------------------------
# get_availability
# ---------------------------------------------------------------------------


def test_get_availability_known_person():
    result = get_availability("Alice", 1.0)
    assert result["person"] == "Alice"
    assert len(result["free_slots"]) > 0


def test_get_availability_min_duration_filters():
    # All slots are at most 3h; asking for >4h should return none
    result = get_availability("Alice", 4.0)
    assert result["free_slots"] == []


def test_get_availability_unknown_person():
    result = get_availability("Zara", 1.0)
    assert "error" in result


# ---------------------------------------------------------------------------
# find_common_slots
# ---------------------------------------------------------------------------


def test_find_common_slots_unknown_person():
    result = find_common_slots(["Alice", "Zara"], 1.0)
    assert "error" in result


def test_find_common_slots_all_four_lunch():
    # Thursday 11am–1pm is the only >=1.5h slot for all four
    result = find_common_slots(["Alice", "Bob", "Charlie", "Dana"], 1.5)
    assert "error" not in result
    slots = result["common_slots"]
    assert len(slots) == 1
    start = datetime.fromisoformat(slots[0]["start"])
    assert start.weekday() == 3  # Thursday


def test_find_common_slots_friday_too_short():
    # Friday overlap is only 1h — not enough for 1.5h but fine for 1.0h
    result_1h = find_common_slots(["Alice", "Bob", "Charlie", "Dana"], 1.0)
    result_15h = find_common_slots(["Alice", "Bob", "Charlie", "Dana"], 1.5)
    assert len(result_1h["common_slots"]) > len(result_15h["common_slots"])


def test_find_common_slots_two_people_more_options():
    # Fewer people → more overlapping windows
    result_4 = find_common_slots(["Alice", "Bob", "Charlie", "Dana"], 1.0)
    result_2 = find_common_slots(["Alice", "Bob"], 1.0)
    assert len(result_2["common_slots"]) >= len(result_4["common_slots"])


# ---------------------------------------------------------------------------
# propose_meeting
# ---------------------------------------------------------------------------


def test_propose_meeting_conflict_free():
    # Thursday 11am–12:30pm should have no conflicts
    slots = find_common_slots(["Alice", "Bob", "Charlie", "Dana"], 1.5)
    best = slots["common_slots"][0]
    start_dt = datetime.fromisoformat(best["start"])
    end_dt = start_dt + timedelta(hours=1.5)
    result = propose_meeting(
        "Dinner",
        start_dt.isoformat(),
        end_dt.isoformat(),
        ["Alice", "Bob", "Charlie", "Dana"],
    )
    assert result["ready_to_confirm"] is True
    assert result["conflicts"] == {}


def test_propose_meeting_with_conflict():
    # Monday noon is only Alice and Bob's slot; Charlie and Dana are busy
    from tlbox.apps.group_scheduling.scheduler import _next_weekday

    monday = _next_weekday(0)
    start = monday + timedelta(hours=12)
    end = start + timedelta(hours=1)
    result = propose_meeting(
        "Lunch",
        start.isoformat(),
        end.isoformat(),
        ["Alice", "Bob", "Charlie", "Dana"],
    )
    assert result["ready_to_confirm"] is False
    assert "Charlie" in result["conflicts"] or "Dana" in result["conflicts"]
