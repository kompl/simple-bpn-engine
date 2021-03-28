from fastapi_camelcase import CamelModel


class BoardIn(CamelModel):
    name: str
    description: str
