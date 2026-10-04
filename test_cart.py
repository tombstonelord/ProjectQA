
#добавление товара в корзину
def test_add_item(api, user):
    headers, user_id = user
    body={ "product_id": "550e8400-e29b-41d4-a716-446655440001", "quantity": 1 }
    response=api.cart.add_item(user_id,body=body,headers=headers)
    assert response.status_code == 200

#получение товара в корзине
def test_get_user_cart(api, user):
    headers, user_id = user
    body={ "product_id": "550e8400-e29b-41d4-a716-446655440001", "quantity": 1 }
    response_add=api.cart.add_item(user_id,body=body,headers=headers)
    assert response_add.status_code == 200
    response_get=api.cart.get_user_cart(user_id,headers=headers)
    print("Response:", response_get.json())
    assert response_get.status_code == 200


#удаление товара из корзины
def test_remove_item(api, user):
    headers, user_id = user
    body={ "product_id": "550e8400-e29b-41d4-a716-446655440001", "quantity": 1 }
    response_add=api.cart.add_item(user_id,body=body,headers=headers)
    assert response_add.status_code == 200
    response_remove=api.cart.remove_item(user_id,body["product_id"],headers=headers)
    assert response_remove.status_code == 200
    response_get=api.cart.get_user_cart(user_id,headers=headers)
    print("Response:", response_get.json())
    assert response_get.status_code == 200


#Получение заказа другого пользователя
def test_get_order_other_user_cart(api, user,other_user):
    headers, user_id = user
    headers_other_user, other_user_user_id = other_user
    body={ "product_id": "550e8400-e29b-41d4-a716-446655440001", "quantity": 1 }
    response_add=api.cart.add_item(user_id,body=body,headers=headers)
    assert response_add.status_code == 200
    response_get = api.cart.get_user_cart(other_user_user_id, headers=headers)
    print("Response:", response_get.json())
    assert response_get.status_code == 403

#Повторное добавление одного и того же товара
def test_double_add_same_item(api, user):
    headers, user_id = user
    body = {"product_id": "550e8400-e29b-41d4-a716-446655440001", "quantity": 1}
    response_1 = api.cart.add_item(user_id, body=body, headers=headers)
    assert response_1.status_code == 200
    response_2 = api.cart.add_item(user_id, body=body, headers=headers)
    assert response_2.status_code == 200
    response_get = api.cart.get_user_cart(user_id, headers=headers)
    assert response_get.status_code == 200
    print("Response:", response_get.json())
    cart = response_get.json()
    items = cart["items"]
    item = next(i for i in items if i["productId"] == "550e8400-e29b-41d4-a716-446655440001")
    assert item["quantity"] == 2
#БАГ= не увеличивается количество товаров при повторном добавлении одного и того же товара


#Добавление разных товаров в корзину
def test_double_add_different_item(api, user):
    headers, user_id = user
    product_id_1 = "550e8400-e29b-41d4-a716-446655440001"
    product_id_2 = "550e8400-e29b-41d4-a716-446655440003"
    body = {"product_id": "550e8400-e29b-41d4-a716-446655440001", "quantity": 1}
    response_1 = api.cart.add_item(user_id, body=body, headers=headers)
    assert response_1.status_code == 200
    body_2={"product_id": "550e8400-e29b-41d4-a716-446655440003", "quantity": 1}
    response_2 = api.cart.add_item(user_id, body=body_2, headers=headers)
    assert response_2.status_code == 200
    response_get = api.cart.get_user_cart(user_id, headers=headers)
    assert response_get.status_code == 200
    print("Response:", response_get.json())
    cart = response_get.json()
    items = cart["items"]
    item_1 = None
    item_2 = None
    for it in items:
        if it["productId"] == product_id_1:
            item_1 = it
        elif it["productId"] == product_id_2:
            item_2 = it
    assert item_1 is not None, "Первый товар не найден"
    assert item_2 is not None, "Второй товар не найден"
    assert item_1["quantity"] == 1
    assert item_2["quantity"] == 1
    assert len(items) == 2