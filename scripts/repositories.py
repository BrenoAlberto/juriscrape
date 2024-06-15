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

def clone_repo(repo_url: str, path: str) -> None:
    repo_name = os.path.basename(repo_url)
    repo_dir = os.path.join(path, repo_name)
    if not os.path.exists(repo_dir):
        logging.info(f"Cloning {repo_url} into {repo_dir}")
        subprocess.run(['git', 'clone', repo_url, repo_dir], check=True)
    else:
        logging.info(f"Repository {repo_name} already exists, skipping.")

def fetch_and_merge(repo_dir: str, remote_branch: str) -> None:
    subprocess.run(['git', '-C', repo_dir, 'fetch', 'origin'], check=True)
    subprocess.run(['git', '-C', repo_dir, 'merge', '--no-edit', f'origin/{remote_branch}'], check=True)

def update_repo(repo_url: str, path: str) -> None:
    repo_name = os.path.basename(repo_url)
    repo_dir = os.path.join(path, repo_name)
    if os.path.exists(repo_dir):
        logging.info(f"Updating {repo_url} in {repo_dir}")
        try:
            current_branch = subprocess.check_output(
                ['git', '-C', repo_dir, 'rev-parse', '--abbrev-ref', 'HEAD']
            ).strip().decode('utf-8')

            for branch in ['master', 'main']:
                if subprocess.call(['git', '-C', repo_dir, 'show-ref', '--verify', '--quiet', f'refs/remotes/origin/{branch}']) == 0:
                    fetch_and_merge(repo_dir, branch)
                    break
            else:
                logging.error(f"Neither 'master' nor 'main' branch found in remote repository for {repo_dir}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error updating repo {repo_url}: {e}")

def process_repos(repos: Dict[str, Union[Dict, List]], base_path: str = '', action: str = 'clone') -> None:
    for key, value in repos.items():
        path = os.path.join(base_path, key)
        if isinstance(value, list):
            for item in value:
                if action == 'clone':
                    clone_repo(item['repository'], path)
                elif action == 'update':
                    update_repo(item['repository'], path)
        elif isinstance(value, dict):
            process_repos(value, path, action)

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
