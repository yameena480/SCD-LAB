BRIEF = ("students browse events, register, and get reminders; "
         "admins add and remove events")


# Activity 1: Draft the module breakdown
# Prompt: "Act as a software project planner. Break the Campus Event
# Management System into 4-6 modules. For each module list 3-5 concrete
# engineering tasks. Give the result as a nested list."
# First draft gave 5 modules (Auth & Accounts, Event Catalogue,
# Registration, Reminders, Admin Console). It missed session-token handling
# under Auth and cancelling a registration under Registration, both added
# by hand.
wbs = {
    "Auth & Accounts": ["Sign up", "Login", "Session tokens (added by hand)"],
    "Event Catalogue": ["List events", "Search/filter events", "Event details page"],
    "Registration": ["Register for event", "Check seat capacity",
                     "Cancel registration (added by hand)"],
    "Reminders": ["Schedule reminder", "Send reminder", "Reminder settings"],
    "Admin Console": ["Add event", "Remove event", "Edit event"],
}


# Activity 2: See the corrected breakdown as a whole (tree view)
def print_tree(tree):
    for module, tasks in tree.items():
        print(module)
        for task in tasks:
            print("  -", task)


print_tree(wbs)
# The first draft treated Reminders as one afterthought task, but the brief
# names reminders directly, so it needs to be its own module. A tree
# shows that gap immediately, a flat list hides it.


# Activity 3: Reshape into user stories and prioritise
# Prompt: "Rewrite these tasks as user stories in the format 'As a <role>,
# I want <goal> so that <benefit>.' Then apply MoSCoW prioritisation (Must,
# Should, Could, Won't) to each, with a one-line justification per label."
# Example: "As a student, I want to cancel my registration so that my spot
# frees up for someone else" -> Must (without it the registration count
# drifts from reality).
# Example: "As an admin, I want to export attendance to CSV" -> Could
# (useful, but the system works without it for launch).


# Activity 4: Poke holes on purpose
# Prompt: "What did you miss?"
# Real gap found: no story covers what happens when an event is cancelled
# after students have already registered. Added to the backlog below as S11.


# ---------------------------------------------------------
# Graded Lab Tasks
# ---------------------------------------------------------

# Task 1: Reconciled work-breakdown structure
# Every row traces to a phrase in the brief, or is marked ADDED with a reason.
wbs_trace = [
    ("Sign up / Login", "ADDED: students must be identified before they can register"),
    ("List events", "browse events"),
    ("Search/filter events", "ADDED: browsing is hard with many events"),
    ("Register for event", "register"),
    ("Cancel registration", "ADDED: the brief does not say it, but seats must free up"),
    ("Send reminder", "get reminders"),
    ("Add event", "admins add"),
    ("Remove event", "remove events"),
]
# Invented task (model produced it, brief doesn't support it):
#   <paste the exact task from YOUR model's output here>
# Tasks the brief needs that the model left out:
#   1. Session-token handling (Auth)
#   2. Cancel registration (Registration)


def check_traceability(rows):
    for task, source in rows:
        if source.startswith("ADDED:"):
            continue
        assert source in BRIEF, f"{task} does not trace to the brief"
    print("All WBS rows trace to the brief or are marked ADDED.")


check_traceability(wbs_trace)


# Task 2: Backlog with at least 10 user stories and MoSCoW labels
backlog = [
    ("S1", "As a student, I want to sign up so that I can register for events", "Must"),
    ("S2", "As a student, I want to log in so that my registrations are mine", "Must"),
    ("S3", "As a student, I want to browse events so that I can find one to attend", "Must"),
    ("S4", "As a student, I want to register for an event so that I get a seat", "Must"),
    ("S5", "As a student, I want to cancel my registration so that my spot frees up", "Must"),
    ("S6", "As a student, I want a reminder before an event so that I don't forget it", "Should"),
    ("S7", "As a student, I want to search events by category so that I find them faster", "Should"),
    ("S8", "As an admin, I want to add an event so that students can see it", "Must"),
    ("S9", "As an admin, I want to remove an event so that old events disappear", "Should"),
    ("S10", "As an admin, I want to export attendance to CSV so that I can share it", "Could"),
    ("S11", "As a student, I want to be told when an event I registered for is cancelled", "Should"),
    ("S12", "As a student, I want to pay for events online so that I skip the cash desk", "Won't"),
]

# Defence of three Must labels against a competing story:
# 1. S5 (cancel registration) is Must, not Should like S7 (search), because
#    without cancelling the seat count drifts from reality, while search
#    only makes browsing a bit slower.
# 2. S4 (register) is Must, not Should like S6 (reminder), because reminders
#    only make sense after registration exists.
# 3. S8 (add event) is Must, not Should like S9 (remove event), because with
#    no events added there is nothing to browse or register for, but the
#    system still works for launch without removing them.

# A backlog where everything is Must scores at most half, so check:
labels = [label for _, _, label in backlog]
assert len(backlog) >= 10
assert labels.count("Must") < len(labels)
for label in ("Must", "Should", "Could", "Won't"):
    print(label, labels.count(label))


# Task 3: A gap the model cannot see (local context)
# NOTE: replace this with something real from YOUR campus/device/network.
# Example format:
#   Requirement: registration must work on the slow hostel Wi-Fi, so the
#                event list should load without images first.
#   Why the model can't know it: it doesn't know the network conditions in
#                                my building.
#   Backlog row: ("S13", "As a student on hostel Wi-Fi, I want a text-only event list", "Should")
backlog.append(("S13", "As a student on slow campus Wi-Fi, I want a text-only event list so that it loads", "Should"))


# Task 4: Honest prompt ledger
# Write your real prompts in order, including the ones that failed:
#   1. <prompt>  -> <what went wrong>  -> <what I changed and why>
#   2. <prompt>  -> <what went wrong>  -> <what I changed and why>
#   3. <prompt>  -> worked
# (At least two failed or superseded attempts are needed.)


# ---------------------------------------------------------
# Lab Assignment (Take-Home)
# ---------------------------------------------------------
# Pick a small app idea of your own, repeat the planning flow, then write a
# short note: was the assistant more or less useful when it had less
# obvious context, and when should you plan first and consult it second?


# ---------------------------------------------------------
# Viva Questions (basic, based on this lab)
# ---------------------------------------------------------

# Q1: What is a work-breakdown structure (WBS)?
# A: A big project split into smaller tasks grouped under modules.

# Q2: What does MoSCoW stand for?
# A: Must, Should, Could, Won't - a way to prioritise backlog items.

# Q3: What is a user story?
# A: A short requirement in the form "As a <role>, I want <goal> so that
# <benefit>".

# Q4: Why not trust an AI-generated plan directly?
# A: It sounds equally confident when right or wrong, it can invent tasks
# that don't belong and miss ones that do, so it's a starting point.

# Q5: Why is an invented task more dangerous than a missing one?
# A: A missing task gets noticed when someone needs it, but an invented one
# gets built.

# Q6: Why keep the plan in Git?
# A: So "what the AI proposed" and "what we decided" stay separate.
