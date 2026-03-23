def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 200          # was 1, 50 — harder means wider, not narrower
                               # FIX (Bug 1): Claude identified the inverted difficulty scaling; range corrected collaboratively.
    return 1, 100              # safe default


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw == "":
        return False, None, "Enter a guess."

    try:
        value = int(float(raw)) if "." in raw else int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess: int, secret: int):
    """
    Compare guess to secret and return (outcome, message).

    outcome: "Win" | "Too High" | "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess > secret:
        return "Too High", "📉 Go LOWER!"    # was "📈 Go HIGHER!"
                                              # FIX (Bug 2): Claude flagged the swapped hint messages; corrected by swapping the emoji/text to match actual direction.
    return "Too Low", "📈 Go HIGHER!"        # was "📉 Go LOWER!"
                                              # FIX (Bug 2): Same swap applied to the Too Low branch.


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = max(10, 100 - 10 * (attempt_number + 1))
        return current_score + points

    if outcome in ("Too High", "Too Low"):
        return current_score - 5            # was: +5 on even attempts for "Too High"
                                            # FIX (Bug 3): Claude spotted the conditional reward on wrong guesses; unified both wrong outcomes to always deduct 5.
                                            # FIX (Bug 4): Claude also flagged the string/int type mismatch in check_guess; resolved by enforcing int-only secrets and removing the fallback string comparison branch entirely.

    return current_score