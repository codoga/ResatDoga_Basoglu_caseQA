from selenium.webdriver.common.by import By
from .base_page import BasePage

class HomePage(BasePage):
    URL="https://useinsider.com/"
    COMPANY_MENU=(By.XPATH,"//nav//*[self::a or self::button][normalize-space()='Company' or normalize-space()='Şirket']")
    CAREERS_IN_MENU=(By.XPATH,"//nav//a[contains(@href,'/careers') or normalize-space()='Careers' or normalize-space()='Kariyer']")
    CAREERS_ANY=(By.XPATH,"//a[contains(@href,'/careers') and not(contains(@href,'quality-assurance'))]")
    CAREERS_FOOTER=(By.XPATH,"//footer//a[contains(@href,'/careers')]")
    COOKIE_ACCEPTS=[
        (By.ID,"onetrust-accept-btn-handler"),
        (By.XPATH,"//button[contains(.,'Accept') or contains(.,'Kabul') or contains(.,'Agree')]"),
        (By.CSS_SELECTOR,"button[aria-label*='accept' i]"),
    ]

    def open_home(self):
        self.open(self.URL)

    def assert_opened(self):
        assert "insider" in self.driver.current_url

    def accept_cookies(self):
        for loc in self.COOKIE_ACCEPTS:
            try:
                self.click(loc)
                break
            except:
                pass

    def goto_careers(self):
        self.accept_cookies()
        try:
            if self.exists_any([self.CAREERS_IN_MENU]):
                self.click(self.CAREERS_IN_MENU)
            else:
                self.hover(self.COMPANY_MENU)
                self.click_any([self.CAREERS_IN_MENU,self.CAREERS_ANY])
        except:
            try:
                self.scroll_into_view(self.CAREERS_FOOTER)
                self.click(self.CAREERS_FOOTER)
            except:
                self.open(self.URL+"careers/")
        self.wait_url_contains("/careers")
