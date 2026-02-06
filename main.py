

from dotenv import load_dotenv
load_dotenv()

from data_fetcher import fetch_stock_data
from indicators import add_indicators
from agent import ai_decision
from email_service import send_email
from config import STOCKS

def run():
    for symbol, name in STOCKS.items():
        df = fetch_stock_data(symbol)
        df = add_indicators(df)
        decision = ai_decision(df, name)

        send_email(
            subject=f"AI Trade Alert: {name}",
            body=decision
        )

if __name__ == "__main__":
    run()
