import pandas as pd
from matplotlib import pyplot as plt
import streamlit as st
from parse_html import parse_html
import os

def plot(sampling='W',engagement_Metric='All'):
    # Resample the DataFrame to daily frequency and calculate the sum of the engagement metrics
    time_based_engagement = engagement_df.resample(sampling).sum()

    print(time_based_engagement)

    # Create a line plot of the daily engagement metrics
    fig, ax = plt.subplots(figsize=(10, 6))
    if engagement_Metric == 'likes':
        ax.set_ylabel("Likes")
        ax.plot(time_based_engagement.index, time_based_engagement["likes"], label="Likes")
    elif engagement_Metric == 'comments':
        ax.set_ylabel("Comments")
        ax.plot(time_based_engagement.index, time_based_engagement["comments"], label="Comments")
    else:
        ax.set_ylabel("Engagement")
        ax.plot(time_based_engagement.index, time_based_engagement["likes"], label="Likes")
        ax.plot(time_based_engagement.index, time_based_engagement["comments"], label="Comments")

    ax.set_xlabel("Date")
    ax.set_title(f"{hashtag} Engagement Metrics")
    ax.set_title(f"{hashtag} Engagement Metrics")
    ax.legend()
    st.pyplot(fig)
# Add a title and intro text
st.title('LinkedIn Hashtag Tracker')
st.text('This is a web app to allow exploration of Engagement of hashtag')

username = st.text_input('Linkedin User Name')
password = st.text_input('Linkedin Password', type="password")
hashtag = st.text_input('Linkedin Hashtag', 'blockchain')
# Create file uploader object
# upload_file = st.file_uploader('Upload a file containing earthquake data')
engagement_Metric = st.radio('Select Engagement Metric:',('likes','comments','both'))
chart_time_level = st.radio('Select Engagement Metric time window:',('daily','weekly','monthly','All'))
time_period_scrapping = st.radio('Select the timeperiod of scrapping:',('from my network','past 24 hrs','past week','past month'))
if st.button("generate result"):
    if not (os.path.isfile(os.path.join(os.getcwd(),'Hashtag_Analytics.csv'))):
        parse_html(username,password,hashtag,time_period_scrapping)

    engagement_df = pd.read_csv('Hashtag_Analytics.csv',parse_dates=['date'])

    # Set the timestamp column as the DataFrame index
    engagement_df.set_index("date", inplace=True)

    st.header(f'Statistics of Engagement on {hashtag}')
    st.write(engagement_df.describe())

    st.header('Plot of Data')
    if chart_time_level == 'daily':
        plot('D',engagement_Metric)
    elif chart_time_level == 'weekly':
        plot('W',engagement_Metric)
    elif chart_time_level == 'monthly':
        plot('M',engagement_Metric)
    
    else:
        plot('D',engagement_Metric)
        plot('W',engagement_Metric)
        plot('M',engagement_Metric)





