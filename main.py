import order as order
import config as cfg
from time import sleep
import argparse
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


chromedriver_autoinstaller.install()

driver = webdriver.Chrome(options=cfg.chrome_options, service=Service())


cli_parser = argparse.ArgumentParser(description="A program for creating fidelity orders.")

cli_parser.add_argument('-T', '--ticker',
                        type=str)

cli_parser.add_argument('-q', '--quantity',
                        type=int)

order_type = cli_parser.add_mutually_exclusive_group()
order_type.add_argument('-b', '--buy',
                        dest='buy',
                        action='store_true')

order_type.add_argument('-s', '--sell',
                        dest='buy',
                        action='store_false')

unit = cli_parser.add_mutually_exclusive_group()
unit.add_argument('-S', '--shares',
                  dest='shares',
                  action='store_true')

unit.add_argument('-D', '--dollars',
                  dest='shares',
                  action='store_false')

execution_type = cli_parser.add_mutually_exclusive_group()
execution_type.add_argument('-m', '--market',
                            dest='market',
                            action='store_true')

execution_type.add_argument('-l', '--limit',
                            dest='market',
                            action='store_false')


# cli_parser.add_argument('--limit_price', '-Lp',
#                         default=False,
#                         type=str,
#                         action='store_true')
#
# cli_parser.add_argument('--expiration', '-E',
#                         default=False,
#                         type=str,
#                         action='store_true',
#                         help='Expiration for the limit. [GTC or day]')


# def agree_tos():
#     try:
#         WebDriverWait(driver, 5).until((EC.element_to_be_clickable((By.CSS_SELECTOR, "a.accept-link")))).click()
#     except:
#         return


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


args = cli_parser.parse_args()
Orders = order.Order(driver)

if __name__ == '__main__':
    login_fidelity()
    sleep(5)
    Orders.create_trade(args.ticker, args.buy, args.quantity, args.shares)
