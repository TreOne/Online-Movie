import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends, Body, HTTPException, Request

from core import endpoints_params as ep_params
from models.general import Response
from services.watcher import WatcherService, get_watcher_service

router = APIRouter(prefix='/registers', tags=['Регистраторы'])


@router.post(
    path='/film_watch',
    name='Просмотр фильма',
    description='Регистрация процесса просмотра фильма.',
    response_model=Response,
)
async def film_watch(
    request: Request,
    movie_id: str = Body(**ep_params.MOVIE_ID),
    view_ts: int = Body(**ep_params.VIEW_TS),
    watcher_service: WatcherService = Depends(get_watcher_service),
) -> Response:
    try:
        movie_id = uuid.UUID(movie_id)
        client_id = request.state.user_uuid
    except ValueError:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Badly formed hexadecimal UUID string.')
    await watcher_service.register_movie_watch(movie_id, client_id, view_ts)
    return Response(msg='ОК')
