import pytest
from pages.home_page import HomePage
from pages.careers_page import CareersPage
from pages.qa_page import QAPage
from pages.lever_page import LeverPage

def ensure_careers_blocks(careers: CareersPage):
    careers.assert_blocks_visible()

def test_insider_qa_flow(driver):
    home = HomePage(driver)
    home.open_home()
    home.accept_cookies()
    home.assert_opened()
    try:
        home.goto_careers()
    except:
        home.goto_careers_fallback()

    careers = CareersPage(driver)
    ensure_careers_blocks(careers)

    careers.goto_qa_page()
    qa = QAPage(driver)

    qa.go_open_positions_with_params()
    qa.filter_on_open_positions_insider(location_text="Istanbul, Turkey")

    cards = qa.jobs() or qa.jobs_on_open_positions()
    assert cards, "Filtre sonrası ilan listesi boş"

    max_check = min(3, len(cards))
    for i in range(max_check):
        qa.open_in_new_tab(cards[i])
        lever = LeverPage(driver)
        lever.wait_new_tab_and_switch("lever.co")
        lever.assert_on_lever()
        lever.assert_job_matches(
            position_kw="quality assurance",
            department_kw="quality assurance",
            location_must_include=("istanbul", "turkey"),
        )
        driver.close()
        driver.switch_to.window(driver.window_handles[0])


