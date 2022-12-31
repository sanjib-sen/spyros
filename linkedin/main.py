from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import json
from pprint import pprint

email = 'nevertrytoknow@outlook.com'
password = 'mahmudabdullah'
var_keywords = "hydrogen"
var_title = "CEO"
var_locations = []

Profiles = {}
Companies = {}

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
    time.sleep(15)


def getFromProfile(profileUrl):
    if "location" in Profiles.get(profileUrl):
        return
    time.sleep(2)
    driver.get(profileUrl)
    time.sleep(4)
    source = BeautifulSoup(driver.page_source)
    company = source.find("a", attrs={
        "data-field": "experience_company_logo"})
    companyUrl = company.get("href")
    companyName = company.parent.parent.find('span', class_="t-14 t-normal").find("span", attrs={
        "aria-hidden": "true"}).text.strip()
    location = source.find_all(
        "span", class_="text-body-small inline t-black--light break-words")[0].text.strip()
    locationList = location.split(",")
    city, state, country = None, None, None
    if len(locationList) > 1:
        state, country = locationList[-2], locationList[-1]
        if len(locationList) > 2:
            city = locationList[-3]
    Profiles[profileUrl]["companyName"] = companyName
    Profiles[profileUrl]["companyUrl"] = companyUrl
    Profiles[profileUrl]["country"] = country
    Profiles[profileUrl]["city"] = city
    Profiles[profileUrl]["state"] = state
    Profiles[profileUrl]["location"] = location
    Companies[companyUrl] = {"companyName": companyName}
    print("\n\nProfile Information\n------------------------------")
    pprint(Profiles[profileUrl])

    getCompanyData(companyUrl)


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
    visibleEmployees = source.find_all(
        'span', class_="entity-result__title-text")

    file1 = open("profileurls.txt", "a")
    visibleEmployeesList = []
    title, firstName, lastName = None, None, None
    for profile in visibleEmployees:
        profile = profile.find_all('a', class_="app-aware-link")[0]
        if "in" in profile.get('href').split('/') and profile.get('href').split("?")[0] not in visibleEmployeesList:
            title = profile.parent.parent.parent.parent.parent.find_all(
                "div", class_="entity-result__primary-subtitle t-14 t-black t-normal")[0].text.strip()
            employeeName = profile.find("span", attrs={
                "aria-hidden": "true"}).text.strip().split(" ")
            firstName, lastName = employeeName[0], employeeName[1]
            profileUrl = profile.get('href').split("?")[0]
            visibleEmployeesList.append(profileUrl)
            file1.write(profile.get('href').split("?")[0]+"\n")
            if Profiles.get(profileUrl) == None:
                Profiles[profileUrl] = {
                    "firstName": firstName,
                    "lastName": lastName,
                    "title": title
                }
            getFromProfile(profileUrl)
    file1.close()
    countOfPersons += len(visibleEmployeesList)
    print(
        f"Found {len(visibleEmployeesList)} persons in page {page-1}. Total so far: {countOfPersons} persons")

    url += f"&page={page}"
    getSearchResults(url, page+1)


def getCompanyData(companyUrl):
    if "noOfEmployees" in Companies.get(companyUrl):
        return
    phone, country, state, city, location, website = [None]*6
    time.sleep(2)
    driver.get(companyUrl+"/about")
    time.sleep(4)
    source = BeautifulSoup(driver.page_source)
    links = source.find_all('a')
    websiteSource = source.find_all(
        'a', class_="ember-view org-top-card-primary-actions__action")
    if len(websiteSource) > 0:
        website = websiteSource[0].get("href")

    fields = source.find_all(
        'dd', class_="text-body-small")

    no_of_employees = None
    for f in fields:
        if "employees" in f.text:
            no_of_employees = f.text.strip()

    for link in links:
        if link.get("href").startswith("tel"):
            phone = link.get("href").split(":")[1]
        elif link.get("href").startswith("https://www.bing.com/maps?where="):
            addr = link.get("href").split(
                "where=")[1].replace('%20', " ").replace('%2C', ",")
            location = addr
            if len(addr.split(",")) == 1:
                country = addr
            if len(addr.split(",")) == 2:
                country = addr.split(",")[1]
                state = addr.split(",")[0]
            if len(addr.split(",")) >= 3:
                country = addr.split(",")[-1]
                state = addr.split(",")[-2]
                city = addr.split(",")[-3]

    Companies[companyUrl]["noOfEmployees"] = no_of_employees
    Companies[companyUrl]["website"] = website
    Companies[companyUrl]["phone"] = phone
    Companies[companyUrl]["location"] = location
    Companies[companyUrl]["country"] = country
    Companies[companyUrl]["city"] = city
    Companies[companyUrl]["state"] = state
    print("\n\nComapny Information\n------------------------------")
    pprint(Companies[companyUrl])


if __name__ == "__main__":
    login()
    url = f'https://www.linkedin.com/search/results/people/?geoUrn=%5B%22103644278%22%2C%22101165590%22%2C%22101174742%22%5D&keywords={var_keywords}&origin=FACETED_SEARCH&sid=aRj&title={var_title}'
    getSearchResults(url)

    getFromProfile('https://www.linkedin.com/in/kartikreddy/')
    getCompanyData(
        'https://www.linkedin.com/company/asociacion-mexicana-de-hidr%C3%B3geno')

    time.sleep(4)
    driver.quit()
