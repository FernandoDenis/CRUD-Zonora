from typing import Annotated

from pydantic import BaseModel, StringConstraints


class ClienteCreate(BaseModel):
    nombre: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]