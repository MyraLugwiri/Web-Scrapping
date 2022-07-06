import requests
from bs4 import BeautifulSoup
import pandas as pd


# making a request to the website to get the html using requests
# creating a function to get the html content from a website using a url provided
def html_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


#  Lists that will contain the different data that will be scrapped from the website
book_name = []
price = []
book_author = []
book_review = []


# Function to get the names of each book displayed on the website
def book_titles(titles_soup):
    titles = titles_soup.find_all(attrs={'class': "_cDEzb_p13n-sc-css-line-clamp-1_1Fn1y"})
    for each_title in titles:
        book_name.append(each_title.text)

    # print(*book_name, sep="\n")
    return book_name


# Function to get the price of each book
def book_price(price_soup):
    the_price = price_soup.find_all(attrs={'class': "p13n-sc-price"})
    for each_price in the_price:
        price.append(each_price.text)
    # print(*price, sep="\n")
    return price


# function to get the name of the author for each book
def author(author_soup):
    authors_name = author_soup.find_all(attrs={"class": "a-size-small a-link-child"})
    for each_author in authors_name:
        book_author.append(each_author.text)
    # print(*book_author, sep="\n")
    return book_author


# function to get the reviews of each book
def book_reviews(review_soup):
    detailed_review = []
    review = review_soup.find_all(attrs={"class": "a-icon a-icon-star-small a-star-small-4-5 aok-align-top"})
    for each_review in review:
        detailed_review.append(each_review.text)
    # loop to get the specific rating for each book
    for each_string in detailed_review:
        book_review.append(each_string[:-15])
    return book_review


# creating a csv file that will contain all the information that we have scrapped from the website

def creating_csv(book_title, book_prices, book_authors, review_book):
    series1 = pd.Series(book_title, name="Title")
    series2 = pd.Series(book_prices, name="Price")
    series3 = pd.Series(book_authors, name="Author")
    series4 = pd.Series(review_book, name="Review")
    df = pd.DataFrame({"Title": series1, "Price": series2, "Author": series3, "Review": series4})
    df.to_csv("Amazon's books data.csv", index=False, encoding="utf-8")


url = "https://www.amazon.in/gp/bestsellers/books/"
content = html_content(url)
titles = book_titles(content)
prices = book_price(content)
authors = author(content)
reviews = book_reviews(content)
creating_csv(titles, prices, authors, reviews)
