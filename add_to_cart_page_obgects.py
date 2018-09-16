import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time

@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd

class MainPage:
    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get("http://localhost/litecart/")
        return self

    def open_first_product(self):
        self.driver.find_elements(By.CSS_SELECTOR , ".product")[0].click()

class CartElement:
    def __init__(self, driver):
        self.cart_element = driver.find_element(By.CSS_SELECTOR , "#cart-wrapper")

    def get_counter(self):
        cart_item_quantity_element = self.cart_element.find_element(By.CSS_SELECTOR,".quantity")
        return int(cart_item_quantity_element.text)

    def go_cart(self):
        self.cart_element.find_element(By.XPATH,".//a[.//*[contains(@class,'quantity')]]").click()

class ProductElement:
    def __init__(self, driver):
        self.wait = WebDriverWait(driver, 10)
        self.box_product = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR , "#box-product")))[0]

    def add_to_cart(self):
        selectors = self.box_product.find_elements(By.CSS_SELECTOR , "select[name='options[Size]']")
        if (len(selectors) > 0):
            Select(selectors[0]).select_by_index(1)
        self.box_product.find_element(By.CSS_SELECTOR,"button[name=add_cart_product]").click()

class CartPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def self_test(self):
        self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR , "#customer-service-wrapper")))
        return self

    def remove_all_products(self):
        remove_buttons = self.driver.find_elements(By.CSS_SELECTOR , "button[name=remove_cart_item]")
        while len(remove_buttons) > 0:
            first_table_line = \
                self.driver.find_elements(By.CSS_SELECTOR,".dataTable.rounded-corners tr:not(.header)")[0]
            self.wait.until(EC.visibility_of(remove_buttons[0])).click()
            self.wait.until(EC.staleness_of(first_table_line))
            remove_buttons = self.driver.find_elements(By.CSS_SELECTOR , "button[name=remove_cart_item]")

def test_cart(driver):
    for x in range(0, 3):
        MainPage(driver).open().open_first_product()
        cart_item_quantity = CartElement(driver).get_counter()
        ProductElement(driver).add_to_cart()
        while CartElement(driver).get_counter() <= cart_item_quantity:
            time.sleep(0.5)
    CartElement(driver).go_cart()
    CartPage(driver).self_test().remove_all_products()
    time.sleep(3)