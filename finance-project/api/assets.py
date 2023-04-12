from fastapi import APIRouter
import yfinance
import uuid
from matplotlib import pyplot
from api.models import AssetInfoPrice
from domain.asset.factory import AssetFactory

assets_router = APIRouter(prefix="/assets")


@assets_router.get("/{ticker}", response_model=AssetInfoPrice)
def get_asset(ticker: str):
    asset = AssetFactory().make_new(ticker)
    return asset


@assets_router.get("/{ticker}/history")
def get_history(ticker: str, start_date: str = "2019-01-30", end_date: str = "2023-04-10"):
    t = yfinance.Ticker(ticker)
    print(start_date)
    history = t.history(interval="1d", start=start_date, end=end_date)
    data = (history["Open"])
    pyplot.plot(data)
    pyplot.savefig(f"{ticker} - {uuid.uuid4()}.png")
    pyplot.clf()




