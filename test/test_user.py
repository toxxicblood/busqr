from user import User

def test_init():
    user = User("Ramsey", "Ngong")
    assert user.name == "Ramsey"
    assert user.address == "Ngong"

def test_str():
    user = User("ramsey", "ngong")
    assert str(user) == "Username:ramsey User address:ngong"