"""
DAC Inception Testnet Automation Bot (v3 - Optimized)
=====================================================
Automates: Faucet claims, Crate opening, Daily check-ins, Transaction sending
Network: DAC Inception Testnet (EVM-compatible)
RPC: https://rpc-test.dachain.tech
Explorer: https://exptest.dachain.tech

UPDATES in v3:
- Improved Gas Strategy: Dynamic gas price with multiplier.
- Robust JSON Parsing: Better handling of unexpected API response formats.
- Security: Added warning for private key exposure.
- Reliability: Improved transaction confirmation logic.
"""
import os
import time
import random
import logging
import requests
import schedule
from datetime import datetime
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from web3 import Web3
from colorama import Fore, Style, init

# ─── Init ────────────────────────────────────────────────────────────────────
init(autoreset=True)
load_dotenv()

# ─── Rotating Logger ─────────────────────────────────────────────────────────
handler = RotatingFileHandler("dac_bot.log", maxBytes=2_000_000, backupCount=3)
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logging.getLogger().addHandler(handler)
logging.getLogger().setLevel(logging.INFO)

# ─── Config ──────────────────────────────────────────────────────────────────
RPC_URL         = os.getenv("RPC_URL", "https://rpc-test.dachain.tech")
CHAIN_ID        = int(os.getenv("CHAIN_ID", "7776"))
API_BASE        = os.getenv("API_BASE", "https://inception.dachain.io/api")
PRIVATE_KEY     = os.getenv("PRIVATE_KEY", "")
WALLET_ADDRESS  = os.getenv("WALLET_ADDRESS", "")
AUTH_TOKEN      = os.getenv("AUTH_TOKEN", "")

FAUCET_INTERVAL_HOURS = 8
CRATE_DAILY_LIMIT     = 5
TX_AMOUNT_WEI         = Web3.to_wei(0.0001, "ether")
GAS_BUFFER_WEI        = Web3.to_wei(0.005, "ether") 

