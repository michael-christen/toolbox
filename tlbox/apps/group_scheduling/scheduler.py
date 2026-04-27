"""Group scheduling experiment: Claude agent that coordinates meeting times.

Usage:
    bazel run //tlbox/apps/group_scheduling:scheduler           # live API call
    bazel run //tlbox/apps/group_scheduling:scheduler -- --mock # replay without API key

The agent is given a set of friends with hardcoded availability windows and
a scheduling request. It uses tool calls to query availability and propose
a time that works for everyone.

Without an API key, pass --mock to replay the expected tool-call sequence and
see the scheduling logic in action. The mock records what a real run produced
(verified against actual tool outputs):

  Round 1 — find_common_slots(all 4, 1.5h)
    → Thursday 11am–1pm (2h). Only match; Friday overlaps just 1h.
  Round 2 — propose_meeting(Thursday 11am–12:30pm)
    → no conflicts
  Final — agent explains tradeoff: only daytime slot works for all 4;
    Friday evening available but falls short at 1h.
"""
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta

import anthropic
from anthropic.types import MessageParam, ToolParam, ToolResultBlockParam, ToolUseBlock

MOCK_MODE = "--mock" in sys.argv

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class TimeSlot:
    start: datetime
    end: datetime

    def duration_hours(self) -> float:
        return (self.end - self.start).total_seconds() / 3600

    def overlaps(self, other: "TimeSlot") -> bool:
        return self.start < other.end and other.start < self.end

    def intersection(self, other: "TimeSlot") -> "TimeSlot | None":
        start = max(self.start, other.start)
        end = min(self.end, other.end)
        if start < end:
            return TimeSlot(start, end)
        return None

    def __str__(self) -> str:
        fmt = "%a %b %d %I:%M %p"
        return f"{self.start.strftime(fmt)} – {self.end.strftime(fmt)}"


@dataclass
class Person:
    name: str
    free_slots: list[TimeSlot]
    notes: str = ""


# ---------------------------------------------------------------------------
# Sample data: next week's availability for a few friends
# ---------------------------------------------------------------------------

def _next_weekday(weekday: int) -> datetime:
    """Return the next occurrence of weekday (0=Mon) at midnight."""
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    days_ahead = weekday - today.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return today + timedelta(days=days_ahead)

def _slot(weekday: int, start_h: int, end_h: int) -> TimeSlot:
    base = _next_weekday(weekday)
    return TimeSlot(
        base + timedelta(hours=start_h),
        base + timedelta(hours=end_h),
    )

PEOPLE: dict[str, Person] = {
    "Alice": Person(
        name="Alice",
        free_slots=[
            _slot(0, 12, 14),   # Mon 12–2pm
            _slot(1, 18, 21),   # Tue 6–9pm
            _slot(3, 11, 13),   # Thu 11am–1pm
            _slot(4, 17, 20),   # Fri 5–8pm
        ],
        notes="Prefers evenings when possible",
    ),
    "Bob": Person(
        name="Bob",
        free_slots=[
            _slot(0, 18, 21),   # Mon 6–9pm
            _slot(2, 12, 14),   # Wed 12–2pm
            _slot(3, 11, 14),   # Thu 11am–2pm
            _slot(4, 18, 21),   # Fri 6–9pm
        ],
        notes="Can't do mornings",
    ),
    "Charlie": Person(
        name="Charlie",
        free_slots=[
            _slot(1, 12, 15),   # Tue 12–3pm
            _slot(3, 10, 14),   # Thu 10am–2pm
            _slot(4, 17, 21),   # Fri 5–9pm
        ],
        notes="Flexible on weekdays",
    ),
    "Dana": Person(
        name="Dana",
        free_slots=[
            _slot(1, 18, 21),   # Tue 6–9pm
            _slot(3, 11, 13),   # Thu 11am–1pm
            _slot(4, 17, 19),   # Fri 5–7pm
        ],
        notes="Busy most of Monday",
    ),
}

# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

