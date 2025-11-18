from pydantic import BaseModel
from datetime import datetime

class History(BaseModel):
    id : int
    user_id : int
    score : int
    unit_name : str
    answered_at: datetime

    model_config = {"from_attributes": True}