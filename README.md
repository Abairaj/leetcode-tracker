# LeetCode Daily Learning Tracker

A lightweight automation tool that tracks your daily accepted LeetCode problems and maintains a daily learning log in your GitHub repository.

Instead of manually recording solved problems, this script fetches your accepted submissions from LeetCode, generates a Markdown log for the current day, and GitHub Actions automatically commits the log to the repository.

---

## Features

* Fetches today's accepted LeetCode submissions.
* Retrieves problem metadata using the LeetCode GraphQL API.
* Records:

  * Problem Title
  * Difficulty
  * Topics
  * Problem URL
  * Solved Time (IST)
* Generates a Markdown log for the day.
* Automatically commits and pushes logs using GitHub Actions.
* Safe to run multiple times—the daily log is regenerated instead of duplicated.

---

## Repository Structure

```
.
├── .github/
│   └── workflows/
│       └── leetcode.yml
├── logs/
│   └── YYYY/
│       └── MM/
│           └── DD.md
├── tracker.py
├── requirements.txt
└── README.md
```

---

## Example Daily Log

```markdown
# LeetCode Log - 2026-07-08

## Problems Solved Today

### Spiral Matrix

- Difficulty: Medium
- Topics: Array, Matrix, Simulation
- URL: https://leetcode.com/problems/spiral-matrix/
- Solved At: 2026-07-08 12:19:34 PM IST

---

Total Problems Solved: 1
```

---

## Installation

Clone the repository.

```bash
git clone <your-repository-url>
cd <repository-name>
```

Install the required dependency.

```bash
pip install -r requirements.txt
```

---

## Running the Tracker

Run the script manually.

```bash
python tracker.py
```

The script will:

1. Connect to the LeetCode GraphQL API.
2. Fetch today's accepted submissions.
3. Retrieve metadata for each solved problem.
4. Generate a Markdown log inside the `logs/` directory.

---

## GitHub Actions

The repository includes a GitHub Actions workflow that can:

* Run on a schedule.
* Run manually using **Run workflow**.
* Execute `tracker.py`.
* Commit newly generated logs.
* Push the changes back to the repository automatically.

---

## Notes

* The tracker currently uses LeetCode's `recentAcSubmissionList` GraphQL endpoint.
* Only **accepted** submissions are included.
* Duplicate accepted submissions for the same problem on the same day are filtered out.
* Running the script multiple times on the same day updates the existing log instead of creating duplicate entries.

---

## Requirements

* Python 3.12+
* `requests`

Install dependencies using:

```bash
pip install -r requirements.txt
```

---

## License

This project is licensed under the MIT License.
