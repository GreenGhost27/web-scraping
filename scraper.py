from selenium import webdriver
from bs4 import BeautifulSoup
import time
import request 
import csv

START_URL = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"
browser = webdriver.Chrome("C:\Users\sheel\OneDrive\Desktop\scraper\chromedriver.exe")
browser.get(START_URL)
time.sleep(10)
headers = ["Name", "Distance", "Mass", "Radius"]
star_data = []
new_star_data = []
def scrape():
    for i in range(1,428):
        while True:
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source, "html.parser")
            current_page_num = int(soup.find_all("input", attrs={"class", "page_num", })[0].get("value"))
            if current_page_num < i:
                browser.find_element_by_xpath('//*[@id="mw-content-text"]/div[1]/table/tbody/tr[1]/td[2]').click()
            elif current_page_num > i:
                browser.find_element_by_xpath('//*[@id="mw-content-text"]/div[1]/table/tbody/tr[1]/td[2]/a').click()
            else:
                break
    for tr_tag in soup.find_all("tr", attrs={"class", "star"}):
            td_tag = tr_tag.find_all("td")
            temp_list = []
            for index, td_tags in enumerate(td_tags):
                if index == 0:
                    temp_list.append(td_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(td_tags.contents[0])
                    except:
                        temp_list.append("")
            hyperlink_td_tag =td_tags[0]
            temp_list.append("https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"+hyperlink_td_tag.find_all("a", href=True)[0]["href"])
            star_data.append(temp_list)
        browser.find_element_by_xpath('//*[@id="mw-content-text"]/div[1]/table/thead/tr/th[2]').click()
        print(f"{i} page done 1")

def scrape_more_data(hyperlink):
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content, "html.parser")
        temp_list = []
        for tr_tag in soup.find_all("tr", attrs={"class":"fact_row"}):
            td_tags = tr_tag.find_all("td")
            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div", attrs={"class":"value"})[0].contents[0])
                
                except:
                    temp_list.append("")
        new_planet_data.append(temp_list)
    except:
        time.sleep(1)
        scrape_more_data(hyperlink)
scrape()

for index, data in enumerate(planet_data):
    scrape_more_data(data[5])      
    print(f"{index+1} page done 2")  
final_star_data = []

for index, data in enumerate(star_data):
    new_star_data_element = new_star_data[index]
    new_star_data_element = [elem.replace("\n","") for elem in new_star_data_element]
    new_star_data_element = new_star_data_element[:7]
    final_star_data.append(data + new_star_data_element)
    
with open("scrapper_2.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(final_planet_data)

