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


driver = webdriver.Chrome("chromedriver.exe")
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


def get_company_url(profileUrl):
    time.sleep(2)
    driver.get(profileUrl)
    time.sleep(4)
    source = BeautifulSoup(driver.page_source)
    print(source.find("a", attrs={
          "data-field": "experience_company_logo"}).get("href"))


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


def getCompanyData(companyUrl):
    time.sleep(2)
    driver.get(companyUrl+"/about")
    time.sleep(4)
    source = BeautifulSoup(driver.page_source)
    links = source.find_all('a')
    website = source.find_all(
        'a', class_="ember-view org-top-card-primary-actions__action")[0].get("href")
    print("website:", website)
    fields = source.find_all(
        'dd', class_="text-body-small")

    no_of_employees = None
    for f in fields:
        if "employees" in f.text:
            no_of_employees = f.text.strip()
    for link in links:
        if link.get("href").startswith("tel"):
            print("Phone:", link.get("href").split(":")[1])
        elif link.get("href").startswith("https://www.bing.com/maps?where="):
            addr = link.get("href").split(
                "where=")[1].replace('%20', " ").replace('%2C', ",")
            print("Address:", addr)
            if len(addr.split(",")) == 1:
                print("Country:", addr)
            if len(addr.split(",")) == 2:
                print("Country:", addr.split(",")[1])
                print("State:", addr.split(",")[0])
            if len(addr.split(",")) >= 3:
                print("Country:", addr.split(",")[-1])
                print("State:", addr.split(",")[-2])
                print("City:", addr.split(",")[-3])


if __name__ == "__main__":
    login()
    # url = f'https://www.linkedin.com/search/results/people/?geoUrn=%5B%22103644278%22%2C%22101165590%22%2C%22101174742%22%5D&keywords={var_keywords}&origin=FACETED_SEARCH&sid=aRj&title={var_title}'
    # getSearchResults(url)

    # get_company_url('https://www.linkedin.com/in/kartikreddy/')
    getCompanyData(
        'https://www.linkedin.com/company/asociacion-mexicana-de-hidr%C3%B3geno')

    time.sleep(4)
    driver.quit()
