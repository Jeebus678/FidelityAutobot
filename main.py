import order as order
import config as cfg
from time import sleep
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains

chromedriver_autoinstaller.install()

driver = webdriver.Chrome(options=cfg.chrome_options, service=Service())
actions = ActionChains(driver)


def agree_tos():
    try:
        WebDriverWait(driver, 5).until((EC.element_to_be_clickable((By.CSS_SELECTOR, "a.accept-link")))).click()
    except:
        return


def login_fidelity():
    driver.get(
        "https://digital.fidelity.com/prgw/digital/login/full-page?AuthRedUrl=https://oltx.fidelity.com/ftgw/fbc/ofsummary/defaultPage")
    # agree_tos()
    WebDriverWait(driver, 30).until((EC.element_to_be_clickable((By.CSS_SELECTOR, "input#userId-input")))).send_keys(
        cfg.account["user"])
    driver.implicitly_wait(1)
    driver.find_element(By.CSS_SELECTOR, "input#password").send_keys(cfg.account["pass"])
    driver.implicitly_wait(1)
    driver.find_element(By.CSS_SELECTOR, "button#fs-login-button").submit()


login_fidelity()
sleep(5)
Orders = order.Order(driver)
Orders.create_trade("GME", "buy", 1, "shares")
