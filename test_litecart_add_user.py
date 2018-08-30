from random import randint
import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_campaigns(driver):
    wait = WebDriverWait(driver, 15)

    password = str(randint(1000, 9999))
    login = 'test' + password
    print(login + ':' + password)

    #  registration form
    driver.get("http://localhost/litecart/")
    product = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#box-account-login tr")))[4]
    link = product.find_element(By.CSS_SELECTOR, "a")
    link.click()

    # Fill the form
    account_box = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#create-account.box")))[0]

    account_box.find_element(By.CSS_SELECTOR, "input[name=firstname]").send_keys(login)
    account_box.find_element(By.CSS_SELECTOR, "input[name=lastname]").send_keys(login)
    account_box.find_element(By.CSS_SELECTOR, "input[name=address1]").send_keys('mbmbmb')
    account_box.find_element(By.CSS_SELECTOR, "input[name=postcode]").send_keys('89896')
    account_box.find_element(By.CSS_SELECTOR, "input[name=city]").send_keys('hghghgh')

    country_selector = account_box.find_element(By.CSS_SELECTOR, "#create-account.box select[name=country_code]")
    selector = Select(country_selector)
    selector.select_by_visible_text('United States')

    state_selector = account_box.find_element(By.CSS_SELECTOR, "#create-account.box select[name=zone_code]")
    wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#create-account.box select[name=zone_code] option")))

    selector = Select(state_selector)
    selector.select_by_visible_text('Kansas')

    account_box.find_element(By.CSS_SELECTOR, "input[name=email]").send_keys(login + '@test.com')
    account_box.find_element(By.CSS_SELECTOR, "input[name=phone]").send_keys(Keys.HOME + "888888888")
    account_box.find_element(By.CSS_SELECTOR, "input[name=password]").send_keys(password)
    account_box.find_element(By.CSS_SELECTOR, "input[name=confirmed_password]").send_keys(password)
    account_box.find_element(By.CSS_SELECTOR, "button[name=create_account]").click()

    #  logout
    account_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#navigation #box-account li a")))
    account_links[3].click()

    # Login
    login_form = \
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#navigation form[name=login_form]")))[0]
    login_form.find_element(By.CSS_SELECTOR, "input[name=email]").send_keys(login + '@test.com')
    login_form.find_element(By.CSS_SELECTOR, "input[name=password]").send_keys(password)
    login_form.find_element(By.CSS_SELECTOR, "button[name=login]").click()

    # 2d logout
    account_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#navigation #box-account li a")))
    account_links[3].click()