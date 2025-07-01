from selenium import webdriver # Library which allows to automate browser through Python
from selenium.webdriver.chrome.service import Service
import yaml

login_url = "https://letterboxd.com/sign-in/"
data_url = "https://letterboxd.com/settings/data/"

conf = yaml.safe_load(open('login_details.yml'))

username = conf['letterboxd_app']['username']
password = conf['letterboxd_app']['password']

service = Service(executable_path="./chromedriver")
driver = webdriver.Chrome(service=service)

def login(url, usernameId, username, passwordId, password, submit_buttonId):
    driver.get(url)
    driver.find_element_by_id(usernameId).send_keys(username)
    driver.find_element_by_id(passwordId).send_keys(password)
    driver.find_element_by_css_selector(submit_buttonId).click() # Because it does not have an id set in the html file

login(login_url, "field-username", username, "field-password", password, "button.standalone-flow-button.-inline.-action.-activity-indicator")