import os
import tempfile

import pytest

# Scenario: a grade-averaging script from an old assignment, critiqued
# against modularity, readability and maintainability.


# ---------------------------------------------------------
# ORIGINAL (cold) code - this is what gets critiqued
# ---------------------------------------------------------
def process(d, path, show, fmt, sort, verbose):
    f = open(path)
    for line in f:
        p = line.strip().split(",")
        if len(p) < 2:
            continue
        n = p[0]
        s = []
        for x in p[1:]:
            try:
                s.append(float(x))
            except:
                pass
        d[n] = s
    f.close()
    out = []
    for n in d:
        if len(d[n]) > 0:
            a = sum(d[n]) / len(d[n])
        else:
            a = 0
        if a >= 90:
            g = "A"
        elif a >= 80:
            g = "B"
        elif a >= 70:
            g = "C"
        elif a >= 60:
            g = "D"
        else:
            g = "F"
        out.append((n, a, g))
    if sort:
        out.sort(key=lambda t: t[1], reverse=True)
    if show:
        for n, a, g in out:
            if fmt == "short":
                print(n, g)
            else:
                print(n, round(a, 2), g)
    return out


# Activity 1: Get the baseline critique
# Prompt: "Critique this code specifically for modularity, readability, and
# maintainability. For each issue, name the principle it violates and where
# in the code it happens."
# Issues found:
# - process() does file reading, parsing, grading and printing (modularity)
# - single-letter names like d, p, s, a, g (readability)
# - the grade boundary if/elif chain is buried inside the loop and hard to
#   change (maintainability)
# - file is opened and closed by hand instead of using "with"


# Activity 2: Apply the real fixes, skip the cosmetic ones
# Rejected: renaming the loop variable x in "for x in p[1:]" - it is a
# 3-line loop, so a longer name adds nothing.
# Kept: split the big function, rename d/p/s/a/g, move the grade logic
# into letter_grade().
def load_records(path):
    records = {}
    with open(path) as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) < 2:
                continue
            records[parts[0]] = parse_scores(parts[1:])
    return records


def parse_scores(raw_scores):
    scores = []
    for value in raw_scores:
        try:
            scores.append(float(value))
        except ValueError:
            pass
    return scores


def calculate_average(scores):
    if not scores:
        return 0
    return sum(scores) / len(scores)


def letter_grade(average):
    for cutoff, grade in ((90, "A"), (80, "B"), (70, "C"), (60, "D")):
        if average >= cutoff:
            return grade
    return "F"


def build_report(records, sort=False):
    rows = []
    for name, scores in records.items():
        avg = calculate_average(scores)
        rows.append((name, avg, letter_grade(avg)))
    if sort:
        rows.sort(key=lambda r: r[1], reverse=True)
    return rows


def print_report(rows, fmt="long"):
    for name, avg, grade in rows:
        if fmt == "short":
            print(name, grade)
        else:
            print(name, round(avg, 2), grade)


# Activity 3: Measure the actual change (real numbers from running ruff and
# radon on the two versions)
#
# | Metric                        | Before | After |
# |-------------------------------|--------|-------|
# | ruff violations               | 2      | 0     |
# | longest function (lines)      | 41     | 10    |
# | highest cyclomatic complexity | 15 (C) | 3 (A) |
# | parameters on worst function  | 6      | 2     |
# | number of functions           | 1      | 6     |
# Note: total lines went up slightly (41 -> 50) because of the extra def
# lines and blank lines, so shorter overall was not the goal.


# ---------------------------------------------------------
# Graded Lab Tasks
# ---------------------------------------------------------

# Task 1: Numeric baseline (before touching anything)
# Commands:
#   ruff check --select E,F,B,S,UP,RUF grades_old.py
#   radon cc -s -a grades_old.py
# Raw output I got for the original file:
#   grades_old.py:12:13: E722 Do not use bare `except`
#   grades_old.py:12:13: S110 `try`-`except`-`pass` detected, consider logging the exception
#   Found 2 errors.
#   F 1:0 process - C (15)
#   Average complexity: C (15.0)
# Longest function: process() = 41 lines. Parameters on it: 6.
# Commit the original file together with this baseline, and write the
# commit hash here: <your hash>

