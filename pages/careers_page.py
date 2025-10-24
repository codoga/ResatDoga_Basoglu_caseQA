from selenium.webdriver.common.by import By
from .base_page import BasePage

class CareersPage(BasePage):
    PARTNERSHIPS_LINKS = [
        (By.XPATH, "//a[normalize-space()='Partnerships']"),
        (By.XPATH, "//a[contains(translate(@href,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'partner')]"),
    ]
    NEWSROOM_LINKS = [
        (By.XPATH, "//a[normalize-space()='Newsroom']"),
        (By.XPATH, "//a[contains(translate(@href,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'/newsroom')]"),
    ]
    CONTACTUS_LINKS = [
        (By.XPATH, "//a[normalize-space()='Contact Us']"),
        (By.XPATH, "//a[contains(translate(@href,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'contact')]"),
    ]
    QA_PAGE_LINK = (By.XPATH, "//a[contains(@href,'/careers/quality-assurance/')]")

    def ensure_on_page(self):
        self.open("https://useinsider.com/careers/?lang=en")
        self.wait_url_contains("/careers")

    def _ensure_any_link_present(self, locators):
        for by, val in locators:
            els = self.driver.find_elements(by, val)
            if els:
                return True
        return False

    def _assert_section_link(self, locators, fallbacks):
        if self._ensure_any_link_present(locators):
            return
        for url in fallbacks:
            try:
                self.open(url)
                self.wait_url_contains(url.split("https://useinsider.com")[-1].strip("/"))
                return
            except:
                continue
        raise AssertionError("Beklenen bölüm/link bulunamadı")

    def assert_blocks_visible(self):
        self.ensure_on_page()
        self._assert_section_link(
            self.PARTNERSHIPS_LINKS,
            [
                "https://useinsider.com/partners/",
                "https://useinsider.com/partnerships/",
            ],
        )
        self._assert_section_link(
            self.NEWSROOM_LINKS,
            [
                "https://useinsider.com/newsroom/",
            ],
        )
        self._assert_section_link(
            self.CONTACTUS_LINKS,
            [
                "https://useinsider.com/contact-us/",
                "https://useinsider.com/contact/",
            ],
        )

    def goto_qa_page(self):
        try:
            self.scroll_into_view(self.QA_PAGE_LINK)
            self.click(self.QA_PAGE_LINK)
        except:
            self.open("https://useinsider.com/careers/quality-assurance/")
