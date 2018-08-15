import pytest
from selenium import webdriver


@pytest.fixture()
def driver(request):
    wd = webdriver.Chrome()
    wd.implicitly_wait(10)

    def fin():
        wd.quit()
    request.addfinalizer(fin)
    return wd


def test_login(driver):
    open_home_page(driver)
    username = "admin"
    password = "admin"
    login(driver, username, password)
    assert ("You are now logged in as %s" % username in driver.page_source)


def login(driver, username, password):
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_name("login").click()


def open_home_page(driver):
    driver.get("http://localhost/litecart/admin/")