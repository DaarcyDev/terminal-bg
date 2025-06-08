#!/bin/bash

set -e

REPO_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "🔄 Terminal-BG: Updating from Git..."

cd "$REPO_DIR"

if [ ! -d ".git" ]; then
    echo "❌ Not a valid Git repository. Did you clone terminal-bg using git?"
    exit 1
fi

git pull origin main || git pull origin master

echo "✅ Repository updated."

echo "🔧 Reinstalling the application..."

if pipx list | grep ' - terminal-bg'; then
    echo "➖ Uninstalling previous version..."
    pipx uninstall terminal-bg
fi

echo "➕ Installing latest version..."
pipx install .


echo "✅ terminal-bg successfully updated."
