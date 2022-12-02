import datetime
import time
import schedule
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import csv


class Scraper:
    def __init__(self):
        self.percentage = []
        self.counter = 0
        self.createCSV()

    def createCSV(self):
        with open("occupancy.csv", "w", encoding="UTF8", newline="") as i:
            header = ["date", "0000", "0100", "0200", "0300", "0400", "0500", "0600", "0700", "0800", "0900",
                      "1000", "1100", "1200", "1300", "1400", "1500", "1600", "1700", "1800", "1900", "2000",
                      "2100", "2200", "2300"]
            writer = csv.writer(i)
            writer.writerow(header)

    def appendRowToCSV(self, data):
        with open("occupancy.csv", "a", encoding="UTF8", newline="") as d:
            writer = csv.writer(d)
            data.insert(0, datetime.datetime.now().strftime('%Y-%m-%d'))
            writer.writerow(data)

    def scrape(self):
        self.counter = self.counter + 1

        options = Options()
        options.headless = True
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get("https://www.fit-star.de/fitnessstudio/nuernberg-zentrum")
        data = driver.find_element(By.ID, "fs-livedata-percentage").text.replace("%", "")
        self.percentage.append(data)
        driver.quit()

        print(f"{self.counter} / {datetime.datetime.now().strftime('%H:%M:%S')} data: {data}")

        if self.counter == 4:
            self.appendRowToCSV(self.percentage)
            self.percentage = []
            self.counter = 0


s = Scraper()
schedule.every().hours.at(":00").do(s.scrape)
#schedule.every(5).seconds.do(s.scrape)

while True:
    schedule.run_pending()
    time.sleep(1)

# s.createCSV()
# percentage = [datetime.datetime.now().strftime("%Y-%m-%d")]
#
# s.appendRowToCSV(percentage)
