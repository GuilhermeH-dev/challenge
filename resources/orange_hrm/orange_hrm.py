from selenium.webdriver.common.by import By
from resources.orange_hrm.locators import (
    LoginPageLocators,
    DashboardPageLocators,
)
from resources.sites import Sites
import time
import requests
import os
import csv
from pathlib import Path


class OrangeHRM(Sites):
    def __init__(self):
        super().__init__()

    def login(self):
        try:
            self.browser.get(
                "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
            )
            self.wait_until_element_is_visible(
                By.XPATH, LoginPageLocators.USERNAME_INPUT
            )
            self.browser.find_element(
                By.XPATH, LoginPageLocators.USERNAME_INPUT
            ).send_keys("Admin")
            self.browser.find_element(
                By.XPATH, LoginPageLocators.PASSWORD_INPUT
            ).send_keys("admin123")
            self.browser.find_element(By.XPATH, LoginPageLocators.LOGIN_BUTTON).click()
            self.wait_until_element_is_visible(
                By.XPATH, DashboardPageLocators.DASHBOARD_TITLE
            )
            time.sleep(4)

        except Exception as e:
            print(e)

    def add_candidate(self):
        try:
            self.browser.find_element(
                By.XPATH, DashboardPageLocators.RECRUITMENT_TAB
            ).click()
            self.wait_until_element_is_visible(
                By.XPATH, DashboardPageLocators.ADD_BUTTON
            )
            self.browser.find_element(
                By.XPATH, DashboardPageLocators.ADD_BUTTON
            ).click()
            time.sleep(4)
        except Exception as e:
            print(e)

    def download_candidates_csv(self, url: str, save_path: str) -> str:
        """Download the CSV containing the candidate data."""
        response = requests.get(url)
        response.raise_for_status()
        output_dir = Path().cwd() / "output"
        os.makedirs(output_dir, exist_ok=True)
        save_path = output_dir / save_path

        with open(save_path, "wb") as f:
            f.write(response.content)

        return save_path

    def read_candidates(self, csv_path: str) -> list[dict]:
        """Read the CSV and return a list of dictionaries."""
        candidates = []

        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                candidates.append(row)

        return candidates

    def fill_candidate_form(self, candidate: dict):
        self.fill_personal_info(candidate)
        self.fill_job_info(candidate)
        resume_file = self.generate_resume(candidate, Path("output"))
        self.upload_resume(resume_file)
        self.save_candidate()

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

    def save_candidate(self):
        self.browser.find_element(By.XPATH, DashboardPageLocators.SAVE_BUTTON).click()
        self.wait_until_element_is_visible(
            By.XPATH, DashboardPageLocators.RECRUITMENT_TAB_TITLE
        )

    def generate_resume(self, candidate: dict, output_dir: Path) -> Path:
        """
        Generate a TXT file acting as a resume for a candidate.

        Args:
            candidate (dict): Candidate data with keys 'full_name', 'email', 'vacancy'
            output_dir (Path): Directory where the TXT file will be saved

        Returns:
            Path: Full path to the generated resume TXT
        """
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

        return resume_path
