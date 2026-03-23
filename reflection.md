# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

At i started to plug in the number i was and felt frusted i wasn't guessing the right number. 
The game told me to go lower despite the correct number being higher.
When i tried to start a new game it wouldn't let me.
I choose i new difficulty to try and see if anything changed and it didn't

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)? Claude Code Extension in VS Code
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
While reviewing app.py, Claude identified that the hint messages in check_guess were reversed. Specifically, when a player's guess was too high, the function returned "📈 Go HIGHER!" — the opposite of the correct direction. Claude suggested swapping the messages so that a high guess returns "📉 Go LOWER!" and a low guess returns "📈 Go HIGHER!".

The logic is straightforward: if your guess is above the secret number, you need to guess lower, not higher. The original code had the emoji and text pointing in the wrong direction for both branches.

I confirmed this by reading the if guess > secret branch in the original app.py and tracing what message a player would see. I also verified it through the pytest case test_high_guess_message_says_lower, which asserts "LOWER" in msg when the guess exceeds the secret. That test passed after the fix was applied, confirming the correction was accurate.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

When writing the tests/test_game_logic.py file, Claude initially attempted to overwrite the file using a PowerShell here-string command (@" ... "@ | Set-Content). Claude suggested this as a way to bypass the need to manually copy and paste the file contents in VS Code.

PowerShell's here-string syntax conflicted with Python's function definition syntax. Characters like parentheses in def test_winning_guess(): caused PowerShell to throw parser errors such as "An expression was expected after '('". The command failed entirely and did not write the file.

The terminal output showed multiple ParserError and Unexpected token errors, and the file was not updated — pytest still collected only 3 items (the old starter tests) instead of the expected 23. The correct fix was to open the file manually in VS Code using code tests\test_game_logic.py, select all, paste the new content, and save. After doing that, pytest collected and pa
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

We started by auditing app.py and identified 7 bugs spanning logic, types, UI, and game state. The most notable ones were: Hard mode returning a narrower range than Normal, hint messages pointing players in the wrong direction, wrong guesses awarding points on even attempts, and the secret being cast to a string on even attempts which broke comparisons. Smaller issues included New Game resetting attempts to 0 instead of 1, the info banner hardcoding "1 to 100" regardless of difficulty, and New Game ignoring the selected difficulty when generating a new secret.
From there we refactored all four logic functions out of app.py into a clean logic_utils.py, applying every fix and annotating each one with a # FIX collaboration comment. We then updated app.py to import from logic_utils and patched the remaining UI-level bugs directly in the Streamlit code.
With the logic cleaned up, we wrote a 23-case pytest suite in tests/test_game_logic.py targeting every bug and function. Along the way we hit two environment issues — a missing conftest.py that blocked imports, and a PowerShell here-string command that failed due to Python syntax conflicts — both of which we worked through before landing on a clean 23/23 passing run.
Finally, we documented the process in reflection.md, drafting Section 2 (one correct and one incorrect AI suggestion from the session) and Section 3 (how each fix was verified through targeted pytest cases and what the test design decisions revealed about the bugs themselves).
---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?


Imagine you're filling out a form on a website. Every time you click a button, the whole page refreshes — but normally that would wipe out everything you typed. Streamlit works the same way: every time you interact with anything (clicking a button, typing in a box, changing a dropdown), Python reruns your entire script from the top, line by line.
That's what a "rerun" is. It's not a bug — it's just how Streamlit works. The tradeoff is that it keeps your UI in sync with your code automatically, but it also means nothing is remembered between runs unless you explicitly save it somewhere.
That's where session state comes in. st.session_state is basically a small backpack that persists across reruns.
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One habit I want to carry into future projects is writing tests that target the exact condition where a bug hides, not just the happy path. The clearest example from this project was Bug 3 — if I had only tested update_score at a single attempt number, the test would have passed even against the broken code, because the bug only triggered on even-numbered attempts. Looping the assertion across attempts 1–8 was what made the test actually meaningful. That idea — ask yourself when does this break, not just if it breaks — is something I want to apply to every function I test going forward.
One thing I would do differently next time is verify that generated code actually exists on disk before running it. Several times during this project I assumed that because Claude produced a correct version of a file in the chat, the file on my machine had been updated. It hadn't — I still had to manually save it. Going forward I'll make a habit of checking the file contents (even just Get-Content for the first few lines) before running tests, so I'm not debugging a problem that was already solved.
This project changed the way I think about AI-generated code because it showed me that AI can identify bugs accurately and explain them clearly, but it has no visibility into your actual file system — it can only see what you paste into the conversation. That gap between what the AI produces and what is actually running on your machine is where most of the friction in this project came from, and being aware of that gap is now something I'll bring to every AI-assisted coding session.
