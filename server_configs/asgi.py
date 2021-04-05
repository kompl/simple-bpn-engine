import os
from fastapi import FastAPI
from authorization.application_layer.auth_routing import auth_router
from server_configs.exception_handlers import handle_exception, handle_does_not_exist_exception, handle_is_dependence, \
    DoesNotExistError, handle_unauthorized, handle_forbidden
from authorization.infrastructure_layer.utils import UnauthorizedError, ForbiddenError
from asyncpg.exceptions import ForeignKeyViolationError
from core.application_layer.routing import boards_router


app = FastAPI(
    debug=os.getenv('DEBUG', False),
    title="WEBMASTERR 2077",
    description="микросервис для управления адаптерами",
    version="0.0.1",
)

app.include_router(auth_router)
app.include_router(boards_router)
app.add_exception_handler(IOError, handle_exception)
app.add_exception_handler(DoesNotExistError, handle_does_not_exist_exception)
app.add_exception_handler(ForeignKeyViolationError, handle_is_dependence)
app.add_exception_handler(UnauthorizedError, handle_unauthorized)
app.add_exception_handler(ForbiddenError, handle_forbidden)
