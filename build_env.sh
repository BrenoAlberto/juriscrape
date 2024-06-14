#!/bin/bash

clear
export USER_ID=$(id -u)
export GROUP_ID=$(id -g)
export USER_NAME="juriscrape-dev"

# Ensure Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Docker is not running. Please start Docker and try again."
    exit 1
fi

# Ensure Dev Containers extension is installed
if ! code --list-extensions | grep -E "ms-vscode-remote.remote-containers" > /dev/null; then
    echo "Please install the 'Remote - Containers' extension in VS Code and try again."
    exit 1
fi

# Bring down any existing containers
docker compose down && clear

# Build the Docker images
docker compose build && clear

echo "Dev Container is ready to start."
echo "Run the following command to start the VSCODE Dev Container:"
echo "CTRL + SHIFT + P -> Dev Containers: Open Folder in Container -> Select the current folder /juriscrape"
echo
echo "Alternatively, just attach to the container using the following command:"
echo "docker compose run dev zsh"