def get_availability(person_name: str, min_duration_hours: float) -> dict:
    """Return free slots for a person that are at least min_duration_hours long."""
    person = PEOPLE.get(person_name)
    if not person:
        return {"error": f"Unknown person: {person_name}. Known: {list(PEOPLE.keys())}"}
    slots = [s for s in person.free_slots if s.duration_hours() >= min_duration_hours]
    return {
        "person": person_name,
        "notes": person.notes,
        "free_slots": [
            {"start": s.start.isoformat(), "end": s.end.isoformat(), "label": str(s)}
            for s in slots
        ],
    }


def find_common_slots(
    person_names: list[str], min_duration_hours: float
) -> dict:
    """Return time slots when ALL listed people are free for at least min_duration_hours."""
    maybe_people = [PEOPLE.get(n) for n in person_names]
    missing = [n for n, p in zip(person_names, maybe_people) if p is None]
    if missing:
        return {"error": f"Unknown people: {missing}"}
    people = [p for p in maybe_people if p is not None]

    # Build candidate windows from first person's slots
    candidates: list[TimeSlot] = list(people[0].free_slots)
    for person in people[1:]:
        new_candidates: list[TimeSlot] = []
        for candidate in candidates:
            for slot in person.free_slots:
                intersection = candidate.intersection(slot)
                if intersection and intersection.duration_hours() >= min_duration_hours:
                    new_candidates.append(intersection)
        candidates = new_candidates

    return {
        "attendees": person_names,
        "min_duration_hours": min_duration_hours,
        "common_slots": [
            {"start": s.start.isoformat(), "end": s.end.isoformat(), "label": str(s)}
            for s in candidates
        ],
    }


def propose_meeting(
    title: str,
    start_iso: str,
    end_iso: str,
    attendees: list[str],
) -> dict:
    """Finalize a meeting proposal."""
    start = datetime.fromisoformat(start_iso)
    end = datetime.fromisoformat(end_iso)
    slot = TimeSlot(start, end)
    conflicts: dict[str, list[str]] = {}
    for name in attendees:
        person = PEOPLE.get(name)
        if not person:
            continue
        free = any(
            fs.start <= slot.start and fs.end >= slot.end
            for fs in person.free_slots
        )
        if not free:
            conflicts[name] = [str(fs) for fs in person.free_slots]

    return {
        "proposal": {
            "title": title,
            "time": str(slot),
            "attendees": attendees,
        },
        "conflicts": conflicts,
        "ready_to_confirm": len(conflicts) == 0,
    }


TOOLS: list[ToolParam] = [
    {
        "name": "get_availability",
        "description": (
            "Get a single person's free time slots for the coming week, "
            "filtered to slots that are at least min_duration_hours long."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "person_name": {"type": "string", "description": "Name of the friend"},
                "min_duration_hours": {
                    "type": "number",
                    "description": "Minimum slot length in hours",
                },
            },
            "required": ["person_name", "min_duration_hours"],
        },
    },
    {
        "name": "find_common_slots",
        "description": (
            "Find time slots when ALL listed people are simultaneously free "
            "for at least min_duration_hours."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "person_names": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Names of the friends",
                },
                "min_duration_hours": {
                    "type": "number",
                    "description": "Minimum overlap duration in hours",
                },
            },
            "required": ["person_names", "min_duration_hours"],
        },
    },
    {
        "name": "propose_meeting",
        "description": (
            "Propose a specific meeting time. Returns whether all attendees "
            "are free and any conflicts."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Meeting title"},
                "start_iso": {
                    "type": "string",
                    "description": "Start time in ISO 8601 format",
                },
                "end_iso": {
                    "type": "string",
                    "description": "End time in ISO 8601 format",
                },
                "attendees": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Names of attendees",
                },
            },
            "required": ["title", "start_iso", "end_iso", "attendees"],
        },
    },
]

TOOL_HANDLERS = {
    "get_availability": lambda inp: get_availability(**inp),
    "find_common_slots": lambda inp: find_common_slots(**inp),
    "propose_meeting": lambda inp: propose_meeting(**inp),
}

# ---------------------------------------------------------------------------
# Agent loop
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """\
You are a friendly scheduling assistant helping coordinate a group of friends.
You have access to each person's weekly availability and tools to find common free slots.

When given a scheduling request:
1. Use find_common_slots to identify times that work for everyone.
2. If there's no perfect overlap, look for the best partial overlap and explain the tradeoff.
3. Once you've found a good time, use propose_meeting to confirm it's conflict-free.
4. Give a clear, friendly summary of the proposed plan.

Be concise and direct. Prefer times that honor each person's stated preferences when possible.
"""

