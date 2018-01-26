import time
import selenium.webdriver as webdriver
from selenium.webdriver.common.keys import Keys
from random import randrange


def scroll(url, lim):
    driver = webdriver.Firefox()
    # driver = webdriver.Chrome()
    driver.get(url)
    body = driver.find_element_by_tag_name('body')

    load_button = body.find_element_by_xpath('//a[contains(@class, "_1cr2e _epyes")]')
    body.send_keys(Keys.END)
    time.sleep(3)

    load_button.click()

    ind = 0
    while ind <= lim:
        print(ind)
        ind += 1
        body.send_keys(Keys.END)
        time.sleep(randrange(2, 5))

    print(driver.page_source)


if __name__ == '__main__':
    scroll('https://www.instagram.com/thalassografia/', 10)


