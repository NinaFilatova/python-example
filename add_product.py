import pytest
from selenium import webdriver
import random
from selenium.webdriver.support.ui import Select


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    wd.implicitly_wait(1)
    request.addfinalizer(wd.quit)
    return wd


def test_countries(driver):
    driver.get("http://localhost/litecart/admin/")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("remember_me").click()
    driver.find_element_by_name("login").click()

    menu = driver.find_elements_by_xpath("//ul[@id='box-apps-menu']//li[@id='app-']")
    menu[1].click()
    table = driver.find_element_by_css_selector(".dataTable")
    rows = table.find_elements_by_xpath("//tr[contains(@class,'row')]")
    start_list = len(rows)

    buttons = driver.find_elements_by_css_selector("a.button")
    buttons[1].click()

    name = "item" + str(random.randint(1,999))
    code = str(random.randint(1,999))
    keywords = "fairy cake"
    short_description = "fairy cake"
    description = "fairy cake"
    head_title = "fairy cake"
    meta_description = "fairy cake"

    #General
    driver.find_element_by_css_selector("input[type=radio][value='1']").click()
    driver.find_element_by_css_selector("input[name='name[en]']").send_keys(name)
    driver.find_element_by_css_selector("input[name='code']").send_keys(code)
    driver.find_element_by_css_selector("input[type='checkbox'][name='product_groups[]'][value='1-2']").click()
    driver.find_element_by_css_selector("input[type='number'][name='quantity']").click()
    driver.find_element_by_css_selector("input[type='number'][name='quantity']").clear()
    driver.find_element_by_css_selector("input[type='number'][name='quantity']").send_keys("19,99")
    #загрузка изображения
    driver.find_element_by_css_selector("input[type='file'][name='new_images[]']").send_keys("C:\\sel\\767.jpg")

    #Information
    driver.find_element_by_xpath("//a[contains(text(),'Information')]").click()
    Select(driver.find_element_by_css_selector("select[name='manufacturer_id']")).select_by_visible_text("ACME Corp.")
    driver.find_element_by_css_selector("input[name='keywords']").send_keys(keywords)
    driver.find_element_by_css_selector("input[name='short_description[en]']").send_keys(short_description)
    driver.find_element_by_css_selector("div.trumbowyg-editor").send_keys(description)
    driver.find_element_by_css_selector("input[name='head_title[en]']").send_keys(head_title)
    driver.find_element_by_css_selector("input[name='meta_description[en]']").send_keys(meta_description)

    #Prices
    driver.find_element_by_xpath("//a[contains(text(),'Prices')]").click()
    driver.find_element_by_css_selector("input[type='number'][name='purchase_price']").click()
    driver.find_element_by_css_selector("input[type='number'][name='purchase_price']").clear()
    driver.find_element_by_css_selector("input[type='number'][name='purchase_price']").send_keys("1,99")
    Select(driver.find_element_by_css_selector("select[name='purchase_price_currency_code']")).select_by_visible_text("US Dollars")
    driver.find_element_by_css_selector("input[type='text'][name='prices[USD]']").send_keys("1,99")
    driver.find_element_by_css_selector("input[type='number'][name='gross_prices[USD]']").click()
    driver.find_element_by_css_selector("input[type='number'][name='gross_prices[USD]']").clear()
    driver.find_element_by_css_selector("input[type='number'][name='gross_prices[USD]']").send_keys("0,99")
    driver.find_element_by_css_selector("input[type='text'][name='prices[EUR]']").send_keys("1,99")
    driver.find_element_by_css_selector("input[type='number'][name='gross_prices[EUR]']").click()
    driver.find_element_by_css_selector("input[type='number'][name='gross_prices[EUR]']").clear()
    driver.find_element_by_css_selector("input[type='number'][name='gross_prices[EUR]']").send_keys("0,09")

    #сохранение
    driver.find_element_by_css_selector("button[type='submit'][name='save']").click()

    #проверка каталоге
    driver.get("http://localhost/litecart/admin/?app=catalog&doc=catalog")
    table = driver.find_element_by_css_selector(".dataTable")
    rows = table.find_elements_by_xpath("//tr[contains(@class,'row')]")
    if len(rows) == start_list+1:
        print("Changes were successfully saved.")
    else:
        print("Error")
