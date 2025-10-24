from selenium.webdriver.common.by import By
from .base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

class QAPage(BasePage):
    SEE_ALL_QA = (By.XPATH, "//a[contains(.,'See all QA jobs') or contains(.,'See all') or contains(@href,'jobs')]")

    FILTER_LOCATION_BTN = (
        By.XPATH,
        "//button[contains(.,'Location') or contains(.,'Locations') or contains(.,'Lokasyon') or contains(.,'Şehir')]"
        " | //summary[contains(.,'Location') or contains(.,'Locations')]"
        " | //div[@role='button' and (contains(.,'Location') or contains(.,'Locations'))]"
    )
    FILTER_DEPT_BTN = (
        By.XPATH,
        "//button[contains(.,'Department') or contains(.,'Departman')]"
        " | //summary[contains(.,'Department')]"
        " | //div[@role='button' and contains(.,'Department')]"
    )

    APPLY_FILTERS_PRIMARY = (By.XPATH, "//button[contains(.,'Apply') or contains(.,'Uygula') or contains(.,'Done') or contains(.,'Bitti')]")
    APPLY_FILTERS_BY_SPAN = (By.XPATH, "//*[contains(normalize-space(),'Apply') or contains(normalize-space(),'Uygula') or contains(normalize-space(),'Done') or contains(normalize-space(),'Bitti')]/ancestor::*[self::button or self::a or @role='button'][1]")
    APPLY_FILTERS_IN_DIALOG = (By.XPATH, "//div[@role='dialog']//button[.//span[contains(.,'Apply') or contains(.,'Done')]]")

    def _safe_click_any_local(self, locators):
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
        return False

    def _open_filter(self, label_texts, max_scrolls=12, step=600):
        try:
            self.driver.execute_script("window.scrollTo(0, 0)"); time.sleep(0.2)
        except:
            pass

        def candidates_for(t):
            return [
                (By.XPATH, f"//button[.//span[contains(.,'{t}')]]"),
                (By.XPATH, f"//button[contains(.,'{t}')]"),
                (By.XPATH, f"//summary[contains(.,'{t}')]"),
                (By.XPATH, f"//*[@role='button' and .//*[contains(.,'{t}')]]"),
                (By.XPATH, f"//*[self::button or self::div or self::summary][contains(@aria-label,'{t}') or contains(.,'{t}')]"),
            ]

        for _ in range(max_scrolls):
            for t in label_texts:
                for by, xp in candidates_for(t):
                    try:
                        el = self.w.until(EC.presence_of_element_located((by, xp)))
                        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'})", el)
                        try:
                            self.w.until(EC.element_to_be_clickable((by, xp))).click()
                        except:
                            self.driver.execute_script("arguments[0].click()", el)
                        return True
                    except:
                        continue
            try:
                self.driver.execute_script(f"window.scrollBy(0,{step});"); time.sleep(0.2)
            except:
                pass

        js = """
        const texts = arguments[0];
        function norm(s){return (s||'').toLowerCase();}
        const btns = Array.from(document.querySelectorAll('button,summary,[role=\"button\"]'));
        for (const t of texts){
          const cand = btns.find(x => x && (norm(x.textContent).includes(norm(t)) || norm(x.getAttribute('aria-label')||'').includes(norm(t))));
          if (cand){ cand.click(); return true; }
        }
        return false;
        """
        try:
            if self.driver.execute_script(js, label_texts):
                return True
        except:
            pass
        return False

    def _try_apply_or_close_panel(self):
        if self._safe_click_any_local([self.APPLY_FILTERS_PRIMARY, self.APPLY_FILTERS_BY_SPAN, self.APPLY_FILTERS_IN_DIALOG]):
            return True
        try:
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        except:
            pass
        try:
            self.driver.execute_script("document.body.click()")
        except:
            pass
        return True

    def click_see_all(self):
        self._safe_click_any_local([
            self.SEE_ALL_QA,
            (By.XPATH, "//a[contains(@href,'/careers/quality-assurance/')]"),
        ])
        self.w.until(lambda d: d.execute_script("return document.readyState") in ("interactive", "complete"))

    def go_open_positions_with_params(self):
        self.driver.get("https://useinsider.com/careers/open-positions/?department=qualityassurance")
        self.w.until(lambda d: d.execute_script("return document.readyState") == "complete")
        for _ in range(8):
            found = self.driver.find_elements(*self.FILTER_LOCATION_BTN) or self.driver.find_elements(*self.FILTER_DEPT_BTN)
            if found:
                break
            self.driver.execute_script("window.scrollBy(0, 500);"); time.sleep(0.2)

    def filter_on_open_positions_insider(self, location_text="Istanbul"):
        opened = self._open_filter(["Location", "Locations", "Lokasyon", "Şehir"])
        assert opened, "Location filtresi açılamadı"

        try:
            box = self.driver.find_element(
                By.XPATH,
                "//div[contains(@class,'filter') or @role='dialog']"
                "//input[@type='search' or contains(@placeholder,'Search') or contains(@aria-label,'Search')]"
            )
            box.clear(); box.send_keys("Istanbul"); time.sleep(0.4)
        except:
            pass

        picked = False

        exact_city = self.driver.find_elements(
            By.XPATH,
            "//div[contains(@class,'filter') or @role='dialog']//*[self::label or self::li or self::span]"
            "[normalize-space()='Istanbul' or normalize-space()='İstanbul']"
        )
        if exact_city:
            try:
                exact_city[0].click()
            except:
                self.driver.execute_script("arguments[0].click()", exact_city[0])
            picked = True

        if not picked:
            city_with_country = self.driver.find_elements(
                By.XPATH,
                "//div[contains(@class,'filter') or @role='dialog']//*[self::label or self::li or self::span]"
                "[contains(normalize-space(),'Istanbul,') or contains(normalize-space(),'İstanbul,')]"
            )
            if city_with_country:
                try:
                    city_with_country[0].click()
                except:
                    self.driver.execute_script("arguments[0].click()", city_with_country[0])
                picked = True

        if not picked:
            try:
                if 'box' in locals():
                    box.clear(); box.send_keys("Turk"); time.sleep(0.4)
            except:
                pass
            country_opts = self.driver.find_elements(
                By.XPATH,
                "//div[contains(@class,'filter') or @role='dialog']//*[self::label or self::li or self::span]"
                "[contains(translate(normalize-space(),'Üİ','UI'),'turkey') or "
                " contains(translate(normalize-space(),'Üİ','UI'),'turkiye') or "
                " contains(translate(normalize-space(),'Üİ','UI'),'türkiye')]"
            )
            if country_opts:
                try:
                    country_opts[0].click()
                except:
                    self.driver.execute_script("arguments[0].click()", country_opts[0])
                picked = True

        self._try_apply_or_close_panel()

        opened_dept = self._open_filter(["Department", "Departman"])
        assert opened_dept, "Department filtresi açılamadı"

        try:
            box2 = self.driver.find_element(
                By.XPATH,
                "//div[contains(@class,'filter') or @role='dialog']"
                "//input[@type='search' or contains(@placeholder,'Search') or contains(@aria-label,'Search')]"
            )
            box2.clear(); box2.send_keys("Quality Assurance"); time.sleep(0.3)
        except:
            pass

        qa_opts = self.driver.find_elements(
            By.XPATH,
            "//div[contains(@class,'filter') or @role='dialog']//*[self::label or self::li or self::span]"
            "[normalize-space()='Quality Assurance' or contains(normalize-space(),'Quality Assurance')]"
        )
        qa_picked = False
        if qa_opts:
            try:
                qa_opts[0].click()
            except:
                self.driver.execute_script("arguments[0].click()", qa_opts[0])
            qa_picked = True
        assert qa_picked, "Listede 'Quality Assurance' seçeneği bulunamadı"

        self._try_apply_or_close_panel()
        self.ensure_jobs_loaded()

        if not self.jobs():
            self.driver.get("https://jobs.lever.co/useinsider?department=Quality%20Assurance&location=Istanbul,%20Turkey")
            self.w.until(lambda d: d.execute_script("return document.readyState") == "complete")
            self.ensure_jobs_loaded()

    def ensure_jobs_loaded(self, max_scrolls=18, sleep_sec=0.7):
        for _ in range(max_scrolls):
            links = self.jobs()
            if links:
                return
            try:
                load_more = self.driver.find_elements(By.XPATH, "//button[contains(.,'Load more') or contains(.,'Daha Fazla')]")
                if load_more:
                    try:
                        load_more[0].click()
                    except:
                        self.driver.execute_script("arguments[0].click()", load_more[0])
                    time.sleep(sleep_sec)
            except:
                pass
            self.driver.execute_script("window.scrollBy(0, 900);")
            time.sleep(sleep_sec)
        self.w.until(lambda d: len(self.jobs()) > 0)

    def jobs(self):
        cur = (self.driver.current_url or "").lower()
        if "jobs.lever.co" in cur:
            posts = self.driver.find_elements(By.CSS_SELECTOR, ".posting, .posting-list .posting, a.posting-title, .postings-group a")
            cleaned = [p for p in posts if (p.text or "").strip()]
            return cleaned
        links = self.driver.find_elements(By.CSS_SELECTOR, "section[id*='open'], section[class*='open'] a[href*='lever.co'], a[href*='jobs.lever.co']")
        if links:
            cleaned = []
            for l in links:
                txt = (l.text or '').strip().lower()
                if not txt:
                    continue
                if "all open positions" in txt:
                    continue
                cleaned.append(l)
            if cleaned:
                return cleaned
        xcards = self.driver.find_elements(By.XPATH, "//a[.//span[contains(.,'View Role')] or contains(normalize-space(),'View Role') or contains(normalize-space(),'Apply')]")
        if xcards:
            return xcards
        return []

    def jobs_on_open_positions(self):
        cur = (self.driver.current_url or "").lower()
        if "useinsider.com/careers/open-positions" in cur:
            anchors = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='lever.co'], a[href*='jobs.lever.co']")
            anchors = [a for a in anchors if (a.text or "").strip()]
            if anchors:
                return anchors
            cards = self.driver.find_elements(By.XPATH, "//a[.//span[contains(.,'View Role')] or contains(.,'View Role') or contains(.,'Apply')]")
            cards = [c for c in cards if (c.text or "").strip()]
            return cards
        return self.jobs()

    def open_in_new_tab(self, element, expected_url_part="lever.co"):
        href = None
        try:
            href = element.get_attribute("href")
        except:
            href = None
        if href:
            self.driver.execute_script("window.open(arguments[0], '_blank')", href)
        else:
            self.driver.execute_script("arguments[0].setAttribute('target','_blank'); arguments[0].click();", element)
        self.wait_new_tab_and_switch(expected_url_part)
        return True

    def open_first_view_role(self):
        cur = (self.driver.current_url or "").lower()
        if "jobs.lever.co" in cur:
            posts = self.jobs()
            assert posts, "Lever sayfasında ilan bulunamadı."
            try:
                posts[0].click()
            except:
                self.driver.execute_script("arguments[0].click()", posts[0])
            return
        cards = self.jobs()
        assert cards, "İş listesi boş görünüyor."
        try:
            cards[0].click()
        except:
            try:
                v = cards[0].find_element(By.XPATH, ".//a[contains(.,'View Role') or contains(.,'Apply') or contains(@href,'lever.co') or contains(@href,'jobs.lever.co')]")
                v.click()
            except:
                self.driver.execute_script("arguments[0].click()", cards[0])
