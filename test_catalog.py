import uuid

#получить список товаров
def test_get_product(api, user):
    headers, user_id = user
    response = api.catalog.get_all_product(headers=headers)
    assert response.status_code == 200
    products = response.json()
    assert len(products["products"]) == 20
    assert products["totalCount"] == 50

#получить конкретный товар
def test_get_product_id(api, user):
    headers, user_id = user
    id='550e8400-e29b-41d4-a716-446655440001'
    response = api.catalog.get_product(id,headers=headers)
    assert response.status_code == 200

#получение несуществующего товара
def test_error_item(api, user):
    headers, user_id = user
    new_id = str(uuid.uuid4())
    id=new_id
    response = api.catalog.get_product(id,headers=headers)
    assert response.status_code == 404


#Проверка категорий товаров
def test_get_categories(api, user):
    headers, user_id = user
    response = api.catalog.get_categories(headers=headers)
    assert response.status_code == 200
    products = response.json()
    expected_names = {
        "Видеокарты",
        "Гаджеты",
        "Накопители и прочее",
        "Ноутбуки",
        "Планшеты",
        "Смартфоны",
    }
    actual_names = {c["name"] for c in products["categories"]}
    assert actual_names == expected_names

#Получение категории по id
def test_get_categories_id(api, user):
    id= "770e8400-e29b-41d4-a716-446655440004"
    headers, user_id = user
    response = api.catalog.get_categories_by_id(id,headers=headers)
    assert response.status_code == 200
    assert response.json()["category"]["name"] == "Гаджеты"

#Проверка фильтров
def test_catalog_filter(api, user):
    headers, user_id = user
    #Параметр бренд
    response_brand= api.catalog.get_all_product(headers=headers, params={"brand": "apple"})
    assert response_brand.status_code == 200
    print(response_brand.json())
    products = response_brand.json()
    data= products["products"]
    brands= {i ["brand"] for i in data}
    assert brands =={'apple'}
    #Параметр имя
    response_q = api.catalog.get_all_product(headers=headers, params={"q": "iPhone 15"})
    assert response_q.status_code == 200
    products_q= response_q.json()
    data_q= products_q["products"]
    q= {i ["name"] for i in data_q}
    assert all("iphone 15" in name.lower() for name in q)
    #Параметр id категории
    response_category = api.catalog.get_all_product(headers=headers, params={"category_id": '770e8400-e29b-41d4-a716-446655440005'})
    assert response_category.status_code == 200
    products_category = response_category.json()
    data_category = products_category["products"]
    category = {i["categoryId"] for i in data_category}
    print(response_category.json())
    assert category == {"770e8400-e29b-41d4-a716-446655440005"}






#ТЕСТЫ С БД
#Базовые операции и защита от инъекций, Тест добавления товара
def test_sql_add(api, cursor):
    cursor.execute(
        "INSERT INTO products (name, description, price_cents, stock_quantity) "
        "VALUES ('Ноутбук', 'описание', 100000, 5)"
    )
    cursor.execute("SELECT name, description, price_cents FROM products WHERE name = %s", ('Ноутбук',))
    row = cursor.fetchone()
    assert row is not None, "Товар не найден"
    name, description, price = row
    assert name == 'Ноутбук'
    assert description == 'описание'
    assert price == 100000


#проверка cart_items
def test_cart_items(api, cursor,user):
    headers, user_id = user
    cursor.execute(
        "INSERT INTO cart_items (user_id, product_id, quantity) VALUES (%s, %s, %s)",
        (user_id, "550e8400-e29b-41d4-a716-446655440001", 1)
    )
    cursor.execute(
        "SELECT * FROM cart_items WHERE user_id = %s AND product_id = %s",
        (user_id, "550e8400-e29b-41d4-a716-446655440001")
    )
    row = cursor.fetchone()
    assert row is not None, "Запись не найдена"



#Задание 3. Подготовка связанных данных (Data Preparation)
def test_prepare_data(api, cursor, user):
    headers, user_id = user
    cursor.execute(
        "INSERT INTO products (name, description, price_cents, stock_quantity) "
        "VALUES (%s, %s, %s, %s) RETURNING id",
        ("Ноутбук", "описание", 100000, 5)
    )
    row = cursor.fetchone()
    assert row is not None, "Не удалось создать товар"
    product_id = row[0]
    cursor.execute(
        "INSERT INTO cart_items (user_id, product_id, quantity) VALUES (%s, %s, %s)",(user_id, product_id, 1))
    cursor.execute(
        "SELECT * FROM cart_items WHERE user_id = %s AND product_id = %s",
        (user_id, product_id)
    )
    row = cursor.fetchone()
    assert row is not None, "Товар не найден в корзине"


#Удаление данных
def test_delete_data(api, cursor, user):
    headers, user_id = user
    cursor.execute(
        "INSERT INTO products (name, description, price_cents, stock_quantity) "
        "VALUES (%s, %s, %s, %s) RETURNING id",
        ("Ноутбук", "описание", 100000, 5)
    )
    row_products = cursor.fetchone()
    assert row_products is not None, "Не удалось создать товар"
    product_id = row_products[0]
    cursor.execute(
        "INSERT INTO cart_items (user_id, product_id, quantity) VALUES (%s, %s, %s)", (user_id, product_id, 1))
    cursor.execute(
        "SELECT * FROM cart_items WHERE user_id = %s AND product_id = %s",
        (user_id, product_id)
    )
    row_cart = cursor.fetchone()
    assert row_cart is not None, "Не удалось добавить товар в корзину"
    cursor.execute("DELETE FROM cart_items WHERE user_id = %s AND product_id = %s",
        (user_id, product_id))
    cursor.execute(
        "SELECT * FROM cart_items WHERE user_id = %s AND product_id = %s",
        (user_id, product_id))
    row = cursor.fetchone()
    assert row is None