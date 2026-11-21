# Set up DecoderLab on a Mac (one time)

This guide does not itself create a local folder. Run the commands below on **your own Mac**.

## 1. Clone the real repository into a visible folder
Install Git if missing (macOS may prompt you to install Command Line Tools). Open Terminal:

```bash
mkdir -p ~/Projects
cd ~/Projects
git clone https://github.com/Naveen-das09/decoderlab.git
cd decoderlab
git fetch origin
git branch -a
```

Now Finder > Go > Go to Folder > `~/Projects/decoderlab`. This is the real project directory, continuously synced through Git. GitHub stores code, not your personal Mac folders.

**Until draft PR #1 is merged**, the backend resides on `feat/initial-backend-baseline`, not on `main`. To examine the backend locally:

```bash
git switch --track origin/feat/initial-backend-baseline
```

If Git says the branch already exists, use `git switch feat/initial-backend-baseline`. Do not run `git pull` blindly while Codex has uncommitted changes. Once PR #1 is merged, switch to `main`, fetch and fast-forward.

## 2. Open the folder in the desktop app
In ChatGPT/Codex on Mac, choose **open folder / add local project**, select `~/Projects/decoderlab`, and work in local mode. You do **not** create a second GitHub repository inside Codex. Codex operates on the files Git has cloned.

If this project doesn't appear in Codex, verify the folder exists in Finder, then add it explicitly. ChatGPT cannot inspect your Mac's folders until you authorize the app/project.

## 3. Run initial backend checks
Use Python 3.11+ and create an isolated environment in the repository's backend directory:

```bash
cd ~/Projects/decoderlab/backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[test,simulation]'
python -m pytest -q
```

This requires the feature branch from PR #1 or a merged backend. The optional `simulation` extras use Stim and PyMatching, so run the true integration tests explicitly before claiming scientific validation.

## 4. Make daily local work happen
Open the **Scheduled** view in the desktop app. Choose the existing DecoderLab task and attach the local folder/worktree if available, or create a local Codex task using the prompt in `automation/DAILY_SPRINT_PROMPT.md`. Choose an isolated worktree and around 08:00 **Asia/Kolkata**. Avoid running two independent agents against the same branch.

The Mac must be powered on, awake and the app running at the scheduled time. Keep automatic approvals limited to the repository workspace. Do not use full-access sandboxing or an API key for this workflow.

## 5. Inspect and ask questions
- In Finder, open `~/Projects/decoderlab` to see every file.
- In Codex, ask: “Explain the experiment API and how a logical failure is counted, citing specific files.”
- In GitHub, inspect draft PRs, CI results, code reviews and issues.
- In ChatGPT, ask for design reviews or QEC scientific review; the canonical requirements live in this repository.

## Troubleshooting
- `git: command not found`: install Apple's Command Line Tools using the system prompt.
- `repository not found`: check GitHub sign-in and link.
- `backend: No such file or directory`: you are still on minimal `main`; fetch and switch to the PR #1 feature branch.
- Missing `codex` terminal command does not prevent using Codex from the desktop app.
- No project in Scheduled: attach the folder in the app; the web GitHub connection alone cannot choose a local directory.

Reference: https://learn.chatgpt.com/docs/automations?surface=app