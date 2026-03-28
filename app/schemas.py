from pydantic import BaseModel
from typing import Optional

class QueryRequest(BaseModel):
    query: str
    module: Optional[str] = None
    submodule: Optional[str] = None