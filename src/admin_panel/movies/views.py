from django.http import HttpResponse


def index(request):
    html = """
        <body>
            <h1>Главная</h1>
            <ul>
                <li><a href="/django_api/v1/movies/01ab9e34-4ceb-4337-bb69-68a1b0de46b2">Проверка Django REST.</a></li>
                <li><a href="/admin">Панель администратора (логин: admin, пароль: password)</a></li>
                <li><a href="/kibana">Kibana.</a></li>
                <li><a href="/api/openapi">FastAPI.</a></li>
            </ul>
        </body>
    """
    return HttpResponse(html)
