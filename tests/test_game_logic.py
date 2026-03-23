"""
tests/test_game_logic.py

Pytest cases targeting each bug identified and fixed in logic_utils.py.
Run with: pytest tests/test_game_logic.py -v
"""

from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
)


# ---------------------------------------------------------------------------
# Starter tests — fixed: check_guess returns a (outcome, message) tuple,
# so we unpack before asserting on outcome.
# ---------------------------------------------------------------------------

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# ---------------------------------------------------------------------------
# Bug 1 — Hard difficulty range was narrower than Normal (1–50 vs 1–100)
# ---------------------------------------------------------------------------

class TestGetRangeForDifficulty:
    def test_easy_range(self):
        low, high = get_range_for_difficulty("Easy")
        assert low == 1 and high == 20

    def test_normal_range(self):
        low, high = get_range_for_difficulty("Normal")
        assert low == 1 and high == 100

    def test_hard_range_is_wider_than_normal(self):
        # BUG 1 FIX: Hard was returning (1, 50), making it *easier* than Normal.
        _, hard_high = get_range_for_difficulty("Hard")
        _, normal_high = get_range_for_difficulty("Normal")
        assert hard_high > normal_high, (
            f"Hard range ({hard_high}) must be wider than Normal ({normal_high})"
        )

    def test_unknown_difficulty_defaults_safely(self):
        low, high = get_range_for_difficulty("Impossible")
        assert low == 1 and high == 100


# ---------------------------------------------------------------------------
# Bug 2 — check_guess hint messages were backwards
# ---------------------------------------------------------------------------

class TestCheckGuess:
    def test_correct_guess_returns_win(self):
        outcome, _ = check_guess(42, 42)
        assert outcome == "Win"

    def test_high_guess_returns_too_high(self):
        outcome, _ = check_guess(80, 42)
        assert outcome == "Too High"

    def test_low_guess_returns_too_low(self):
        outcome, _ = check_guess(10, 42)
        assert outcome == "Too Low"

    def test_high_guess_message_says_lower(self):
        # BUG 2 FIX: Message used to say "Go HIGHER!" when guess was too high.
        _, msg = check_guess(80, 42)
        assert "LOWER" in msg, f"Expected 'LOWER' in message, got: {msg!r}"

    def test_low_guess_message_says_higher(self):
        # BUG 2 FIX: Message used to say "Go LOWER!" when guess was too low.
        _, msg = check_guess(10, 42)
        assert "HIGHER" in msg, f"Expected 'HIGHER' in message, got: {msg!r}"

    def test_int_types_compare_correctly(self):
        # BUG 4 FIX: Passing a str secret caused lexicographic errors
        # (e.g. "7" > "42" is True). Both args must be ints.
        outcome, _ = check_guess(7, 42)
        assert outcome == "Too Low"

        outcome, _ = check_guess(99, 42)
        assert outcome == "Too High"


# ---------------------------------------------------------------------------
# Bug 3 — update_score rewarded +5 points for "Too High" on even attempts
# ---------------------------------------------------------------------------

class TestUpdateScore:
    def test_win_increases_score(self):
        new_score = update_score(0, "Win", 1)
        assert new_score > 0

    def test_win_score_floors_at_10_points(self):
        # attempt_number=9 → 100 - 10*(9+1) = 0, clamped to 10
        new_score = update_score(0, "Win", 9)
        assert new_score == 10

    def test_too_high_always_decreases_score(self):
        # BUG 3 FIX: Even-numbered attempts used to award +5 for "Too High".
        for attempt in range(1, 9):
            score_after = update_score(50, "Too High", attempt)
            assert score_after < 50, (
                f"Score should decrease on attempt {attempt}, got {score_after}"
            )

    def test_too_low_always_decreases_score(self):
        for attempt in range(1, 9):
            score_after = update_score(50, "Too Low", attempt)
            assert score_after < 50

    def test_unknown_outcome_leaves_score_unchanged(self):
        assert update_score(100, "Unknown", 3) == 100


# ---------------------------------------------------------------------------
# parse_guess — regression tests
# ---------------------------------------------------------------------------

class TestParseGuess:
    def test_valid_integer_string(self):
        ok, val, err = parse_guess("42")
        assert ok is True and val == 42 and err is None

    def test_valid_float_string_truncates(self):
        ok, val, err = parse_guess("7.9")
        assert ok is True and val == 7

    def test_none_input_returns_error(self):
        ok, val, err = parse_guess(None)
        assert ok is False and val is None and err is not None

    def test_empty_string_returns_error(self):
        ok, val, err = parse_guess("")
        assert ok is False and err is not None

    def test_non_numeric_string_returns_error(self):
        ok, val, err = parse_guess("abc")
        assert ok is False and err is not None