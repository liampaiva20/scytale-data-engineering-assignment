# Scytale Data Engineering Assessment

This project was created for a graduate data engineering assessment.  
It connects to the GitHub API to extract and analyze pull request (PR) data from specified repositories within the `Scytale-exercise` organization.

## Project Structure

- `extract.py`:  
  Connects to the GitHub API and fetches all **merged pull requests** for the specified repositories.  
  Saves the data as JSON files in the `extract/` folder.

- `transform.py`:  
  Reads the extracted PR data, checks if the PR was approved and if all checks passed.  
  Creates a summary CSV report with the processed information and saves it in the `Documents/Scytale Assessment PR/` folder.

- `extract/`:  
  Folder containing the raw JSON files of merged PRs.

- `Documents/Scytale Assessment PR/`:  
  Folder where the final CSV report is saved.

## How to Run

1. Make sure you have Python installed.
2. Install required packages (like `requests`) if not installed.
3. Set your GitHub personal access token in the scripts as the variable `GITHUB_TOKEN`.
4. Run `extract.py` to fetch PR data.
5. Run `transform.py` to generate the CSV report.

## Notes

- This project only considers **merged** pull requests.
- PR approval status and checks status are retrieved via additional API calls.
- The CSV report contains columns: PR number, title, author, merge date, approval status, and checks status.

---

Thanks for reviewing!
