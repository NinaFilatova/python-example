import pytest
from selenium import webdriver
import time

@pytest.fixture
def driver(request):
    wd = webdriver.Firefox()
    wd.implicitly_wait(5)
    request.addfinalizer(wd.quit)
    return wd


def test_cart(driver):
    driver.get(
        "https://multivarka.pro/catalog/umnye-chajniki-i-termopoty/umnyy-chayniksvetilnik-redmond-skykettle-g201s/")
    driver.find_element_by_xpath("//form[@id='no-colors-form']//button[.='В КОРЗИНУ']").click()


time.sleep(3)

