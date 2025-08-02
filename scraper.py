from linkedin_scraper import Person, actions
from selenium import webdriver
driver = webdriver.Chrome()

email = "some-email@email.address"
password = "password123"

def scrape_linkedin_profile(linkedin_url):
    actions.login(driver, email, password)
    person = Person(linkedin_url, driver=driver)