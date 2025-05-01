from pydantic import BaseModel
from typing import Optional

class ModelInput(BaseModel):
    input_data: str
    task: str
    max_memory: Optional[int] = None
    allow_proprietary: Optional[bool] = False