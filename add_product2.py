import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time
import os

@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd

def test_example(driver):
    driver.get("http://localhost/litecart/admin/")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()

    wait = WebDriverWait(driver, 15)
    menu_items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR , "#app- > a")))
    for x in range(0, len(menu_items)):
         if ('Catalog' in menu_items[x].text):
            menu_items[x].click()
            break

    add_buttons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR , "#content a.button")))
    for x in range(0, len(add_buttons)):
        if ('Product' in add_buttons[x].text):
            add_buttons[x].click()
            break

    product_name = 'pirog'
    product_code = 'ch001'
    product_image = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),'pirog.jpg'))

    tab_general = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#tab-general")))[0]
    tab_general.find_element(By.CSS_SELECTOR,"input[type=radio]").click()
    tab_general.find_element(By.CSS_SELECTOR,"input[name='name[en]']").send_keys(product_name)
    tab_general.find_element(By.CSS_SELECTOR,"input[name=code]").send_keys(product_code)
    quantity_field = tab_general.find_element(By.CSS_SELECTOR,"input[name=quantity]")
    quantity_field.clear()
    quantity_field.send_keys('3')

    sold_out_status = tab_general.find_element(By.CSS_SELECTOR,"select[name=sold_out_status_id]")
    selector = Select(sold_out_status)
    selector.select_by_visible_text('Temporary sold out')

    tab_general.find_element(By.CSS_SELECTOR,"input[name='new_images[]'").send_keys(product_image)

    time.sleep(5)