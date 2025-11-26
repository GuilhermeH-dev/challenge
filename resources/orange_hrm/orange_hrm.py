from selenium.webdriver.common.by import By
from resources.orange_hrm.locators import LoginPageLocators, DashboardPageLocators
from resources.sites import Sites
from pathlib import Path
import requests
import csv
import time
from retry import retry
import logging

logger = logging.getLogger(__name__)


class OrangeHRM(Sites):
    def __init__(self):
        super().__init__()

    def login(self):
        """Log in to OrangeHRM."""
        logger.info("Accessing OrangeHRM login page.")
        self.browser.get(
            "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
        )
        self.wait_until_element_is_visible(By.XPATH, LoginPageLocators.USERNAME_INPUT)
        self.browser.find_element(By.XPATH, LoginPageLocators.USERNAME_INPUT).send_keys(
            "Admin"
        )
        self.browser.find_element(By.XPATH, LoginPageLocators.PASSWORD_INPUT).send_keys(
            "admin123"
        )
        self.browser.find_element(By.XPATH, LoginPageLocators.LOGIN_BUTTON).click()
        self.wait_until_element_is_visible(
            By.XPATH, DashboardPageLocators.DASHBOARD_TITLE
        )
        logger.info("Login successful.")

    def add_candidate(self):
        """Navigate to recruitment and click 'Add Candidate'."""
        self.browser.find_element(
            By.XPATH, DashboardPageLocators.RECRUITMENT_TAB
        ).click()
        self.wait_until_element_is_visible(By.XPATH, DashboardPageLocators.ADD_BUTTON)
        self.browser.find_element(By.XPATH, DashboardPageLocators.ADD_BUTTON).click()
        time.sleep(2)  # pequeno delay para garantir que a tela carregou
        logger.info("Add candidate form opened.")

    def download_candidates_csv(self, url: str, save_path: str) -> Path:
        """Download CSV with candidate data."""
        logger.info(f"Downloading candidates CSV from {url}")
        response = requests.get(url)
        response.raise_for_status()
        output_dir = Path().cwd() / "output"
        output_dir.mkdir(exist_ok=True)
        file_path = output_dir / save_path
        file_path.write_bytes(response.content)
        logger.info(f"CSV saved to {file_path}")
        return file_path

    def read_candidates(self, csv_path: Path) -> list[dict]:
        """Read CSV and return list of candidate dicts."""
        candidates = []
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                candidates.append(row)
        logger.info(f"{len(candidates)} candidates loaded from CSV.")
        return candidates

    @retry(tries=3, delay=2)
    def fill_candidate_form(self, candidate: dict):
        """Fill the candidate form with data and save."""
        logger.info(f"Filling form for candidate {candidate['full_name']}")
        self.fill_personal_info(candidate)
        self.fill_job_info(candidate)
        resume_file = self.generate_resume(candidate, Path("output"))
        self.upload_resume(resume_file)
        self.save_candidate()
        logger.info(f"Candidate {candidate['full_name']} saved successfully.")
        self.add_candidate()

    def fill_personal_info(self, candidate: dict):
        full_name = candidate["full_name"].split()
        first = full_name[0]
        middle = full_name[1] if len(full_name) == 3 else ""
        last = full_name[-1]

        self.browser.find_element(
            By.XPATH, DashboardPageLocators.FIRST_NAME_INPUT
        ).send_keys(first)
        self.browser.find_element(
            By.XPATH, DashboardPageLocators.MIDDLE_NAME_INPUT
        ).send_keys(middle)
        self.browser.find_element(
            By.XPATH, DashboardPageLocators.LAST_NAME_INPUT
        ).send_keys(last)
        self.browser.find_element(
            By.XPATH, DashboardPageLocators.EMAIL_INPUT
        ).send_keys(candidate["email"])
        self.browser.find_element(
            By.XPATH, DashboardPageLocators.PHONE_INPUT
        ).send_keys(candidate["contact_number"])

    def fill_job_info(self, candidate: dict):
        self.browser.find_element(
            By.XPATH, DashboardPageLocators.VACANCY_SELECT
        ).click()
        option = self.browser.find_element(
            By.XPATH,
            f"//div[@role='option' and normalize-space()='{candidate['vacancy']}']",
        )
        option.click()
        self.browser.find_element(
            By.XPATH, DashboardPageLocators.KEYWORDS_INPUT
        ).send_keys(candidate["keywords"])

    def upload_resume(self, resume_file: Path):
        file_input = self.browser.find_element(
            By.XPATH, DashboardPageLocators.UPLOAD_RESUME_BUTTON
        )
        file_input.send_keys(str(resume_file.resolve()))
        logger.info(f"Uploaded resume {resume_file.name}")

    def save_candidate(self):
        self.browser.find_element(By.XPATH, DashboardPageLocators.SAVE_BUTTON).click()
        self.wait_until_element_is_visible(
            By.XPATH, DashboardPageLocators.RECRUITMENT_TAB_TITLE
        )

    def generate_resume(self, candidate: dict, output_dir: Path) -> Path:
        """Generate a TXT resume file for the candidate."""
        output_dir.mkdir(parents=True, exist_ok=True)
        safe_name = "".join(
            c for c in candidate["full_name"] if c.isalnum() or c in (" ", "_")
        ).rstrip()
        resume_path = output_dir / f"{safe_name.replace(' ', '_')}_resume.txt"

        content = (
            f"Full Name: {candidate['full_name']}\n"
            f"E-mail: {candidate['email']}\n"
            f"Vacancy: {candidate['vacancy']}\n"
        )

        resume_path.write_text(content, encoding="utf-8")
        logger.info(f"Resume generated at {resume_path}")
        return resume_path

    def load_processed(self) -> set:
        path = Path("output/processed_candidates.txt")
        if not path.exists():
            return set()

        return set(path.read_text().splitlines())

    def save_processed(self, full_name: str):
        path = Path("output/processed_candidates.txt")
        path.parent.mkdir(exist_ok=True)

        with open(path, "a", encoding="utf-8") as f:
            f.write(full_name + "\n")

    def close_browser(self):
        """Close the browser."""
        self.browser.quit()
        logger.info("Browser closed.")
