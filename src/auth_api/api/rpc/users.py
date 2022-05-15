from typing import Any

from flask_jsonrpc import JSONRPCBlueprint

from auth_api.api.v1.schemas.user import RpcUserSchema
from auth_api.models import User

users = JSONRPCBlueprint('users', __name__)


@users.method('Users.index')
def index(page: int, page_size: int) -> dict[str, Any]:
    schema = RpcUserSchema(many=True)
    users = User.query.filter_by(
        is_active=True,
        is_superuser=False,
    ).filter(
        User.email is not None,
    ).paginate(page, page_size)
    return {
        'users': schema.dump(users.items),
        'count': users.total,
        'has_next': users.has_next,
        'has_prev': users.has_prev,
        'page': page,
        'page_size': page_size,
        'pages': users.pages,
    }
