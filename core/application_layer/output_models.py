from fastapi_camelcase import CamelModel
from uuid import UUID


class BoardOut(CamelModel):
    uuid: UUID = None
    name: str = None
    description: str = None