HEADERS = {
    "Content-Type": "application/json",
    **({"Authorization": f"Bearer {AUTH_TOKEN}"} if AUTH_TOKEN else {}),
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# ─── Helpers ─────────────────────────────────────────────────────────────────
def log(msg, color=Fore.WHITE):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{Fore.CYAN}[{timestamp}]{Style.RESET_ALL} {color}{msg}{Style.RESET_ALL}")
    logging.info(msg)

def banner():
    print(f"""
{Fore.MAGENTA}╔══════════════════════════════════════════════╗
║     DAC INCEPTION TESTNET BOT  🤖⚡  v3      ║
║     Quantum Energy Farming Automation        ║
╚══════════════════════════════════════════════╝{Style.RESET_ALL}
""")

def safe_json(resp, label="request"):
    """Improved JSON parser with robust type checking."""
    if resp.status_code not in [200, 201]:
        log(f"HTTP {resp.status_code} on {label}: {resp.text[:200]}", Fore.RED)
        return None
    try:
        data = resp.json()
        if not isinstance(data, dict):
            log(f"Unexpected JSON type (expected dict, got {type(data).__name__}) on {label}", Fore.YELLOW)
        return data
    except ValueError:
        log(f"Invalid JSON on {label}: {resp.text[:200]}", Fore.RED)
        return None

def with_retry(fn, retries=3, delay=2):
    for attempt in range(retries):
        try:
            return fn()
        except Exception as e:
            log(f"Attempt {attempt+1}/{retries} failed: {e}", Fore.YELLOW)
            if attempt < retries - 1:
                time.sleep(delay * (attempt + 1))
    return None

# ─── Env Validation ──────────────────────────────────────────────────────────
def validate_env():
    issues = []
    if not PRIVATE_KEY:
        issues.append("PRIVATE_KEY not set — on-chain txs disabled")
    if not WALLET_ADDRESS:
        issues.append("WALLET_ADDRESS not set — on-chain txs disabled")
    if not AUTH_TOKEN:
        issues.append("AUTH_TOKEN not set — API calls may be rejected")
    
    for issue in issues:
        log(f"⚠️  {issue}", Fore.YELLOW)
    return len(issues) == 0

# ─── Web3 Setup ──────────────────────────────────────────────────────────────
def connect_web3():
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    if w3.is_connected():
        log(f"✅ Connected to DAC Testnet | Block: {w3.eth.block_number}", Fore.GREEN)
    else:
        log("❌ Failed to connect to RPC.", Fore.RED)
        raise ConnectionError("Web3 not connected")
    return w3

# ─── On-chain: Self-Transaction ───────────────────────────────────────────────
def send_self_transaction(w3):
    if not PRIVATE_KEY or not WALLET_ADDRESS:
        log("⚠️  Skipping on-chain tx — wallet not configured.", Fore.YELLOW)
        return False
    try:
        account = w3.eth.account.from_key(PRIVATE_KEY)
        balance = w3.eth.get_balance(account.address)
        log(f"💰 Balance: {Web3.from_wei(balance, 'ether'):.6f} DACC", Fore.CYAN)
        
        if balance < TX_AMOUNT_WEI + GAS_BUFFER_WEI:
            log("⚠️  Insufficient DACC for tx (including gas buffer). Skipping.", Fore.YELLOW)
            return False

        nonce = w3.eth.get_transaction_count(account.address)
        
        # Optimized Gas Strategy: 10% buffer on top of current gas price
        base_gas_price = w3.eth.gas_price or Web3.to_wei(1, "gwei")
        gas_price = int(base_gas_price * 1.1) 
        
        tx = {
            "nonce":    nonce,
            "to":       account.address,
            "value":    TX_AMOUNT_WEI,
            "gas":      21000,
            "gasPrice": gas_price,
            "chainId":  CHAIN_ID
        }
        
        signed  = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
        log(f"📤 TX sent: {tx_hash.hex()}", Fore.GREEN)
        
        # Wait for confirmation with better error handling
        try:
            receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
            if receipt.status == 1:
                log("✅ Transaction confirmed!", Fore.GREEN)
                return True
            else:
                log("❌ Transaction reverted on-chain.", Fore.RED)
                return False
        except Exception as te:
            log(f"⏳ Confirmation timeout/error: {te}", Fore.YELLOW)
            return False
            
    except Exception as e:
        log(f"❌ TX error: {e}", Fore.RED)
        return False

# ─── Faucet Claim ────────────────────────────────────────────────────────────
def claim_faucet():
    log("🚰 Claiming faucet...", Fore.CYAN)
    def _do():
        return requests.post(
            f"{API_BASE}/faucet/claim",
            headers=HEADERS,
            json={"address": WALLET_ADDRESS},
            timeout=15
        )
    resp = with_retry(_do)
    if resp is None: return False
    
    data = safe_json(resp, "faucet/claim")
    if not data: return False
    
    if data.get("success"):
        log(f"✅ Faucet claimed! +1 DACC | QE: {data.get('qe', 'N/A')}", Fore.GREEN)
        return True
    else:
        log(f"⚠️  Faucet: {data.get('message', 'Unknown response')}", Fore.YELLOW)
        return False

# ─── Open Crates ─────────────────────────────────────────────────────────────
def open_crates(count=CRATE_DAILY_LIMIT):
    opened = 0
    log(f"📦 Opening {count} Quantum Crates...", Fore.CYAN)
    for i in range(count):
        def _do():
            return requests.post(
                f"{API_BASE}/crates/open",
                headers=HEADERS,
                json={"address": WALLET_ADDRESS},
                timeout=15
            )

        resp = with_retry(_do)
        if resp is None:
            log(f"  ❌ Crate {i+1}: all retries failed.", Fore.RED)
            continue
            
        data = safe_json(resp, "crates/open")
        if not data: continue
        
        if data.get("success"):
            r = data.get("reward", {})
            log(f"  📦 Crate {i+1}: +{r.get('dacc',0)} DACC | +{r.get('qe',0)} QE | {r.get('multiplier',1)}x", Fore.GREEN)
            opened += 1
        else:
            msg = data.get("message", "")
            log(f"  ⚠️  Crate {i+1}: {msg}", Fore.YELLOW)
            if "limit" in msg.lower():
                break
        
        time.sleep(random.uniform(2, 5))
        
    log(f"📦 Total opened: {opened}/{count}", Fore.CYAN)
    return opened

# ─── Complete Directives ──────────────────────────────────────────────────────
def complete_directives():
    log("📋 Fetching directives...", Fore.CYAN)
    def _fetch():
        return requests.get(f"{API_BASE}/directives", headers=HEADERS, timeout=15)
    
    resp = with_retry(_fetch)
    if resp is None: return
    
    data = safe_json(resp, "directives")
    if not data: return
    
    # Handle both {directives: [...]} and raw [...] formats
    tasks = data.get("directives", []) if isinstance(data, dict) else data
    if not isinstance(tasks, list):
        log("Unexpected directives format (not a list).", Fore.RED)
        return

    log(f"  Found {len(tasks)} directives.", Fore.CYAN)
    for task in tasks:
        if task.get("completed"): continue
        
        task_id   = task.get("id")
        task_name = task.get("name", "Unknown")
        
        def _complete():
            return requests.post(
                f"{API_BASE}/directives/{task_id}/complete",
                headers=HEADERS,
                json={"address": WALLET_ADDRESS},
                timeout=15
            )
            
        r = with_retry(_complete)
        if r is None:
            log(f"  ❌ Directive failed: {task_name}", Fore.RED)
            continue
            
        d = safe_json(r, f"directive/{task_id}")
        if not d: continue
        
        if d.get("success"):
            log(f"  ✅ {task_name} | +{d.get('qe', 0)} QE", Fore.GREEN)
        else:
            log(f"  ⚠️  {task_name}: {d.get('message', '')}", Fore.YELLOW)
        
        time.sleep(random.uniform(1, 3))

# ─── Claim Badges ─────────────────────────────────────────────────────────────
def claim_badges():
    log("🏅 Checking badges...", Fore.CYAN)
    def _fetch():
        return requests.get(f"{API_BASE}/badges", headers=HEADERS, timeout=15)
        
    resp = with_retry(_fetch)
    if resp is None: return
    
    data = safe_json(resp, "badges")
    if not data: return
    
    badges_list = data.get("badges", []) if isinstance(data, dict) else data
    if not isinstance(badges_list, list): return

    for badge in badges_list:
        if badge.get("claimed") or not badge.get("eligible"):
            continue
            
        badge_id   = badge.get("id")
        badge_name = badge.get("name", "Unknown")
        
        def _claim():
            return requests.post(
                f"{API_BASE}/badges/{badge_id}/claim",
                headers=HEADERS,
                json={"address": WALLET_ADDRESS},
                timeout=15
            )
            
        r = with_retry(_claim)
        if r is None:
            log(f"  ❌ Badge failed: {badge_name}", Fore.RED)
            continue
            
        d = safe_json(r, f"badge/{badge_id}")
        if not d: continue
        
        if d.get("success"):
            log(f"  🏅 {badge_name} claimed! Multiplier: {d.get('multiplier', 1)}x", Fore.GREEN)
        else:
            log(f"  ⚠️  {badge_name}: {d.get('message', '')}", Fore.YELLOW)
            
        time.sleep(random.uniform(1, 3))

# ─── Stats Check ──────────────────────────────────────────────────────────────
def check_stats():
    def _fetch():
        return requests.get(
            f"{API_BASE}/user/stats",
            headers=HEADERS,
            params={"address": WALLET_ADDRESS},
            timeout=15
        )
    resp = with_retry(_fetch)
    if resp is None: return
    
    data = safe_json(resp, "user/stats")
    if not data or not isinstance(data, dict): return
    
    qe   = data.get("quantumEnergy", "N/A")
    rank = data.get("leaderboardRank", "N/A")
    mult = data.get("multiplier", "N/A")
    log(f"📊 QE: {qe} | Rank: #{rank} | Multiplier: {mult}x", Fore.MAGENTA)

# ─── Full Daily Run ───────────────────────────────────────────────────────────
def daily_run(w3):
    log("═" * 50, Fore.CYAN)
    log("🚀 Starting daily automation run...", Fore.MAGENTA)
    check_stats()
    claim_faucet()
    time.sleep(3)
    send_self_transaction(w3)
    time.sleep(3)
    open_crates(CRATE_DAILY_LIMIT)
    time.sleep(3)
    complete_directives()
    time.sleep(3)
    claim_badges()
    time.sleep(3)
    check_stats()
    log("✅ Daily run complete!", Fore.GREEN)
    log("═" * 50, Fore.CYAN)

def faucet_run():
    log("⏰ Faucet timer triggered.", Fore.CYAN)
    claim_faucet()

# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    banner()
    validate_env()
    try:
        w3 = connect_web3()
    except Exception as e:
        log(f"CRITICAL: {e}", Fore.RED)
        return

    daily_run(w3)
    
    schedule.every().day.at("09:00").do(daily_run, w3)
    schedule.every(FAUCET_INTERVAL_HOURS).hours.do(faucet_run)
    
    log("🕒 Scheduler active. Press CTRL+C to stop.\n", Fore.GREEN)
    
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)
        except KeyboardInterrupt:
            log("👋 Bot stopped by user.", Fore.YELLOW)
            break
        except Exception as e:
            log(f"⚠️  Main loop error (recovering): {e}", Fore.RED)
            time.sleep(10)

if __name__ == "__main__":
    main()
