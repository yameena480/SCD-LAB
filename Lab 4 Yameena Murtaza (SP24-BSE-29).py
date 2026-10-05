# Scenario: the Lab 3 backlog for the Campus Event Management System,
# estimated by the AI and by the team in a Planning Poker round.
# NOTE: the numbers below are sample data, replace them with your own
# group's real blind estimates.

FIBONACCI = [1, 2, 3, 5, 8, 13]


# Activity 1: Get AI estimates on the whole backlog
# Prompt: "Estimate these user stories in story points on a Fibonacci scale
# (1,2,3,5,8,13). For each, give the number and one line on the main source
# of complexity. Assume a small team that is new to the codebase."
# Example: the AI sized "register for an event" at 5 points because of
# concurrency (two students racing for the last seat).


# Activity 2: Run Planning Poker and reveal
# The team's independent estimate for the same story was 8. The team knew
# the event-capacity data model was not finalised, which the AI couldn't
# see, and that unknown justified the extra points.


# Story id: (title, member A, member B, member C, agreed, AI, AI reason known from backlog text?)
stories = {
    "S1": ("Sign up",              3, 2, 3, 3, 3, True),
    "S2": ("Login",                2, 3, 2, 2, 2, True),
    "S3": ("Browse events",        3, 3, 5, 3, 3, True),
    "S4": ("Register for event",   8, 5, 8, 8, 5, False),
    "S5": ("Cancel registration",  3, 5, 3, 3, 3, True),
    "S6": ("Reminders",            8, 13, 8, 8, 5, False),
    "S7": ("Search events",        5, 3, 5, 5, 3, False),
    "S8": ("Add event",            3, 2, 3, 3, 3, True),
    "S9": ("Remove event",         2, 2, 3, 2, 2, True),
    "S10": ("Export attendance",   3, 5, 5, 5, 3, False),
}


# Activity 3: Line up every story
def compare_table():
    print(f"{'ID':4}{'Story':22}{'A':>3}{'B':>3}{'C':>3}{'Team':>6}{'AI':>4}{'Diff':>6}")
    for sid, (title, a, b, c, team, ai, _) in stories.items():
        print(f"{sid:4}{title:22}{a:>3}{b:>3}{c:>3}{team:>6}{ai:>4}{team - ai:>6}")


compare_table()
# The AI and team matched on simple stories (login, browse) and differed
# most on stories that depend on things still unsettled (registration,
# reminders).


# Activity 4: Work out what fits in a sprint
def fit_in_sprint(order, velocity):
    total = 0
    chosen = []
    for sid in order:
        points = stories[sid][4]
        if total + points > velocity:
            break
        total += points
        chosen.append(sid)
    return chosen, total


# ---------------------------------------------------------
# Graded Lab Tasks
# ---------------------------------------------------------

# Task 1: Estimate blind, then reveal
# Each member wrote all 10 estimates down before anyone spoke. The full
# spread per story is kept in the table above (columns A, B, C), because the
# disagreement is the data.
for sid, (title, a, b, c, *_rest) in stories.items():
    values = [a, b, c]
    assert all(v in FIBONACCI for v in values), sid
    print(sid, "spread:", min(values), "to", max(values))

# Task 2: Add the AI as a fourth voice and audit its reasoning
# For each story, was the AI's stated reason something it could know from
# the backlog text, or something it assumed? (last column of `stories`)
assumed = [sid for sid, row in stories.items() if not row[6]]
print("AI reasons that were assumed, not known:", len(assumed), assumed)

# Task 3: Explain the three biggest gaps with team knowledge
gaps = sorted(stories.items(), key=lambda kv: abs(kv[1][4] - kv[1][5]), reverse=True)
top3 = [sid for sid, _ in gaps[:3]]
print("Three biggest gaps:", top3)
# Replace the explanations below with things YOUR team really knows:
#   S4 Register: the AI cannot know our event-capacity schema is not
#      finalised, which is most of the work in this story.
#   S6 Reminders: the AI cannot know we have no notification service set up
#      yet and nobody in the team has used a scheduler before.
#   S7 Search: the AI cannot know our event table has no indexes and the
#      categories are still free text.

# Task 4: Derive sprint capacity and state confidence
# Two-week sprint, assumed velocity = 20 points (a starting guess for a new
# team, to be revised after the first real sprint).
VELOCITY = 20
order_by_priority = ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10"]
chosen, total = fit_in_sprint(order_by_priority, VELOCITY)
all_points = sum(row[4] for row in stories.values())
print("Total backlog points:", all_points)
print("Fits in sprint 1:", chosen, "=", total, "points out of", VELOCITY)
# Working: 3 + 2 + 3 + 8 + 3 = 19 points. Adding S6 (8) would make 27 > 20,
# so it moves to sprint 2. The full backlog is 42 points, which is over two
# sprints at this velocity.
# Confidence: I expect to be off by about 30% because the team is new. At
# the end of the sprint I would measure the points actually completed to
# replace the guessed velocity.


# ---------------------------------------------------------
# Lab Assignment (Take-Home)
# ---------------------------------------------------------
# Re-estimate the same backlog a week later without looking at the earlier
# numbers, then compare the drift per story.
def drift(first, second):
    return {sid: second[sid] - first[sid] for sid in first}


# Then answer: is the drift larger on stories where you disagreed with the
# AI, or where you agreed with it? (write your own answer from your data)


# ---------------------------------------------------------
# Viva Questions (basic, based on this lab)
# ---------------------------------------------------------

# Q1: What is a story point?
# A: A relative measure of effort, complexity and uncertainty of a story,
# not a number of hours.

# Q2: Why use relative sizing instead of hours?
# A: People are better at comparing pieces of work than guessing exact hours
# for work they haven't done.

# Q3: What is Planning Poker?
# A: Each member picks an estimate privately, all are revealed together, then
# the differences are discussed until the team agrees.

# Q4: Why must estimates be written before anyone speaks?
# A: Otherwise the first number said aloud anchors everyone else.

# Q5: What is the Fibonacci scale used for?
# A: Sizes like 1, 2, 3, 5, 8, 13 get further apart as they grow, which
# reflects that big estimates are less certain.

# Q6: What is velocity?
# A: The number of story points a team finishes in one sprint, used to
# decide how much fits in the next sprint.

# Q7: Why is "the AI underestimated complexity" a weak explanation?
# A: It doesn't name what the AI couldn't know. A good explanation names
# specific team knowledge, like an unfinished data model.
