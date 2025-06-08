import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="IndieWire Film News", layout="wide")
st.title("🎬 IndieWire Film Headlines Scraper")

URL = "https://www.indiewire.com/c/film/news/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

try:
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")
    articles = soup.find_all("article")

    for article in articles[:10]:  # show top 10
        headline_tag = article.find("h2")
        summary_tag = article.find("p")
        link_tag = article.find("a", href=True)

        if headline_tag and link_tag:
            st.subheader(headline_tag.get_text(strip=True))
            st.write(summary_tag.get_text(strip=True) if summary_tag else "_No summary available_")
            st.markdown(f"[Read More]({link_tag['href']})")
            st.markdown("---")
except Exception as e:
    st.error(f"Failed to fetch news: {e}")
