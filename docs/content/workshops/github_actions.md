# GitHub Actions

!!! success "Learning Objectives"

    By the end of this activity, you will be able to:

    - [ ] Describe what GitHub Actions is and how workflows are structured
    - [ ] Write a workflow that runs code quality checks on every push and pull request
    - [ ] Write a workflow that deploys documentation to GitHub Pages
    - [ ] Configure Python and install dependencies in CI

---

## What is GitHub Actions?

**[GitHub Actions](https://docs.github.com/en/actions)** is GitHub's built-in CI/CD platform. You define **workflows** as YAML files stored in `.github/workflows/`. GitHub automatically runs these workflows when specified events occur in your repository — such as a push, a pull request, or a scheduled time.

Each workflow runs inside a fresh virtual machine (**runner**) provisioned by GitHub. This means every run starts from a clean slate, making your checks reproducible and consistent.

A workflow has this basic structure:

```yaml
name: My Workflow            # (1)!

on:                          # (2)!
  push:
  pull_request:

jobs:                        # (3)!
  my-job:
    runs-on: ubuntu-latest   # (4)!
    steps:                   # (5)!
      - uses: actions/checkout@v4
      - run: echo "Hello, CI!"
```

1. A human-readable name shown in the **Actions** tab on GitHub.
2. **Triggers** — the events that cause the workflow to run. `push` fires on every push to any branch; `pull_request` fires when a PR is opened or updated.
3. **Jobs** — groups of steps. Multiple jobs run in parallel by default; add `needs:` to sequence them.
4. The **runner** image. `ubuntu-latest` is the most common choice for Python projects.
5. **Steps** — the individual tasks within a job. `uses:` runs a pre-built Action from the GitHub Marketplace; `run:` executes a shell command.

---

## Why Automate with GitHub Actions in Data Science?

Pre-commit hooks and GitHub Actions solve related but different problems:

| | Pre-Commit Hooks | GitHub Actions |
|---|---|---|
| **Where it runs** | Your local machine | GitHub's servers |
| **When it runs** | Before every local commit | On every push / pull request |
| **Who controls it** | Each developer installs it | Enforced for the whole repository |
| **Can auto-fix files** | Yes | No — reports failures only |
| **Can block merges** | No | Yes — via branch protection rules |

Use both together: hooks give fast local feedback, and Actions enforce the same checks for every developer on every push.

!!! info "R Equivalents"

    GitHub Actions is language-agnostic. For R projects:

    === "Python"
        Use `actions/setup-python` to install Python, then `pip install` to install dependencies.

        ```yaml
        - name: Set up Python
          uses: actions/setup-python@v5
          with:
            python-version: "3.12"

        - name: Install dependencies
          run: pip install -e ".[dev]"
        ```

    === "R"
        Use [`r-lib/actions`](https://github.com/r-lib/actions) for a standardised R setup. The `pak` package manager handles fast dependency installation.

        ```yaml
        - uses: r-lib/actions/setup-r@v2
          with:
            r-version: '4.4'

        - uses: r-lib/actions/install-r-dependencies@v2
          with:
            cache-version: 1

        - name: Run tests
          run: Rscript -e 'testthat::test_dir("tests/testthat")'

        - name: Lint
          run: Rscript -e 'lintr::lint_dir("R")'
        ```

---

## Activity: Build Two CI/CD Workflows

### Task 1: Create the Workflows Directory

GitHub Actions looks for workflow files in `.github/workflows/`. Create the directory:

```bash
mkdir -p .github/workflows
```

---

### Task 2: Give the Workflow a Name and Triggers

Create a new file `.github/workflows/quality-checks.yml`. Start with just the name and the events that should trigger it:

```yaml
name: Quality Checks

on:
  push:
  pull_request:
```

!!! info "What are triggers?"
    The `on:` block controls *when* the workflow runs.

    - `push` fires on every push to any branch.
    - `pull_request` fires when a pull request is opened or updated.

    Together these mean: run quality checks whenever any code change arrives, whether directly pushed or proposed via PR. You can narrow them down with `branches:` filters once you are comfortable with the basics.

---

### Task 3: Add a Job and Choose a Runner

Add the `jobs:` block below your triggers:

```yaml
jobs:
  quality:
    runs-on: ubuntu-latest
```

!!! info "Jobs and runners"
    A **job** is a group of steps that run together. Multiple jobs in the same workflow run in parallel by default — add `needs:` to sequence them.

    `runs-on: ubuntu-latest` tells GitHub to spin up a fresh Ubuntu virtual machine for each run. The machine starts completely empty; every run must install its own dependencies from scratch. This is what makes CI reproducible.

---

### Task 4: Check Out the Code

Add a `steps:` key under your job, with the checkout step as its first entry:

```yaml
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
```

!!! info "`uses:` vs `run:`"
    Steps can do one of two things:

    - `uses:` runs a **pre-built Action** from the GitHub Marketplace. `actions/checkout@v4` is maintained by GitHub and handles the full `git clone` for you.
    - `run:` executes a **shell command** directly on the runner, just like typing it in a terminal.

    The `@v4` suffix pins the Action to a specific major version, preventing unexpected changes from breaking your workflow.

---

### Task 5: Install Python and Dependencies

Append two more steps directly below the checkout step:

```yaml
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install -e ".[dev]"
```

!!! info "Why install dependencies every run?"
    The runner is a fresh VM — it has no packages installed. `pip install -e ".[dev]"` installs the project in editable mode along with everything in the `dev` dependency group, which includes `pytest` and `ruff`.

    The `with:` block passes inputs to an Action. Here it tells `setup-python` exactly which Python version to install, keeping every run consistent.

---

### Task 6: Add the Quality Check Steps

Append the final two steps:

```yaml
      - name: Lint and format check
        run: ruff check .

      - name: Run tests
        run: pytest tests/
```

`ruff check .` exits with a non-zero code if there are any linting violations, which fails the step and the whole job. `pytest tests/` does the same if any test fails.

!!! warning "This workflow will fail on the first push — deliberately"
    The repository contains a logic bug in `practice_level_gp_appointments/analytics.py` that causes two test failures. Pre-commit hooks catch secrets and formatting violations locally, but they cannot run your test suite — that is what GitHub Actions is for.

    You will see the `pytest` step fail in the **Actions** tab. The **Bonus Activity** at the end of this workshop walks through tracking down and fixing the bug.

---

### Task 7: Push and Watch it Run

Stage and push the new workflow file:

```bash
git add .github/workflows/quality-checks.yml
git commit -m "add quality checks workflow"
git push
```

Navigate to your forked repository on GitHub and click the **Actions** tab. You should see the workflow running (or already completed). Click into it to see the logs from each step.

!!! tip "Protecting your main branch"
    Once your workflow is passing, go to **Settings → Branches → Add branch protection rule** on your fork. Enable **Require status checks to pass before merging** and select `Quality Checks`. This prevents any pull request from being merged until CI passes — the same pattern used on production repositories.

---

### Task 8: Name and Trigger the Deploy Workflow

Create a second file `.github/workflows/deploy-docs.yml`. This workflow has a different purpose — it deploys documentation — so it needs different triggers:

```yaml
name: Deploy Documentation

on:
  push:
    branches:
      - main
```

!!! info "Narrowing triggers with `branches:`"
    Unlike the quality checks workflow that fires on every push, documentation should only deploy when code reaches `main`. Deploying from feature branches would overwrite the live site with unreviewed work.

    The `branches:` filter restricts the `push` trigger to only that branch.

---

### Task 9: Add Permissions and the Deploy Job

This workflow needs write access to push the built site to the `gh-pages` branch. Add the `permissions:` block and the job below your triggers:

```yaml
permissions:
  contents: write

jobs:
  deploy:
    runs-on: ubuntu-latest
```

!!! info "Why declare permissions?"
    By default, GitHub Actions workflows have read-only access to the repository. `contents: write` grants the job permission to push commits — which `mkdocs gh-deploy` needs in order to update the `gh-pages` branch.

    Declaring only the permissions you need is good security practice: it limits the blast radius if a third-party Action in the job were ever compromised.

---

### Task 10: Add the Steps

Complete the workflow by adding `steps:` under the job:

```yaml
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install docs dependencies
        run: pip install -e ".[docs]"

      - name: Deploy to GitHub Pages
        run: mkdocs gh-deploy --force
```

Notice `pip install -e ".[docs]"` instead of `.[dev]` — there is no reason to install `pytest` or `ruff` for a documentation build. Keeping dependency groups separate makes CI faster and the intent clearer.

`mkdocs gh-deploy --force` builds the static site and force-pushes it to the `gh-pages` branch. [GitHub Pages](https://pages.github.com/) serves this branch automatically.

!!! info "Enabling GitHub Pages on your fork"
    For the deployment to work, go to **Settings → Pages** in your forked repository. Set the source to **Deploy from a branch** and select `gh-pages`. After the workflow runs for the first time, your site will be live at:

    ```
    https://\<your-username\>.github.io/git-and-github-cicd-workshop/
    ```

---

### Task 11: Push and Verify the Deployment

```bash
git add .github/workflows/deploy-docs.yml
git commit -m "add docs deploy workflow"
git push
```

Once the workflow completes, your documentation site will be live. Check the **Actions** tab to confirm the deployment step succeeded, then open your GitHub Pages URL to see the site.

!!! success "Well done!"
    You now have two automated workflows:

    - **Quality Checks** — ruff and pytest run on every push and pull request, catching issues before they reach `main`
    - **Deploy Documentation** — your MkDocs site is built and published automatically whenever code is merged

    If you haven't already, try the **[Pre-Commit Hooks](pre-commit-hooks.md)** workshop to catch secrets and formatting violations before they ever reach CI.

---

## Complete Files Reference

If anything looks wrong in your workflow files, compare against the complete versions here.

??? note "`.github/workflows/quality-checks.yml` — complete file"

    ```yaml
    name: Quality Checks

    on:
      push:
      pull_request:

    jobs:
      quality:
        runs-on: ubuntu-latest

        steps:
          - name: Checkout code
            uses: actions/checkout@v4

          - name: Set up Python
            uses: actions/setup-python@v5
            with:
              python-version: "3.12"

          - name: Install dependencies
            run: pip install -e ".[dev]"

          - name: Lint and format check
            run: ruff check .

          - name: Run tests
            run: pytest tests/
    ```

??? note "`.github/workflows/deploy-docs.yml` — complete file"

    ```yaml
    name: Deploy Documentation

    on:
      push:
        branches:
          - main

    permissions:
      contents: write

    jobs:
      deploy:
        runs-on: ubuntu-latest

        steps:
          - name: Checkout code
            uses: actions/checkout@v4

          - name: Set up Python
            uses: actions/setup-python@v5
            with:
              python-version: "3.12"

          - name: Install docs dependencies
            run: pip install -e ".[docs]"

          - name: Deploy to GitHub Pages
            run: mkdocs gh-deploy --force
    ```

---

## Bonus Activity: Fix the Failing Tests

The `quality` job is failing because `analytics.py` contains a subtle logic bug. Open the failing test run in the **Actions** tab and read the assertion error to understand what is going wrong.

The bug is in `practice_level_gp_appointments/analytics.py`. Look at how `total_appointments` is calculated — it is counting the number of *rows* in the DataFrame rather than the total number of *appointments*.

??? success "Reveal the fix"

    Find this line:

    ```python
    total_appointments = len(df)
    ```

    Replace it with:

    ```python
    total_appointments = df["count_of_appointments"].sum()
    ```

    Run `uv run pytest tests/unittests/test_analytics.py` locally to confirm both tests pass, then push. Watch the workflow go green.

---

## Going Further

??? info "Workflow badges"
    You can add a status badge to your `README.md` to show whether your CI is passing. On the Actions tab, click your workflow name, then click the three-dot menu and select **Create status badge**.

    ```markdown
    ![Quality Checks](https://github.com/<org>/<repo>/actions/workflows/quality-checks.yml/badge.svg)
    ```

??? info "Secrets in GitHub Actions"
    Never hardcode credentials in your workflow files. Store them in **Settings → Secrets and variables → Actions** and reference them as environment variables:

    ```yaml
    - name: Deploy
      env:
        MY_API_KEY: ${{ secrets.MY_API_KEY }}
      run: python deploy.py
    ```

??? info "Caching dependencies"
    You can cache your `pip` dependencies to speed up subsequent workflow runs. Add the `cache` input to `actions/setup-python`:

    ```yaml
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: "3.12"
        cache: "pip"
    ```

    This caches the pip download cache between runs, meaning dependencies install much faster after the first run.
