# Getting Started

Before starting the workshop activities, you need to get your environment set up. This should take about 10 minutes.

!!! success "By the end of this page you will have"
    - [ ] Forked this repository to your own GitHub account
    - [ ] Opened it in GitHub Codespaces (or cloned it locally)
    - [ ] Verified that `uv` and the project dependencies are installed
    - [ ] Confirmed the MkDocs site serves correctly

---

## Step 1: Fork the Repository

1. Navigate to the [Git and GitHub CI/CD Workshop repository](https://github.com/nhsengland/git-and-github-cicd-workshop).
2. Click the **Fork** button in the top-right corner.
3. Click **Create fork** to confirm.

!!! info "Why fork?"
    Forking creates your own copy of the repository under your GitHub account. This means you can push commits, trigger GitHub Actions, and publish GitHub Pages — all without affecting the original repository.

---

## Step 2: Open in GitHub Codespaces

1. In your forked repository, click the green **Code** button.
2. Select the **Codespaces** tab.
3. Click **Create codespace on main**.

The Codespace will take a minute or two to start. It automatically runs `uv sync --all-groups` to install all project dependencies, including the `dev` and `docs` groups.

!!! tip "Working locally instead?"
    If you prefer to work on your own machine rather than [Codespaces](https://docs.github.com/en/codespaces), clone your fork and run:

    ```bash
    # Install uv if you do not already have it
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # Install all project dependencies
    uv sync --all-groups
    ```

    See the [uv documentation](https://docs.astral.sh/uv/) for alternative installation methods.

---

## Step 3: Verify the Environment

Once the Codespace is ready, open a terminal (**Terminal → New Terminal**) and check everything is installed:

```bash
uv run python --version
uv run pytest --version
uv run ruff --version
```

You should see version numbers printed for each. If any command fails, run `uv sync --all-groups` to reinstall.

---

## Step 4: Serve the Workshop Site

Start a live preview of this documentation site:

```bash
uv run mkdocs serve --livereload
```

Once running, a notification will appear in VS Code / Codespaces offering to open the forwarded port. Click it to open the site in your browser.

!!! tip "Live reload"
    The server watches your `docs/` folder for changes. Every time you save a Markdown file, the browser tab refreshes automatically — no manual reload needed. Try it: edit a line in any `.md` file, save, and watch the browser update within a second or two.

!!! info "Stopping the server"
    Press `Ctrl + C` in the terminal to stop the MkDocs server.

---

## You're Ready

Head to the [workshops section](./workshops/index.md) and pick your activity.
