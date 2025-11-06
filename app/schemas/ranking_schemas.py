from pydantic import BaseModel

class Ranking(BaseModel):
    rank: int | None = None
    username: str
    user_id: int
    score: int
    model_config = {"from_attributes": True}