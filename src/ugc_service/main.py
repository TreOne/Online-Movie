from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
import router
from core import config
import uvicorn
# import asyncio
from jose import JWTError, jwt


app = FastAPI(
    title=config.PROJECT_NAME,
    description=config.PROJECT_DESCRIPTION,
    version=config.PROJECT_VERSION,
    license_info=config.PROJECT_LICENSE_INFO,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.middleware('http')
async def jwt_handler(request: Request, call_next):
    roles = {}
    token_status = 'None'

    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        token_status = 'OK'
        jwt_token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(
                jwt_token,
                config.jwt_secret_key,
                algorithms=config.jwt_algorithms
            )
            roles = set(payload.get('roles', {}))
        except JWTError as e:
            token_status = f'Error: {e}'

    request.state.user_roles = roles
    response = await call_next(request)
    response.headers['X-Token-Status'] = token_status
    return response

app.include_router(router.route)
# asyncio.create_task(router.consume())
