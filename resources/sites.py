from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Sites:
    def setup_browser(
        self,
        timeout: int = 30,
        maximized: bool = True,
        remote_port: int = None,
    ):
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--log-level=3")
        options.add_argument("--disable-logging")
        options.add_argument("--lang=en")
        options.add_argument("--disable-blink-features=AutomationControlled")

        if isinstance(remote_port, int):
            options.add_argument(f"--remote-debugging-port={remote_port}")

        self.browser = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )

        if maximized:
            self.browser.maximize_window()

        self.browser.set_page_load_timeout(timeout)

    def wait_until_element_is_visible(self, by: By, locator: str, timeout: int = 20):
        """Wait until element is visible on the page."""
        try:
            wait = WebDriverWait(self.browser, timeout)
            return wait.until(EC.visibility_of_element_located((by, locator)))
        except Exception as e:
            print(f"Element not visible: {locator} - {e}")
            raise
