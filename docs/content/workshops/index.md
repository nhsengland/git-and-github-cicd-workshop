# Workshops

There are two workshop activities. Pick one to work through during the live session — you can come back and do the other in your own time.

!!! question "Not sure which to pick?"
    If you are more interested in local tooling and developer workflow, start with **[Pre-Commit Hooks](pre-commit-hooks.md)**.

    If you are more interested in cloud automation and GitHub integrations, start with **[GitHub Actions](github_actions.md)**.

    Both activities use the same flawed repository as their starting point, so they work independently.

---

## [Pre-Commit Hooks](pre-commit-hooks.md)

Configure automation that runs on your **local machine** before every `git commit`. You will set up three hooks:

- **[gitleaks](https://github.com/gitleaks/gitleaks)** — scans for hardcoded secrets and credentials
- **[ruff](https://docs.astral.sh/ruff/)** — checks and auto-fixes code formatting and linting violations
- **[nbstripout](https://github.com/kynan/nbstripout)** — strips Jupyter notebook outputs before they are committed

The repository already has intentional problems baked in — you will watch the hooks catch them.

---

## [GitHub Actions](github_actions.md)

Write CI/CD workflows that run automatically on **GitHub's servers** on every push and pull request. You will build:

- A **quality checks** workflow — runs `ruff` and `pytest`
- A **documentation deployment** workflow — builds and publishes this MkDocs site to [GitHub Pages](https://pages.github.com/)

---

!!! question "Getting Help"
    During the workshops, please ask questions — do not hesitate to flag if something is not working.

    Outside of the workshop, [open an issue](https://github.com/nhsengland/git-and-github-cicd-workshop/issues/new) if you find a problem with the materials.
