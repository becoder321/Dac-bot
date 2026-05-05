# DAC Inception Testnet Bot 🤖⚡

> Automation bot for the [DAC Inception Quantum-Resistant Testnet](https://inception.dachain.io) — auto-farms Quantum Energy (QE), claims faucet tokens, opens crates, completes directives, and sends on-chain transactions 24/7.

---

## 📋 Table of Contents
- [What It Does](#what-it-does)
- [Requirements](#requirements)
- [Getting Your Credentials](#getting-your-credentials)
- [Setup — Windows](#setup--windows)
- [Setup — macOS](#setup--macos)
- [Setup — Linux / VPS](#setup--linux--vps)
- [Setup — Android (Termux)](#setup--android-termux)
- [How to Run](#how-to-run)
- [Upload to GitHub](#upload-to-github)
- [Network Info](#network-info)
- [Security Warning](#security-warning)
- [Troubleshooting](#troubleshooting)

---

## What It Does

| Feature | Details |
|---|---|
| 🚰 Auto Faucet | Claims 1 DACC every 8 hours automatically |
| 📦 Quantum Crates | Opens all 5 daily crates (DACC + QE + multipliers) |
| 📋 Directives | Completes all available daily tasks |
| 🏅 Badges | Claims any eligible badges automatically |
| 📤 On-chain TX | Sends self-transactions to earn on-chain activity QE |
| 📊 Stats | Logs your QE balance and leaderboard rank |
| 🔄 24/7 Scheduler | Runs daily at 09:00 UTC + faucet every 8 hours |

---

## Requirements

| Requirement | What it is | How to get it |
|---|---|---|
| **Python 3.8+** | Language the bot runs on | See device setup below |
| **pip** | Python package installer | Included with Python |
| **Git** | Version control tool | https://git-scm.com/downloads |
| **A crypto wallet** | MetaMask or any EVM wallet | https://metamask.io |
| **DAC testnet account** | Account on the DAC Inception site | https://inception.dachain.io |

---

## Getting Your Credentials

You need 3 values for your `.env` file:

### 1. `PRIVATE_KEY` — Your wallet private key
> ⚠️ **NEVER share this with anyone. Use a fresh testnet-only wallet.**

- **MetaMask**: Click account icon → Account Details → Show Private Key → enter password → copy

### 2. `WALLET_ADDRESS` — Your 0x wallet address
- Your public address starting with `0x`
- Visible on the MetaMask home screen

### 3. `AUTH_TOKEN` — Your session token from the DAC website
1. Open **https://inception.dachain.io** and log in
2. Press **F12** to open Developer Tools
3. Click the **Network** tab
4. Refresh the page
5. Click any API request → find the **Authorization** header
6. Copy everything **after** `Bearer ` — that is your token

> 💡 Tokens expire. If the bot gets 401 errors, grab a fresh token and update your `.env`.

---

## Setup — Windows

### Step 1: Install Python
1. Go to https://www.python.org/downloads/
2. Download the latest Python 3.x installer
3. Run it — **tick "Add Python to PATH"** before clicking Install
4. Open **Command Prompt** (search `cmd` in Start menu)
5. Verify: `python --version`

### Step 2: Download the bot
```cmd
git clone https://github.com/becoder321/Dac-bot.git
cd Dac-bot
```

### Step 3: Install dependencies
```cmd
pip install -r requirements.txt
```

### Step 4: Configure your .env
```cmd
copy .env.example .env
notepad .env
```
Fill in your `PRIVATE_KEY`, `WALLET_ADDRESS`, and `AUTH_TOKEN`, then save.

> 💡 **Cannot see the .env file?** It starts with a dot so Windows hides it by default.
> Open File Explorer → View → tick **Show hidden items** to make it visible.
> When renaming `.env.example` to `.env`, click **Yes** if Windows warns about changing the extension.

### Step 5: Run
```cmd
python dac_bot.py
```

---

## Setup — macOS

### Step 1: Install Python
```bash
# Install Homebrew first (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Then install Python
brew install python
```

### Step 2: Download the bot
```bash
git clone https://github.com/becoder321/Dac-bot.git
cd Dac-bot
```

### Step 3: Install dependencies
```bash
pip3 install -r requirements.txt
```

### Step 4: Configure your .env
```bash
cp .env.example .env
nano .env
```
Fill in your credentials. Press `CTRL+X` → `Y` → Enter to save.

> 💡 **Cannot see the .env file in Finder?** Press `CMD + SHIFT + .` to toggle hidden files.
> Files starting with a dot are hidden by default on macOS.

### Step 5: Run
```bash
python3 dac_bot.py
```

---

## Setup — Linux / VPS

### Step 1: Install Python & Git
```bash
# Ubuntu / Debian
sudo apt update && sudo apt install python3 python3-pip git -y

# CentOS / Fedora
sudo yum install python3 python3-pip git -y
```

### Step 2: Download the bot
```bash
git clone https://github.com/becoder321/Dac-bot.git
cd Dac-bot
```

### Step 3: Install dependencies
```bash
pip3 install -r requirements.txt
```

### Step 4: Configure your .env
```bash
cp .env.example .env
nano .env
```
Fill in your credentials. Press `CTRL+X` → `Y` → Enter to save.

> 💡 **Cannot see the .env file?** Run `ls -a` in the terminal to show hidden files (those starting with a dot).

### Step 5: Run (keep alive on VPS with screen)
```bash
# Install screen so bot keeps running after you disconnect
sudo apt install screen -y

# Start a screen session
screen -S dacbot

# Run the bot
python3 dac_bot.py

# Detach (bot keeps running in background): CTRL+A then D
# Re-attach later:
screen -r dacbot
```

---

## Setup — Android (Termux)

Termux lets you run the bot directly on your Android phone — no PC needed.

### Step 1: Install Termux
- Download from **F-Droid** (recommended): https://f-droid.org/packages/com.termux/
- ⚠️ Do NOT use the old Play Store version — it is outdated. Use F-Droid.

### Step 2: Install required packages
```bash
pkg update && pkg upgrade -y
pkg install python git -y
pip install --upgrade pip
```

### Step 3: Download the bot
```bash
git clone https://github.com/becoder321/Dac-bot.git
cd Dac-bot
```

### Step 4: Install Python dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Configure your .env
```bash
cp .env.example .env
nano .env
```
Fill in your `PRIVATE_KEY`, `WALLET_ADDRESS`, and `AUTH_TOKEN`.
Press `CTRL+X` → `Y` → Enter to save.

> 💡 **Cannot see the .env file?** Run `ls -a` to list all files including hidden ones.
> On Android, files starting with a dot are hidden in most file manager apps — use the terminal to access them.

### Step 6: Keep bot running when phone sleeps
```bash
# Prevent Android from killing the process
termux-wake-lock

# Run the bot
python dac_bot.py
```

> 💡 Go to phone Settings → Battery → find Termux → set to **Unrestricted** or **Don't optimize** so Android does not kill it in the background.

---

## How to Run

```bash
# Windows
python dac_bot.py

# macOS / Linux / Termux
python3 dac_bot.py
```

The bot will:
1. Connect to the DAC testnet RPC
2. Show your current QE stats
3. Claim faucet, open crates, complete directives, claim badges, send TX
4. Sit in the background and repeat on schedule

**To stop the bot:** Press `CTRL+C`

---

## Upload to GitHub

### First time setup:

**1.** Create a GitHub account at https://github.com if you do not have one.

**2.** Create a new repository:
- Go to https://github.com/new
- Name it: `Dac-bot`
- Do NOT tick "Add README" — you already have one
- Click **Create repository**

**3.** Upload from your computer:
```bash
cd Dac-bot
git init
git add dac_bot.py requirements.txt README.md .env.example .gitignore
git commit -m "Add DAC Inception testnet bot v3"
git remote add origin https://github.com/becoder321/Dac-bot.git
git branch -M main
git push -u origin main
```

**4.** Visit https://github.com/becoder321/Dac-bot to see it live.

### Updating the bot later:
```bash
git add .
git commit -m "Update bot"
git push
```

---

## Network Info

| Setting | Value |
|---|---|
| Network Name | DAC Inception Testnet |
| RPC URL | https://rpc-test.dachain.tech |
| Chain ID | 7776 |
| Explorer | https://exptest.dachain.tech |

**Add to MetaMask:**
1. Open MetaMask → Networks → Add Network
2. Fill in the table above
3. Save

---

## Security Warning

> 🔴 **Read this before running.**

- **Never use your main wallet** — create a fresh wallet just for this testnet
- **Never commit your `.env` file** — the `.gitignore` blocks it automatically
- **Your `AUTH_TOKEN` expires** — grab a fresh one from DevTools if you get 401 errors
- This bot is for **testnet only** — no real funds at risk if you use a fresh wallet

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` again |
| `Web3 not connected` | Check internet or try a different RPC URL |
| `401 Unauthorized` | AUTH_TOKEN expired — grab a fresh one from DevTools |
| `Insufficient DACC` | Wait for faucet or lower `TX_AMOUNT_WEI` in the bot |
| Cannot see `.env` file | Windows: View → Show hidden items / macOS: CMD+SHIFT+. / Linux & Termux: run `ls -a` |
| Bot stops randomly | VPS: use `screen` / Android: set Termux battery to Unrestricted |
| `JSONDecodeError` | API returned an error page — check your AUTH_TOKEN |
| Termux: `pkg not found` | Run `pkg update` first then retry |
| Windows: `python not found` | Reinstall Python and tick "Add to PATH" |

---

## Disclaimer

This bot is for educational and personal use on a public testnet. No real funds are involved. Always DYOR. The author is not responsible for any issues arising from use of this bot.
