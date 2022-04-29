from django.http import HttpResponse


def index(request):
    html = """
        <body>
            <h1>Главная</h1>
            <ul>
                <li><a href="/django_api/v1/movies/01ab9e34-4ceb-4337-bb69-68a1b0de46b2">Проверка Django REST.</a></li>
                <li><a href="/admin">Панель администратора (логин: admin, пароль: password)</a></li>
                <li><a href="/kibana">Kibana.</a></li>
                <li><a href="/api/openapi">Api service.</a></li>
                <li><a href="/auth/swagger">Auth service.</a></li>
                <li><a href="/ugc_service/openapi">UGC service.</a></li>
                <li><a href="http://localhost:16686/">Jaeger.</a></li>
                <li><a href="http://localhost:5602/app/observability/overview">ELK logs.</a></li>
            </ul>
        </body>
    """
    return HttpResponse(html)
