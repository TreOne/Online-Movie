import uuid

from core import endpoints_params as ep_params
from fastapi import APIRouter, Body, Depends, Request
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
    movie_id: uuid.UUID = Body(**ep_params.MOVIE_ID),
    view_ts: int = Body(**ep_params.VIEW_TS),
    watcher_service: WatcherService = Depends(get_watcher_service),
) -> Response:
    client_id = request.state.user_uuid
    await watcher_service.register_movie_watch(
        movie_id=movie_id, client_id=client_id, view_ts=view_ts,
    )
    return Response(msg='ОК')
