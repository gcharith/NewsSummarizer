import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from openai import OpenAI
import requests
import streamlit as st

load_dotenv()
openai_key = os.getenv('OPENAI_API_KEY')

openai = OpenAI()

headers = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

class Website:
    def __init__(self,url):
        self.url = url
        resp = requests.get(url,headers=headers)
        soup = BeautifulSoup(resp.content,'html.parser')
        self.title = soup.title if soup.title else 'no title'
        for x in soup.body(["script","style","img","input"]):
            x.decompose()
        self.text = soup.body.get_text(separator='\n',strip=True)

def user_prompt(website):
    user_prompt_msg = f"You are looking at a website that has the title {website.title}"
    user_prompt_msg += "\n The text from the website is as follows: \n Provide summary for the top 5 news in different paragraph paragraphs\n\n"
    user_prompt_msg += website.text
    return user_prompt_msg

def message(website):
    system = "you are a summarizing assistant that help people by analyzing news website and producing top news from a text from news  website. You will iignore all the text that not relate to news inside the text."
    messages = [
    {'role':'system','content': system},
    {'role':'user','content':user_prompt(website)}
    ]
    return messages

def summarize(url):
    website = Website(url)
    resp = openai.chat.completions.create(model='gpt-4o-mini', messages = message(website))
    return resp.choices[0].message.content

st.title("News Summarizer")

news_websites = {
    "Choose a Site...":"",
    "BBC News": "https://www.bbc.com/news",
    "CNN": "https://www.cnn.com",
    "New York Times": "https://www.nytimes.com",
    "The Guardian": "https://www.theguardian.com/us",
    "Al Jazeera": "https://www.aljazeera.com",
    "Fox News": "https://www.foxnews.com",
    "NPR": "https://www.npr.org"
}

selection = st.selectbox("Select site from popular options",list(news_websites.keys()))
load_url = news_websites[selection]

user_url = st.text_input("Or enter your favourite news website url: ", value = load_url)

url = user_url or load_url

if url:
    st.write(summarize(url))
    
