import requests
from bs4 import BeautifulSoup as BS
import csv
from model import engine, Post, create_db_table
from sqlalchemy.orm import Session, sessionmaker


session = Session(bind=engine)

def get_response(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.text
    else:
        return "Error"

def get_data(html):
    soup = BS(html, 'html.parser')
    content = soup.find('div', class_= "col-2 new-real-estate-srp")
    main = content.find_all('div', class_="container-results large-images")[-1]
    posts = main.find_all('div', class_="clearfix")
    for post in posts: 
        image = post.find('div', class_="image").find('img').get('data-src')
        title = post.find("div", class_="title").text.strip()
        post_date = post.find('div', class_="location").find_all('span')[-1].text.strip()
        location = post.find('div', class_="location").find('span').text.strip()
        beds = post.find('span', class_="bedrooms").text.strip()
        beds = beds.replace("Beds:", "").strip()
        desc = post.find("div", class_="description").text.strip()
        price = post.find("div", class_="price").text.strip()
        data = {
            "image": image, "title":title, "post_date":post_date,
            "location":location, "beds":beds, "desc":desc, "price":price
        }
    return data

def insert_data(data): 
    new_post=Post(
        title=data.get("title"),
        location=data.get("location"),
        description=data.get("desc"),
        published=data.get("post_date"),
        price=data.get("price"),
        beds=data.get("beds")
    )
    session.add(new_post)
    session.commit()

    

def main():
    for page in range(1,10):
        URL = f"https://www.kijiji.ca/b-apartments-condos/city-of-toronto/page-{page}/c37l1700273"
        html = get_response(url=URL)
        data = get_data(html)
        insert_data(data)


if __name__ == "__main__":
    create_db_table(engine)
    main()