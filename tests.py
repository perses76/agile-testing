from user_api import save_new_user


def test_save_new_user():
    result = save_new_user()
    assert result is True


test_save_new_user()
