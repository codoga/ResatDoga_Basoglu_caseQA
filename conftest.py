import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="session")
def driver():
    o = Options()
    o.add_argument("--start-maximized")
    o.add_argument("--disable-gpu")
    o.add_argument("--no-sandbox")
    o.add_argument("--disable-dev-shm-usage")
    s = Service(ChromeDriverManager().install())
    d = webdriver.Chrome(service=s, options=o)
    yield d
    d.quit()
