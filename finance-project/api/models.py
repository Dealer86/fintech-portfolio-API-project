from pydantic import BaseModel, Field


class UserAdd(BaseModel):
    username: str = Field(
        description="Alphanumeric username between 6 and 20 characters"
    )


class UserInfo(BaseModel):
    username: str
    stocks: list[str]

    class Config:
        orm_mode = True
