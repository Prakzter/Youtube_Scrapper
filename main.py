import pandas as pd
import os
from selenium import webdriver
import re
import time
driver = webdriver.Chrome("/Users/prakky/Desktop/DataSCIENCE/Git_proj/Youtube_Scrapper/drafts/chromedriver")


# sample channel_url = "https://www.youtube.com/c/DataProfessor/videos"
# sample single_url = "https://www.youtube.com/watch?v=ZtTt822bDNE"

# extracting video Urls from a Channel
channel_url = input("Link to Youtube Channel (Videos page): ")
print("\n")
driver.get(channel_url)

# page loading to retrieve all videos
last_height = driver.execute_script("return document.documentElement.scrollHeight")
while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

    # Wait to load page
    time.sleep(3)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.documentElement.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

#put the urls in the list
video_url_list = []
elems = driver.find_elements_by_xpath('//*[@id="video-title"]')
for link in elems:
    each_link = link.get_attribute("href")
    video_url_list.append(each_link)

print(f"{len(video_url_list)} videos found in the Youtube Channel\nScanning videos now")
current_path = os.getcwd()
filepath = os.mkdir(current_path + "/scrapped")

# function to extract comments from a single video
def get_video_comments(url):

    driver.get(url)
    time.sleep(2)
    vid_title = driver.find_element_by_xpath('//*[@id="container"]/h1/yt-formatted-string').text
    vid_id = url.split("https://www.youtube.com/watch?v=")[1]
    print("\n")
    print(f"Loading video -->> {url} now")

    # page loading to retrieve all comments
    comment_section = driver.find_element_by_xpath('//*[@id="comments"]')
    driver.execute_script("arguments[0].scrollIntoView();", comment_section)
    time.sleep(1)

    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

        # Wait to load page
        time.sleep(3)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    

    # extracting comments (not comment replies) to dataframe
    name_elems=driver.find_elements_by_xpath('//*[@id="author-text"]')
    comment_elems = driver.find_elements_by_xpath('//*[@id="content-text"]')
    num_of_names = len(name_elems)
    full_list = {}
    for i in range(num_of_names):
        username = name_elems[i].text 
        comment = comment_elems[i].text  
        full_list[username] = comment

    dataf = pd.DataFrame(columns = ['Username','Comment',"Video_title","Video_Id"])
    dataf["Username"] = full_list.keys()
    dataf["Comment"] =  full_list.values()
    dataf["Video_title"] = vid_title
    dataf["Video_Id"] = vid_id

    dataf.to_csv(current_path + "/scrapped/" + "YTS_" + str(vid_title) + ".csv")
    # return dataf
    del dataf
    del full_list
    

  

for link in video_url_list:
    get_video_comments(link)
print(f"{len(video_url_list)} csv files have been created. Please check the directory of the main python file.")
    
  

# end webdriver
driver.close()






