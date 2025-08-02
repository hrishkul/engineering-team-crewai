import unittest
from accounts import Account, Transaction, get_share_price

class TestAccount(unittest.TestCase):

    def setUp(self):
        self.account = Account()

    def test_deposit(self):
        self.account.deposit(1000, "2023-01-01T10:00:00Z")
        self.assertEqual(self.account.cash_balance, 1000)
        self.assertEqual(self.account.initial_deposit, 1000)

    def test_deposit_negative_amount(self):
        with self.assertRaises(ValueError):
            self.account.deposit(-500, "2023-01-01T10:00:00Z")

    def test_withdraw(self):
        self.account.deposit(1000, "2023-01-01T10:00:00Z")
        self.account.withdraw(200, "2023-01-02T10:00:00Z")
        self.assertEqual(self.account.cash_balance, 800)

    def test_withdraw_insufficient_funds(self):
        self.account.deposit(100, "2023-01-01T10:00:00Z")
        with self.assertRaises(ValueError):
            self.account.withdraw(200, "2023-01-02T10:00:00Z")

    def test_withdraw_negative_amount(self):
        self.account.deposit(1000, "2023-01-01T10:00:00Z")
        with self.assertRaises(ValueError):
            self.account.withdraw(-100, "2023-01-02T10:00:00Z")

    def test_buy_shares(self):
        self.account.deposit(20000, "2023-01-01T10:00:00Z")
        self.account.buy_shares("AAPL", 50, "2023-01-02T12:00:00Z")
        self.assertIn("AAPL", self.account.positions)
        self.assertEqual(self.account.positions["AAPL"], 50)
        expected_balance = 20000 - (get_share_price("AAPL") * 50)
        self.assertEqual(self.account.cash_balance, expected_balance)
        self.assertEqual(len(self.account.transactions), 1)
        self.assertEqual(self.account.transactions[0].transaction_type, "buy")

    def test_buy_shares_insufficient_funds(self):
        self.account.deposit(100, "2023-01-01T10:00:00Z")
        with self.assertRaises(ValueError):
            self.account.buy_shares("TSLA", 1, "2023-01-02T12:00:00Z")  # cost 700

    def test_buy_shares_negative_quantity(self):
        self.account.deposit(1000, "2023-01-01T10:00:00Z")
        with self.assertRaises(ValueError):
            self.account.buy_shares("AAPL", -10, "2023-01-02T12:00:00Z")

    def test_sell_shares(self):
        self.account.deposit(20000, "2023-01-01T10:00:00Z")
        self.account.buy_shares("AAPL", 50, "2023-01-02T12:00:00Z")
        self.account.sell_shares("AAPL", 20, "2023-01-03T14:00:00Z")
        self.assertEqual(self.account.positions["AAPL"], 30)
        self.assertEqual(len(self.account.transactions), 2)
        self.assertEqual(self.account.transactions[-1].transaction_type, "sell")
        self.assertEqual(self.account.cash_balance, 20000 - (get_share_price("AAPL") * 50) + (get_share_price("AAPL") * 20))

    def test_sell_shares_insufficient(self):
        self.account.deposit(10000, "2023-01-01T10:00:00Z")
        self.account.buy_shares("AAPL", 10, "2023-01-02T12:00:00Z")
        with self.assertRaises(ValueError):
            self.account.sell_shares("AAPL", 20, "2023-01-03T14:00:00Z")  # only owns 10

    def test_sell_shares_negative_quantity(self):
        self.account.deposit(10000, "2023-01-01T10:00:00Z")
        self.account.buy_shares("AAPL", 10, "2023-01-02T12:00:00Z")
        with self.assertRaises(ValueError):
            self.account.sell_shares("AAPL", -5, "2023-01-03T14:00:00Z")

    def test_get_portfolio_value(self):
        self.account.deposit(10000, "2023-01-01T10:00:00Z")
        self.account.buy_shares("AAPL", 10, "2023-01-02T12:00:00Z")
        total_value = self.account.get_portfolio_value()
        expected_value = self.account.cash_balance + get_share_price("AAPL") * 10
        self.assertAlmostEqual(total_value, expected_value)

    def test_get_profit_loss_increase(self):
        self.account.deposit(10000, "2023-01-01T10:00:00Z")
        self.account.buy_shares("AAPL", 10, "2023-01-02T12:00:00Z")
        self.account.buy_shares("TSLA", 5, "2023-01-02T13:00:00Z")
        # simulate price increase
        def mocked_get_share_price(symbol):
            return 200  # for simplicity, override the function
        self.account.get_share_price = mocked_get_share_price
        pl = self.account.get_profit_loss()
        self.assertAlmostEqual(pl, self.account.get_portfolio_value() - self.account.initial_deposit)

    def test_get_holdings(self):
        self.account.deposit(5000, "2023-01-01T10:00:00Z")
        self.account.buy_shares("AAPL", 10, "2023-01-02T12:00:00Z")
        holdings = self.account.get_holdings()
        self.assertEqual(holdings, {"AAPL": 10})
        # test after selling all shares
        self.account.sell_shares("AAPL", 10, "2023-01-03T10:00:00Z")
        self.assertEqual(self.account.get_holdings(), {})

    def test_get_transaction_history(self):
        self.account.deposit(1000, "2023-01-01T10:00:00Z")
        self.account.buy_shares("AAPL", 5, "2023-01-02T12:00:00Z")
        self.account.sell_shares("AAPL", 2, "2023-01-03T14:00:00Z")
        history = self.account.get_transaction_history()
        self.assertEqual(len(history), 3)
        self.assertEqual(history[0]['type'], 'deposit')
        self.assertEqual(history[1]['type'], 'buy')
        self.assertEqual(history[2]['type'], 'sell')

if __name__ == '__main__':
    unittest.main()