from http import HTTPStatus

import uvicorn
from core import config
from core.config import jwt_algorithms, jwt_secret_key
from db.kafka import kafka_reconnect, kafka_disconnect
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from jose import JWTError, jwt
from starlette.responses import JSONResponse

import api

app = FastAPI(
    title=config.PROJECT_NAME,
    description=config.PROJECT_DESCRIPTION,
    version=config.PROJECT_VERSION,
    license_info=config.PROJECT_LICENSE_INFO,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    await kafka_reconnect()


@app.on_event('shutdown')
async def shutdown():
    await kafka_disconnect()


@app.middleware('http')
async def jwt_handler(request: Request, call_next):
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return JSONResponse(
            {'Detail': 'Unauthorized'}, status_code=HTTPStatus.UNAUTHORIZED,
        )
    jwt_token = auth_header.split(' ')[1]
    try:
        payload = jwt.decode(jwt_token, jwt_secret_key, algorithms=jwt_algorithms)
    except JWTError as e:
        return JSONResponse(
            {'Detail': f'JWTError: {e}'}, status_code=HTTPStatus.UNAUTHORIZED,
        )
    user_uuid = payload.get('user_uuid')
    request.state.user_uuid = user_uuid
    response = await call_next(request)
    return response


app.include_router(api.router)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000)
