from typing import Annotated

from pydantic import BaseModel, StringConstraints, ConfigDict


class ClienteCreate(BaseModel):
    nombre: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
        
class ClienteRead(BaseModel):
    id: int
    nombre: str
    model_config = ConfigDict(from_attributes=True)
    
class ClienteUpdate(BaseModel):
    nombre: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]