def celsius_to_fahrenheit(c):
    return c * 9 / 5 + 32


print(celsius_to_fahrenheit(100))  # 212.0


# Activity 2: Build it again with AI assistance

def celsius_to_fahrenheit_ai(celsius: float) -> float:
    """Convert a Celsius temperature to Fahrenheit."""
    return celsius * 9 / 5 + 32


def read_celsius():
    try:
        return float(input("Celsius: "))
    except ValueError:
        print("Please enter a number.")
        return None


# Activity 3: Compare honestly
# The AI version didn't get lucky, it defaulted to float division and input
# checking. The hand-written bug was a common mistake, not carelessness.

# Activity 4: Commit both, clearly labelled
# $ git init cse325-lab01 && cd cse325-lab01
# $ git add hand_written.py && git commit -m "Hand-written converter (found and fixed integer-division bug)"
# $ git add ai_assisted.py && git commit -m "AI-assisted converter (float division and input validation from first draft)"

if __name__ == "__main__":
    value = read_celsius()
    if value is not None:
        print(f"{value}C = {celsius_to_fahrenheit_ai(value)}F")



# ---------------------------------------------------------
# Lab Assignment (Take-Home)
# ---------------------------------------------------------
# Small utility built twice: tip splitter
def split_tip(bill, tip_percent, people):
    total = bill * (1 + tip_percent / 100)
    return total / people


# Give the AI version to a classmate for five minutes and note what they
# broke (e.g. people = 0 gives ZeroDivisionError, negative bill accepted).
def split_tip_safe(bill, tip_percent, people):
    if bill < 0 or tip_percent < 0:
        raise ValueError("bill and tip must not be negative")
    if people < 1:
        raise ValueError("people must be at least 1")
    return bill * (1 + tip_percent / 100) / people


# ---------------------------------------------------------
# Viva Questions (basic, based on this lab)
# ---------------------------------------------------------

# Q1: Why use relative rather than exact checks like 100C = 212F?
# A: A known value is a quick way to catch a wrong formula, it's how the
# integer-division bug was found.

# Q2: What did the AI version do that the hand-written one did not?
# A: Used float division, added a type hint/docstring, and handled
# non-numeric input.

# Q3: Why commit at least three times instead of once at the end?
# A: The commit history shows the work was done step by step, with
# timestamps, which is the evidence for the time comparison.

# Q4: Does the AI always give the right answer?
# A: No. Its output must be tested and understood by the developer, who
# stays responsible for deciding whether it is right.

# Q5: What is agent mode in Copilot Chat?
# A: A mode where the assistant can read the whole workspace, run commands
# and iterate on its own output, unlike plain inline completion.
