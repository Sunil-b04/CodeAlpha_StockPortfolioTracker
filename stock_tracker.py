# ============================================================
#   STOCK PORTFOLIO TRACKER — CodeAlpha Python Internship
#   Author: CodeAlpha Intern
# ============================================================

import csv
import os
from datetime import datetime

# ── Live-style hardcoded prices ───────────────────────────────────
MARKET = {
    "AAPL":  {"name": "Apple Inc.",        "price": 182.50},
    "TSLA":  {"name": "Tesla Inc.",         "price": 248.00},
    "GOOGL": {"name": "Alphabet (Google)",  "price": 175.30},
    "MSFT":  {"name": "Microsoft Corp.",    "price": 415.20},
    "AMZN":  {"name": "Amazon.com Inc.",    "price": 195.80},
    "META":  {"name": "Meta Platforms",     "price": 520.10},
    "NFLX":  {"name": "Netflix Inc.",       "price": 680.40},
    "NVDA":  {"name": "NVIDIA Corp.",       "price": 950.00},
    "AMD":   {"name": "AMD Inc.",           "price": 165.75},
    "INTC":  {"name": "Intel Corp.",        "price":  35.20},
}

portfolio = {}   # { symbol: {"qty": int, "buy_price": float} }

# ── Helpers ───────────────────────────────────────────────────────
def separator(char="─", n=58): print("  " + char * n)

def show_market():
    print("\n  📊  MARKET PRICES")
    separator()
    print(f"  {'Symbol':<8} {'Company':<26} {'Price (USD)'}")
    separator()
    for sym, data in MARKET.items():
        print(f"  {sym:<8} {data['name']:<26} ${data['price']:>8.2f}")
    separator()

def add_stock():
    show_market()
    sym = input("\n  Enter stock symbol: ").strip().upper()
    if sym not in MARKET:
        print(f"  ❌  '{sym}' not available. Choose from the list above.")
        return
    try:
        qty = int(input(f"  Quantity to buy [{sym}]: "))
        if qty <= 0:
            raise ValueError
    except ValueError:
        print("  ⚠️  Enter a valid positive integer.")
        return

    buy_price = MARKET[sym]["price"]
    if sym in portfolio:
        # weighted average buy price
        old_qty   = portfolio[sym]["qty"]
        old_bp    = portfolio[sym]["buy_price"]
        new_qty   = old_qty + qty
        avg_price = ((old_bp * old_qty) + (buy_price * qty)) / new_qty
        portfolio[sym] = {"qty": new_qty, "buy_price": round(avg_price, 2)}
        print(f"  ✅  Added {qty} more. Total: {new_qty} shares @ avg ${avg_price:.2f}")
    else:
        portfolio[sym] = {"qty": qty, "buy_price": buy_price}
        print(f"  ✅  Bought {qty} × {sym} @ ${buy_price:.2f}")

def remove_stock():
    if not portfolio:
        print("  ⚠️  Portfolio is empty.")
        return
    print(f"\n  Holdings: {', '.join(portfolio.keys())}")
    sym = input("  Symbol to remove: ").strip().upper()
    if sym not in portfolio:
        print(f"  ❌  '{sym}' not in portfolio.")
        return
    del portfolio[sym]
    print(f"  ✅  '{sym}' removed.")

def view_portfolio():
    if not portfolio:
        print("\n  ⚠️  Portfolio is empty! Buy some stocks first.")
        return

    print("\n  📈  YOUR PORTFOLIO")
    separator("═")
    print(f"  {'Symbol':<7}{'Qty':>5}  {'Buy @':>8}  {'Now @':>8}  {'P&L':>9}  {'Value':>10}")
    separator()

    total_invested = total_value = 0.0
    for sym, data in portfolio.items():
        qty        = data["qty"]
        buy_p      = data["buy_price"]
        cur_p      = MARKET[sym]["price"]
        invested   = buy_p * qty
        value      = cur_p * qty
        pnl        = value - invested
        pnl_str    = f"+${pnl:.2f}" if pnl >= 0 else f"-${abs(pnl):.2f}"
        total_invested += invested
        total_value    += value
        print(f"  {sym:<7}{qty:>5}  ${buy_p:>7.2f}  ${cur_p:>7.2f}  {pnl_str:>9}  ${value:>9.2f}")

    separator("═")
    total_pnl = total_value - total_invested
    sign      = "+" if total_pnl >= 0 else "-"
    pct       = (total_pnl / total_invested * 100) if total_invested else 0
    print(f"  {'Invested:':<30} ${total_invested:>10.2f}")
    print(f"  {'Current Value:':<30} ${total_value:>10.2f}")
    print(f"  {'Total P&L:':<30} {sign}${abs(total_pnl):>9.2f}  ({sign}{abs(pct):.2f}%)")
    separator("═")

def save_portfolio():
    if not portfolio:
        print("  ⚠️  Nothing to save.")
        return
    ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
    rows = []
    total = 0.0
    for sym, data in portfolio.items():
        qty   = data["qty"]
        buy_p = data["buy_price"]
        cur_p = MARKET[sym]["price"]
        value = cur_p * qty
        pnl   = value - buy_p * qty
        total += value
        rows.append([sym, MARKET[sym]["name"], qty,
                     f"${buy_p:.2f}", f"${cur_p:.2f}",
                     f"${value:.2f}", f"${pnl:.2f}"])

    # CSV
    csv_path = f"portfolio_{ts}.csv"
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Symbol","Company","Qty","Buy Price","Current Price","Value","P&L"])
        w.writerows(rows)
        w.writerow(["TOTAL","","","","",f"${total:.2f}",""])

    # TXT
    txt_path = f"portfolio_{ts}.txt"
    with open(txt_path, "w") as f:
        f.write("STOCK PORTFOLIO REPORT\n")
        f.write(f"Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*55 + "\n")
        for r in rows:
            f.write(f"{r[0]:<7} {r[1]:<25} qty={r[2]:>4}  val={r[5]}\n")
        f.write("="*55 + "\n")
        f.write(f"TOTAL VALUE: ${total:.2f}\n")

    print(f"  ✅  Saved → {csv_path}  &  {txt_path}")

# ── Main menu ─────────────────────────────────────────────────────
def main():
    MENU = """
  ╔══════════════════════════════════╗
  ║   💹  STOCK PORTFOLIO TRACKER   ║
  ╠══════════════════════════════════╣
  ║  1. View Market Prices           ║
  ║  2. Buy / Add Stock              ║
  ║  3. View My Portfolio            ║
  ║  4. Remove a Stock               ║
  ║  5. Save Portfolio (CSV + TXT)   ║
  ║  6. Exit                         ║
  ╚══════════════════════════════════╝"""

    actions = {
        "1": show_market,
        "2": add_stock,
        "3": view_portfolio,
        "4": remove_stock,
        "5": save_portfolio,
    }

    while True:
        print(MENU)
        ch = input("  Choose (1-6): ").strip()
        if ch == "6":
            print("\n  👋  Goodbye! Happy Investing! 📈\n")
            break
        elif ch in actions:
            actions[ch]()
        else:
            print("  ⚠️  Invalid choice.")

if __name__ == "__main__":
    main()
