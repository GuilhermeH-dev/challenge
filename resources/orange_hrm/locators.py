class LoginPageLocators:
    USERNAME_INPUT = "//input[@placeholder='Username']"
    PASSWORD_INPUT = "//input[@placeholder='Password']"
    LOGIN_BUTTON = "//button[@type='submit']"


class DashboardPageLocators:
    DASHBOARD_TITLE = "//h6[text() = 'Dashboard']"
    RECRUITMENT_TAB = "//span[text() = 'Recruitment']"
    ADD_BUTTON = "//button[normalize-space(.)='Add']"
    FIRST_NAME_INPUT = "//input[@name='firstName']"
    MIDDLE_NAME_INPUT = "//input[@name='middleName']"
    LAST_NAME_INPUT = "//input[@name='lastName']"
    EMAIL_INPUT = "//label[normalize-space()='Email']/ancestor::div[contains(@class,'oxd-input-group')]//input"
    PHONE_INPUT = "//label[normalize-space()='Contact Number']/ancestor::div[contains(@class,'oxd-input-group')]//input"
    VACANCY_SELECT = (
        "//label[normalize-space()='Vacancy']/"
        "following::div[contains(@class,'oxd-select-text-input')][1]"
    )

    KEYWORDS_INPUT = "//label[normalize-space()='Keywords']/following::input[1]"
    SAVE_BUTTON = "//button[normalize-space(.)='Save']"
    UPLOAD_RESUME_BUTTON = "//input[@type='file']"
    RECRUITMENT_TAB_TITLE = "//h6[normalize-space()='Recruitment']"
