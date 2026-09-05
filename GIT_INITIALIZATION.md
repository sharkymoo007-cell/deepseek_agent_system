# Git Initialization Guide

This document explains how to initialize a new Git repository from scratch,
configure your identity, and make your first commit.

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Check Git Installation](#2-check-git-installation)
3. [Configure Your Identity (one time)](#3-configure-your-identity-one-time)
4. [Initialize a Repository](#4-initialize-a-repository)
5. [Add a .gitignore](#5-add-a-gitignore)
6. [Create/Add a Remote (Optional)](#6-createadd-a-remote-optional)
7. [Make Your First Commit](#7-make-your-first-commit)
8. [Verify the Repository State](#8-verify-the-repository-state)
9. [Troubleshooting](#9-troubleshooting)
10. [Cheat Sheet](#10-cheat-sheet)

---

## 1. Prerequisites

- Git installed on your machine (see next section).
- A terminal / command prompt.
- (Optional) A hosting service account, e.g. GitHub, GitLab, or Bitbucket.

---

## 2. Check Git Installation

Verify that Git is installed and check the version:

```bash
git --version
```

Example output:

```
git version 2.43.0
```

> If the command is not recognized, install Git first:
> - **Windows:** https://git-scm.com/download/win (or via `winget install Git.Git`)
> - **macOS:** `brew install git`
> - **Linux (Debian/Ubuntu):** `sudo apt install git`

---

## 3. Configure Your Identity (one time)

Git stamps every commit with an author name and email. Set them globally (applies
to all repositories on your machine):

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

To set values only for the current repository, omit `--global`:

```bash
git config user.name "Your Name"
git config user.email "you@example.com"
```

Verify your configuration:

```bash
git config --list
```

---

## 4. Initialize a Repository

### Option A – Start in a new project directory

```bash
mkdir my-project
cd my-project
git init
```

### Option B – Initialize in the current directory

```bash
cd path/to/your/project
git init
```

`git init` creates a hidden `.git` folder that stores all version history. You can
confirm it exists:

```bash
ls -a        # macOS / Linux
dir /a       # Windows
```

### Start from a specific branch name (optional)

```bash
git init -b main
```

> Initializing with a default branch of `main` (instead of `master`) is now common
> practice.

---

## 5. Add a .gitignore

Before your first commit, add a `.gitignore` file to tell Git which files and
folders should **never** be tracked. This keeps your repository clean and prevents
accidentally committing secrets or junk.

### Why it matters

- OS junk (`.DS_Store`, `Thumbs.db`), editor files, logs, and build output clutter
  the history and diffs.
- Credentials / environment files (`.env`, keys) must **never** be committed.

### Create a `.gitignore`

A starter `.gitignore` for a docs/universal project is provided in this repo.
Create a custom one for your project type:

```bash
# Example for a Node.js project
echo "node_modules/" > .gitignore
echo ".env" >> .gitignore
```

Or write it in your editor. You can use a generator for a full template:
https://www.toptal.com/developers/gitignore  (or `npx gitignore node`)

### Verify it works

```bash
# Create a file that should be ignored, then check status
touch .DS_Store
git status
# .DS_Store should NOT appear in the list of untracked files
```

### Important notes

- A `.gitignore` **only affects untracked files**. If a file was already committed,
  add it with `git rm --cached <file>` to untrack it (keeps the local copy):
  ```bash
  git rm --cached .env
  ```
- A `#` starts a comment; `!` re-includes a previously excluded pattern.
- Rule order matters: later patterns override earlier ones.

---

## 6. Create/Add a Remote (Optional)

If you plan to push to GitHub, GitLab, etc., link your local repo to a remote one.

First create an empty repository on your hosting service, then:

```bash
git remote add origin https://github.com/<username>/<repository>.git
```

Check the configured remotes:

```bash
git remote -v
```

---

## 7. Make Your First Commit

### a) Stage files

Add all files:

```bash
git add .
```

Or add specific files:

```bash
git add README.md index.html
```

### b) Commit

```bash
git commit -m "Initial commit"
```

### c) (Optional) Push to the remote

```bash
git branch -M main                    # rename current branch to main
git push -u origin main               # push and set upstream tracking
```

---

## 8. Verify the Repository State

Useful commands to confirm everything worked:

```bash
git status                 # current state of the working tree
git log --oneline          # commit history (one line per commit)
git branch -a              # list all branches
```

---

## 9. Troubleshooting

| Issue                                        | Fix                                                            |
| -------------------------------------------- | -------------------------------------------------------------- |
| `git commit` asks for identity              | Run `git config --global user.email` / `user.name` (Section 3) |
| Commit opens a text editor unexpectedly      | `git commit -m "message"` supplies the message inline          |
| `fatal: not a git repository`                | Run `git init` first                                           |
| Wrong default branch name                    | `git branch -M main` then push                                 |
| Want to undo the init (remove history)       | Delete the `.git` directory                                    |
| Push rejected (remote has commits)           | `git pull --rebase origin main` then push again                |
| `.gitignore` isn't ignoring an added file    | It was already tracked — run `git rm --cached <file>`          |
| Need a full `.gitignore` template            | Use https://www.toptal.com/developers/gitignore                |

---

## 10. Cheat Sheet

```bash
git --version                       # check install
git config --global user.name "..." # set name
git config --global user.email ...  # set email
git init                            # start a repo
git init -b main                    # start a repo with main branch
git add .                           # stage all changes
git status                          # view working tree state
git commit -m "message"             # commit staged changes
git remote add origin <url>         # add remote
git remote -v                       # list remotes
git push -u origin main             # push first time
git log --oneline                   # view history
git rm --cached <file>              # untrack a file already committed
```

---

*Generated on request to document the Git initialization process.*
