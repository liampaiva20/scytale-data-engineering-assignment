# This script takes the saved PR data and creates a clean report with the data we need

import os
import json
import csv
import requests


GITHUB_TOKEN = "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"

USER = os.getlogin()

TRANSFORM_DIR = f"C:\\Users\\{USER}\\Documents\\Scytale Assessment PR"
os.makedirs(TRANSFORM_DIR, exist_ok=True)

OUTPUT_FILE = os.path.join(TRANSFORM_DIR, "merged_pr_report.csv")

EXTRACT_DIR = "extract"

ORG_NAME = "Scytale-exercise"
REPOS = ["Scytale_repo",
         "scytale-repo2",
         "scytale-repo3",
         "SCytale-repo4"]

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

#This function checks if a pull request was approved in code review
def check_cr_passed(pr):
    # Check if PR was approved by at least one reviewer
    reviews_url = pr["_links"]["self"]["href"] + "/reviews"
    response = requests.get(reviews_url, headers=headers)
    if response.status_code != 200: # If anything goes wrong like a 404 or 401 error code, we return False
        return False
    reviews = response.json()
    return any(review.get("state") == "APPROVED" for review in reviews)

# This function checks if the required Github checks were passed
def check_checks_passed(pr):
    # Get merge commit sha
    merge_sha = pr.get("merge_commit_sha")
    if not merge_sha:
        return False

    status_url = f"https://api.github.com/repos/{ORG_NAME}/{pr['base']['repo']['name']}/commits/{merge_sha}/status"
    response = requests.get(status_url, headers=headers)
    if response.status_code != 200:
        return False
    status_data = response.json()
    return status_data.get("state") == "success"

def main():
    merged_prs = []
    for repo in REPOS:
        # Load merged PRs from extract folder
        file_path = os.path.join(EXTRACT_DIR, f"{repo}_merged_prs.json")
        if not os.path.exists(file_path):
            print(f"Warning: {file_path} not found, skipping {repo}")
            continue

        with open(file_path, "r") as f:
            prs = json.load(f)

        for pr in prs:
            pr_number = pr["number"]
            pr_title = pr["title"]
            author = pr["user"]["login"]
            merge_date = pr["merged_at"]

            cr_passed = check_cr_passed(pr)
            checks_passed = check_checks_passed(pr)

            merged_prs.append({
                "PR Number": pr_number,
                "PR Title": pr_title,
                "Author": author,
                "Merge Date": merge_date,
                "CR_Passed": cr_passed,
                "CHECKS_PASSED": checks_passed
            })

    # Write the CSV report
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["PR Number", "PR Title", "Author", "Merge Date", "CR_Passed", "CHECKS_PASSED"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for pr in merged_prs:
            writer.writerow(pr)

    print(f"Report saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
