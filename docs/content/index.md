# Git and GitHub CI/CD Workshop

Welcome to the **Git and GitHub CI/CD** workshop, run by the NHS England Data Science and Applied AI team.

> This workshop is a dive into the automated features of Git and GitHub, specifically focusing on CI/CD workflows for Data Science projects. We will cover the mechanics and practical implementation of pre-commit hooks and GitHub Actions — two tools that automate quality checks, protect your repository from common mistakes, and keep your project standards consistent across a whole team.

!!! tip "Pre-requisite Knowledge"

    | Pre-requisite | Description |
    |---------------|-------------|
    | Python | Knowledge of how to write and run Python code |
    | Git | Basic command line usage — staging, committing, pushing |
    | GitHub | Familiarity with repositories, Codespaces, and forking |

## Workshop Activities

There are two activities. Pick one to complete during the live session and work through the other at your own pace.

<div class="grid cards" markdown>

- **[Pre-Commit Hooks](workshops/pre-commit-hooks.md)**

    Set up local automation that runs before every commit. You will configure hooks for secret detection ([`gitleaks`](https://github.com/gitleaks/gitleaks)), code linting and formatting ([`ruff`](https://docs.astral.sh/ruff/)), and notebook output stripping ([`nbstripout`](https://github.com/kynan/nbstripout)).

- **[GitHub Actions](workshops/github_actions.md)**

    Write [CI/CD workflows](https://docs.github.com/en/actions) that run automatically on GitHub. You will build a quality checks pipeline (`ruff` + `pytest`) and a documentation deployment workflow.

</div>

## Getting Started

Start with [Getting Started](getting_started.md) to fork the repository and set up your environment.
