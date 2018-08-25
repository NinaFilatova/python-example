import time
import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

@pytest.fixture
def driver(request):
    # 1) Chrome:
    wd = webdriver.Chrome()

    # 2) Firefox:
    # wd = webdriver.Firefox()

    # 3) Edge:
    # wd = webdriver.Edge()

    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd

def get_rgba_array(rgba_string):
    # Simpler way?
    rgba_string = rgba_string.split('(')[1]
    rgba_string = rgba_string.split(')')[0]
    rgba_array = rgba_string.split(',')
    for x in range(0, len(rgba_array)):
        rgba_array[x] = int(rgba_array[x])
    return rgba_array

def style_check(old_price_element,new_price_element):
    # How to check stroke and bold styles in any browser? I cannot find text-decoration for stroke in FF.
    # So I use "s"-tag for stroke and "strong"-tag for bold checks

    # check grey:
    old_price_color = old_price_element.value_of_css_property("color")
    print(old_price_color)
    old_price_color = get_rgba_array(old_price_color)
    assert old_price_color[0] == old_price_color[0]
    assert old_price_color[1] == old_price_color[2]

    # check red:
    new_price_color = new_price_element.value_of_css_property("color")
    print(new_price_color)
    new_price_color = get_rgba_array(new_price_color)
    assert new_price_color[0] > 0
    assert new_price_color[1] == 0
    assert new_price_color[2] == 0

    # compare size, namely the height
    old_price_size = old_price_element.size
    print(old_price_size)
    new_price_size = new_price_element.size
    print(new_price_size)
    assert old_price_size['height'] < new_price_size['height']


def test_campaigns(driver):
    wait = WebDriverWait(driver, 15)
    driver.get("http://localhost/litecart/")
    product = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#box-campaigns li")))[0]
    link = product.find_element(By.CSS_SELECTOR,"a.link")
    name_element = product.find_element(By.CSS_SELECTOR,".name")
    regular_price_element = product.find_element(By.CSS_SELECTOR,"s.regular-price")
    campaign_price_element = product.find_element(By.CSS_SELECTOR,"strong.campaign-price")

    name = name_element.text
    print(name)
    regular_price = regular_price_element.text
    print(regular_price)
    campaign_price = campaign_price_element.text
    print(campaign_price)

    style_check(regular_price_element,campaign_price_element)

    # Go to the product page:
    link.click()
    product = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#box-product")))[0]
    name_element = product.find_element(By.CSS_SELECTOR,"[itemprop=name]")
    regular_price_element = product.find_element(By.CSS_SELECTOR,"s.regular-price")
    campaign_price_element = product.find_element(By.CSS_SELECTOR,"strong.campaign-price")

    assert name == name_element.text
    print(name)
    assert regular_price == regular_price_element.text
    print(regular_price)
    assert campaign_price == campaign_price_element.text
    print(campaign_price)

    style_check(regular_price_element,campaign_price_element)