# This script connects to GitHub and downloads information about pull requests (PRs) from specific repositories.

import requests    # This allows us to communicate with the internet
import os          # This helps our script interact with our computer's files and folders.
import json        # This lets our script work with JSON Data

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # This is the Personal Access Token
ORG_NAME = "Scytale-exercise"

# Here is a list of all the repos
REPOS = [
    "Scytale_repo",
    "scytale-repo2",
    "scytale-repo3",
    "SCytale-repo4"
]

headers = {
    "Authorization": f"token {GITHUB_TOKEN}", # Shows Github that I can access the data
    "Accept": "application/vnd.github+json" # Tell Github we want the data in JSON format
}

# This function gets all the pull requests that have been merged
def fetch_merged_prs(org, repo):
    url = f"https://api.github.com/repos/{org}/{repo}/pulls?state=closed&per_page=100"
    prs = []
    while url:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        # Filter merged PRs
        merged_prs = [pr for pr in data if pr.get('merged_at') is not None]
        prs.extend(merged_prs)
        # Pagination
        if 'next' in response.links:
            url = response.links['next']['url']
        else:
            url = None
    return prs

# This function saves the merged pull requests into a json file
def save_prs(prs, repo):
    os.makedirs('extract', exist_ok=True)
    file_path = f"extract/{repo}_merged_prs.json"
    with open(file_path, 'w') as f:
        json.dump(prs, f, indent=2)
    print(f"Saved {len(prs)} merged PRs to {file_path}")

if __name__ == "__main__":
    for repo in REPOS:
        print(f"Fetching merged PRs for repo: {repo}")
        prs = fetch_merged_prs(ORG_NAME, repo)
        save_prs(prs, repo)

