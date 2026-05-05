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

You need the following installed on your device:

| Requirement | What it is | How to get it |
|---|---|---|
| **Python 3.8+** | Programming language the bot runs on | See device setup below |
| **pip** | Python package installer (comes with Python) | Included with Python |
| **Git** | Version control tool (for GitHub) | https://git-scm.com/downloads |
| **A crypto wallet** | MetaMask or any EVM wallet | https://metamask.io |
| **DAC testnet account** | Account on the DAC Inception site | https://inception.dachain.io |

---

## Getting Your Credentials

You need 3 values to fill in your `.env` file:

### 1. `PRIVATE_KEY` — Your wallet private key
> ⚠️ **NEVER share this with anyone. Use a fresh testnet-only wallet.**

- **MetaMask**: Click account icon → Account Details → Show Private Key → enter password → copy
- **Any EVM wallet**: Look for "Export Private Key" in settings

### 2. `WALLET_ADDRESS` — Your 0x wallet address
- This is your public wallet address starting with `0x`
- Visible on MetaMask home screen or any EVM wallet

### 3. `AUTH_TOKEN` — Your session token from the DAC website
This is the hardest one. Here's how to get it:

1. Open **https://inception.dachain.io** in Chrome or Firefox and **log in**
2. Press **F12** to open Developer Tools
3. Click the **Network** tab
4. Refresh the page or click anything on the site
5. Click any request that goes to the DAC API
6. Look at the **Headers** section → find `Authorization:`
7. Copy everything **after** `Bearer ` — that's your token

> 💡 Tokens expire. If the bot starts getting 401 errors, repeat these steps to get a fresh token and update your `.env` file.

---

## Setup — Windows

### Step 1: Install Python
1. Go to https://www.python.org/downloads/
2. Download the latest Python 3.x installer
3. Run it — **tick "Add Python to PATH"** before clicking Install
4. Open **Command Prompt** (search `cmd` in Start menu)
5. Verify: `python --version` — should show `Python 3.x.x`

### Step 2: Download the bot
```cmd
git clone https://github.com/YOUR_USERNAME/dac-inception-bot.git
cd dac-inception-bot
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
git clone https://github.com/YOUR_USERNAME/dac-inception-bot.git
cd dac-inception-bot
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
git clone https://github.com/YOUR_USERNAME/dac-inception-bot.git
cd dac-inception-bot
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

### Step 5: Run (keep alive on VPS with screen)
```bash
# Install screen so bot keeps running after you disconnect
sudo apt install screen -y

# Start a screen session
screen -S dacbot

# Run the bot
python3 dac_bot.py

# Detach from screen (bot keeps running): CTRL+A then D
# Re-attach later: screen -r dacbot
```

---

## Setup — Android (Termux)

Termux lets you run Python scripts directly on your Android phone — no PC needed.

### Step 1: Install Termux
- Download from **F-Droid** (recommended): https://f-droid.org/packages/com.termux/
- Or from Google Play: search "Termux"
- ⚠️ Do NOT use the old Play Store version — it's outdated. Use F-Droid.

### Step 2: Install required packages
Open Termux and run these one by one:
```bash
pkg update && pkg upgrade -y
pkg install python git -y
pip install --upgrade pip
```

### Step 3: Download the bot
```bash
git clone https://github.com/YOUR_USERNAME/dac-inception-bot.git
cd dac-inception-bot
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
- Use volume-down + E to go to end of line in nano
- Press `CTRL+X` → `Y` → Enter to save

### Step 6: Keep bot running when phone sleeps
```bash
# Install termux-wake-lock to prevent Android killing the process
termux-wake-lock

# Run the bot
python dac_bot.py
```

> 💡 **Tip for Android**: Go to your phone's battery settings → find Termux → set to "Unrestricted" or "Don't optimize" so Android doesn't kill it in the background.

---

## How to Run

Once set up, simply run:
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
4. Then sit in the background and repeat on schedule

**To stop the bot:** Press `CTRL+C`

---

## Upload to GitHub

### First time setup:

**1. Create a GitHub account** at https://github.com if you don't have one.

**2. Create a new repository:**
- Go to https://github.com/new
- Name it: `dac-inception-bot`
- Set to **Public** or **Private** (your choice)
- Do NOT tick "Add README" — you already have one
- Click **Create repository**

**3. Upload the bot from your computer:**
```bash
# Navigate into the bot folder
cd dac-inception-bot

# Initialize git (if not already done)
git init

# Add all files EXCEPT .env (it's in .gitignore already)
git add dac_bot.py requirements.txt README.md .env.example .gitignore

# Commit
git commit -m "Add DAC Inception testnet bot v3"

# Connect to your GitHub repo (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/dac-inception-bot.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**4. Done!** Visit `https://github.com/YOUR_USERNAME/dac-inception-bot` to see it live.

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
| Faucet | Via bot (every 8 hours) |

**Add to MetaMask manually:**
1. Open MetaMask → Networks → Add Network
2. Fill in the table above
3. Save — you're now on the DAC testnet

---

## Security Warning

> 🔴 **Read this before running.**

- **Never put your main wallet private key** in this bot. Create a fresh wallet just for this testnet.
- **Never commit your `.env` file to GitHub** — the `.gitignore` blocks it automatically, but double-check.
- **Your `AUTH_TOKEN` expires** — if API calls start failing with 401 errors, grab a fresh one from DevTools.
- This bot is for **testnet only** — no real funds are at risk if you use a fresh testnet wallet.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` again |
| `Web3 not connected` | Check your internet connection or try a different RPC URL |
| `401 Unauthorized` | Your `AUTH_TOKEN` expired — grab a fresh one from DevTools |
| `Insufficient DACC` | Wait for the faucet to give you DACC, or lower `TX_AMOUNT_WEI` |
| Bot stops randomly | On VPS use `screen`, on Android enable battery unrestricted for Termux |
| `JSONDecodeError` | The API returned an error page — check your `AUTH_TOKEN` |
| Termux: `pkg not found` | Run `pkg update` first then retry |
| Windows: `python not found` | Reinstall Python and tick "Add to PATH" |

---

## Disclaimer

This bot is for educational and personal use on a public testnet. No real funds are involved. Always DYOR (Do Your Own Research). The author is not responsible for any issues arising from use of this bot.
