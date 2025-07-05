import chromedriver_autoinstaller
chromedriver_autoinstaller.install() # Installs latest version of ChromeDriver and skips if already installed
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains  # Add this import
import yaml
import os
import time
import zipfile
import pandas as pd
import random
import shutil

# Set download directory:
download_dir = os.getcwd()

# Configure Chrome options
options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
options.add_experimental_option("prefs", prefs)
options.add_argument("--headless")  # Uncomment for headless mode

# Initialize driver
chromedriver_autoinstaller.install()
driver = webdriver.Chrome(options=options)

# Login function
def login(url, usernameId, username, passwordId, password, submit_buttonId):
    driver.get(url)
    driver.find_element(By.ID, usernameId).send_keys(username)
    driver.find_element(By.ID, passwordId).send_keys(password)
    driver.find_element(By.CSS_SELECTOR, submit_buttonId).click()

# Click on function
def click_on(parameter):
    return WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, parameter))).click()

# Clean function
def clean_files(*args):
    for arg in args:
        os.remove(arg)

def clean_directories(*args):
    for arg in args:
        shutil.rmtree(os.path.join(os.getcwd(), arg))

def delete_zip():
    for file in os.listdir(os.getcwd()):
        if file.endswith('.zip'):
            os.remove(file)

def main():

    # Target URLs
    LOGIN_URL = "https://letterboxd.com/sign-in/"
    DATA_URL = "https://letterboxd.com/settings/data/"

    # Load letterboxd credentials
    conf = yaml.safe_load(open('login_details.yml'))
    username = conf['letterboxd_app']['username']
    password = conf['letterboxd_app']['password']

    # Log in
    login(LOGIN_URL, "field-username", username, "field-password", password, "button.standalone-flow-button.-inline.-action.-activity-indicator")

    # Click on "do not consent" for cookies management
    click_on(".fc-button.fc-cta-do-not-consent.fc-secondary-button")

    # Hover over profile menu to reveal dropdown
    profile_menu = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.has-icon.toggle-menu"))
    )
    ActionChains(driver).move_to_element(profile_menu).perform()

    # Wait for dropdown to appear and click Settings
    click_on("a[href='/settings/']")

    # Click on "data"
    click_on("a[data-id='data']")

    # Click on the "Export data" button
    click_on("a[class='export-data-link cboxElement button'")

    # Click on "Export data" button in the pop-up window
    click_on("a[class='button -action button-action export-data-button'")
    time.sleep(2)

    # Unzip downloaded file in the current directory
    for file in os.listdir(os.getcwd()):
        if file.endswith('.zip'):
            zip_file_dir = os.path.join(os.getcwd(), file)
            with zipfile.ZipFile(zip_file_dir, 'r') as zip_file:
                zip_file.extractall(os.getcwd())

    # Load watchlist data
    watchlist = pd.read_csv('watchlist.csv')

    # Select and ouput random movie
    random = random.randint(0, len(watchlist['Name']))
    print(f"Selected movie: {watchlist['Name'][random]}")

    # Clean 
    clean_files('comments.csv', 'diary.csv', 'profile.csv', 'ratings.csv', 'reviews.csv', 'watched.csv', 'watchlist.csv')
    clean_directories('deleted', 'likes', 'orphaned')
    delete_zip()

if __name__ == '__main__':
    main()