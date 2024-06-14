#!/bin/bash

FAIL=0
FAILED_REPOS=""

process_repo() {
  repo=$1
  repo_name=$(basename $repo)
  if [ -d "$repo_name" ]; then
    echo "Repository $repo_name already exists, skipping."
  else
    echo "Cloning $repo"
    output=$(git clone $repo 2>&1)
    if [[ $output == *"done."* ]]; then
      echo "Successfully cloned $repo"
    elif [[ $output == *"Repository not found"* ]]; then
      echo "Failed to clone $repo - Repository not found"
      let "FAIL+=1"
      FAILED_REPOS="$FAILED_REPOS $repo"
    else
      echo "Failed to clone $repo"
      echo "Error: $output"
      let "FAIL+=1"
      FAILED_REPOS="$FAILED_REPOS $repo"
    fi
  fi
}

while read repo || [[ -n $repo ]]; do
  process_repo $repo &
done < ./repositories.txt

wait

if [ "$FAIL" == "0" ]; then
  echo "All repositories cloned successfully."
else
  echo "Failed to clone the following repositories:"
  echo $FAILED_REPOS
fi