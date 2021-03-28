from fastapi_camelcase import CamelModel


class BoardOut(CamelModel):
    name: str
    description: str
