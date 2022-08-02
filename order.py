import datetime
import pytz
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import config as cfg

current_time = datetime.datetime.now(pytz.timezone('America/New_York'))
timestamp = current_time.strftime("%d/%m/%y - %H:%M ")


def cash_text_to_float(text):
    try:
        new_text = text.replace("$", "").replace(",", "")
        return float(new_text)
    except (Exception,):
        print("Failed converting text to float.\n")
        print("Input text: \t", text)


class Order:
    def __init__(self, driver):
        self.driver = driver
        self.actions = ActionChains(driver)

    def clickout(self):
        self.driver.find_element(By.CSS_SELECTOR, "div.funds-cash").click()

    def set_order_ticker(self, ticker):
        self.driver.find_element(By.CSS_SELECTOR, "input#eq-ticket-dest-symbol").send_keys(ticker)
        self.driver.implicitly_wait(1)
        self.clickout()

    def set_order_buy(self):
        self.driver.find_element(By.CSS_SELECTOR, "label.pvd-segment__label[for=buy-segment]").click()
        self.driver.implicitly_wait(1)

    def set_order_sell(self):
        self.driver.find_element(By.CSS_SELECTOR, "label.pvd-segment__label[for=sell-segment]").click()
        self.driver.implicitly_wait(1)

    def set_order_amount(self, amount):
        self.driver.find_element(By.CSS_SELECTOR, "input#eqt-shared-quantity").send_keys(amount)
        self.driver.implicitly_wait(1)
        self.clickout()

    def set_order_dollars(self, amount):
        self.driver.find_element(By.CSS_SELECTOR, "label.pvd-segment__label[for=dollars-segment]").click()
        self.set_order_amount(amount)
        self.driver.implicitly_wait(1)
        self.clickout()

    def set_order_shares(self, amount):
        self.driver.find_element(By.CSS_SELECTOR, "label.pvd-segment__label[for=shares-segment]").click()
        self.set_order_amount(amount)
        self.driver.implicitly_wait(1)
        self.clickout()

    def set_order_market(self):
        self.driver.find_element(By.CSS_SELECTOR, "label.pvd-segment__label[for=market-yes-segment]").click()
        self.driver.implicitly_wait(1)

    def set_order_expiration(self, expiration_type):
        if expiration_type:
            self.driver.find_element(By.CSS_SELECTOR, "label.pvd-segment__label[for=pvd-segment-id-873531696156]").click()
        else:
            self.driver.find_element(By.CSS_SELECTOR, "label.pvd-segment__label[for=pvd-segment-id-487340035056]").click()

    def set_order_limit(self, limit_price, expiration_type):
        self.driver.find_element(By.CSS_SELECTOR, "label.pvd-segment__label[for=market-no-segment]").click()
        self.driver.find_element(By.CSS_SELECTOR, "input.dropdown-toggle[id=eqt-ordsel-limit-price-field").send_keys(limit_price)
        self.set_order_expiration(expiration_type)
        self.driver.implicitly_wait(1)
        self.clickout()

    def set_order_trade_type(self, trade_type):
        self.driver.implicitly_wait(2)
        if trade_type:
            self.set_order_buy()
        else:
            self.set_order_sell()
        self.driver.implicitly_wait(1)
        self.clickout()

    def set_order_trigger_type(self, trigger_type, limit_price, limit_expiration):
        self.driver.implicitly_wait(2)
        if trigger_type:
            self.set_order_market()
        else:
            self.set_order_limit(limit_price, limit_expiration)
        self.driver.implicitly_wait(1)
        self.clickout()

    def set_order_quantity_type(self, quantity, quantity_type):
        self.driver.implicitly_wait(2)
        if quantity < 0:
            self.set_order_shares(self.get_available_shares())
        elif quantity_type:
            self.set_order_shares(quantity)
        else:
            self.set_order_dollars(quantity)
        self.driver.implicitly_wait(1)
        self.clickout()

    def get_ticker_price(self):
        price = WebDriverWait(self.driver, timeout=10).until(
            (EC.visibility_of_element_located((By.CSS_SELECTOR, "span.last-price")))).text
        return cash_text_to_float(price)

    def get_total_cost(self):
        WebDriverWait(self.driver, timeout=10).until(
            (EC.text_to_be_present_in_element((By.CSS_SELECTOR, "span.eqt-commission__pricing-total-cost"), "$")))
        total = self.driver.find_element(By.CSS_SELECTOR, "span.eqt-commission__pricing-total-cost").text
        return cash_text_to_float(total)

    def get_available_cash(self):
        balance = WebDriverWait(self.driver, timeout=10).until(
            (EC.visibility_of_element_located((By.CSS_SELECTOR, "div.funds-cash")))).text
        return cash_text_to_float(balance)

    def get_available_shares(self):
        element = self.driver.find_element(By.ID, "shareAmount")
        self.actions.move_to_element(element).click().perform()
        owned = WebDriverWait(self.driver, timeout=10).until(
            (EC.visibility_of_element_located((By.CSS_SELECTOR, "div.eqt-quantity__dropdownlist__item__field")))).text
        return float(owned)

    def print_trade_error(self):
        error_msg = self.driver.find_element(By.CSS_SELECTOR, "div.pvd-inline-alert__content").text
        print(timestamp + error_msg + '\n')

    def submit_order(self):
        self.click_preview_order()
        try:
            WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "h2.pvd-modal__heading")))
            self.print_trade_error()
            exit()
        except TimeoutException:
            WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button#placeOrderBtn"))).click()
            WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span#order-reveived-lable")))
            print(timestamp + "Order Success.\n")
            exit()

    def click_preview_order(self):
        self.driver.find_element(By.CSS_SELECTOR, "pvd3-button#previewOrderBtn").click()
        self.driver.implicitly_wait(2)

    def create_trade(self, ticker, trade_type, quantity, quantity_type, trade_trigger_type=True, limit_price=0, limit_expiration=True):
        self.driver.get(
            "https://digital.fidelity.com/ftgw/digital/trade-equity/index?FRAME_LOADED=Y&NAVBAR=Y&ACCOUNT={account_id}".format(
                account_id=cfg.account["id"]))
        self.set_order_ticker(ticker)
        self.set_order_trade_type(trade_type)
        self.set_order_quantity_type(quantity, quantity_type)
        self.set_order_trigger_type(trade_trigger_type, limit_price, limit_expiration)
        self.submit_order()
