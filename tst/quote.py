import requests
from bs4 import BeautifulSoup

url = "http://quotes.toscrape.com/tag/inspirational/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

quotes = soup.find_all("div", class_="quote")

for q in quotes:
    text = q.find("span", class_="text").get_text(strip=True)
    author = q.find("small", class_= "author").get_text(strip=True)
    tags_list = []
    tags_div = q.find("div", class_="tags")
    if tags_div:
        tag_elements = tags_div.find_all("a", class_="tag")
        tags_list = [tag.get_text(strip=True) for tag in tag_elements]
    
    tags = ", ".join(tags_list)
    print(text + " --- " + author)
    if tags:
        print("Tags: " + tags)
    print()