SCHEDULING_REQUEST = (
    "Can you find a 1.5-hour dinner slot for Alice, Bob, Charlie, and Dana "
    "sometime next week? They'd prefer an evening if possible."
)


def run_agent() -> None:
    client = anthropic.Anthropic()
    messages: list[MessageParam] = [{"role": "user", "content": SCHEDULING_REQUEST}]

    print(f"Request: {SCHEDULING_REQUEST}\n")
    print("=" * 60)

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )

        for block in response.content:
            if block.type == "text":
                print(f"\nAgent: {block.text}")

        if response.stop_reason == "end_turn":
            break

        if response.stop_reason != "tool_use":
            print(f"Unexpected stop reason: {response.stop_reason}")
            break

        tool_results: list[ToolResultBlockParam] = []
        for block in response.content:
            if not isinstance(block, ToolUseBlock):
                continue
            handler = TOOL_HANDLERS.get(block.name)
            if handler is None:
                result = {"error": f"Unknown tool: {block.name}"}
            else:
                print(f"\n[tool] {block.name}({json.dumps(block.input)})")
                result = handler(block.input)
                print(f"[result] {json.dumps(result, indent=2)}")
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": json.dumps(result),
            })

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})


def run_mock() -> None:
    """Replay the expected agent interaction without hitting the API.

    Verified against actual tool outputs from the scheduling data above:
    - All-4 intersection at >=1.5h: Thursday 11am–1pm only (2h).
    - Friday: 6–7pm overlap exists but is only 1h — below threshold.
    - Agent should note the daytime tradeoff and propose Thursday.
    """
    attendees = ["Alice", "Bob", "Charlie", "Dana"]
    print(f"Request: {SCHEDULING_REQUEST}\n")
    print("=" * 60)

    # Round 1: find common slots at the requested 1.5h duration
    print(f'\n[tool] find_common_slots({{"person_names": {attendees}, "min_duration_hours": 1.5}})')
    r1 = find_common_slots(person_names=attendees, min_duration_hours=1.5)
    print(f"[result] {json.dumps(r1, indent=2)}")

    # Round 2: relax to 1.0h to expose the Friday overlap
    print(f'\n[tool] find_common_slots({{"person_names": {attendees}, "min_duration_hours": 1.0}})')
    r2 = find_common_slots(person_names=attendees, min_duration_hours=1.0)
    print(f"[result] {json.dumps(r2, indent=2)}")

    # Round 3: propose the best slot (Thursday 11am–12:30pm)
    common = r1.get("common_slots", [])
    if not common:
        print("\nAgent: No common slots found — would need to negotiate partial attendance.")
        return
    best = common[0]
    start_dt = datetime.fromisoformat(best["start"])
    end_dt = start_dt + timedelta(hours=1.5)
    print(
        f'\n[tool] propose_meeting({{"title": "Group Dinner", '
        f'"start_iso": "{start_dt.isoformat()}", '
        f'"end_iso": "{end_dt.isoformat()}", '
        f'"attendees": {attendees}}})'
    )
    r3 = propose_meeting(
        title="Group Dinner",
        start_iso=start_dt.isoformat(),
        end_iso=end_dt.isoformat(),
        attendees=attendees,
    )
    print(f"[result] {json.dumps(r3, indent=2)}")

    slot_label = TimeSlot(start_dt, end_dt)
    print(f"""
Agent: Here's what I found:

The only 1.5-hour slot where all four of you are free is:
  📅 {slot_label}

I know it's not the evening you hoped for — the only evening overlap
is Friday 6–7pm, which is only an hour. Thursday midday is the one
window that gives you the full 1.5 hours with everyone.

Options:
  1. Go with Thursday 11am–12:30pm (lunch, not dinner — but everyone fits).
  2. Do Friday 6–7pm and keep it to 1 hour.
  3. Drop one person: Alice + Bob + Charlie are all free Friday 6–8pm (2h).
""")


if __name__ == "__main__":
    if MOCK_MODE:
        run_mock()
    else:
        run_agent()
