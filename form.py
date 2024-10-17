import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def fillForm(name, email):

    # installing chrome driver if not available
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://tally.so/r/waDMG2")
    driver.implicitly_wait(0.5)

    name_element = driver.find_element_by_id("e729bd5e-3362-4712-823c-9b426dcb0610")
    name_element.send_keys(name)
    email_element = driver.find_element_by_id("9271d54a-c70b-4375-ac4b-7ad4502d321d")
    email_element.send_keys(email)
    button_element = driver.find_element_by_class_name("sc-5b8353b7-1")
    button_element.click()

    time.sleep(5)

    driver.quit()

"""
NOTE: 

I just like to add comments for my own readability and debugging,
it's not GPT code :)
"""
