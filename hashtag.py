import os
from linkedin_api import Linkedin
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
load_dotenv()

# Set up credentials for the LinkedIn API
username = os.getenv("LINKEDIN_USERNAME")
password = os.getenv("LINKEDIN_PASSWORD")

# Log in to LinkedIn
api = Linkedin(username, password)

# Define the hashtag you want to analyze
hashtag = "ABISupplyChainAnalytics"

# Set up a start and end date for the analysis
start_date = datetime.now() - timedelta(days=30)
end_date = datetime.now()

# profile = api.get_profile('billy-g')
# print(profile)

# Define a function to retrieve the posts that contain the hashtag
def get_hashtag_posts(hashtag, start_date, end_date):
    posts = api.search({"keywords":"ABISupplyChainAnalytics","origin":"HISTORY"},
        limit=100
    )
    filtered_posts = []
    print(posts)
    for post in posts:
        if "created" in post and "totalLikes" in post and "totalComments" in post:
            created_time = datetime.fromtimestamp(post["created"] / 1000.0)
            if start_date <= created_time <= end_date:
                filtered_posts.append(post)
    return filtered_posts
   

# Call the function to retrieve the posts
hashtag_posts = get_hashtag_posts(hashtag, start_date, end_date)
print(hashtag_posts)
print("*"*50)

# # Create an empty list to store the engagement data
# engagement_data = []

# # Loop through the posts and extract the engagement data
# for post in hashtag_posts:
#     engagement_data.append({
#         "timestamp": post["date"],
#         "likes": post["total_likes"],
#         "comments": post["total_comments"]
#     })

# # Convert the engagement data to a pandas DataFrame
# engagement_df = pd.DataFrame(engagement_data)

# # Convert the timestamp column to a datetime format
# engagement_df["timestamp"] = pd.to_datetime(engagement_df["timestamp"])

# # Set the timestamp column as the DataFrame index
# engagement_df.set_index("timestamp", inplace=True)

# # Resample the DataFrame to daily frequency and calculate the sum of the engagement metrics
# daily_engagement = engagement_df.resample("D").sum()

# # Create a line plot of the daily engagement metrics
# fig, ax = plt.subplots(figsize=(10, 6))
# ax.plot(daily_engagement.index, daily_engagement["likes"], label="Likes")
# ax.plot(daily_engagement.index, daily_engagement["comments"], label="Comments")
# ax.set_xlabel("Date")
# ax.set_ylabel("Engagement")
# ax.set_title(f"{hashtag} Engagement Metrics")
# ax.legend()
# plt.show()