# Task 2: Critique and contest it
# | Suggestion                                   | Verdict | Reason                                                                                        |
# |----------------------------------------------|---------|-----------------------------------------------------------------------------------------------|
# | Split process() into load/average/grade/print | Accept  | process() has 4 jobs and complexity 15                                                        |
# | Rename d to student_records                   | Accept  | d is passed in and mutated, the reader can't tell what it holds                               |
# | Move the if/elif grade chain into letter_grade| Accept  | the grade boundaries were only in one place but buried in the loop                            |
# | Use "with open" instead of open/close         | Accept  | f.close() would be skipped if an exception happened inside the loop                           |
# | Rename x in "for x in p[1:]"                  | Reject  | 3-line loop, name is clear from the float(x) call                                             |
# | Remove the verbose parameter                  | Reject  | callers may still pass 6 arguments to process(), removing it would break them                 |
# | Replace round(a, 2) with f-string formatting  | Reject  | the return value still goes to other code as a float, printing is not the bottleneck          |

# Task 3: Apply, re-measure and explain every number (see the table in
# Activity 3 above)
# - ruff violations 2 -> 0: bare except became "except ValueError", which
#   fixed E722 and S110 together.
# - longest function 41 -> 10: the work was split across 6 functions.
# - complexity 15 -> 3: the if/elif chain became a loop over a tuple and
#   parsing moved out of the main loop.
# - parameters 6 -> 2: the unused verbose/sort/show flags no longer need
#   to travel together (sort moved to build_report, fmt to print_report).
# - total lines 41 -> 50: did NOT go down, more def lines and blank lines.
# Evidence to add on your machine: git diff --stat <before> <after>


# Task 4: Prove behaviour did not change
# Same three tests run against the original process() and the new code.
def make_file(text):
    f = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False)
    f.write(text)
    f.close()
    return f.name


SAMPLE = "ali,90,95\nsara,55,65\nbad\nzain,x,80\n"


def old_run(path):
    return process({}, path, False, "long", True, False)


def new_run(path):
    return build_report(load_records(path), sort=True)


@pytest.fixture
def sample_path():
    path = make_file(SAMPLE)
    yield path
    os.remove(path)


@pytest.mark.parametrize("run", [old_run, new_run])
def test_sorted_by_average(sample_path, run):
    names = [row[0] for row in run(sample_path)]
    assert names == ["ali", "zain", "sara"]


@pytest.mark.parametrize("run", [old_run, new_run])
def test_letter_grades(sample_path, run):
    grades = {name: grade for name, _, grade in run(sample_path)}
    assert grades == {"ali": "A", "zain": "B", "sara": "D"}


@pytest.mark.parametrize("run", [old_run, new_run])
def test_bad_line_is_skipped(sample_path, run):
    assert "bad" not in [row[0] for row in run(sample_path)]


# These tests would NOT catch a change in printing (print_report output)
# because they only check returned data.


# ---------------------------------------------------------
# Lab Assignment (Take-Home)
# ---------------------------------------------------------
# Repeat the cycle on a second, different piece of old code, then answer:
# of modularity, readability and maintainability, which did the assistant
# handle worst and why? (write your own answer using your two runs)


# ---------------------------------------------------------
# Viva Questions (basic, based on this lab)
# ---------------------------------------------------------

# Q1: What is modularity?
# A: Splitting code into small parts that each do one job, so they can be
# changed and tested separately.

# Q2: Is renaming every variable to a longer name always more readable?
# A: No. Longer is not the goal, clearer is. Renaming a loop variable in a
# 3-line loop is busywork.

# Q3: Why measure quality with numbers instead of "it feels cleaner"?
# A: Numbers like complexity, function length and rule violations can be
# re-checked by anyone by running the same tool.

# Q4: Why should the same tests pass before and after a refactor?
# A: A refactor must not change behaviour, only structure. If the same
# tests pass on both, behaviour was preserved.

# Q5: What is cyclomatic complexity?
# A: A count of the independent paths through a function (roughly the
# number of decisions plus one). Higher means harder to test.

# Q6: Should every AI suggestion be accepted?
# A: No. Treat it like a pull request from a fast colleague who has never
# met your users, accept the real improvements and reject the rest.


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
