import requests
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path

LEETCODE_API = "https://leetcode.com/graphql"
USERNAME = "AbaiRaj"

IST = ZoneInfo("Asia/Kolkata")


# ==========================================================
# GraphQL Helper
# ==========================================================

def graphql(query, variables):
    response = requests.post(
        LEETCODE_API,
        json={
            "query": query,
            "variables": variables,
        },
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
        },
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    if "errors" in data:
        raise Exception(data["errors"])

    return data["data"]


# ==========================================================
# Fetch Today's Accepted Problems
# ==========================================================

def get_recent_submissions(username):
    query = """
    query recentAcSubmissions($username: String!, $limit: Int!) {
      recentAcSubmissionList(username: $username, limit: $limit) {
        title
        titleSlug
        timestamp
      }
    }
    """

    data = graphql(
        query,
        {
            "username": username,
            "limit": 20
        },
    )

    return data["recentAcSubmissionList"]


# ==========================================================
# Fetch Problem Metadata
# ==========================================================

def get_problem_metadata(slug):
    query = """
    query getQuestion($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        difficulty

        topicTags {
          name
        }
      }
    }
    """

    data = graphql(
        query,
        {
            "titleSlug": slug
        },
    )

    question = data["question"]

    return {
        "difficulty": question["difficulty"],
        "topics": [x["name"] for x in question["topicTags"]],
    }


# ==========================================================
# Today's Problems
# ==========================================================

def get_today_problems():

    today = datetime.now(IST).date()

    problems = []

    seen = set()

    submissions = get_recent_submissions(USERNAME)

    for sub in submissions:

        solved_time = datetime.fromtimestamp(
            int(sub["timestamp"]),
            tz=IST,
        )

        if solved_time.date() != today:
            continue

        if sub["titleSlug"] in seen:
            continue

        seen.add(sub["titleSlug"])

        meta = get_problem_metadata(sub["titleSlug"])

        problems.append(
            {
                "title": sub["title"],
                "slug": sub["titleSlug"],
                "difficulty": meta["difficulty"],
                "topics": meta["topics"],
                "url": f"https://leetcode.com/problems/{sub['titleSlug']}/",
                "solved_at": solved_time,
            }
        )

    return problems


# ==========================================================
# Markdown Generator
# ==========================================================

def generate_markdown(problems):

    today = datetime.now(IST)

    lines = []

    lines.append(f"# LeetCode Log - {today.date()}")
    lines.append("")
    lines.append("## Problems Solved Today")
    lines.append("")

    if not problems:
        lines.append("_No problems solved today._")
        return "\n".join(lines)

    for p in problems:

        lines.append(f"### {p['title']}")
        lines.append("")
        lines.append(f"- Difficulty: **{p['difficulty']}**")
        lines.append(f"- Topics: {', '.join(p['topics'])}")
        lines.append(f"- URL: {p['url']}")
        lines.append(
            "- Solved At: "
            + p["solved_at"].strftime("%Y-%m-%d %I:%M:%S %p IST")
        )
        lines.append("")
        lines.append("---")
        lines.append("")

    lines.append(f"Total Problems Solved: **{len(problems)}**")

    return "\n".join(lines)


# ==========================================================
# Save Markdown
# ==========================================================

def save_markdown(markdown):

    today = datetime.now(IST)

    folder = Path("logs") / str(today.year) / f"{today.month:02d}"

    folder.mkdir(parents=True, exist_ok=True)

    file_path = folder / f"{today.day:02d}.md"

    file_path.write_text(markdown, encoding="utf-8")

    return file_path


# ==========================================================
# Main
# ==========================================================

def main():

    print("Fetching today's LeetCode submissions...")

    problems = get_today_problems()

    print(f"Found {len(problems)} problem(s).")

    markdown = generate_markdown(problems)

    file_path = save_markdown(markdown)

    print(f"Log written to {file_path}")


if __name__ == "__main__":
    main()