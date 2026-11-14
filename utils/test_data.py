class TestData:
    VALID_USER = ("srikar", "Test123!")

    INVALID_USERS = [
        ("wrong_user", "Test123!"),
        ("srikar", "wrong_pass"),
        ("", "Test123!"),
        ("srikar", ""),
    ]
