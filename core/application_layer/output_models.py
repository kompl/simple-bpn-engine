from fastapi_camelcase import CamelModel
from uuid import UUID


class BoardOut(CamelModel):
    uuid: UUID
    name: str
    description: str
