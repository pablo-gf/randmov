import chromedriver_autoinstaller
chromedriver_autoinstaller.install() # Installs latest version of ChromeDriver and skips if allready installed
from selenium import webdriver
from selenium.webdriver.common.by import By
import yaml

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
login("https://letterboxd.com/sign-in/", "field-username", username, "field-password", password, "button.standalone-flow-button.-inline.-action.-activity-indicator")
