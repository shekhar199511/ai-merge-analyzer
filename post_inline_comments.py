import os
import sys
import requests
from ai_postprocess import parse_ai_issues
from diff_parser import get_valid_diff_lines

# Load AI analysis report
REPORT_PATH = "ai_analysis_report.txt"
if not os.path.exists(REPORT_PATH):
    print(f"Error: {REPORT_PATH} not found.")
    sys.exit(1)

with open(REPORT_PATH, "r") as f:
    report_text = f.read()

issues = parse_ai_issues(report_text)
if not issues:
    print("No issues found to post as inline comments.")
    sys.exit(0)

# Load diff content and get valid lines for inline comments
DIFF_PATH = "diff.txt"
if not os.path.exists(DIFF_PATH):
    print(f"Error: {DIFF_PATH} not found.")
    sys.exit(1)

with open(DIFF_PATH, "r") as f:
    diff_content = f.read()

valid_lines = get_valid_diff_lines(diff_content)

# GitHub environment variables
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO = os.environ.get("GITHUB_REPOSITORY")  # e.g., "owner/repo"
PR_NUMBER = os.environ.get("PR_NUMBER")     # Should be set in workflow

if not all([GITHUB_TOKEN, REPO, PR_NUMBER]):
    print("Missing required GitHub environment variables.")
    sys.exit(1)

owner, repo = REPO.split("/")

# Get the latest commit SHA for the PR
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}
pr_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{PR_NUMBER}"
pr_resp = requests.get(pr_url, headers=headers)
if pr_resp.status_code != 200:
    print(f"Failed to fetch PR info: {pr_resp.text}")
    sys.exit(1)
commit_id = pr_resp.json()["head"]["sha"]

# Post inline comments for each issue, only if (file, line) is valid in the diff
for issue in issues:
    if (issue['file'], issue['line']) not in valid_lines:
        print(f"Skipping hallucinated issue: {issue['file']}:{issue['line']}")
        continue
    comment_body = (
        f"**AI Merge Analyzer Issue**\n\n"
        f"**Problem:** {issue['problem']}\n"
        f"**Why:** {issue['why']}\n"
        f"**Solution:** {issue['solution']}\n"
    )
    payload = {
        "body": comment_body,
        "commit_id": commit_id,
        "path": issue["file"],
        "line": issue["line"],
        "side": "RIGHT"
    }
    comment_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{PR_NUMBER}/comments"
    resp = requests.post(comment_url, headers=headers, json=payload)
    if resp.status_code == 201:
        print(f"Posted inline comment for {issue['file']}:{issue['line']}")
    else:
        print(f"Failed to post comment for {issue['file']}:{issue['line']}")