import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.get("http://localhost:8081")  # или какой у вас URL
    yield driver
    driver.quit()



# 1. Авторизация
# 2. Регистрация
# 3. Проверка неправильного ввода данных при авторизации
# 4. Проверка неправильного ввода данных при регистрации
# В кейсах должны быть проверки на успешную авторизацию и на появление сообщений об ошибках

# 1. Авторизация
def test_ui_registration(driver):
    driver.find_element(By.CSS_SELECTOR, '[data-testid="tab-register"]').click()
    driver.find_element(By.CSS_SELECTOR, '[data-testid="register-name"]').send_keys("Andrey")
    driver.find_element(By.CSS_SELECTOR, '[data-testid="login-email"]').send_keys("andr1e@mail.ru")
    driver.find_element(By.CSS_SELECTOR, '[data-testid="login-password"]').send_keys("pass123")
    driver.find_element(By.CSS_SELECTOR, '[data-testid="auth-submit"]').click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="nav-catalog"]'))
    )


# 2. Регистрация
def test_ui_login(driver):
    driver.find_element(By.CSS_SELECTOR, '[data-testid="tab-login"]').click()
    driver.find_element(By.CSS_SELECTOR, '[data-testid="login-email"]').send_keys("andr1e@mail.ru")
    driver.find_element(By.CSS_SELECTOR, '[data-testid="login-password"]').send_keys("pass123")
    driver.find_element(By.CSS_SELECTOR, '[data-testid="auth-submit"]').click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="nav-catalog"]'))
    )

# 3. Проверка неправильного ввода данных при авторизации
def test_ui_login_error(driver):
    driver.find_element(By.CSS_SELECTOR, '[data-testid="tab-login"]').click()
    driver.find_element(By.CSS_SELECTOR, '[data-testid="login-email"]').send_keys("323@mail.ru")
    driver.find_element(By.CSS_SELECTOR, '[data-testid="login-password"]').send_keys("pass123")
    driver.find_element(By.CSS_SELECTOR, '[data-testid="auth-submit"]').click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="auth-error"]'))
    )

# 4. Проверка неправильного ввода данных при регистрации
def test_ui_registration_error(driver):
    driver.find_element(By.CSS_SELECTOR, '[data-testid="tab-register"]').click()
    driver.find_element(By.CSS_SELECTOR, '[data-testid="register-name"]').send_keys("Andrey")
    driver.find_element(By.CSS_SELECTOR, '[data-testid="login-email"]').send_keys("andr1e@mail.ru")
    driver.find_element(By.CSS_SELECTOR, '[data-testid="login-password"]').send_keys("pass123")
    driver.find_element(By.CSS_SELECTOR, '[data-testid="auth-submit"]').click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="auth-error"]'))
    )

