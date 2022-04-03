MOVIE_ID = {
    "title": "UUID фильма.",
    "description": "UUID просматриваемого пользователем фильма.",
    "default": None,
    "example": "2f89e116-4827-4ff4-853c-b6e058f71e31",
}

VIEW_TS = {
    "title": "Метка времени.",
    "description": "Метка времени просмотра в формате UNIX Epoch time.",
    "default": None,
    "example": 270,
    "ge": 0,
    "le": 65535,
}
