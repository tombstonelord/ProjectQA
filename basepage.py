


class BasePage:

    def __init__(self, page):
        self.page = page
        self.base_url = "localhost:8081"

    def open(self, path: str = ""):
        url = f"{self.base_url}{path}"
        self.page.goto(url)

    def click_element(self, locator):
        locator.click()

    def fill_text_area(self, locator: str, text: str):
        locator.fill(text)


class LoginPage(BasePage):

    def __init__(self, page ):
        super().__init__(page)


        self.register_button = page.get_by_test_id("tab-register")
        self.username_input = page.get_by_test_id("register-name")
        self.password_input = page.get_by_test_id("login-password")
        self.mail_input=page.get_by_test_id("login-email")
        self.submit_button_login = page.get_by_role("button", name="Войти")
        self.submit_button_register =page.get_by_test_id("auth-submit")
        self.login_button=page.get_by_test_id("tab-login")
        self.logout_button=page.get_by_test_id("logout-button")
        self.auth_error=page.get_by_test_id("auth-error")
        self.path = "/login"

    def open_login_page(self):
        self.open(self.path)

    def register(self, name, mail, password):
        self.click_element(self.register_button)
        self.fill_text_area(self.username_input, name)
        self.fill_text_area(self.mail_input, mail)
        self.fill_text_area(self.password_input, password)
        self.click_element(self.submit_button_register)

    def login(self, mail, password):
        self.fill_text_area(self.mail_input, mail)
        self.fill_text_area(self.password_input, password)
        self.click_element(self.submit_button_register)


class CatalogPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.search_bar = page.get_by_test_id("catalog-search")
        self.path = "/catalog"
        self.cart_button=page.get_by_test_id('nav-cart')

    def add_to_cart(self, product_name):
        self.fill_text_area(self.search_bar, product_name)
        card = self.page.locator(
            "[data-testid='product-card']",
            has_text=product_name
        ).first
        card.wait_for(state="visible")
        card.get_by_role("button", name="В корзину").click()
        self.search_bar.fill("")




class CartPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.order_button = page.get_by_test_id("checkout-button")
        self.promo_input = page.get_by_test_id("promo-input")
        self.promo_confirm=page.get_by_test_id("promo-apply")
        self.del_promo=page.get_by_test_id("promo-clear")
        self.toast=page.get_by_test_id("toast")
        self.clear_cart_button = page.get_by_test_id("clear-cart-button")
        self.cart_items = page.get_by_test_id('cart-item')
        self.item_name = page.get_by_test_id('cart-item-name')
        self.item_price= page.get_by_test_id('cart-item-line-total')
        self.subtotal_price = page.get_by_test_id('cart-subtotal')
        self.cart_discount=page.get_by_test_id('cart-discount')
        self.cart_prise=page.get_by_test_id('cart-item-line-total')
        self.cart_item_qty=page.get_by_test_id('cart-item-qty')
        self.total_price=page.get_by_test_id('cart-total')
        self.combo_flag=page.get_by_test_id("combo-flag")
        self.applied_promo=page.get_by_test_id("applied-promo")
        self.clear_cart_button=page.get_by_test_id("clear-cart-button")
        self.cart_empty=page.get_by_test_id("cart-empty")

    def get_subtotal_cents(self):
        return self.parse_money(self.subtotal_price.inner_text())

    def get_discount_cents(self):
        return self.parse_money(self.cart_discount.inner_text())

    def get_total_cents(self):
        return self.parse_money(self.total_price.inner_text())

    def use_promo(self,promo):
        self.fill_text_area(self.promo_input, promo)
        self.click_element(self.promo_confirm)

    def remove_promo(self):
        self.click_element(self.del_promo)


    def remove_item_by_name(self, product_name: str):
        card = self.cart_items.filter(
            has=self.page.get_by_test_id("cart-item-name").filter(has_text=product_name)
        ).first
        card.get_by_test_id("remove-item").click()



    def parse_money(self, text: str) -> int:
        cleaned = (
            text.replace("$", "")
            .replace("\xa0", "")  # неразрывный пробел
            .replace(" ", "")  # обычный пробел
            .replace(",", ".")
        )
        return int(float(cleaned) * 100)



    def get_items(self):
        result = []
        count = self.cart_items.count()
        for i in range(count):
            card = self.cart_items.nth(i)
            name = card.get_by_test_id("cart-item-name").inner_text()
            qty = int(card.get_by_test_id("cart-item-qty").inner_text())
            line_total_text = card.get_by_test_id("cart-item-line-total").inner_text()
            line_total_cents = self.parse_money(line_total_text)

            result.append({
                "name": name,
                "quantity": qty,
                "line_total": line_total_cents,
            })
        return result



class OrderPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.self_pickup = page.get_by_role("button", name="Самовывоз")
        self.courier_delivery = page.get_by_role("button", name="Курьер")
        self.go_to_pay = page.get_by_role("button", name="К оплате")
        self.pickup_options = page.get_by_test_id("pickup-option")
        self.card_pan=page.get_by_test_id("card-pan")
        self.card_expiry=page.get_by_test_id("card-expiry")
        self.card_cvc=page.get_by_test_id("card-cvc")
        self.card_holder=page.get_by_test_id("card-holder")
        self.pay_button=page.get_by_test_id("pay-button")
        self.threeds_otp=page.get_by_test_id("threeds-otp")
        self.threeds_otp_hint=page.get_by_test_id("threeds-otp-hint")
        self.threeds_confirm = page.get_by_role("button", name="Подтвердить")
        self.orders_placed_notice= page.get_by_test_id("orders-placed-notice")
        self.orders_list = page.get_by_test_id("orders-page")



    def select_self_pickup_address(self, text):
        address = self.pickup_options.filter(has_text=text).first
        address.wait_for(state="visible", timeout=10000)
        address.click()


    def fill_card_data(self, card_pan,card_expiry, card_cvc,cc_name ):
        self.fill_text_area(self.card_pan, card_pan)
        self.fill_text_area(self.card_expiry, card_expiry)
        self.fill_text_area(self.card_cvc, card_cvc)
        self.card_holder.clear()
        self.fill_text_area(self.card_holder, cc_name)
        self.pay_button.click()

    def sms_code(self):
        self.threeds_otp_hint.wait_for(state="visible", timeout=10000)
        return self.threeds_otp_hint.locator("strong").inner_text()

    def confirm_sms_code(self):
        code = self.sms_code()
        self.fill_text_area(self.threeds_otp, code)
        self.threeds_confirm.click()

    def get_order_id_from_notice(self):
        self.orders_placed_notice.wait_for(state="visible", timeout=10000)
        return self.orders_placed_notice.get_attribute("data-order-id")

    def has_order_in_list(self, order_id) :
        short_id = order_id[:8]
        order_card = self.page.locator(
            "[data-testid='order-card']",
            has_text=short_id
        )
        return order_card.count() > 0


























