from datetime import datetime, timedelta


USERS = {
    "admin": {
        "password": "admin123",
        "permissions": ["read", "write", "delete"]
    },
    "user": {
        "password": "user123",
        "permissions": ["read"]
    }
}

SESSIONS = {}


def reset_sessions():
    """
    Clears all active sessions.

    This function is mainly used in tests to avoid one test affecting another.
    """
    SESSIONS.clear()


def login(username, password):
    """
    Authenticates a user and creates a session token.

    Returns a token if the credentials are valid.
    Returns None if the credentials are invalid.
    """
    user = USERS.get(username)

    if user is None:
        return None

    if user["password"] != password:
        return None

    token = f"token_{username}"

    SESSIONS[token] = {
        "username": username,
        "expires_at": datetime.now() + timedelta(minutes=30)
    }

    return token


def logout(token):
    """
    Removes an active session.
    """
    if token in SESSIONS:
        del SESSIONS[token]
        return True

    return False


def validate_session(token):
    """
    Validates if a session token exists.

    Intentional defect:
    This function only checks if the token exists, but it does not verify
    if the session has expired.
    """
    return token in SESSIONS


def has_permission(username, permission):
    """
    Checks if a user has a given permission.

    Intentional weak design:
    The admin user receives all permissions automatically.
    """
    if username == "admin":
        return True

    user = USERS.get(username)

    if user is None:
        return False

    return permission in user["permissions"]