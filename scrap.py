
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import csv
import sys
import pathlib


options = webdriver.ChromeOptions()
prefs = {'profile.default_content_setting_values': {'cookies': 2, 'images': 2, 'javascript': 2,
                            'plugins': 2, 'popups': 2, 'geolocation': 2,
                            'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2,
                            'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
                            'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2,
                            'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2,
                            'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2,
                            'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2,
                            'durable_storage': 2,
                            'images': 2}}
options.add_experimental_option('prefs', prefs)
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("headless")

file = pathlib.Path("cosmotics.csv")

data = []

for x in range(1,20000):
    print(x)
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
    driver.get('https://beta.sfda.gov.sa/en/cosmetics-list?pg='+str(x))
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table", {"class":"table table-striped display"})
    try:
        for a in table.find_all("a"):
            data.append({"pagenumber": x, "barcode": a["data-barcode"],"brandname": a["data-brandname"],"catarabic": a["data-catarabic"],"catenglish": a["data-catenglish"],"counrtyar": a["data-counrtyar"],
            "counrtyen": a["data-counrtyen"],"listednamear": a["data-listednamear"],"listednameen": a["data-listednameen"],"manufacturearabicname": a["data-manufacturearabicname"],"manufactureenglishname":  a["data-manufactureenglishname"],
            "manufacturetype": a["data-manufacturetype"],"packagevolume": a["data-packagevolume"],"productarname": a["data-productarname"],"productenname": a["data-productenname"],"productnotificationsid": a["data-productnotificationsid"],
            "productnumber": a["data-productnumber"],"status": a["data-status"],"unitar": a["data-unitar"],"uniten": a["data-uniten"]})
        if file.exists ():
            with open('cosmotics.csv', mode='a+', encoding="utf8") as csv_file:
                fieldnames = ['pagenumber', 'barcode', 'brandname', 'catarabic', 'catenglish', 'counrtyar', 'counrtyen', 'listednamear', 'listednameen',
                            'manufacturearabicname', 'manufactureenglishname', 'manufacturetype', 'packagevolume', 'productarname', 'productenname', 'productnotificationsid',
                            'productnumber', 'status', 'unitar', 'uniten']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                for item in data:
                    writer.writerow(item)
        else:
            with open('cosmotics.csv', mode='w', encoding="utf8") as csv_file:
                fieldnames = ['pagenumber', 'barcode', 'brandname', 'catarabic', 'catenglish', 'counrtyar', 'counrtyen', 'listednamear', 'listednameen',
                            'manufacturearabicname', 'manufactureenglishname', 'manufacturetype', 'packagevolume', 'productarname', 'productenname', 'productnotificationsid',
                            'productnumber', 'status', 'unitar', 'uniten']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                for item in data:
                    writer.writerow(item)
        driver.quit()
        data = []
    except (RuntimeError, TypeError, NameError):
        pass
