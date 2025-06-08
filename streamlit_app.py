import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="IndieWire Film News", layout="wide")
st.title("🎬 IndieWire Film Headlines Scraper")

URL = "https://www.indiewire.com/c/film/news/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Referer": "https://www.google.com/"
}

try:
    response = requests.get(URL, headers=HEADERS, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")
    articles = soup.find_all("article")

    if not articles:
        st.warning("No articles found — site structure may have changed or blocked our scraper.")
    
    for article in articles[:10]:  # Top 10 headlines
        headline_tag = article.find("h2")
        summary_tag = article.find("p")
        link_tag = article.find("a", href=True)

        if headline_tag and link_tag:
            st.subheader(headline_tag.get_text(strip=True))
            st.write(summary_tag.get_text(strip=True) if summary_tag else "_No summary available_")
            st.markdown(f"[Read More]({link_tag['href']})")
            st.markdown("---")

except Exception as e:
    st.error("❌ Failed to fetch or parse articles.")
    st.exception(e)
