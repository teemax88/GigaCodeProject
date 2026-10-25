"""Authentication request payloads."""

LOGIN_PAYLOAD = {
    "username": "{username}",
    "password": "{password}",
}

REGISTER_PAYLOAD = {
    "username": "{username}",
    "email": "{email}",
    "password": "{password}",
    "first_name": "{first_name}",
    "last_name": "{last_name}",
}

REFRESH_TOKEN_PAYLOAD = {
    "refresh_token": "{refresh_token}",
}

FORGOT_PASSWORD_PAYLOAD = {
    "email": "{email}",
}

RESET_PASSWORD_PAYLOAD = {
    "token": "{token}",
    "new_password": "{new_password}",
}
