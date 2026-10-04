
from conftest import api,unique_email,unique_password,unique_name


#успешная регистрация
def test_register_user(api,unique_email,unique_password,unique_name):
    data = {
        "email": unique_email,
        "password": unique_password,
        "name": unique_name
    }
    response = api.users.register_user(data)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["accessToken"] is not None



#регистрация с уже существующим email
def test_register_duplicate_email(api,unique_email,unique_password,unique_name):
    data = {
        "email": unique_email,
        "password": unique_password,
        "name": unique_name
    }
    resp1 = api.users.register_user(data)
    assert resp1.status_code == 200
    resp2 = api.users.register_user(data)
    assert resp2.status_code == 500
    error_body = resp2.json()
    assert error_body["code"] == 13



# регистрация без почты
def test_error_register_user_no_mail(api,unique_email,unique_password,unique_name):
    data = {
        "password": unique_password,
        "name": unique_name
    }
    json_of_response = api.users.register_user(data)
    assert json_of_response.status_code == 400
    error_body = json_of_response.json()
    assert error_body["code"] == 3



# регистрация без пароля
def test_error_register_user_no_pass(api,unique_email,unique_password,unique_name):
    data = {"email": unique_email,
            "name": unique_name}
    json_of_response = api.users.register_user(data)
    assert json_of_response.status_code == 400
    error_body = json_of_response.json()
    assert error_body["code"] == 3


#БАГ- с бека можно регистрироваться без имени
# регистрация без имени <FI
def test_error_register_user_no_name(api,unique_email,unique_password,unique_name):
    data = {"email": unique_email,
            "password": unique_password,
}
    json_of_response = api.users.register_user(data)
    assert json_of_response.status_code == 400
    error_body = json_of_response.json()
    assert error_body["code"] == 3




#Успешный логин
def test_success_login_user(api,unique_email,unique_password,unique_name):
    data = {
        "email": unique_email,
        "password": unique_password,
        "name": unique_name
    }
    json_of_register = api.users.register_user(data)
    register_json = json_of_register.json()
    assert register_json["accessToken"] is not None
    assert register_json["user"]["email"] == data["email"]
    json_of_login= api.users.login_user(data)
    login_json = json_of_login.json()
    assert login_json["accessToken"] is not None
    assert login_json["user"]["email"] == data["email"]


#неверный пароль
def test_wrong_password_login_user(api,unique_email,unique_password,unique_name):
    data = {
        "email": unique_email,
        "password": unique_password,
        "name": unique_name
    }
    resp_reg = api.users.register_user(data)
    assert resp_reg.status_code == 200
    reg_json = resp_reg.json()
    assert reg_json["accessToken"] is not None
    assert reg_json["user"]["email"] == data["email"]
    login_data = {
        "email": data["email"],
        "password": "wrong_password"
    }
    resp_login = api.users.login_user(login_data)
    assert resp_login.status_code == 401
    error_json = resp_login.json()
    assert error_json["code"] == 16


#неверная почта
def test_wrong_mail_login_user(api,unique_email,unique_password,unique_name):
    data = {
        "email": unique_email,
        "password": unique_password,
        "name": unique_name
    }
    resp_reg = api.users.register_user(data)
    assert resp_reg.status_code == 200
    reg_json = resp_reg.json()
    assert reg_json["accessToken"] is not None
    assert reg_json["user"]["email"] == data["email"]
    login_data = {
        "email": 'wrong_email',
        "password": data["email"]
    }
    resp_login = api.users.login_user(login_data)
    assert resp_login.status_code == 401
    error_json = resp_login.json()
    assert error_json["code"] == 16



#получить существующего пользователя
def test_get_user_by_id(api,unique_email,unique_password,unique_name):
    data = {
        "email": unique_email,
        "password": unique_password,
        "name": unique_name
    }
    resp_reg = api.users.register_user(data)
    assert resp_reg.status_code == 200
    reg_json = resp_reg.json()
    assert reg_json["accessToken"] is not None
    assert reg_json["user"]["email"] == data["email"]
    get_user=api.users.get_user(reg_json["user"]["id"])
    assert get_user.status_code == 200
    assert get_user.json()["user"]["email"] == data["email"]




#удаление пользователя
def test_delete_user_by_id(api,unique_email,unique_password,unique_name):
    data = {
        "email": unique_email,
        "password": unique_password,
        "name": unique_name

    }
    resp_reg = api.users.register_user(data)
    assert resp_reg.status_code == 200
    reg_json = resp_reg.json()
    token=reg_json["accessToken"]
    assert reg_json["accessToken"] is not None
    headers = {"Authorization": f"Bearer {token}"}
    resp_delete=api.users.delete_user(reg_json["user"]["id"], headers=headers)
    assert resp_delete.status_code == 200
























