from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

class BasePage:
    def __init__(self, driver, timeout=30):
        self.driver = driver
        self.w = WebDriverWait(driver, timeout)

    def open(self, url):
        self.driver.get(url)

    def el(self, locator):
        return self.w.until(EC.presence_of_element_located(locator))

    def els(self, locator):
        return self.w.until(EC.presence_of_all_elements_located(locator))

    def visible(self, locator):
        return self.w.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        self.w.until(EC.element_to_be_clickable(locator)).click()

    def js_click(self, locator):
        e = self.visible(locator)
        self.driver.execute_script("arguments[0].click()", e)

    def scroll_into_view(self, locator):
        e = self.el(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'})", e)

    def hover(self, locator):
        e = self.visible(locator)
        ActionChains(self.driver).move_to_element(e).perform()

    def click_any(self, locators):
        for by, val in locators:
            try:
                self.w.until(EC.element_to_be_clickable((by, val))).click()
                return True
            except:
                try:
                    e = self.driver.find_element(by, val)
                    self.driver.execute_script("arguments[0].click()", e)
                    return True
                except:
                    pass
        raise AssertionError("Locator not clickable")

    def click_element(self, element):
        try:
            self.w.until(EC.element_to_be_clickable(element)).click()
        except:
            try:
                ActionChains(self.driver).move_to_element(element).pause(0.2).click().perform()
            except:
                self.driver.execute_script("arguments[0].click()", element)

    def click_text_any(self, texts):
        for txt in texts:
            xpath = f"//*[self::button or self::summary or self::div or self::li or self::label or self::span][contains(normalize-space(),'{txt}')]"
            els = self.driver.find_elements(By.XPATH, xpath)
            if els:
                el = els[0]
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'})", el)
                self.click_element(el)
                return True
        return False

    def exists_any(self, locators):
        for by, val in locators:
            try:
                self.driver.find_element(by, val)
                return True
            except:
                pass
        return False

    def find_all_present_any(self, locators):
        for by, val in locators:
            els = self.driver.find_elements(by, val)
            if els:
                return els
        return []

    def wait_url_contains(self, part):
        self.w.until(EC.url_contains(part))

    def wait_new_tab_and_switch(self, expected_url_part=None):
        h = len(self.driver.window_handles)
        self.w.until(lambda d: len(d.window_handles) > h)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        if expected_url_part:
            self.wait_url_contains(expected_url_part)

