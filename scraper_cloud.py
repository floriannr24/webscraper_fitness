import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import csv

def loadCSV():
    with open("occupancy.csv", "r", encoding="UTF8", newline="") as c:
        pass

def createCSV():
    with open("occupancy.csv", "w", encoding="UTF8", newline="") as i:
        header = ["date", "0000", "0100", "0200", "0300", "0400", "0500", "0600", "0700", "0800", "0900",
                  "1000", "1100", "1200", "1300", "1400", "1500", "1600", "1700", "1800", "1900", "2000",
                  "2100", "2200", "2300"]
        writer = csv.writer(i)
        writer.writerow(header)


def writeToCSV(data):
    with open("occupancy.csv", "r", encoding="UTF8", newline="") as r:
        readerList = list(csv.reader(r))
        row = readerList[len(readerList)-1]
        if len(row) == 25:
            with open("occupancy.csv", "a", encoding="UTF8", newline="") as a:
                appender = csv.writer(a)
                rowData = []
                rowData.append(datetime.datetime.now().strftime('%Y-%m-%d'))
                rowData.append(data)
                appender.writerow(rowData)
        else:
            with open("occupancy.csv", "w", encoding="UTF8", newline="") as w:
                writer = csv.writer(w)
                readerList[len(readerList)-1].append(data)
                writer.writerows(readerList)


def scrape():
    options = Options()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.fit-star.de/fitnessstudio/nuernberg-zentrum")
    data = driver.find_element(By.ID, "fs-livedata-percentage").text.replace("%", "")
    writeToCSV(data)

    print(f"{datetime.datetime.now().strftime('%H:%M:%S')} / data: {data}")

try:
    loadCSV()
except FileNotFoundError:
    createCSV()

scrape()



