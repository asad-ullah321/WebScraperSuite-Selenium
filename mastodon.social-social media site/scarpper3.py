from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import requests
import time

driver = webdriver.Chrome()
driver.get("https://mastodon.social/explore")
SCROLL_PAUSE_TIME = 1
dic1 = {
    "name": [],
    "profile_link": [],
    "profile_pic_link": [],
    "date_time": [],
    "post_text": [],
    "picture_link": [],
    "video_link": [],
    "other_link": [],
    "hashtags": [],
}
my_set = set()
image = 0


for i in range(20):
    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)
    try:
        elem = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.status")
            )  # This is a dummy element
        )
    finally:
        postElem = driver.find_elements(By.CSS_SELECTOR, "div.status")
        print(len(postElem))
        if len(postElem) > 0:
            for i in postElem:
                text = i.find_elements(By.CSS_SELECTOR, "div.status__content__text")
                print("post", len(text))
                if len(text) > 0:
                    postText = text[0].text
                    if postText[:10] in my_set or postText in my_set:
                        continue
                    if len(postText) > 10:
                        my_set.add(postText[:10])
                    elif postText:
                        my_set.add(postText)

                    dic1["post_text"].append(postText)
                else:
                    dic1["post_text"].append("-")

                name = i.find_elements(By.CSS_SELECTOR, "strong.display-name__html")
                if len(name) > 0:
                    dic1["name"].append(name[0].text)
                else:
                    dic1["name"].append("-")


                profile_link = i.find_elements(By.CSS_SELECTOR, "a.status__display-name")
                if len(profile_link) > 0:
                    dic1["profile_link"].append(profile_link[0].get_attribute("href"))
                else:
                    dic1["profile_link"].append("-")


                profile_pic_link = i.find_elements(By.CSS_SELECTOR, "div.account__avatar > img")
                if len(profile_pic_link) > 0:
                    dic1["profile_pic_link"].append(profile_pic_link[0].get_attribute("src"))
                else:
                    dic1["profile_pic_link"].append("-")


                date_time = i.find_elements(By.CSS_SELECTOR, "a.status__relative-time > time")
                if len(date_time) > 0:

                    dic1["date_time"].append(date_time[0].text)
                else:
                    dic1["date_time"].append("-")
                  
                  
                picture_link = i.find_elements(By.CSS_SELECTOR, "a.media-gallery__item-thumbnail > img")
                if len(picture_link) > 0:
                    links = ""
                    for j in picture_link:
                        link = j.get_attribute("src")
                        links = link + " , " + links
                        print(link)
                        if link.startswith("http"):
                            r = requests.get(link)
                            time.sleep(1)
                            with open("post_images/"+str(image)+".webp", 'wb') as outfile:
                                    outfile.write(r.content)
                                    image=image+1
                    dic1["picture_link"].append(links)
                else:
                    dic1["picture_link"].append("-")
                

                video_link = i.find_elements(By.CSS_SELECTOR, "div.video-player > video")
                if len(video_link) > 0:
                    dic1["video_link"].append(video_link[0].get_attribute("src"))
                else:
                    dic1["video_link"].append("-")

                other_link = i.find_elements(By.CSS_SELECTOR, "a.status-link")
                if len(other_link) > 0:
                    dic1["other_link"].append(other_link[0].get_attribute("href"))
                else:
                    dic1["other_link"].append("-")
                


                hashtags = i.find_elements(By.CSS_SELECTOR, "div.hashtag-bar > a > span")
                if len(hashtags) > 0:
                    HashTags = ""
                    for j in hashtags:
                        HashTags = HashTags + " #" + j.text
                    dic1["hashtags"].append(HashTags)
                else:
                    dic1["hashtags"].append("-")
                

    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, window.scrollY + 1000);")



##################################################
# code to save data in csv is generated from gpt #
##################################################
csv_file = "posts.csv"
# Write data to CSV file
with open(csv_file, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=dic1.keys())
    # Write the header
    writer.writeheader()
    # Write the data rows
    for i in range(len(dic1["post_text"])):
        row = {key: dic1[key][i] for key in dic1}
        writer.writerow(row)
# for i in range(len(dic1["title_image_link"])):
#     urllib.request.urlretrieve(dic1["title_image_link"][i], "images/{dic1[title][i]}{i}.jpg")

print(f"CSV file '{csv_file}' has been created successfully.")