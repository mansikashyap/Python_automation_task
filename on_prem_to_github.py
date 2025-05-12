import requests
import os
import subprocess
import git
import time
from datetime import datetime

CRIBL_CONFIG_PATH = "/opt/cribl/local/"
GITHUB_REPO = 'https://github/test.git'
API_URL = 'https://api.github.com/repos/username/repo/contents'
CRIBL_CLOUD_TOKEN = os.getenv("CRIBL_CLOUD_TOKEN")
CRIBL_API_URL = "https://<your-cribl-cloud-endpoint>/api/deploy"

def commit_to_github():
    os.chdir(CRIBL_CONFIG_PATH)
    subprocess.run(["git","add","."], check = True)
    github_commit_message = f"Automated commit at {time.strftime('%Y-%m-%d %H:%M:%S')}"
    subprocess.run(["git", "commit", "-m", github_commit_message], check=True)
    subprocess.run(["git", "push"], check=True)
    print('Changes pushed to github')


def deploy_to_cloud():
    headers = {
        "authorization": f"bearer {CRIBL_CLOUD_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "path": "/path/to/gitub",
        "source": "github",
        "repo": "your-org/cribl-configs"
    }

    response = requests.post(CRIBL_API_URL,headers=headers, json = payload)

    if response.status_code == 200 :
        print("Deployed to CRIBL cloud")

    else:
        print("Deployment failed: {response.status_code} > {response.text}")

def has_changes():
    os.chdir(CRIBL_CONFIG_PATH)
    repo = git.Repo(GITHUB_REPO)
    return repo.is_dirty(untracked_files=True)


def main():
    if has_changes():
        print('detected changes. Pushing to github')
        try:
            commit_to_github()
            print('Changes pushed to github')
        except subprocess.CalledProcessError as e:
            print(f"Error during git operations: {e}")
    else:
        print('No changes detected')
        
if __name__ == "__main__":
    main()