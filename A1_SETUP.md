# A1_SETUP — One-Time Workstation Setup Runbook

**Goal:** Bring a fresh Windows machine to the state where `python code/utils/verify_a1.py` exits 0.

**Time budget:** 2–4 hours including downloads.

**Read every step before running anything.** Do not skip the verification commands at the end of each section.

---

## Step 0 — Prerequisites Check

You need:
- Windows 10 version 2004+ or Windows 11 (run `winver` to check)
- Administrator access on the machine
- ~30 GB free disk space (WSL2 + conda + data buffers)
- A GitHub account with an SSH key configured (`ssh -T git@github.com` should authenticate)
- A Google account for GEE
- (Later) A Copernicus CDS account for ERA5 acquisition

---

## Step 1 — Install WSL2 + Ubuntu 24.04

Open **PowerShell as Administrator** and run:

```powershell
wsl --install -d Ubuntu-24.04
```

Reboot when prompted. On reboot Ubuntu will finish installing and ask for a UNIX username + password. Pick something memorable; you will use this every time you `sudo` inside WSL2.

**Verify:**
```powershell
wsl --list --verbose
```
Expected output: Ubuntu-24.04 running on VERSION 2. If VERSION shows 1, run `wsl --set-version Ubuntu-24.04 2`.

**Enable Windows long-path support** (one-time, prevents file-write errors on deep CMIP6 paths). Run in **elevated PowerShell**:
```powershell
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" `
  -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

---

## Step 2 — Update Ubuntu and install base toolchain

From now on, all commands run **inside the WSL2 Ubuntu shell** unless explicitly marked PowerShell.

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential git curl wget unzip make ca-certificates \
  software-properties-common gnupg2
