from pydantic import BaseModel, Field


class UserAdd(BaseModel):
    username: str = Field(
        description="Alphanumeric username between 6 and 20 characters"
    )


class UserInfo(BaseModel):
    id: str = Field(
        description="ID by which to identify a specific user",
        default=None
    )
    username: str
    stocks: list[str]

    class Config:
        orm_mode = True
