#!/bin/bash

update_repo() {
  repo=$1
  dir=$(basename $repo)
  if [ -d "$dir/.git" ]; then
    echo "Updating repository in $dir"
    cd $dir
    git fetch origin
    current_branch=$(git rev-parse --abbrev-ref HEAD)
    if git show-ref --verify --quiet refs/remotes/origin/master; then
      remote_branch='master'
    elif git show-ref --verify --quiet refs/remotes/origin/main; then
      remote_branch='main'
    else
      echo "Neither 'master' nor 'main' branch found in remote repository for $dir"
      return
    fi

    git merge --no-edit origin/$remote_branch
    cd ..
  fi
}

while read repo || [[ -n $repo ]]; do
  update_repo $repo &
done < ./repositories.txt

wait