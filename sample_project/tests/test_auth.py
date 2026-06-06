from sample_project.auth import (
    login,
    logout,
    validate_session,
    has_permission,
    reset_sessions
)


def setup_function():
    reset_sessions()


def test_login_success():
    token = login("admin", "admin123")

    assert token is not None
    assert validate_session(token) is True


def test_login_fail_with_wrong_password():
    token = login("admin", "wrong_password")

    assert token is None


def test_logout_removes_session():
    token = login("admin", "admin123")

    assert logout(token) is True
    assert validate_session(token) is False


def test_regular_user_has_read_permission():
    assert has_permission("user", "read") is True


def test_regular_user_does_not_have_delete_permission():
    assert has_permission("user", "delete") is False