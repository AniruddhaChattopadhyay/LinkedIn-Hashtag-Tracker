from bs4 import BeautifulSoup
import re
from datetime import datetime,timedelta
import pandas as pd
from scrapper import scrapper


def parse_html(username,password,hashtag,time_period_scrapping):
    scrapper(username, password, hashtag,time_period_scrapping)

    with open('file_new.html','r',encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content,'html.parser')
    post_info = []
    last_date = datetime.now()
    for ultag in soup.find_all('ul', {'class': 'reusable-search__entity-result-list'}):
        for litag in ultag.findChildren('li',recursive=False):
            regex_comment = re.compile('.*social-details-social-counts__comments.*')
            regex_like = re.compile('social-details-social-counts__reactions-count')
            try:
                comments = litag.find('li',{'class': regex_comment}).getText().replace('\n','').replace(' ', '').replace('comments','').replace('comment','')
            except:
                comments = 0
            try:
                likes = litag.find('span',{'class': regex_like}).getText()
            except:
                likes = 0
            try:
                date_posted_div = litag.find("div",{'class':'update-components-text-view break-words'})
                date_posted_parent_span = date_posted_div.findChildren("span",{'aria-hidden':"true"})[0]
                date_posted_span = date_posted_div.findChildren()[0]
                date_posted = date_posted_span.getText()
                date_posted = date_posted[:3].strip()
                number_date = re.findall(r'\d+', date_posted)[0]
                number_date = int (number_date)

                if date_posted.find('h')!=-1:
                    number_date = 1
                elif date_posted.find('d')!=-1:
                    number_date = number_date
                    
                elif date_posted.find('w')!=-1:
                    number_date = number_date*7

                elif date_posted.find('m')!=-1:
                    number_date = number_date*30

                elif date_posted.find('y')!=-1:
                    number_date = number_date*365
                
                date = datetime.now() - timedelta(days=number_date)
                last_date = date
            except Exception as e:
                print(e)
                date = last_date
            print(likes,comments,date)
            print("*"*50)
            post_info.append([likes,comments,date])
        break

    df = pd.DataFrame(post_info,columns=['likes','comments','date'])
    df.to_csv("Hashtag_Analytics.csv")
