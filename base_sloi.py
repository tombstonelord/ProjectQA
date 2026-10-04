import requests
from urllib3.util import url


class BaseHttpClient:

    def __init__(self):
        self.__url = None

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, value):
        if value:
            self.__url = value

    def _call_method(self, method: str, endpoint: str, **kwargs):
        request = getattr(requests, method.lower())

        response = request(
            url=f"{self.url}{endpoint}",
            verify=False,
            **kwargs
        )

        return response


class UserClient(BaseHttpClient):

    def __init__(self, url):
        super().__init__()
        self.url = url

    def register_user(self, body, headers=None, **kwargs):
        return self._call_method(
            "POST",
            "/v1/users/register",
            json=body, headers=headers,
            **kwargs)

    def login_user(self, body, headers=None, **kwargs):
        return self._call_method(
            "POST",
            "/v1/users/login",
            json=body, headers=headers,
            **kwargs)

    def get_user(self, user_id, headers=None, **kwargs):
        return self._call_method(
            "GET",
            f"/v1/users/{user_id}",
            headers=headers, **kwargs)

    def delete_user(self, user_id, headers=None, **kwargs):
        return self._call_method(
            "DELETE",
            f"/v1/users/{user_id}",
            headers=headers, **kwargs)

class Catalog(BaseHttpClient):

    def __init__(self, url):
        super().__init__()
        self.url = url

    def get_product(self, product_id, headers=None, **kwargs):
        return self._call_method(
            "GET",
            f"/v1/products/{product_id}",
            headers=headers,
            **kwargs
        )

    def get_categories(self, headers=None, **kwargs ):
        return self._call_method(
            "GET",
            "/v1/categories",
            headers=headers,
            **kwargs
        )

    def get_categories_by_id(self, category_id, headers=None, **kwargs):
        return self._call_method(
            "GET",
            f"/v1/categories/{category_id}",
            headers=headers,
            **kwargs
        )

    def get_all_product(self, headers=None, **kwargs):
        return self._call_method(
            "GET",
            "/v1/products",
            headers=headers,
            **kwargs
        )


class Cart(BaseHttpClient):
    def __init__(self, url):
        super().__init__()
        self.url = url

    def get_user_cart(self, user_id, headers=None, **kwargs):
        return self._call_method(
            "GET",
            f"/v1/users/{user_id}/cart",
            headers=headers,
            **kwargs
        )


    def add_item(self, user_id, body, headers=None, **kwargs):
        return self._call_method(
            "POST",
            f"/v1/users/{user_id}/cart/items",
            json=body,
            headers=headers,
            **kwargs
        )


    def remove_item(self, user_id, product_id, headers=None, **kwargs):
        return self._call_method(
            "DELETE",
            f"/v1/users/{user_id}/cart/items/{product_id}",
            headers=headers,
            **kwargs
        )


    def delete_all_cart(self,user_id, headers=None, **kwargs):
        return self._call_method(
            "DELETE",
            f'/v1/users/{user_id}/cart',
            headers=headers,
            **kwargs
        )


    def add_promocode(self ,user_id, body, headers=None, **kwargs):
        return self._call_method(
            "POST",
            f"/v1/users/{user_id}/cart/promocode",
            json=body,
            headers=headers,
            **kwargs
        )


    def remove_promocode(self ,user_id, headers=None, **kwargs):
        return self._call_method(
            "DELETE",
            f"/v1/users/{user_id}/cart/promocode",
            headers=headers,
            **kwargs
        )



class Orders(BaseHttpClient):
    def __init__(self, url):
        super().__init__()
        self.url = url


    def post_order(self, body, headers=None, **kwargs):
        return self._call_method(
            "POST",
            f"/v1/orders",
            json=body,
            headers=headers,
            **kwargs
        )


    def get_order(self, order_id, headers=None, **kwargs):
        return self._call_method(
            "GET",
            f"/v1/orders/{order_id}",
            headers=headers,
            **kwargs
        )


    def cancel_order(self, order_id, headers=None, **kwargs):
        return self._call_method(
            "POST",
            f"/v1/orders/{order_id}/cancel",
            headers=headers,
            **kwargs
        )


    def order_status(self, order_id, body, headers=None, **kwargs):
        return self._call_method(
            "POST",
            f"/v1/orders/{order_id}/status",
            json=body,
            headers=headers,
            **kwargs
        )


    def delete_order(self, order_id, headers=None, **kwargs):
        return self._call_method(
            "DELETE",
            f"/v1/orders/{order_id}",
            headers=headers,
            **kwargs
        )


class Promo(BaseHttpClient):
    def __init__(self, url):
        super().__init__()
        self.url = url

# GET    /v1/admin/promocodes
# POST   /v1/admin/promocodes
# PATCH  /v1/admin/promocodes/{code}
# DELETE /v1/admin/promocodes/{code}

    def get_promo(self, headers=None, **kwargs):
        return self._call_method(
            "GET",
            f"/v1/admin/promocodes",
            headers=headers,
            **kwargs
        )


    def new_promo(self,headers=None, **kwargs):
        return self._call_method(
            "POST",
            f"/v1/admin/promocodes",
            headers=headers,
            **kwargs
        )


    def patch_promo(self,promo_id,headers=None, **kwargs):
        return self._call_method(
            "PATCH",
            f"/v1/admin/promocodes/{promo_id}",
            headers=headers,
            **kwargs
        )

    def delete_promo(self,promo_id,headers=None, **kwargs):
        return self._call_method(
            "DELETE",
            f"/v1/admin/promocodes/{promo_id}",
            headers=headers,
            **kwargs
        )





class HttpFacade:

    def __init__(self, url):
        self.__users = UserClient(url)
        self.__catalog = Catalog(url)
        self.__cart = Cart(url)
        self.__orders = Orders(url)


    @property
    def users(self):
        return self.__users

    @property
    def catalog(self):
        return self.__catalog

    @property
    def cart(self):
        return self.__cart

    @property
    def orders(self):
        return self.__orders



