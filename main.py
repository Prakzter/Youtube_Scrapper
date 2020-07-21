import pandas as pd
from selenium import webdriver
import re
import time
driver = webdriver.Chrome("/Users/prakky/Desktop/DataSCIENCE/Git_proj/Youtube_Scrapper/drafts/chromedriver")



# open browser and print video title

url = "https://www.youtube.com/watch?v=ZtTt822bDNE"
driver.get(url)
time.sleep(2)
vid_title = driver.find_element_by_xpath('//*[@id="container"]/h1/yt-formatted-string').text
vid_id = url.split("https://www.youtube.com/watch?v=")[1]
print("\n\n")
print("------------------------------------------------------------------------------------")

# page loading to retrieve all comments
comment_section = driver.find_element_by_xpath('//*[@id="comments"]')
driver.execute_script("arguments[0].scrollIntoView();", comment_section)
time.sleep(2)

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


df = pd.DataFrame(list(full_list.items()),columns = ['Username','Comment'])
df["Video_title"] = vid_title
df["Video_Id"] = vid_id
print(df)


driver.close()








# def remove_emoji(string):
#     emoji_pattern = re.compile("["
#                                u"\U0001F600-\U0001F64F"  # emoticons
#                                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
#                                u"\U0001F680-\U0001F6FF"  # transport & map symbols
#                                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
#                                u"\U00002500-\U00002BEF"  # chinese char
#                                u"\U00002702-\U000027B0"
#                                u"\U00002702-\U000027B0"
#                                u"\U000024C2-\U0001F251"
#                                u"\U0001f926-\U0001f937"
#                                u"\U00010000-\U0010ffff"
#                                u"\u2640-\u2642"
#                                u"\u2600-\u2B55"
#                                u"\u200d"
#                                u"\u23cf"
#                                u"\u23e9"
#                                u"\u231a"
#                                u"\ufe0f"  # dingbats
#                                u"\u3030"
#                                "]+", flags=re.UNICODE)
#     return emoji_pattern.sub(r'', string)

# yt_link = input("Link to Youtube video: ")
# print("-------------------------------------------------------------------------------")