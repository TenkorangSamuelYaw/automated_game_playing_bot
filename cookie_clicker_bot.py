from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

URL = "http://orteil.dashnet.org/experiments/cookie/"
#  time.time() is the point where time starts.
timeout = time.time() + (60 * 5)  # 5 min from now.
click_timeout = time.time() + 10  # 5 secs from now.
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(url=URL)
cookie = driver.find_element(by=By.ID, value="cookie")
#  Get the id for all items.
items = driver.find_elements(by=By.CSS_SELECTOR, value="#store div")
item_ids = [item.get_attribute("id") for item in items]

#  Get the price for all items.
prices = driver.find_elements(by=By.CSS_SELECTOR, value="#store b")

while True:
    cookie.click()
    if time.time() > click_timeout:
        #  Get the price for all items as an integer.
        try:
            item_prices = [int(price.text.split("-")[1].strip().replace(",", "")) for price in prices if price.text != ""]
        except NoSuchElementException:
            print("There are no items on the page.")

        #  Create a dictionary of store items and prices
        cookie_upgrades = {item_prices[n]: item_ids[n] for n in range(len(item_prices))}

        #  Get current cookie count
        cookie_money = driver.find_element(by=By.ID, value="money").text
        if "," in cookie_money:
            cookie_money.replace(",", "")
        cookie_count = int(cookie_money)

        #  Find upgrades that we can currently afford
        affordable_upgrades = {cost: item_id for cost, item_id in cookie_upgrades.items() if cookie_count > cost}

        #  Purchase the most expensive affordable upgrade
        highest_affordable_price = max(affordable_upgrades.keys())
        print(highest_affordable_price)
        #  highest_affordable_price is now a key.
        id_to_purchase_upgrade = affordable_upgrades[highest_affordable_price]
        driver.find_element(by=By.ID, value=id_to_purchase_upgrade).click()

        #  Add another 5 secs until the next check
        click_timeout = time.time() + 5

    #  After 5 min stop the bot and print the cookies per second count.
    if time.time() > timeout:
        cookie_per_sec = driver.find_element(by=By.ID, value="cps").text
        print(cookie_per_sec)
        break
driver.quit()
