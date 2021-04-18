from fastapi import Request, Response
import json


class DoesNotExistError(Exception):
    pass


async def handle_exception(request: Request, call_next):
    error_text = ' '.join([str(arg) for arg in call_next.args])
    return Response(status_code=502, content=json.dumps({'detail': error_text}))


async def handle_does_not_exist_exception(request: Request, call_next):
    error_text = ' '.join([str(arg) for arg in call_next.args])
    return Response(status_code=204, content=json.dumps({'detail': error_text}))


async def handle_is_dependence(request: Request, call_next):
    error_text = ' '.join([str(arg) for arg in call_next.args])
    return Response(status_code=409, content=json.dumps({'detail': error_text}))


async def handle_unauthorized(request: Request, call_next):
    return Response(status_code=401, content=json.dumps({'detail': 'incorrect credentials'}))


async def handle_forbidden(request: Request, call_next):
    error_text = ' '.join([str(arg) for arg in call_next.args])
    return Response(status_code=403, content=json.dumps({'detail': error_text}))
