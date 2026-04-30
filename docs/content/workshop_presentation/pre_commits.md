# Pre-Commit Hooks

## What is a pre-commit hook?

A small script that runs **automatically before every `git commit`**.

<div class="grid cards" markdown>

- :material-shield-check: **Catches problems early**

    Before code ever reaches GitHub — on your machine, every time.

- :material-account-group: **Shared across the team**

    The config lives in the repo. Everyone gets the same checks automatically.

- :material-wrench: **Can fix things for you**

    Many hooks (like formatters) just fix the issue silently. Others block the commit and tell you what's wrong.

- :material-lock: **Can't be skipped by accident**

    If a hook fails, the commit doesn't happen. The bar is raised for everyone.

</div>

---

## How does it work?

<div class="grid" markdown>

<div markdown>

### The flow

1. You run `git commit`
2. Pre-commit intercepts it
3. Each hook runs in order
4. :white_check_mark: All pass → commit goes through
5. :x: Any fail → commit is blocked, fix and retry

</div>

<div markdown>

### The config file

One file in your repo controls everything:

```yaml title=".pre-commit-config.yaml"
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.0
    hooks:
      - id: ruff         # linting
      - id: ruff-format  # formatting
```

- Hooks are pulled from public repos
- Pin the version with `rev:`
- Run `pre-commit install` once to activate

</div>

</div>

---

!!! info "Hooks we'll use today"
    - **gitleaks** — blocks accidentally committed passwords or API keys
    - **ruff** — automatically fixes Python linting violations
    - **ruff-format** — automatically formats Python code
    - **nbstripout** — strips outputs from Jupyter notebooks before committing
