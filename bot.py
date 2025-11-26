from resources.orange_hrm.orange_hrm import OrangeHRM
from pathlib import Path

if __name__ == "__main__":
    orange_hrm = OrangeHRM()
    orange_hrm.setup_browser()
    orange_hrm.login()
    orange_hrm.add_candidate()

    csv_path = orange_hrm.download_candidates_csv(
        "https://workshop.botcity.dev/assets/candidatos.csv", "candidates.csv"
    )
    candidates = orange_hrm.read_candidates(Path("output") / csv_path)

    for candidate in candidates:
        orange_hrm.fill_candidate_form(candidate)
        orange_hrm.add_candidate()  # prepare for next candidate
