import pytest
from selenium import webdriver


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    wd.implicitly_wait(1)
    request.addfinalizer(wd.quit)
    return wd


def test_menu(driver):
    driver.get("http://localhost/litecart/admin/")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("remember_me").click()
    driver.find_element_by_name("login").click()

    menu = driver.find_elements_by_xpath("//ul[@id='box-apps-menu']//li[@id='app-']")
    for i in range(len(menu)):
        menu[i].click()
        h1 = driver.find_elements_by_xpath("//h1")
        if len(h1) == 0:
            print("Page hasn't elements h1")
        second = driver.find_elements_by_xpath("//li[@id='app-' and contains(@class, 'selected')]//li")
        if len(second) > 0:
            for k in range(len(second)):
                second[k].click()
                h1 = driver.find_elements_by_xpath("//h1")
                if len(h1) == 0:
                    print("Page hasn't elements h1")
                second = driver.find_elements_by_xpath("//li[@id='app-' and contains(@class, 'selected')]//li")
        menu = driver.find_elements_by_xpath("//ul[@id='box-apps-menu']//li[@id='app-']")