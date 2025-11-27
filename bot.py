from resources.orange_hrm.orange_hrm import OrangeHRM
from pathlib import Path
import logging
import os

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

if __name__ == "__main__":
    # Ideally, we should use a more secure way to store the username, password (e.g. bitwarden, BotCity Credentials etc)
    orange_hrm = OrangeHRM(
        username=os.getenv("USERNAME"),
        password=os.getenv("PASSWORD"),
        url="https://opensource-demo.orangehrmlive.com/web/index.php/auth/login",
    )
    try:
        orange_hrm.setup_browser()
        orange_hrm.login()
        orange_hrm.add_candidate()

        csv_path = orange_hrm.download_candidates_csv(
            "https://workshop.botcity.dev/assets/candidatos.csv", "candidates.csv"
        )
        candidates = orange_hrm.read_candidates(Path("output") / csv_path)

        processed = orange_hrm.load_processed()
        for candidate in candidates:
            try:
                if candidate["full_name"] in processed:
                    logger.debug(
                        f"Candidate {candidate['full_name']} already processed."
                    )
                    continue
                orange_hrm.fill_candidate_form(candidate)
                orange_hrm.save_processed(candidate["full_name"])
            except Exception as e:
                logger.error(
                    f"Failed to process candidate {candidate.get('full_name')}: {e}"
                )

        logger.info("All candidates processed.")
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")

    finally:
        orange_hrm.close_browser()
