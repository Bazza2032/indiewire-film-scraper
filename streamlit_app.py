import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai

# Set up OpenAI from secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="The Playlist Film Headlines", layout="wide")
st.title("🎞️ The Playlist Film Headlines Scraper + GPT Summarizer")

URL = "https://theplaylist.net/category/news/"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def summarize_with_gpt(title, summary):
    prompt = f"Rewrite the following film news headline and summary into a short, elegant 2-line summary suitable for a film digest.\n\nTitle: {title}\n\nSummary: {summary}\n\nOutput:"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a concise, engaging film newsletter editor."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=80,
            temperature=0.7,
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"GPT Summary failed: {e}"

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

            # Optional GPT summary
            with st.spinner("✨ Summarizing with GPT..."):
                refined = summarize_with_gpt(title, summary)
                st.success(refined)

            st.markdown("---")

except Exception as e:
    st.error("❌ Failed to fetch or parse articles.")
    st.exception(e)
