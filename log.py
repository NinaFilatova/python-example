import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def introduce_error(drw):
    drw.execute_script("setTimeout(function() { throw \"lalala\"; }, 1000);")
    time.sleep(2)


def test_example(driver):
    driver.get("http://localhost/litecart/admin/")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()

    wait = WebDriverWait(driver, 15)
    driver.get("http://localhost/litecart/admin/?app=catalog&doc=catalog&category_id=1")
    product_links = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//form[@name='catalog_form']//a[./../..//input[contains(@name,'product')] and not(./i)]")))

    for x in range(0, len(product_links)):
        product_links[x].click()
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"#tab-general")))
        browser_log = driver.get_log("browser")
        for l in browser_log:
            print(l)
        if (len(browser_log)):
            assert(False),'somthing in browser log'
        driver.get("http://localhost/litecart/admin/?app=catalog&doc=catalog&category_id=1")
        product_links = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//form[@name='catalog_form']//a[./../..//input[contains(@name,'product')] and not(./i)]")))

    time.sleep(3)