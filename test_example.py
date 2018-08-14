import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture()
def driver(request):
    wd = webdriver.Chrome()

    def fin():
        wd.quit()
    request.addfinalizer(fin)
    return wd


def test_example(driver):
    driver.get("http://www.google.ru/")
    elem = driver.find_element_by_name("q")
    elem.send_keys("webdriver")
    elem.send_keys(Keys.RETURN)
    WebDriverWait(driver, 10).until(EC.title_is("webdriver - Поиск в Google"))