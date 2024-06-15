import argparse
import yaml
import os
import subprocess
import logging
from typing import Any, Dict, List, Union
import sys

def setup_logging() -> None:
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

def read_yaml(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def run_git_command(command: List[str], repo_dir: str = '') -> int:
    if repo_dir:
        command = ['git', '-C', repo_dir] + command
    else:
        command = ['git'] + command
    result = subprocess.run(command)
    return result.returncode

def clone_repo(repo_url: str, path: str) -> None:
    repo_name = os.path.basename(repo_url)
    repo_dir = os.path.join(path, repo_name)
    if not os.path.exists(repo_dir):
        logging.info(f"Cloning {repo_url} into {repo_dir}")
        run_git_command(['clone', repo_url, repo_dir])
    else:
        logging.info(f"Repository {repo_name} already exists, skipping.")

def fetch_and_merge(repo_dir: str, branch: str) -> None:
    run_git_command(['fetch', 'origin'], repo_dir)
    run_git_command(['merge', '--no-edit', f'origin/{branch}'], repo_dir)

def update_repo(repo_url: str, path: str) -> None:
    repo_name = os.path.basename(repo_url)
    repo_dir = os.path.join(path, repo_name)
    if os.path.exists(repo_dir):
        logging.info(f"Updating {repo_url} in {repo_dir}")
        try:
            for branch in ['master', 'main']:
                if run_git_command(['show-ref', '--verify', '--quiet', f'refs/remotes/origin/{branch}'], repo_dir) == 0:
                    fetch_and_merge(repo_dir, branch)
                    break
            else:
                logging.error(f"Neither 'master' nor 'main' branch found in remote repository for {repo_dir}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error updating repo {repo_url}: {e}")

def process_repos(repos: Dict[str, Union[Dict, List]], base_path: str = '', action: str = 'clone') -> None:
    if action == 'update':
        update_current_repo()

    for key, value in repos.items():
        path = os.path.join(base_path, key)
        if isinstance(value, list):
            for item in value:
                repo_action(item['repository'], path, action)
        elif isinstance(value, dict):
            process_repos(value, path, action)

def repo_action(repo_url: str, path: str, action: str) -> None:
    if action == 'clone':
        clone_repo(repo_url, path)
    elif action == 'update':
        update_repo(repo_url, path)

def update_current_repo() -> None:
    try:
        logging.info("Updating current repository")
        for branch in ['master', 'main']:
            if run_git_command(['show-ref', '--verify', '--quiet', f'refs/remotes/origin/{branch}']) == 0:
                fetch_and_merge(os.getcwd(), branch)
                break
        else:
            logging.error("Neither 'master' nor 'main' branch found in remote repository for current repo")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error updating current repo: {e}")

def main() -> None:
    setup_logging()

    if sys.version_info < (3, 7):
        logging.error("This script requires Python 3.7+.")
        sys.exit(1)

    parser = argparse.ArgumentParser(description='Manage repositories.')
    parser.add_argument('action', choices=['clone', 'update'], help='The action to perform.')
    args = parser.parse_args()

    repos = read_yaml(os.path.join(os.path.dirname(__file__), '..', 'repositories.yaml'))
    process_repos(repos, action=args.action)

if __name__ == "__main__":
    main()
