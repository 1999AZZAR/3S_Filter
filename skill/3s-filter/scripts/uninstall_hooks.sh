#!/bin/bash

# 3S_Filter Hook Uninstallation Script

echo "Uninstalling 3S_Filter hooks..."

# 1. Remove git pre-commit hook
if [ -f ".git/hooks/pre-commit" ]; then
    # Check if it's our hook
    if grep -q "3S_Filter pre-commit safety check" ".git/hooks/pre-commit"; then
        rm -f ".git/hooks/pre-commit"
        echo "[OK] Git pre-commit hook removed."
    else
        echo "[INFO] Git pre-commit hook exists but does not appear to be from 3S_Filter. Skipping removal."
    fi
else
    echo "[INFO] No git pre-commit hook found."
fi

# 2. Remove alias from shell config files
if [ -f "$HOME/.bashrc" ]; then
    # Use sed to delete lines containing the alias
    sed -i '/alias 3s-eval=/d' "$HOME/.bashrc"
    echo "[OK] Alias removed from .bashrc"
fi

if [ -f "$HOME/.zshrc" ]; then
    sed -i '/alias 3s-eval=/d' "$HOME/.zshrc"
    echo "[OK] Alias removed from .zshrc"
fi

echo "Done. Please restart your terminal or run 'unalias 3s-eval' in your current session."
