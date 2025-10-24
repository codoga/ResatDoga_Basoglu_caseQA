from selenium.webdriver.common.by import By
from .base_page import BasePage

class LeverPage(BasePage):
    META = (By.CSS_SELECTOR, ".posting-categories")
    TITLE = (By.CSS_SELECTOR, "h2, h1, .posting-headline, .posting-title")

    def assert_on_lever(self):
        assert "lever.co" in self.driver.current_url.lower()
        assert self.visible(self.TITLE)

    def read_meta_text(self) -> str:
        try:
            el = self.visible(self.META)
            return (el.text or "").lower()
        except:
            return (self.driver.page_source or "").lower()

    def assert_job_matches(
        self,
        position_kw="quality assurance",
        department_kw="quality assurance",
        location_must_include=("Istanbul", "turkey")
    ):
        txt = self.read_meta_text()
        page = ((self.driver.title or "") + " " + (self.driver.page_source or "")).lower()

        assert (position_kw in txt) or (position_kw in page), f"Position '{position_kw}' bulunamadı"
        assert (department_kw in txt) or (department_kw in page), f"Department '{department_kw}' bulunamadı"

        has_istanbul = ("Istanbul" in txt) or ("Istanbul" in page)
        has_country  = ("Turkey" in txt) or ("Türkiye" in txt) or ("Turkiye" in txt) or ("Turkıye" in txt)
        assert has_istanbul and has_country, "Location 'Istanbul, Turkey' doğrulanamadı"

