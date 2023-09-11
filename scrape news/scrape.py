from requests import get
from bs4 import BeautifulSoup as soup
import csv
import datetime

path = "https://www.bbc.com/news/world-60525350"

url = get(path)

request = url.text

soup_data = soup(request, 'html.parser' )

latest = soup_data.find("div", {"class":"gel-layout__item gel-3/5@l"})

ol = latest.find("ol")

li = ol.find_all("li")

titles = []

for lii in li:
    header = lii.find("header")
    if header:
        # fetch title
        title = header.text

        # fetch link
        link = header.find("a").get("href")
        link = f"https://www.bbc.com{link}"

        # for time that has no specified date, set it to today
        time = lii.find("span", {"class":"qa-post-auto-meta"}).text
        if len(time) <= 5:
            time = f'{time} {datetime.datetime.now().strftime("%d %b")}'
        
        # getting into the link of a particular news in iteration
        news = get(link)
        news_request = news.text
        news_soup = soup(news_request, 'html.parser')

        # fetch autho
        author = news_soup.find("div", {"class":"ssrcss-68pt20-Text-TextContributorName e8mq1e96"})

        # fetch content
        text_blocks = news_soup.find_all("div", {"data-component":"text-block"})
        text = []
        if text_blocks:
            for text_block in text_blocks:
                text.append(text_block.text)
            text_block = " ".join(text_block for text_block in text)
        else:
            text_block = ""
        
        if author:
            titles.append((time,title,text_block,author.text[3:],link))
        else:
            titles.append((time,title,text_block,None,link))

with open('data.csv', 'w') as file:
    # create a writer object
    writer = csv.writer(file)

    writer.writerow(["time","title","content","author","link"])
    # write the data to the file
    for row in titles:
        writer.writerow(row)

