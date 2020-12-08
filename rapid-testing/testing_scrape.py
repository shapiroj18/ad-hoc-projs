import requests
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def notify(title, text):
    os.system(
        f"""
              osascript -e 'display alert "Washington Heights Appointment Found!"'
              """
    )


def create_browser(webdriver_path):
    # create a selenium object that mimics the browser
    browser_options = Options()
    # headless tag created an invisible browser
    browser_options.add_argument("--headless")
    browser_options.add_argument("--no-sandbox")
    browser = webdriver.Chrome(webdriver_path, options=browser_options)
    print("Done Creating Browser")
    return browser


def parse_data(page_html):
    soup = BeautifulSoup(page_html, "html.parser")
    depts = soup.findAll("div", {"class": "departmentName"})  # parse for dept names
    wash_heights = '<div class="departmentName">DH WASHINGTON HTS C19 TEST CLINIC</div>'
    if len(depts) == 0:
        print("No locations found :(")
    elif len(depts) > 0:
        print("Locations found!!")

        for i in depts:
            if str(i) == wash_heights:
                print("Washington Heights Appts Found!")
                notify("Rapid Test Appts Avail", "Check em out!")


def main():
    url = "https://epicmychart.nychhc.org/MyChart/SignupAndSchedule/EmbeddedSchedule?lang=english&id=RES^,5100184,5100351,5100180,5100182,5100348,5100174,5100347,5100350,5100349,&dept=1000000006,1000000008,1000000004,1000000005,1000000003,1000000002,1000000001,1000000010,1000000011&vt=11790649#slotdetails"
    browser = create_browser(
        "/Users/jonathanshapiro/Downloads/chromedriver"
    )  # path of downloaded chromedriver https://chromedriver.storage.googleapis.com/index.html?path=2.41/
    browser.get(url)
    page_html = browser.page_source
    parse_data(page_html=page_html)


if __name__ == "__main__":
    main()
