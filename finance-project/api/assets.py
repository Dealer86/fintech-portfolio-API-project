from fastapi import APIRouter
import yfinance

assets_router = APIRouter(prefix="/assets")


@assets_router.get("/{ticker}")
def get_asset(ticker: str):
    t = yfinance.Ticker(ticker)
    print(t.history())
    return t.fast_info
