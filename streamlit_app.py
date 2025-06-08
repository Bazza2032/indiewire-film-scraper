import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="The Playlist Film Headlines", layout="wide")
st.title("🎞️ The Playlist Film Headlines Scraper")

URL = "https://theplaylist.net/category/news/"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

try:
    response = requests.get(URL, headers=HEADERS, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")
    articles = soup.find_all("div", class_="td-module-container")

    if not articles:
        st.warning("No articles found — site layout may have changed.")

    for article in articles[:10]:
        title_tag = article.find("h3", class_="entry-title")
        link_tag = title_tag.find("a") if title_tag else None
        summary_tag = article.find("div", class_="td-excerpt")

        if title_tag and link_tag:
            title = link_tag.get_text(strip=True)
            link = link_tag["href"]
            summary = summary_tag.get_text(strip=True) if summary_tag else "No summary available"

            st.subheader(title)
            st.write(summary)
            st.markdown(f"[Read More]({link})")
            st.markdown("---")

except Exception as e:
    st.error("❌ Failed to fetch or parse articles.")
    st.exception(e)
