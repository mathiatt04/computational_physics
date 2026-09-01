# Pushing this to GitHub

You have a folder that is already a git repository with one commit in it. Everything below
happens on your own machine. Nothing here asks you to share a password or token with anyone.

---

## 1. Install git (if you don't have it)

Open a terminal and run:

```bash
git --version
```

If that prints a version number, skip to step 2. If not:

- **Windows**: download from https://git-scm.com/download/win and accept the defaults.
- **macOS**: `git --version` will offer to install the developer tools. Accept.
- **Linux**: `sudo apt install git`

---

## 2. Download and unpack the folder

Download the `github-repo` folder from this conversation and put it somewhere sensible,
for example `Documents/computational-physics`. Then open a terminal **inside that folder**:

```bash
cd ~/Documents/computational-physics
git log --oneline
```

You should see one commit. If instead you get "not a git repository", the `.git` folder
did not survive the download — see the box at the bottom of this file.

---

## 3. Set your identity

The commit currently has my best guess at your name and email on it. Fix it:

```bash
git config user.name "Mathias Thorrud Thorkildsen"
git config user.email "your@email.com"
git commit --amend --reset-author --no-edit
```

Use whichever email you register on GitHub with. If you'd rather not have a personal
address in your public commit history, GitHub can give you a private no-reply address —
turn on "Keep my email address private" in Settings → Emails, and use the
`...@users.noreply.github.com` address it shows you.

---

## 4. Create the repository on GitHub

1. Sign in at https://github.com (create an account if you need one).
2. Click **+** in the top right → **New repository**.
3. Name it something a recruiter will understand: `computational-physics` works well.
4. Set it to **Public**.
5. **Do not** tick "Add a README", "Add .gitignore" or "Choose a license" —
   you already have all three, and ticking them creates a conflict you'd have to untangle.
6. Click **Create repository**.

GitHub then shows you a page with a URL like
`https://github.com/yourusername/computational-physics.git`. Keep that page open.

---

## 5. Connect and push

Back in your terminal, in the project folder:

```bash
git remote add origin https://github.com/yourusername/computational-physics.git
git push -u origin main
```

Replace `yourusername` with your actual username.

**On the authentication prompt:** git will ask for a username and password. Your GitHub
account password will *not* work here — GitHub stopped accepting it in 2021. Instead:

1. Go to https://github.com/settings/tokens
2. **Generate new token** → **Fine-grained token**
3. Give it a name, an expiry (90 days is fine), and under *Repository access* pick
   **Only select repositories** → your new repo
4. Under *Permissions* → *Repository permissions*, set **Contents** to **Read and write**
5. Generate it, and copy the token — it is shown once and never again
6. Paste the token when git asks for your **password**

The token is a password. Don't paste it into a chat, a document, or anywhere other than
your own terminal or password manager.

A gentler alternative if the token flow annoys you: install
[GitHub CLI](https://cli.github.com), run `gh auth login`, and it handles all of this
through your browser. After that, `git push` just works.

---

## 6. Check it

Refresh your repository page. You should see the folder structure, and the root README
rendered underneath with the table of the two projects. Click into `usadel-josephson`
and confirm the notebook renders with its figures — GitHub displays `.ipynb` files
natively, which is the whole reason this makes a good portfolio piece.

---

## 7. Making changes later

Once you re-run the Cahn–Hilliard notebook and fix the reports:

```bash
git add -A
git commit -m "Re-run Cahn-Hilliard notebook with spinodal decomposition results"
git push
```

That's the whole loop: `add`, `commit`, `push`.

---

## Before you tell anyone the URL

Work through `CLEANUP.md`. The three items at the top are blocking — coordinator's
permission, your co-author's agreement, and crediting them by name. Delete `CLEANUP.md`
once it's all done:

```bash
git rm CLEANUP.md
git commit -m "Remove pre-publication checklist"
git push
```

---

## Then put it on your CV

In the header of your CV, replace the placeholder:

```
github.com/[brukernavn]  →  github.com/yourusername
```

---

> **If the `.git` folder didn't survive the download**
>
> Some browsers and unzip tools silently drop hidden folders. If `git log` fails, run
> this inside the project folder to start fresh — you lose nothing except the commit
> message I wrote:
>
> ```bash
> git init -b main
> git add -A
> git commit -m "Add TMA4320 computational physics projects"
> ```
>
> Then carry on from step 4.
