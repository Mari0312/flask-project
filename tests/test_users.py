from models import User


def test_get_user_info(client, app):
    test_user = User(
        name='test_name',
        birthday="2022-04-12",
        password='password'
    ).save()
    resp = client.get(f'/users/{test_user.id}')

    assert resp.json['id'] == test_user.id


def test_delete_user(client, app):
    test_user = User(
        name='test_name',
        birthday="2022-04-12",
        password='password',
    ).save()

    delete_user_response = client.delete(f'/users/{test_user.id}')
    get_user_response = client.get(f'/users/{test_user.id}')

    assert get_user_response.status_code == 404
    assert delete_user_response.json['message'] == "Deleted"


def test_update_user(client, app):
    test_user = User(
        name='test_name',
        birthday="2022-04-12",
        password='password',
    ).save()

    resp = client.patch(f'/users/{test_user.id}',
                        json={
                            "name": "Mariia",
                        })
    assert resp.json['name'] == test_user.name