```

**Configure Git identity (do this once):**
```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
git config --global pull.rebase false
git config --global core.autocrlf input   # keep LF endings in repo
```

**Verify:**
```bash
git --version  # expect 2.40+
```

---

## Step 3 — Install miniforge (conda + mamba)

Inside the WSL2 home directory:

```bash
cd ~
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
bash Miniforge3-Linux-x86_64.sh -b -p $HOME/miniforge3
$HOME/miniforge3/bin/conda init bash
exec bash   # reload shell
```

**Verify:**
```bash
conda --version  # expect 24.x or newer
mamba --version  # mamba ships with miniforge
```

---

## Step 4 — Clone the repository

The repo MUST live inside the WSL2 filesystem (`~/`), NOT in `/mnt/c/Users/...`. Cross-filesystem I/O on WSL2 is roughly 10× slower than native ext4.

```bash
mkdir -p ~/code && cd ~/code
git clone git@github.com:YOUR-USERNAME/thesis-rp-migration.git
cd thesis-rp-migration
```

If you have not yet created the GitHub repo, do that first via the GitHub web UI (Public, no README/license/gitignore — we ship our own), then clone.

---

## Step 5 — Build the conda environment

```bash
cd ~/code/thesis-rp-migration
mamba env create -f environment.yml
conda activate thesis-rp
```

This takes 10–20 minutes depending on network. **If it fails on a specific package**, note which one and report it for an `environment.yml` patch — do not paper over it with ad-hoc `pip install`.

**Verify:**
```bash
conda env list      # 'thesis-rp' should be marked active
python --version    # expect 3.11.x
which python        # expect ~/miniforge3/envs/thesis-rp/bin/python
```

**Install the pip-pinned layer inside the conda env:**
```bash
pip install -r requirements.txt
```

**Install the repo as an editable local package** (so `from utils.paths import ...` works without `sys.path` hacks):
```bash
pip install -e .
```

---

## Step 6 — Configure the `.env` file

```bash
cp .env.example .env
nano .env   # or your editor of choice
```

Fill in:
- `DATA_ROOT` — absolute path inside WSL2 where bulky data will live (NOT in the repo). Example: `/home/YOUR_USER/thesis-data`. Create the directory: `mkdir -p ~/thesis-data`
- `BWDB_PATH` — path to the BWDB SW46.9L Excel file once you place it under `$DATA_ROOT/observed/`
- `BMD_PATH` — path to the BMD daily rainfall raw archive
- `GEE_PROJECT_ID` — your GEE-enabled Google Cloud project ID (created at <https://console.cloud.google.com/earth-engine>)
- `CDS_API_UID` and `CDS_API_KEY` — from <https://cds.climate.copernicus.eu/user> (needed for ERA5 acquisition in Chain B.0b; can defer until Day 4)

**Verify:**
```bash
test -f .env && echo ".env present" || echo "MISSING"
```

The `.env` file is gitignored. Never commit it.

---

## Step 7 — Authenticate Google Earth Engine

GEE personal-account auth is interactive. Inside WSL2:

```bash
earthengine authenticate
```

Follow the printed URL in a Windows browser, paste the auth code back into the WSL2 terminal. This stores credentials at `~/.config/earthengine/credentials`.

**Verify:**
```bash
python -c "import ee; ee.Initialize(project='YOUR-GEE-PROJECT-ID'); print('GEE OK:', ee.Image('USGS/SRTMGL1_003').bandNames().getInfo())"
```

Expected: prints `GEE OK: ['elevation']`. If it fails, check that GEE access has been granted to your Google account at <https://earthengine.google.com>.

---

## Step 8 — Link the GitHub remote

If you cloned in Step 4 the remote is already set. Verify:

```bash
git remote -v
```

Expected: `origin git@github.com:YOUR-USERNAME/thesis-rp-migration.git (fetch)` and `(push)`.

---

## Step 9 — Install pre-commit hooks

```bash
pre-commit install
```

This wires `.pre-commit-config.yaml` into `.git/hooks/pre-commit`. From now on, every `git commit` will run black + isort + nbstripout. Commits that introduce formatting violations or notebooks with cell outputs will be rejected.

**Test:**
```bash
pre-commit run --all-files
```

The first run will reformat any files that need it. Stage and commit the changes.

---

## Step 10 — Run the A.1 acceptance gate

This is the gate. A.1 has not passed until this exits 0.

```bash
python code/utils/verify_a1.py
```

Expected output: a banner, a checklist with all green ✓, and exit code 0. If anything is red, fix it before declaring A.1 done.

```bash
echo $?   # must print 0
```

You can also run `make verify` as a convenience.

---

## Step 11 — Initial commit and tag

If the repo skeleton was placed manually rather than cloned, do the initial commit now:

```bash
git add .
git commit -m "A.1: repo + environment skeleton (v0.1.0-alpha)"
git tag v0.1.0-alpha
git push origin main --tags
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `wsl --install` says "feature not enabled" | Hyper-V/VM Platform missing | Run `dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart` in elevated PowerShell, reboot |
| `mamba env create` hangs on solving | conda-forge channel slow | Re-run; if it persists, refresh with `mamba install -n base -c conda-forge mamba` |
| `pip install -e .` says "no setup.py" | Older pip | `pip install --upgrade pip` then retry |
| GEE auth opens Edge but URL is malformed | Browser/WSL handoff issue | Copy the URL printed in terminal, paste manually into the browser |
| `pre-commit` fails with `black: error: cannot parse` | Mid-file syntax error | Fix the Python error first; pre-commit cannot reformat broken code |
| File-write errors on long CMIP6 paths | Windows MAX_PATH | Confirm `LongPathsEnabled` registry value, restart WSL: `wsl --shutdown` then reopen |
| Slow file I/O on data | Repo or data dir on `/mnt/c/` | Move to native `~/` (WSL2 ext4) — required, not optional |

---

## Done

A.1 is complete when:
- ✓ `python code/utils/verify_a1.py` exits 0
- ✓ `git push` to GitHub succeeds
- ✓ A `v0.1.0-alpha` tag exists on the remote
- ✓ Pre-commit hooks installed and `pre-commit run --all-files` is clean

Move to A.2 (BWDB Q/H QC + AMS extraction) in a new session.
