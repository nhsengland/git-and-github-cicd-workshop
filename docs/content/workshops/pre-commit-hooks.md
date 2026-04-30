# Pre-Commit Hooks

!!! success "Learning Objectives"

    By the end of this activity, you will be able to:

    - [ ] Explain what pre-commit hooks are and why they matter in Data Science
    - [ ] Configure hooks for secret detection, linting, and notebook output stripping
    - [ ] Install and run the `pre-commit` framework using `uv`
    - [ ] Understand the difference between hooks that auto-fix files and hooks that block commits

---

## What are Pre-Commit Hooks?

A **pre-commit hook** is a script that runs automatically every time you run `git commit`, *before* the commit is actually created. If the hook fails, the commit is blocked.

The [`pre-commit`](https://pre-commit.com/) framework manages hooks as shareable configuration. Instead of each developer writing their own scripts, you define all your hooks in a single `.pre-commit-config.yaml` file that lives in the repository. Everyone gets the same checks.

```
git commit -m "my changes"
        │
        ▼
┌───────────────────┐
│  pre-commit runs  │  ← hooks fire here, before the commit exists
│  your hooks       │
└───────┬───────────┘
        │
   ┌────┴────┐
   │ PASS?   │
   └────┬────┘
        │
   ✓ Yes → commit is created
   ✗ No  → commit is blocked (files may be auto-fixed for you)
```

---

## Why Use Pre-Commit Hooks in Data Science?

!!! info "Three problems hooks solve"

    === "Leaked Secrets"

        Hardcoded passwords, API keys, and database credentials accidentally committed to Git are one of the most common security incidents in software teams. Once pushed to a remote repository, a secret is effectively compromised — even if you delete it in a later commit, it remains in the Git history.

        **[gitleaks](https://github.com/gitleaks/gitleaks)** scans your staged files for patterns that look like credentials before they can reach Git history.

    === "Messy Code"

        Inconsistent formatting and style makes code harder to review and maintain. Fixing it manually is tedious and easy to forget.

        **[ruff](https://docs.astral.sh/ruff/)** checks and automatically fixes formatting and linting violations on every commit.

    === "Dirty Notebooks"

        Jupyter notebooks store cell outputs — plots, tables, printed values — inside the `.ipynb` file as JSON. Committing these outputs bloats the repository, makes diffs near-unreadable, and can accidentally publish sensitive data.

        **[nbstripout](https://github.com/kynan/nbstripout)** automatically strips all outputs from notebooks before they are committed.

!!! tip "R Equivalents"

    The `pre-commit` framework is language-agnostic and works for R projects too.

    - **Secrets**: the same `gitleaks` hook works for any language
    - **Formatting/Linting**: the [`precommit`](https://lorenzwalthert.github.io/precommit/) R package provides hooks for `styler` (formatting) and `lintr` (linting). Install it with `usethis::use_precommit()`.
    - **Notebooks**: `nbstripout` handles R-backed Jupyter notebooks. For R Markdown and Quarto files, `lintr` hooks can check code quality.

---

## Activity: Implement the Hooks

### Task 1: Explore What's Already Wrong

This repository has some intentional problems baked in. Let's find them first.

Run the ruff linter to see the formatting issues:

```bash
uv run ruff check practice_level_gp_appointments/
```

You should see errors in `analytics.py`:

- **E401** — multiple imports on one line (`import os, sys`)
- **F401** — unused imports (`os` and `sys` are never used)
- **I001** — imports are not sorted correctly

Now open `practice_level_gp_appointments/config.py`. Notice the hardcoded AWS credentials near the top of the file.

!!! danger "This is exactly how credential leaks happen"
    These keys would be committed to Git, pushed to GitHub, and could be scraped by automated bots within minutes of being public. The `gitleaks` hook is specifically designed to catch this before it ever reaches version control.

Finally, open `notebooks/analysis.ipynb`. Notice that the cells have execution counts and outputs stored inside them — exactly the kind of content that bloats repositories and makes diffs difficult to read.

---

### Task 2: Create the Config File and Add Secret Detection

Create a new file called `.pre-commit-config.yaml` in the **root of the repository**. Start with just the `gitleaks` hook:

```yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.4
    hooks:
      - id: gitleaks
```

!!! info "How the config file works"
    The `pre-commit` framework reads `.pre-commit-config.yaml` to know which hooks to run. Each entry under `repos:` points to an external Git repository that provides one or more hooks.

    The `rev` field pins the exact version to use — `pre-commit` downloads and caches it automatically. Pinning versions means your hooks behave identically for every developer on the team, regardless of when they cloned the repository.

    **gitleaks** scans staged files for patterns that match real credentials — AWS keys, tokens, passwords. It cannot auto-fix the problem; only you can remove a secret.

---

### Task 3: Add Linting

Append the `ruff` entry to `.pre-commit-config.yaml`:

```yaml
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

!!! info "Two hooks from one repo"
    `ruff-pre-commit` provides two separate hooks:

    - `ruff` — linting. The `--fix` argument tells it to auto-correct any violations it knows how to fix, then exit with an error because it modified files (prompting you to review and re-stage them).
    - `ruff-format` — code formatting, equivalent to running `ruff format`. Formats to a consistent style automatically.

    Both hooks read your project's `pyproject.toml` for configuration, so they behave the same as running `ruff` locally.

---

### Task 4: Add Notebook Output Stripping

Append the final entry to `.pre-commit-config.yaml`:

```yaml
  - repo: https://github.com/kynan/nbstripout
    rev: 0.7.1
    hooks:
      - id: nbstripout
```

!!! info "Why strip notebook outputs?"
    Jupyter notebooks store cell outputs — plots, tables, printed values — as JSON inside the `.ipynb` file. Committing these outputs bloats the repository, produces near-unreadable diffs, and can accidentally publish sensitive query results or data previews.

    **nbstripout** strips all outputs and execution counts before the file is staged. It modifies the file in-place, so after it runs you will see the notebook as "modified" in `git diff` — which is exactly what you want.

---

### Task 5: Install the Hooks

Install the hooks into your local Git repository:

```bash
uv run pre-commit install
```

You should see:

```
pre-commit installed at .git/hooks/pre-commit
```

!!! info "What does this do?"
    It writes a small script to `.git/hooks/pre-commit`. Git calls this script automatically on every `git commit`. The hook tools themselves are downloaded and cached in `~/.cache/pre-commit/` the first time they run.

    Note that hooks are **local** — they live in `.git/`, which is never committed. Every developer who clones the repository needs to run `pre-commit install` themselves. This is a good thing to document in your `README.md`.

---

### Task 6: Attempt a Commit

Stage all the changes made so far and attempt a commit:

```bash
git add .
git commit -m "add analysis notebook and config"
```

Watch what happens. You should see output similar to this:

```
gitleaks................................................................Failed
- hook id: gitleaks
- exit code: 1

Finding:     AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
  RuleID:    aws-secret-access-key
  File:      practice_level_gp_appointments/config.py
  Line:      19

ruff (run with --fix)...............................................Failed
- hook id: ruff
- exit code: 1
- files were modified by this hook

ruff-format..........................................................Passed
nbstripout...........................................................Passed
```

!!! warning "The commit was blocked — and that is the point"

    Three hooks ran. Here is what each one did:

    | Hook | Result | Why |
    |------|--------|-----|
    | `gitleaks` | **FAILED** | Found hardcoded AWS credentials in `config.py`. Cannot auto-fix — only you can remove a secret. |
    | `ruff` | **FAILED** (but auto-fixed) | Fixed the import issues in `analytics.py`, then exited with an error because it modified files. |
    | `ruff-format` | Passed | Formatting was already acceptable. |
    | `nbstripout` | Passed | Stripped outputs from the notebook. |

    Because the commit was blocked, **nothing was committed**. Run `git diff` to see the fixes `ruff` made automatically to `analytics.py`.

---

### Task 7: Fix the Secret

Open `practice_level_gp_appointments/config.py` and remove the hardcoded credentials. Replace them with a comment explaining the correct approach:

```python
# Credentials must come from environment variables, never hardcoded.
# Set these in your shell or a .env file (which should be in .gitignore):
#   export AWS_ACCESS_KEY_ID="your-key-here"
#   export AWS_SECRET_ACCESS_KEY="your-secret-here"
```

---

### Task 8: Re-stage and Commit Successfully

Stage all the changes — including the files `ruff` auto-fixed:

```bash
git add .
git commit -m "add analysis notebook and config"
```

This time, all hooks should pass and the commit should succeed:

```
gitleaks................................................................Passed
ruff (run with --fix)...................................................Passed
ruff-format.............................................................Passed
nbstripout...............................................................Passed
[main abc1234] add analysis notebook and config
```

!!! success "Well done!"
    You have set up three automated quality gates that will protect this repository on every future commit:

    - No more accidental secret leaks
    - Consistent code formatting, maintained automatically
    - Clean notebook commits, always

    Note that pre-commit hooks run *locally* and handle formatting and secrets — they do not run your test suite. When you're ready, try the **[GitHub Actions](github_actions.md)** workshop to run automated tests in CI and catch logic bugs that slip past local checks.

---

## Complete File Reference

If anything looks wrong in your config, compare against the complete version here.

??? note "`.pre-commit-config.yaml` — complete file"

    ```yaml
    repos:
      - repo: https://github.com/gitleaks/gitleaks
        rev: v8.18.4
        hooks:
          - id: gitleaks

      - repo: https://github.com/astral-sh/ruff-pre-commit
        rev: v0.4.0
        hooks:
          - id: ruff
            args: [--fix]
          - id: ruff-format

      - repo: https://github.com/kynan/nbstripout
        rev: 0.7.1
        hooks:
          - id: nbstripout
    ```

---

## Going Further

??? info "Running hooks manually"
    You can run all hooks against every file in the repository at any time — not just on staged files:

    ```bash
    uv run pre-commit run --all-files
    ```

    This is useful for applying hooks to a repository that already exists, or for checking that everything passes before a code review.

??? info "Updating hook versions"
    To update all hooks to their latest tagged versions:

    ```bash
    uv run pre-commit autoupdate
    ```

    This updates the `rev` fields in your `.pre-commit-config.yaml`. Always review the changes and test before committing.

??? info "Skipping a hook in an emergency"
    If you genuinely need to bypass a hook (for example, a known false-positive), you can skip it with:

    ```bash
    git commit --no-verify -m "my message"
    ```

    Use this sparingly. Pre-commit hooks only work as a safety net if you actually let them run.
