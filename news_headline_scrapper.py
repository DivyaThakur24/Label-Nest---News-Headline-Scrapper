# -*- coding: utf-8 -*-
"""News Headline Scraper

# **News Headlines Scraper Workflow**

For each news source:

1. Fetch its RSS feed.

2. Parse it as XML.

3. Take the first 4 news items.

4. Extract title, link, and date.

5. Format the date nicely.

6. Save everything into a list.

7. If something goes wrong, print an error but continue.
"""

!pip install bs4


import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# Define RSS feeds
sources = {
    "TechCrunch": "http://feeds.feedburner.com/TechCrunch/",
    "Economic Times": "https://economictimes.indiatimes.com/rssfeedstopstories.cms"
}

headlines = []

# Fetch and parse 4 headlines per source
for source, url in sources.items():
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "xml")  # RSS is XML

        items = soup.find_all("item")[:4]  # get first 4 headlines

        for item in items:
            title = item.title.text if item.title else "N/A"
            link = item.link.text if item.link else "N/A"
            pub_date = item.pubDate.text if item.pubDate else "N/A"

            # Try formatting publication date
            if pub_date != "N/A":
                try:
                    pub_date = datetime.strptime(pub_date[:25], "%a, %d %b %Y %H:%M:%S").strftime("%Y-%m-%d %H:%M")
                except:
                    pass

            headlines.append({
                "Source": source,
                "Title": title,
                "Link": link,
                "Published Date": pub_date
            })

    except Exception as e:
        print(f"⚠️ Error fetching {source}: {e}")

# Save results into CSV
df = pd.DataFrame(headlines)
output_file = "news_headlines.csv"
df.to_csv(output_file, index=False, encoding="utf-8")

# Or save as Excel
df.to_excel("news_headlines.xlsx", index=False, engine="openpyxl")

print(f"✅ Headlines saved to {output_file}\n")

# Print Top 2 Headlines Summary
print("📢 Top 2 Headlines Summary:")
for i, row in df.head(2).iterrows():
    print(f"\n{i+1}. {row['Title']}\n   ({row['Source']}, {row['Published Date']})\n   Link: {row['Link']}")

df_csv = pd.read_csv(output_file)
df_csv.head(n=10)

df_xl = pd.read_excel("news_headlines.xlsx")
df_xl.head(n=10)