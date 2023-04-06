from fastapi import APIRouter
import yfinance

from api.models import AssetInfoPrice
from domain.asset.factory import AssetFactory

assets_router = APIRouter(prefix="/assets")


@assets_router.get("/{ticker}", response_model=AssetInfoPrice)
def get_asset(ticker: str):
    asset = AssetFactory().make_new(ticker)
    return asset


@assets_router.get("/{ticker}/history")
def get_history(ticker: str):
    t = yfinance.Ticker(ticker)
    history = t.history(interval="1d", start="2019-01-30")
    print(t.fast_info)
    print(t.fast_info.values())
    print(history)
    print(type(history))
    return t.fast_info
