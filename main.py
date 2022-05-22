from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests

SITE_URL = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"
browser = webdriver.Chrome(r"C:\Users\crysi\OneDrive\Documents\c127\chromedriver_win32 - Copy\chromedriver.exe")
browser.get(SITE_URL)
time.sleep(10)
headers = ["star", "Constellation", "Right_ascension", "Declination", "Apparent_magnitude","hyperlink", "Initial_Mass", "Main_Sequence", "Subgiant", "First_Red_Giant_Core_He_Burning"]
star_data = []
new_star_data = []
def scrap():
  
    for i in range(0,428):
    
        soup = BeautifulSoup(browser.page_source, "html.parser")
        for tr_tag_row in soup.find_all("tr", attrs={"class", "Star"}):
            td_tags = td_tag_row.find_all("td")
            temp_list = []
            for index, td_tag in enumerate(td_tags):
                    if index == 0:
                        temp_list.append(td_tag.find_all("a")[0].contents[0])
                    else:
                        try:
                            temp_list.append(td_tag.contents[0])
                        except:
                            temp_list.append("")
            hyperlink_td_tag  = td_tags[0]
            temp_list.append("https://en.wikipedia.org/wiki/List_of_brown_dwarfs"+ hyperlink_td_tag.find_all("a", href=True)[0]["href"])
            planet_data.append(temp_list)
        browser.find_element_by_xpath('//*[@id="primary_column"]/tbody/tr/td/td/nav/span[2]/a').click()
        print(f"{i} page done 1")


def scrapMoreData(hyperlink):
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content, "html.parser")
        temp_list = []
        for tr_tag in soup.find_all("tr", attrs={"class": "fact_row"}):
            td_tags = tr_tag.find_all("td")
            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div", attrs={"class":"value"})[0].contents[0])
                except:
                    temp_list.append("")

        new_star_data.append(temp_list)
    except:
        time.sleep(1)
        scrapMoreData(hyperlink)
    

scrap()
for index, data in enumerate(star_data):
    scrapMoreData(data[5])
    print(f"{index+1} page done 2")

final_star_data = []

for index, data in enumerate(star_data):
    new_star_data_element= new_star_data[index]
    new_star_data_element = [elem.replace("\n", "") for elem in new_star_data_element]
    new_star_data_element = new_star_data_element[:7]
    final_star_data.append(data+new_star_data_element)

with open("final.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(final_star_data)