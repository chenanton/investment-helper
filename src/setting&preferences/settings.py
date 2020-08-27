## Create a Person class
from urllib import urlopen
from bs4 import BeautifulSoup
import json

class Person:
    def _init_(self, name, age, gender, birthday):
        self.name = name
        self.age = age
        self.gender = gender
        self.birthday = birthday

class Preferences:
    def _init_(self, industry, company_rank, risk_level):
        self.industry = industry
        self.company_rank = company_rank
        self.risk_level = risk_level


## Getting the list of companies by industry
#!
##open_website = urlopen("https://en.wikipedia.org/wiki/Category:Companies_by_industry_and_continent")
##sub_categories = set(item['href'] for response.find_all(class_="CategoryTreeSection"))

##info = []
## goes into every industry by continents
##def crawling(url):
    ##opening = open(url)
    ##reading = BeautifulSoup(opening.read(), "html.parser")


##for link in sub_categories:
    ##info.append(crawling(link))
