import chromedriver_autoinstaller
chromedriver_autoinstaller.install() # Installs latest version of ChromeDriver and skips if already installed
from selenium import webdriver
from selenium.webdriver.common.by import By
import yaml

# Target URLs
LOGIN_URL = "https://letterboxd.com/sign-in/"
DATA_URL = "https://letterboxd.com/settings/data/"

# Read credentials
conf = yaml.safe_load(open('login_details.yml'))
username = conf['letterboxd_app']['username']
password = conf['letterboxd_app']['password']

# Set up Chrome options
options = webdriver.ChromeOptions()
#options.add_argument("--headless")  # optional to make it not show
driver = webdriver.Chrome(options=options)

# Login function
def login(url, usernameId, username, passwordId, password, submit_buttonId):
    driver.get(url)
    driver.find_element(By.ID, usernameId).send_keys(username)
    driver.find_element(By.ID, passwordId).send_keys(password)
    driver.find_element(By.CSS_SELECTOR, submit_buttonId).click()

# Run it
login(LOGIN_URL, "field-username", username, "field-password", password, "button.standalone-flow-button.-inline.-action.-activity-indicator")

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Click on "settings"


# Click on "data"


# Click on the "Export data" button
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "export-data-link cboxElement button"))
).click()

# Click on "Export data" button in the pop-up window
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.-action.button-action.export-data-button"))
).click()