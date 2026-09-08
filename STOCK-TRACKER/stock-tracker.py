import csv
from datetime import datetime

# ---------------------------------------------------------
# STOCK PORTFOLIO TRACKER
# ---------------------------------------------------------

STOCK_PRICES = {
    "AAPL": 180.00,
    "TSLA": 250.00,
    "NVDA": 120.00,
    "MSFT": 410.00,
    "AMZN": 175.00,
    "GOOGL": 160.00,
}


def display_market_prices():
    """Displays available stocks and their market prices."""
    print("\n" + "=" * 45)
    print("        AVAILABLE STOCKS & CURRENT PRICES       ")
    print("=" * 45)
    for ticker, price in STOCK_PRICES.items():
        print(f"  • {ticker:<8} : ${price:,.2f}")
    print("=" * 45)


def get_user_portfolio():
    """Collects stock tickers and quantities from user input."""
    portfolio = {}
    print("\n--- ENTER PORTFOLIO HOLDINGS ---")
    print("(Type 'DONE' when finished entering stocks)\n")

    while True:
        ticker = input("Enter Stock Ticker (e.g., AAPL): ").strip().upper()

        if ticker == "DONE":
            break

        if not ticker:
            print("❌ Input cannot be empty. Try again.")
            continue

        if ticker not in STOCK_PRICES:
            print(f"❌ '{ticker}' is not in the system. Available: {', '.join(STOCK_PRICES.keys())}")
            continue

        while True:
            try:
                quantity_input = input(f"Enter quantity for {ticker}: ").strip()
                quantity = int(quantity_input)
                if quantity <= 0:
                    print("❌ Quantity must be a positive integer.")
                    continue
                break
            except ValueError:
                print("❌ Invalid input. Please enter a valid whole number for quantity.")

        portfolio[ticker] = portfolio.get(ticker, 0) + quantity
        print(f"✔ Added {quantity} shares of {ticker}.\n")

    return portfolio


def calculate_portfolio_summary(portfolio):
    """Calculates individual stock totals and overall portfolio total value."""
    summary_data = []
    total_investment = 0.0

    for ticker, qty in portfolio.items():
        price = STOCK_PRICES[ticker]
        total_val = price * qty
        total_investment += total_val
        summary_data.append({
            "ticker": ticker,
            "quantity": qty,
            "price": price,
            "total_value": total_val
        })

    return summary_data, total_investment


def build_report_text(summary_data, total_investment):
    """Generates exact same formatted report lines for screen and files."""
    lines = []
    lines.append("=======================================================")
    lines.append("               PORTFOLIO SUMMARY REPORT                ")
    lines.append("=======================================================")
    lines.append(f"Generated Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    lines.append(f"{'Ticker':<10} | {'Quantity':<10} | {'Price ($)':<12} | {'Total ($)':<12}")
    lines.append("-" * 55)

    for item in summary_data:
        lines.append(
            f"{item['ticker']:<10} | "
            f"{item['quantity']:<10} | "
            f"${item['price']:<11,.2f} | "
            f"${item['total_value']:<11,.2f}"
        )

    lines.append("-" * 55)
    lines.append(f"TOTAL PORTFOLIO VALUE: ${total_investment:,.2f}")
    lines.append("=======================================================")
    return lines


def display_summary(report_lines):
    """Prints formatted report directly to screen."""
    print("\n")
    for line in report_lines:
        print(line)


def save_to_file(report_lines, filename):
    """Saves formatted report to .txt or .csv with identical layout."""
    try:
        with open(filename, mode="w", encoding="utf-8") as file:
            for line in report_lines:
                file.write(line + "\n")
        print(f"✅ Saved successfully as '{filename}'.")
    except IOError as e:
        print(f"❌ Error saving file '{filename}': {e}")


def main():
    """Main function."""
    display_market_prices()
    portfolio = get_user_portfolio()

    if not portfolio:
        print("\n⚠️ No holdings entered. Exiting program.")
        return

    summary_data, total_investment = calculate_portfolio_summary(portfolio)
    report_lines = build_report_text(summary_data, total_investment)

    # 1. Screen par report show hogi
    display_summary(report_lines)

    # 2. Same format .csv aur .txt file mein save karne ki options
    print("\n--- SAVE REPORT OPTIONS ---")
    print("1. Save as .csv file")
    print("2. Save as .txt file")
    print("3. Save Both (.csv & .txt)")
    print("4. Do Not Save")

    choice = input("Select an option (1-4): ").strip()

    if choice == "1":
        save_to_file(report_lines, "portfolio_summary.csv")
    elif choice == "2":
        save_to_file(report_lines, "portfolio_summary.txt")
    elif choice == "3":
        save_to_file(report_lines, "portfolio_summary.csv")
        save_to_file(report_lines, "portfolio_summary.txt")
    else:
        print("Report export skipped.")

    print("\nProgram finished successfully!")


if __name__ == "__main__":
    main()