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

def test_cart(driver):
    wait = WebDriverWait(driver, 15)
    for x in range(0, 3):
        driver.get("http://localhost/litecart/")
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR , ".product")))[0].click()

        box_product = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR , "#box-product")))[0]

        cart_item_quantity_element = driver.find_element(By.CSS_SELECTOR,"#cart-wrapper .quantity")
        cart_item_quantity = int(cart_item_quantity_element.text)
        print(cart_item_quantity)

        selectors = box_product.find_elements(By.CSS_SELECTOR , "select[name='options[Size]']")
        if (len(selectors) > 0):
            Select(selectors[0]).select_by_index(1)
        box_product.find_element(By.CSS_SELECTOR,"button[name=add_cart_product]").click()

        while int(cart_item_quantity_element.text) <= cart_item_quantity:
            time.sleep(0.5)

        print(int(cart_item_quantity_element.text))


    driver.find_element(By.XPATH,"//*[@id='cart-wrapper']//a[.//*[contains(@class,'quantity')]]").click()

    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR , "#customer-service-wrapper")))
    remove_buttons = driver.find_elements(By.CSS_SELECTOR , "button[name=remove_cart_item]")
    while len(remove_buttons) > 0:
        first_table_line = driver.find_elements(By.CSS_SELECTOR,".dataTable.rounded-corners tr:not(.header)")[0]
        wait.until(EC.visibility_of(remove_buttons[0])).click()
        wait.until(EC.staleness_of(first_table_line))
        remove_buttons = driver.find_elements(By.CSS_SELECTOR , "button[name=remove_cart_item]")

    time.sleep(3)