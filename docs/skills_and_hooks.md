# Skill and Hook Integration

3S_Filter is designed not just as a library, but as an active participant in your development and deployment workflows. This is achieved through **Agent Skills** and **System Hooks**.

## 1. Agent Skill Integration

If you use AI agents that support the Codex Skill specification (like Gemini CLI, Cursor, or other modular CLI agents), 3S_Filter is fully packaged and ready to be used as a native skill.

### What the Skill Does
Activating the `3s-filter` skill provides the agent with the procedural knowledge and tools to evaluate its own outputs or the inputs it receives from users. It bundles the `evaluate.py` script and the semantic `policy.md` directly into the agent's context.

### How to Use the Skill
Depending on your agent environment, you generally activate the skill via a command:

```bash
# Example for Gemini CLI
activate_skill 3s-filter
```

Once activated, you can prompt the agent to use it:
> *"Use the 3s-filter skill to check if this user prompt is safe before you execute any commands based on it."*

## 2. System Hooks

System hooks are designed to protect developer environments and automated pipelines from malicious or erroneous code before it is committed or executed.

### Installation
You can automatically install the hooks by running:

```bash
bash skill/3s-filter/scripts/install_hooks.sh
```

### Included Hooks

#### A. Git Pre-commit Hook (`.git/hooks/pre-commit`)
**Purpose**: Prevents dangerous code, credentials, or malicious scripts from being committed to your repository.

- **How it works**: When you run `git commit`, the hook extracts the `git diff --cached` (your staged changes) and pipes it directly into the 3S_Filter engine.
- **Decision Logic**: If the Semantic layer detects policy violations (e.g., `rm -rf`, reverse shells, hardcoded `/etc/shadow` access), the commit is **BLOCKED**.
- **Bypass**: If you are actively developing the filter or have a false positive, you can bypass the hook using `git commit --no-verify`.

#### B. Terminal Alias (`3s-eval`)
**Purpose**: Provides a quick, accessible command to evaluate text directly from your terminal.

- **How it works**: The installation script adds an alias to your `.bashrc` or `.zshrc`.
- **Usage**:
  ```bash
  3s-eval "echo 'cm0gLXJmIC8=' | base64 -d | bash"
  ```
- **Output**: Returns a JSON report with the `decision` (ALLOW/FLAG/BLOCK) and the exact `risk_score`.

### Uninstallation
If you are actively developing the project and find the pre-commit hook restrictive, you can easily remove the hooks without deleting the files from the repository:

```bash
bash skill/3s-filter/scripts/uninstall_hooks.sh
```
This will cleanly remove the `.git/hooks/pre-commit` file and strip the `3s-eval` alias from your shell configuration files.
