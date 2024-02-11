from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import csv
import requests
import time

driver = webdriver.Chrome()
driver.get("https://www.politifact.com/")
assert "Fact-checks" in driver.page_source
factsELem = driver.find_elements(By.CSS_SELECTOR, "article.m-statement")


dic = {
    "source": [],
    "m-statement__name-Link": [],
    "stated_on": [],
    "statement_quote": [],
    "statement_quote_link": [],
    "footer": [],
    "meter_Image_link": [],
    "meter_alt_text": [],
    "source_image_link": [],
}
image = 0
for i in factsELem:


    ###################################################################################
    #  <a href="/personalities/elon-musk/" class="m-statement__name" title="Elon Musk">
    #                Elon Musk
    #   </a>
    source = i.find_elements(By.CSS_SELECTOR, "a.m-statement__name")
    if len(source) > 0:
        dic["source"].append(source[0].text)
        dic["m-statement__name-Link"].append(source[0].get_attribute("href"))
    else:
        dic["source"].append("-")
        dic["m-statement__name-Link"].append("-")


    ##############################################
    # <div class="m-statement__desc">
    #      stated on February 2, 2024 in an X post
    # </div>
    stated_on = i.find_elements(By.CSS_SELECTOR, "div.m-statement__desc")
    if len(stated_on) > 0:
        dic["stated_on"].append(stated_on[0].text)
    else:
        dic["stated_on"].append("-")


    ######################################################################################################
    # <div class="m-statement__quote">
    #    <a href="/factchecks/2024/feb/06/elon-musk/elon-musk-is-wrong-to-say-joe-biden-is-recruiting/">
    #        Biden’s strategy is to “get as many illegals in the country as possible” and “legalize them
    #            to create a permanent majority.”
    #    </a>
    # </div>
    statement_quote = i.find_elements(
        By.CSS_SELECTOR, "div.m-statement__quote"
    )  # use gpt for the css selector by giving it the html of the element
    if len(statement_quote) > 0:
        dic["statement_quote"].append(statement_quote[0].text)
        statement_quote = i.find_elements(
        By.CSS_SELECTOR, "div.m-statement__quote > a"
         )  # use gpt for the css selector by giving it the html of the element
        if len(statement_quote) > 0:
            dic["statement_quote_link"].append(statement_quote[0].get_attribute("href"))
    else:
        dic["statement_quote"].append("-")
        dic["statement_quote_link"].append("-")


    #############################################
    # <footer class="m-statement__footer">
    #        By Amy Sherman • February 6, 2024
    # </footer>
    footer = i.find_elements(By.CSS_SELECTOR, "footer.m-statement__footer")
    if len(footer) > 0:
        dic["footer"].append(footer[0].text)
    else:
        dic["footer"].append("-")


    ###################################################################################################################################
    #   #<div class="m-statement__meter">
    #    <div class="c-image" style="padding-top: 89.49771689497716%;">
    #        <img src="https://static.politifact.com/CACHE/images/politifact/rulings/meter-false/33efdb6633e5e2fdc2d4e2f63383a1e0.jpg."
    #            class="c-image__thumb" alt="true" width="219" height="196">
    #       <picture>
    #            <img src="https://static.politifact.com/politifact/rulings/meter-false.jpg"
    #               class="c-image__original " width="219" height="196" alt="false">
    #        </picture>
    #    </div>
    # </div>
    meter_Image = i.find_elements(
        By.CSS_SELECTOR,
        "div.m-statement__meter > div.c-image > picture > img.c-image__original",
    )  # use gpt for the css selector by giving it the html of the element
    if len(meter_Image) > 0:
        dic["meter_Image_link"].append(meter_Image[0].get_attribute("src"))
        dic["meter_alt_text"].append(meter_Image[0].get_attribute("alt"))
    else:
        dic["meter_Image_link"].append("-")
        dic["meter_alt_text"].append("-")


    ###################################################################################################################################
    # <div class="m-statement__image">
    # <div class="c-image" style="padding-top: 119.27710843373494%;">
    # <img src="https://static.politifact.com/CACHE/images/politifact/mugs/Elon_Musk/d50faad08cda7bbd7dd969afe5f2429f.jpeg"
    #    class="c-image__thumb" width="83" height="99">
    # <picture>
    # <img src="https://static.politifact.com/CACHE/images/politifact/mugs/Elon_Musk/8df03bfbd751cfd40656bb49396945af.jpeg"
    #    class="c-image__original " width="83" height="99">
    # </picture>
    # </div>
    # </div>
    source_image_link = i.find_elements(
        By.CSS_SELECTOR,
        "div.m-statement__image > div.c-image > picture > img.c-image__original",
    )  # use gpt for the css selector by giving it the html of the element
    if len(source_image_link) > 0:
        link = source_image_link[0].get_attribute("src")
        dic["source_image_link"].append(link)
        r = requests.get(link)
        time.sleep(1)
        with open("politifact_facts_image/"+str(image)+".png", 'wb') as outfile:
            outfile.write(r.content)
            image=image+1
    else:
        dic["source_image_link"].append("-")


##################################################
# code to save data in csv is generated from gpt #
##################################################
csv_file = "politifact_factChecks.csv"
# Write data to CSV file
with open(csv_file, "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=dic.keys())
    # Write the header
    writer.writeheader()
    # Write the data rows
    for i in range(len(dic["source"])):
        row = {key: dic[key][i] for key in dic}
        writer.writerow(row)

print(f"CSV file '{csv_file}' has been created successfully.")




######################################################################
#                Scrapping code for latest articles                  #
######################################################################

assert "Latest Articles" in driver.page_source
ArticleELem = driver.find_elements(By.CSS_SELECTOR, "div.m-teaser")
dic1 = {
    "title": [],
    "title_link": [],
    "stated_on": [],
    "title_image_link": [],
    "title_image_alt": [],

}
image = 1
for i in ArticleELem:
    title = i.find_elements(By.CSS_SELECTOR, "h3.m-teaser__title > a")
    if len(title) > 0:
        dic1["title"].append(title[0].text)
        dic1["title_link"].append(title[0].get_attribute("href"))
    else:
        dic1["title"].append("-")
        dic1["title_link"].append("-")

  

    title_image_link = i.find_elements(
        By.CSS_SELECTOR,
        "div.c-image > a > picture > img.c-image__original",
    )  # use gpt for the css selector by giving it the html of the element
    if len(title_image_link) > 0:
        link = title_image_link[0].get_attribute("src")
        altText = title_image_link[0].get_attribute("alt")
        if not link:
            link = title_image_link[0].get_attribute("data-src")
        dic1["title_image_link"].append(link)
        dic1["title_image_alt"].append(altText)
        # urllib.request.urlretrieve(link, str(image)+".png")
        r = requests.get(link)
        time.sleep(1)
        with open("politifact_articles_image/"+str(image)+".png", 'wb') as outfile:
            outfile.write(r.content)
            image=image+1

    else:
        dic1["meter_Image_link"].append("-")
        dic1["title_image_alt"].append("-")

    stated_on = i.find_elements(By.CSS_SELECTOR, "div.m-teaser__meta")
    if len(stated_on) > 0:
        dic1["stated_on"].append(stated_on[0].text)
    else:
        dic1["stated_on"].append("-")
 
       
driver.close()


##################################################
# code to save data in csv is generated from gpt #
##################################################
csv_file = "politifact_articles.csv"
# Write data to CSV file
with open(csv_file, "w", newline="") as csvfile:
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
