# This is Arjun Koshal's SSMIF Quant 21 Application
# 2.1 Basket Portfolio of Stocks

import numpy as np
import pandas_datareader as web
import datetime as dt

start = dt.datetime(2020, 1, 1)
end = dt.datetime(2021, 1, 1)
stocks = {"AAPL": 50, "GME": 150, "TSLA": 5, "AAL": 200, "AMZN": 1}

class Portfolio:
    def __init__(self, symbol: dict(), start, end, ticker):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.ticker = ticker

    def averageDailyReturn(self):
        average_sum = 0
        for stock, shares in self.symbol.items():
            df = web.DataReader(stock, 'yahoo', self.start, self.end)
            open = df["Open"]
            average_stock = open.pct_change()
            average_percent = sum(average_stock[1:])/(len(average_stock)-1)
            average_sum += average_percent
        average_daily_returns = (average_sum/len(self.symbol)) * 100
        return average_daily_returns

    def volatility(self):
        total_volatility = float()
        for stock, shares in self.symbol.items():
            df = web.DataReader(stock, 'yahoo', self.start, self.end)
            close = df["Close"]
            simple_returns = close.pct_change()
            log_returns = np.log(1 + simple_returns)
            stock_volatility = np.exp(log_returns.cumsum()[-1]) - 1
            total_volatility += stock_volatility * shares
        return total_volatility

    def riskRatio(self):
        df2 = web.DataReader(self.ticker, 'yahoo', self.start, self.end)
        volatility = self.volatility()
        close = df2["Close"]
        log_returns = np.log(close) - np.log(close.shift(1))
        log_returns.fillna(0, inplace=True)
        days = len(close)
        bench_volatility = np.sqrt(days) * np.std(log_returns)
        risk = volatility/bench_volatility
        return risk

    def marginalVolatility(self, ticker: str, shares: int):
        self.symbol[ticker] += shares
        highest_volatility = self.volatility()
        self.symbol[ticker] -= shares
        lowest_volatility = self.volatility()
        marginal_volatility = abs(highest_volatility - lowest_volatility)
        return marginal_volatility

    def maxDrawDown(self):
        for stock, shares in self.symbol.items():
            df = web.DataReader(stock, 'yahoo', self.start, self.end)
            close = df["Close"]
            max_drawdown = ((close.min() - close.max()) / close.max()) * 100
        return max_drawdown


new_portfolio = Portfolio(stocks, start, end, "VOO")
average_daily_returns = new_portfolio.averageDailyReturn()
volatility = new_portfolio.volatility()
risk_ratio = new_portfolio.riskRatio()
marginal_volatility = new_portfolio.marginalVolatility("AAPL", 5)
max_drawdown = new_portfolio.maxDrawDown()

print("Average Daily Returns:", average_daily_returns, "%")
print("Volatility:", volatility)
print("Risk Ratio:", risk_ratio)
print("Marginal Volatility:", marginal_volatility)
print("Max Draw Down:", max_drawdown, "%")
