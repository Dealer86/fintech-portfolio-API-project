from pydantic import BaseModel, Field
from uuid import UUID


class OrmModel(BaseModel):
    class Config:
        orm_mode = True


class UserAdd(BaseModel):
    username: str = Field(
        description="Alphanumeric username between 6 and 20 characters that can also contain '-'"
    )


class AssetAdd(BaseModel):
    ticker: str = Field(
        description="A ticker is a unique series of letters that represents a specific company's stock or security."
    )


class AssetInfoBase(OrmModel):
    ticker: str = Field(
        description="A ticker is a unique series of letters that represents a specific company's stock or security."
    )
    name: str = Field(
        description="Represents the name of a specific company based on the ticker given"
    )
    country: str = Field(
        description="Represents the country where a specific company is located based on the ticker given"
    )
    sector: str = Field(
        description="Refers to a group of companies or industries that share similar characteristics "
    )


class AssetInfoUser(AssetInfoBase):
    units: float = Field(description="Number of stocks or security a user have")


class AssetInfoPrice(AssetInfoBase):
    current_price: float = Field(description="Current price of a stock or security")
    currency: str
    today_low_price: float = Field(
        description="Highest price at which a stock or security traded"
    )
    today_high_price: float = Field(
        description="Lowest price at which a stock or security traded"
    )
    open_price: float = Field(
        description="Price at which a stock or security begins trading"
    )
    closed_price: float = Field(
        description="Last recorded price of a stock or security"
    )
    fifty_day_price: float = Field(description="Average price for fifty days")
    percentage_difference_between_closed_and_current_price: str = Field(
        description="Percentage difference between closed price and current price"
    )


class UserInfo(OrmModel):
    id: UUID = Field(
        description="ID by which to identify a specific user",
    )
    username: str
    stocks: list[AssetInfoBase] = Field(
        description="List of stocks, also known as shares or equities, represent ownership in a publicly-traded company"
    )
