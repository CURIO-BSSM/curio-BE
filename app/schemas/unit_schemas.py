from pydantic import BaseModel

class Units(BaseModel):
    id: int
    name: str
    description: str
    order: int
    model_config = {"from_attributes": True}