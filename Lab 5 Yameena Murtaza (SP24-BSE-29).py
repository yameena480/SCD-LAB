# CSE325 - Software Construction and Development
# Lab 05: NLP for Requirements Engineering & Automated Requirement Analysis
# Seerat Rauf - SP24-BSE-27

# Scenario: stakeholder notes about student login, event registration and
# reminders, run through extraction, classification and a vagueness pass.

NOTES = (
    "We need the app to let students log in with their university email. "
    "It should be fast and secure. "
    "Students register for events and get a reminder before each event. "
    "Admins can add or remove events. "
    "Login must also be quick. "
    "The system should handle many users."
)

SENTENCES = [s.strip() + "." for s in NOTES.split(". ") if s.strip()]
SENTENCES = [s.replace("..", ".") for s in SENTENCES]


def sentence_number(quote):
    for number, sentence in enumerate(SENTENCES, start=1):
        if quote.lower() in sentence.lower():
            return number
    return None


# Activity 1: Extract without inventing
# Prompt: "Extract all software requirements from the text below as a
# numbered list. Do not invent requirements that are not there."
# Nine requirements came back. Cross-checking against the source caught one
# the AI drifted on: "the system should support multiple languages", which
# appears nowhere in the notes. That is a confident-sounding hallucination.

# Activity 2: Classify and count
# Of the genuine nine: 5 Functional (login, register, reminder, add event,
# remove event) and 2 Non-Functional (fast, secure), with 2 more flagged for
# a problem before they could be classified cleanly (the duplicate "quick"
# and the vague "many users").

# Activity 3: Find the duplicate
# "Login must also be quick" (sentence 5) restates "It should be fast"
# (sentence 2) in different words. The AI listed both as separate items.

# Activity 4: Rewrite the vague ones
# "fast" -> "Login must complete in under 2 seconds on standard university
#           WiFi, 95% of the time."
# "many users" -> "The system must support at least 5,000 concurrent active
#           users without degraded response time."


# ---------------------------------------------------------
# Graded Lab Tasks
# ---------------------------------------------------------

# Task 1: Requirements register with hard traceability
# (ID, requirement, type, exact source quote from the notes)
register = [
    ("R1", "Students can log in with their university email", "Functional",
     "let students log in with their university email"),
    ("R2", "The app is fast", "Non-Functional", "It should be fast"),
    ("R3", "The app is secure", "Non-Functional", "secure"),
    ("R4", "Students can register for events", "Functional",
     "Students register for events"),
    ("R5", "Students get a reminder before each event", "Functional",
     "get a reminder before each event"),
    ("R6", "Admins can add events", "Functional", "Admins can add or remove events"),
    ("R7", "Admins can remove events", "Functional", "Admins can add or remove events"),
    ("R8", "Login is quick", "Non-Functional", "Login must also be quick"),
    ("R9", "The system handles many users", "Non-Functional",
     "handle many users"),
]

# Anything with no quote goes here. Not deleted, it is the finding.
unsourced = [
    ("U1", "The system should support multiple languages", "Functional"),
]

for rid, text, kind, quote in register:
    number = sentence_number(quote)
    assert number is not None, f"{rid} has no source in the notes"
    print(rid, kind, "| sentence", number, "|", text)
for rid, text, kind in unsourced:
    print(rid, "UNSOURCED |", text)


# Task 2: Catch the model inventing
# Invented requirement: U1 "the system should support multiple languages".
# What it probably over-read: "handle many users" - the model assumed a
# large user base means international users.
# Second run with a different prompt:
#   Prompt 2 used         : <paste your real second prompt here>
#   Did U1 appear again?  : <yes / no, from your own run>
# (A repeatable invention is a more useful finding than a one-off.)


# Task 3: Make the vague ones testable, and say how to test them
testable = [
    {
        "original": "It should be fast",
        "rewrite": "Login completes in under 2 seconds on university WiFi, "
                   "for 95% of attempts.",
        "measurement": "Run 200 scripted logins from a campus network with a "
                       "load-testing tool and check the 95th percentile "
                       "response time is below 2 seconds.",
    },
    {
        "original": "secure",
        "rewrite": "Passwords are stored hashed, all traffic uses HTTPS, and "
                   "an account locks after 5 failed logins.",
        "measurement": "Inspect the database for plain-text passwords, scan "
                       "the site for non-HTTPS endpoints, and try 6 wrong "
                       "passwords to confirm the lock.",
    },
    {
        "original": "handle many users",
        "rewrite": "Supports 5,000 concurrent users with response time within "
                   "10% of the 100-user response time.",
        "measurement": "Ramp a load test from 100 to 5,000 virtual users and "
                       "compare average response times at each step.",
    },
    {
        "original": "a reminder before each event",
        "rewrite": "A reminder is sent 24 hours (+/- 5 minutes) before the "
                   "event starts to every registered student.",
        "measurement": "Create a test event 24 hours ahead with 3 test "
                       "registrations and compare the send timestamps with "
                       "the event start.",
    },
]

for item in testable:
    assert item["measurement"], "a requirement without a measurement is still vague"
    print(item["original"], "->", item["rewrite"])


# Task 4: Find the contradiction and the duplicate
# Duplicate:
#   "It should be fast"         (sentence 2)
#   "Login must also be quick"  (sentence 5)
print("Duplicate positions:", sentence_number("It should be fast"),
      "and", sentence_number("Login must also be quick"))
# Conflict: I found no hard contradiction, but two requirements pull
# against each other: "fast" (R2) and "secure" (R3). Strong security like
# slow password hashing and account lockout adds time to every login, so a
# very tight speed target may not be possible together with the security
# target.
# Question for the stakeholder: "If a stronger security check makes login
# take 3 seconds instead of 2, which one wins?"


# ---------------------------------------------------------
# Lab Assignment (Take-Home)
# ---------------------------------------------------------
# Take a few sentences from a past project brief or an app's documentation,
# run the same extract-trace-flag process, and write one line on what the
# model missed that a human reviewer would catch immediately, and why.


# ---------------------------------------------------------
# Viva Questions (basic, based on this lab)
# ---------------------------------------------------------

# Q1: What is a functional requirement?
# A: What the system must do, e.g. students can register for events.

# Q2: What is a non-functional requirement?
# A: A quality the system must have, e.g. speed, security, capacity.

# Q3: What is traceability in requirements?
# A: Each requirement points back to the exact sentence that produced it.
# Anything with no pointer is only a proposal.

# Q4: Why is an invented requirement dangerous?
# A: It reads exactly like a real one, so it may get built even though
# nobody asked for it.

# Q5: Why is "the system should be fast" a bad requirement?
# A: It can't be tested. A good one has a number, a condition and a
# tolerance, plus a stated way to measure it.

# Q6: How do you find a duplicate requirement?
# A: Read the source carefully. Different wording, like "fast" and
# "quick", can hide the same requirement.

# Q7: Why is "users must be told when interacting with an AI system" a
# requirement worth writing down?
# A: Under the EU AI Act, transparency obligations may apply to systems in
# scope, so it must be specified up front, not added afterwards.
