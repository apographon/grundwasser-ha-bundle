# Git push setup for grundwasser-ha-bundle

Choose one method so `git push` works without interactive prompts.

---

## Option 1: GitHub CLI (recommended)

1. Install [GitHub CLI](https://cli.github.com/): `brew install gh` (macOS).
2. Log in (browser or token):
   ```bash
   gh auth login
   ```
   Select: GitHub.com → HTTPS → Yes (authenticate Git with GitHub credentials).
3. From the bundle folder, push:
   ```bash
   cd /Users/oli/HAss/grundwasser-bundle
   git push -u origin main
   ```
   GitHub CLI will use your login.

---

## Option 2: Personal Access Token (HTTPS)

1. Create a token: [GitHub → Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens).  
   Scope: **repo**.
2. Store it so Git can use it (run once):
   ```bash
   git config --global credential.helper store
   ```
   Then:
   ```bash
   cd /Users/oli/HAss/grundwasser-bundle
   git push -u origin main
   ```
   When prompted: **Username** = your GitHub username, **Password** = the token (not your GitHub password).
3. The credential is saved; future pushes won’t ask.

---

## Option 3: SSH key

1. Generate a key (if you don’t have one):
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com" -f ~/.ssh/id_ed25519_github -N ""
   ```
2. Add the public key to GitHub: [SSH keys](https://github.com/settings/keys) → New SSH key → paste contents of `~/.ssh/id_ed25519_github.pub`.
3. Use SSH for this repo and push:
   ```bash
   cd /Users/oli/HAss/grundwasser-bundle
   git remote set-url origin git@github.com:apographon/grundwasser-ha-bundle.git
   git push -u origin main
   ```
   If your key isn’t in the default name, configure SSH (e.g. in `~/.ssh/config`) so `github.com` uses that key.

---

## Check

After a successful push, open:  
https://github.com/apographon/grundwasser-ha-bundle

You should see the committed files (README, integration, scripts, ui, docs).
