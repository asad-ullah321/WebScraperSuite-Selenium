from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import requests
import time


driver = webdriver.Chrome()
driver.get("https://www.altnews.in")
assert "Home" in driver.page_source

dic1 = {
    "title": [],
    "story_link": [],
    "date_time": [],
    "authors": [],
    "authors_link": [],
    "thumbnail_link": [],
}
image = 1
SCROLL_PAUSE_TIME = 1
my_set = set()

for i in range(10):
    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)
    try:
        elem = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "article.status-publish")
            )  # This is a dummy element
        )
    finally:
        ArticleELem = driver.find_elements(By.CSS_SELECTOR, "article.status-publish")
        print(len(ArticleELem))
        if len(ArticleELem) > 0:
            for i in ArticleELem:
                
                title = i.find_elements(By.CSS_SELECTOR, "h4.entry-title > a")

                if len(title) > 0:
                    if title[0].text in my_set:
                        continue
                    my_set.add(title[0].text)
                    dic1["title"].append(title[0].text)
                    dic1["story_link"].append(title[0].get_attribute("href"))
                else:
                    dic1["title"].append("-")
                    dic1["story_link"].append("-")



                date_time = i.find_elements(By.CSS_SELECTOR, "time.entry-date")
                if len(date_time) > 0:
                    dic1["date_time"].append(date_time[0].text)
                else:
                    dic1["date_time"].append("-")


        

                date_time = i.find_elements(By.CSS_SELECTOR, "a.status__relative-time > time")
                if len(date_time) > 0:

                    dic1["date_time"].append(date_time[0].text)
                else:
                    dic1["date_time"].append("-")
                  
                  
                authors = i.find_elements(By.CSS_SELECTOR, "a.author")
                if len(authors) > 0:
                    Authors = ""
                    links = ""
                    for j in authors:
                        link = j.get_attribute("href")
                        links = link + " , " + links
                        Authors = j.text + " , " + Authors 
                    dic1["authors"].append(Authors)
                    dic1["authors_link"].append(links)
                        
                else:
                    dic1["authors"].append("-")
                    dic1["authors_link"].append("-")

                

                thumbnail_link = i.find_elements(By.CSS_SELECTOR, "div.thumb-w > img")
                if len(thumbnail_link) > 0:
                    link = thumbnail_link[0].get_attribute("src")
                    dic1["thumbnail_link"].append(link)
                    if link.startswith("http"):
                            r = requests.get(link)
                            time.sleep(1)
                            with open("images/"+str(image)+".png", 'wb') as outfile:
                                    outfile.write(r.content)
                                    image=image+1
                else:
                    dic1["thumbnail_link"].append("-")

               
                

    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight*2);")



##################################################
# code to save data in csv is generated from gpt #
##################################################
csv_file = "articles.csv"
# Write data to CSV file
with open(csv_file, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=dic1.keys())
    # Write the header
    writer.writeheader()
    # Write the data rows
    for i in range(len(dic1["title"])):
        row = {key: dic1[key][i] for key in dic1}
        writer.writerow(row)
# for i in range(len(dic1["title_image_link"])):
#     urllib.request.urlretrieve(dic1["title_image_link"][i], "images/{dic1[title][i]}{i}.jpg")

print(f"CSV file '{csv_file}' has been created successfully.")
