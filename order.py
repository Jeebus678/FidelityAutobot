import config as cfg
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains as actions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def cash_text_to_float(text):
    try:
        new_text = text.replace("$", "").replace(",", "")
        return float(new_text)
    except:
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
        self.driver.find_element(By.CSS_SELECTOR, "label.eq-ticket__action-toggle[for=action-buy]").click()
        self.driver.implicitly_wait(1)

    def set_order_sell(self):
        self.driver.find_element(By.CSS_SELECTOR, "label.eq-ticket__action-toggle[for=action-sell]").click()
        self.driver.implicitly_wait(1)

    def set_order_amount(self, amount):
        self.driver.find_element(By.CSS_SELECTOR, "input#eqt-shared-quantity").send_keys(amount)
        self.driver.implicitly_wait(1)

    def set_order_dollars(self, amount):
        self.driver.find_element(By.CSS_SELECTOR, "label.eq-ticket-toggle-button[for=quantity-type-dollars]").click()
        self.set_order_amount(amount)
        self.clickout()
        self.driver.implicitly_wait(1)

    def set_order_shares(self, amount):
        self.driver.find_element(By.CSS_SELECTOR, "label.eq-ticket-toggle-button[for=quantity-type-shares]").click()
        self.set_order_amount(amount)
        self.clickout()
        self.driver.implicitly_wait(1)

    def set_order_market(self):
        self.driver.find_element(By.CSS_SELECTOR, "label.eq-ticket__ordertype-toggle[for=market-yes]").click()
        self.driver.implicitly_wait(1)

    def set_order_limit(self, limit_price, expiration_type):
        self.driver.find_element(By.CSS_SELECTOR, "label.eq-ticket__ordertype-toggle[for=market-no]").click()
        self.driver.find_element(By.CSS_SELECTOR, "input.dropdown-toggle[id=eqt-ordsel-limit-price-field").send_keys(
            limit_price)
        self.driver.find_element(By.CSS_SELECTOR,
                                 "label.eq-ticket__action-toggle.eq-ticket-toggle-button[for=action-{operator}]".format(
                                     operator=expiration_type)).click()
        self.driver.implicitly_wait(1)

    def set_order_trade_type(self, trade_type):
        self.driver.implicitly_wait(2)
        if trade_type:
            self.set_order_buy()
        else:
            self.set_order_sell()

    def set_order_trigger_type(self, trigger_type, limit_price=0, limit_expiration="day"):
        self.driver.implicitly_wait(2)
        if trigger_type:
            self.set_order_market()
        else:
            self.set_order_limit(limit_price, limit_expiration)

    def set_order_quantity_type(self, quantity, quantity_type):
        self.driver.implicitly_wait(2)
        if quantity_type:
            self.set_order_shares(quantity)
        else:
            self.set_order_dollars(quantity)

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

    def click_preview_order(self):
        self.driver.implicitly_wait(2)
        self.driver.find_element(By.CSS_SELECTOR, "pvd3-button#previewOrderBtn").click()

    def trade_error(self, trade_type):
        quantity_type = "cash"
        balance = "$" + str(self.get_available_cash())
        if not trade_type:
            quantity_type = "shares"
            balance = self.get_available_shares()
        print("\nNot enough {quantity_type} on balance to execute order. See Details: \n".format(
            quantity_type=quantity_type, trade_type=trade_type))
        print("Order total: ${:.2f}\n".format(self.get_total_cost()))
        print("{quantity_type} on balance: {balance}\n".format(
            quantity_type=quantity_type[0].upper() + quantity_type[1:],
            balance=balance))
        if quantity_type == "shares":
            print("Total position: ${:.2f}\n".format(balance * self.get_ticker_price()))

    def test_order(self, trade_type):
        if trade_type:
            return self.get_available_cash() >= self.get_total_cost()
        else:
            return self.get_available_shares() * self.get_ticker_price() >= self.get_total_cost()

    def execute_trade(self, trade_type):
        if self.test_order(trade_type):
            self.click_preview_order()
            print("{trade_type} order executed.".format(trade_type=trade_type[0].upper() + trade_type[1:]))
        else:
            return False

    def create_trade(self, ticker, trade_type, quantity, quantity_type, trade_trigger_type="market", limit_price=0, limit_expiration="day"):
        self.driver.get(
            "https://digital.fidelity.com/ftgw/digital/trade-equity/index?FRAME_LOADED=Y&NAVBAR=Y&ACCOUNT={account_id}".format(
                account_id=cfg.account["id"]))
        self.set_order_ticker(ticker)
        self.set_order_trade_type(trade_type)
        self.set_order_trigger_type(trade_trigger_type, limit_price, limit_expiration)
        self.set_order_quantity_type(quantity, quantity_type)
        if not self.execute_trade(trade_type):
            self.trade_error(trade_type)
