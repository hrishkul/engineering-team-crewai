import gradio as gr
from datetime import datetime
from accounts import Account  # Assumed to be in the same directory
from typing import List, Dict

# Instantiate a single user account
user_account = Account()

def get_share_price(symbol: str) -> float:
    """Return fixed share prices for testing."""
    prices = {
        'AAPL': 150.0,
        'TSLA': 700.0,
        'GOOGL': 2800.0
    }
    return prices.get(symbol, 0.0)

def create_account():
    global user_account
    user_account = Account()
    return "Account created successfully."

def deposit_funds(amount: float):
    try:
        user_account.deposit(amount, datetime.now().isoformat())
        return f"Deposited ${amount:.2f} successfully."
    except Exception as e:
        return str(e)

def withdraw_funds(amount: float):
    try:
        user_account.withdraw(amount, datetime.now().isoformat())
        return f"Withdrew ${amount:.2f} successfully."
    except Exception as e:
        return str(e)

def buy_shares(symbol: str, quantity: int):
    try:
        user_account.buy_shares(symbol, quantity, datetime.now().isoformat())
        return f"Bought {quantity} shares of {symbol}."
    except Exception as e:
        return str(e)

def sell_shares(symbol: str, quantity: int):
    try:
        user_account.sell_shares(symbol, quantity, datetime.now().isoformat())
        return f"Sold {quantity} shares of {symbol}."
    except Exception as e:
        return str(e)

def get_portfolio_value():
    value = user_account.get_portfolio_value()
    return f"Total Portfolio Value: ${value:,.2f}"

def get_profit_loss():
    pl = user_account.get_profit_loss()
    return f"Profit/Loss since initial deposit: ${pl:,.2f}"

def get_holdings():
    holdings = user_account.get_holdings()
    if not holdings:
        return "No holdings."
    return "\n".join([f"{symbol}: {qty} shares" for symbol, qty in holdings.items()])

def get_transactions():
    transactions = user_account.get_transaction_history()
    if not transactions:
        return "No transactions."
    lines = []
    for t in transactions:
        lines.append(f"{t['timestamp']}: {t['type'].capitalize()} {t['quantity']} {t['symbol']} at ${t['price']:.2f}")
    return "\n".join(lines)

app = gr.Blocks()

with app:
    gr.Markdown("# Trading Simulation Platform (Demo)")
    
    with gr.Row():
        create_btn = gr.Button("Create Account")
        create_msg = gr.Textbox(label="", interactive=False)
    create_btn.click(create_account, outputs=create_msg)

    with gr.Row():
        deposit_input = gr.Number(label="Deposit Amount", value=0.0, precision=2)
        deposit_btn = gr.Button("Deposit Funds")
        deposit_msg = gr.Textbox(label="", interactive=False)
    deposit_btn.click(deposit_funds, inputs=deposit_input, outputs=deposit_msg)

    with gr.Row():
        withdraw_input = gr.Number(label="Withdraw Amount", value=0.0, precision=2)
        withdraw_btn = gr.Button("Withdraw Funds")
        withdraw_msg = gr.Textbox(label="", interactive=False)
    withdraw_btn.click(withdraw_funds, inputs=withdraw_input, outputs=withdraw_msg)

    with gr.Tab("Trade Shares"):
        symbol_input = gr.Dropdown(choices=["AAPL", "TSLA", "GOOGL"], label="Share Symbol")
        quantity_input = gr.Number(label="Quantity", value=1, precision=0)
        buy_btn = gr.Button("Buy Shares")
        sell_btn = gr.Button("Sell Shares")
        trade_msg = gr.Textbox(label="", interactive=False)
        buy_btn.click(buy_shares, inputs=[symbol_input, quantity_input], outputs=trade_msg)
        sell_btn.click(sell_shares, inputs=[symbol_input, quantity_input], outputs=trade_msg)

    with gr.Tab("Portfolio & History"):
        port_value_btn = gr.Button("Get Portfolio Value")
        profit_loss_btn = gr.Button("Get Profit/Loss")
        holdings_btn = gr.Button("Get Holdings")
        transactions_btn = gr.Button("Get Transaction History")
        port_value_output = gr.Textbox(label="Portfolio Value", interactive=False)
        profit_loss_output = gr.Textbox(label="Profit/Loss", interactive=False)
        holdings_output = gr.Textbox(label="Holdings", interactive=False)
        transactions_output = gr.Textbox(label="Transactions", interactive=False)

        port_value_btn.click(get_portfolio_value, outputs=port_value_output)
        profit_loss_btn.click(get_profit_loss, outputs=profit_loss_output)
        holdings_btn.click(get_holdings, outputs=holdings_output)
        transactions_btn.click(get_transactions, outputs=transactions_output)

app.launch(share=True)