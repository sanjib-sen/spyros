from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import json

email = 'tiheri5035@cmeinbox.com'
password = 'mahmudabdullah'
var_keywords = "hydrogen"
var_title = "CEO"
var_locations = []


driver = webdriver.Chrome()
file1 = open("profileurls.txt", "w")
file1.write("List of profile urls: \n\n\n")
file1.close()
countOfPersons = 0


def login():
    driver.get("https://www.linkedin.com/login")
    time.sleep(1)
    eml = driver.find_element(by=By.ID, value="username")
    eml.send_keys(email)
    passwd = driver.find_element(by=By.ID, value="password")
    passwd.send_keys(password)
    loginbutton = driver.find_element(
        by=By.XPATH, value="//*[@id=\"organic-div\"]/form/div[3]/button")
    loginbutton.click()
    time.sleep(3)


def getSearchResults(url, page=2):
    global countOfPersons
    time.sleep(2)
    driver.get(url)
    time.sleep(4)
    source = BeautifulSoup(driver.page_source)
    not_visible = source.find_all(
        'h2', class_="ember-view artdeco-empty-state__headline artdeco-empty-state__headline--mercado-empty-room-small artdeco-empty-state__headline--mercado-spots-small")
    if len(not_visible) > 0:
        return
    visibleEmployees = source.find_all('a')

    file1 = open("profileurls.txt", "a")
    visibleEmployeesList = []
    for profile in visibleEmployees:
        if "in" in profile.get('href').split('/') and profile.get('href').split("?")[0] not in visibleEmployeesList:
            visibleEmployeesList.append(profile.get('href').split("?")[0])
            file1.write(profile.get('href').split("?")[0]+"\n")
    file1.close()

    countOfPersons += len(visibleEmployeesList)
    print(
        f"Found {len(visibleEmployeesList)} persons in page {page-1}. Total so far: {countOfPersons} persons")
    print("\n".join(visibleEmployeesList))
    url += f"&page={page}"
    getSearchResults(url, page+1)


if __name__ == "__main__":
    login()
    url = f'https://www.linkedin.com/search/results/people/?geoUrn=%5B%22103644278%22%2C%22101165590%22%2C%22101174742%22%5D&keywords={var_keywords}&origin=FACETED_SEARCH&sid=aRj&title={var_title}'
    getSearchResults(url)
    time.sleep(4)
    driver.quit()
