# GitHub Actions

## What is GitHub Actions?

Automation that runs **in the cloud, triggered by events in your repository**.

<div class="grid cards" markdown>

- :material-cloud-check: **Runs on GitHub's servers**

    No local setup needed. Every contributor gets the same environment.

- :material-lightning-bolt: **Triggered by events**

    Push a commit, open a pull request, merge to `main` — Actions reacts automatically.

- :material-test-tube: **The server-side safety net**

    Pre-commit hooks can be skipped locally. GitHub Actions can't be bypassed.

- :material-recycle: **Reusable building blocks**

    Use community-built Actions from the GitHub Marketplace — no reinventing the wheel.

</div>

---

## How does it work?

<div class="grid" markdown>

<div markdown>

### The flow

1. You push code to GitHub
2. GitHub reads your workflow files
3. A runner (a fresh virtual machine) spins up
4. Your steps execute in order
5. :white_check_mark: All pass → green tick on your PR
6. :x: Any fail → red cross, merge is blocked

</div>

<div markdown>

### The workflow file

One YAML file defines everything:

```yaml title=".github/workflows/tests.yml"
name: Run tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - run: uv run pytest tests/
```

- Stored in `.github/workflows/`
- `on:` controls when it triggers
- `steps:` are the commands to run

</div>

</div>

---

## Pre-commit hooks vs GitHub Actions

<div class="grid cards" markdown>

- :material-laptop: **Pre-commit hooks**

    Fast, local, immediate feedback. Runs before you can even push.

- :material-cloud: **GitHub Actions**

    Server-side, can't be skipped, runs in a clean environment every time.

</div>

!!! success "Use both"
    Hooks give you speed. Actions give you the guarantee. Together they cover every angle.
