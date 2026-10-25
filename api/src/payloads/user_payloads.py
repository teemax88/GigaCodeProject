"""User management request payloads."""

CREATE_USER_PAYLOAD = {
    "username": "{username}",
    "email": "{email}",
    "password": "{password}",
    "first_name": "{first_name}",
    "last_name": "{last_name}",
}

UPDATE_USER_PAYLOAD = {
    "first_name": "{first_name}",
    "last_name": "{last_name}",
    "email": "{email}",
    "phone": "{phone}",
}

SEARCH_USERS_PAYLOAD = {
    "query": "{query}",
    "page": 1,
    "limit": 20,
}
