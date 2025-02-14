#!/bin/bash

# Check if a commit message was provided
if [ -z "$1" ]; then
    echo "Error: Please provide a commit message."
    exit 1
fi

# Staging all changes
git add .

# Committing changes with the provided commit message
git commit -m "$1"

# Pushing changes to the remote repository (assuming the default remote is 'origin' and branch is 'main')
git push origin main

# Optionally, you can add a check to see if the push was successful
if [ $? -eq 0 ]; then
    echo "Changes pushed successfully!"
else
    echo "Failed to push changes."
fi
