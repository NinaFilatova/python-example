import time
import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd


def test_example(driver):
    driver.get("http://localhost/litecart/")
    wait = WebDriverWait(driver, 15)
    products = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product")))
    number_of_products = len(products)
    print(number_of_products)
    for x in range(0, number_of_products):
        product = products[x]
        stickers = product.find_elements(By.CSS_SELECTOR, ".sticker")
        number_of_stickers = len(stickers)
        assert number_of_stickers == 1;
        print(stickers[0].text)
