#!/bin/bash

# 3S_Filter Hook Installation Script

set -e

PROJECT_ROOT=$(pwd)
EVAL_SCRIPT="$PROJECT_ROOT/skill/3s-filter/scripts/evaluate.py"

echo "Installing 3S_Filter hooks..."

# 1. Register as a git pre-commit hook (optional)
if [ -d ".git" ]; then
    cat << EOF > .git/hooks/pre-commit
#!/bin/bash
# 3S_Filter pre-commit safety check

echo "🔍 Running 3S_Filter on staged changes..."

# Get the git diff of staged changes
DIFF_CONTENT=\$(git diff --cached)

if [ -z "\$DIFF_CONTENT" ]; then
    exit 0
fi

# Run the 3S_Filter evaluation on the diff
# Since diffs can be large and have special characters, we pipe it to python
# Assuming evaluate.py can handle stdin if text is not passed as argument, 
# or we pass it securely. Actually, let's pass it via temporary file.

TMP_FILE=\$(mktemp)
echo "\$DIFF_CONTENT" > "\$TMP_FILE"

# Evaluate using python
if [ -f "$PROJECT_ROOT/.venv/bin/python" ]; then
    PYTHON_CMD="$PROJECT_ROOT/.venv/bin/python"
else
    PYTHON_CMD="python3"
fi

\$PYTHON_CMD "$EVAL_SCRIPT" "\$(cat "\$TMP_FILE")"
RESULT=\$?

rm -f "\$TMP_FILE"

if [ \$RESULT -ne 0 ]; then
    echo "❌ 3S_Filter BLOCKED this commit due to safety policy violations."
    echo "Please review the output above and remove dangerous contents."
    exit 1
fi

echo "✅ 3S_Filter check passed."
exit 0
EOF
    chmod +x .git/hooks/pre-commit
    echo "[OK] Git pre-commit hook installed."
fi

# 2. Add an alias to the current shell session (bash/zsh)
ALIAS_CMD="alias 3s-eval='python3 $EVAL_SCRIPT'"

if [ -f "$HOME/.bashrc" ]; then
    if ! grep -q "3s-eval" "$HOME/.bashrc"; then
        echo "$ALIAS_CMD" >> "$HOME/.bashrc"
        echo "[OK] Alias added to .bashrc"
    fi
fi

if [ -f "$HOME/.zshrc" ]; then
    if ! grep -q "3s-eval" "$HOME/.zshrc"; then
        echo "$ALIAS_CMD" >> "$HOME/.zshrc"
        echo "[OK] Alias added to .zshrc"
    fi
fi

echo "Done. Please restart your terminal or source your config file."
