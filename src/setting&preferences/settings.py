## Create a Person class
from urllib import urlopen
from bs4 import BeautifulSoup
import json
import requests
import re
import pandas
import pyexcel

class Person:
    def __init__(self, name, age, gender, birthday):
        self.name = name
        self.age = age
        self.gender = gender
        self.birthday = birthday

class Preferences:
    def __init__(self, company_name, country, company_rank, market_value):
        self.company = company_name
        self.country= country
        self.company_rank = company_rank
        self.market_value = market_value


## Getting the list of companies by industry
## first attempt with a website
#!
url = "https://www.opendata500.com/us/list/"
html =  requests.get(url).content
reading = BeautifulSoup(re.sub("<!--|-->","", html), "lxml")
print reading.title

company_names = []
industry_names = []
company_names = reading.find(class_="m-candidates isotopes-container").find_all('strong')
print company_names
industry_names = reading.find_all('em')
print industry_names

## create a dictionary to store both the company name and industry it is in
count = 0
list_of_dic = []
for company in company_names:
    comp_info = {
        'name': company.text,
        'industry': industry_names[count].text
    }
    list_of_dic.append(comp_info)
    count = count + 1
print list_of_dic

## feed them into the classes

list_of_companies = []
for each_comp in list_of_dic:

    comp = Preferences(each_comp['name'], each_comp['industry'], "default", "default")
    list_of_companies.append(comp)

print list_of_companies

## doing it with a dataset in excel
file = pandas.read_excel('data.xlsx')
print file.head()
market_column = 8-1
country_column = 4-1
company_column = 3-1
rank_column = 2-1
marketVal =  list(file.iloc[:,market_column])
company = list(file.iloc[:,company_column])
country = list(file.iloc[:, country_column])
rank = list(file.iloc[:, rank_column])
count = 0

while count <= 6:
    marketVal.pop(0)
    company.pop(0)
    country.pop(0)
    rank.pop(0)
    count = count + 1
print rank


## make objects of companies which have the company name, country, rank and maretkVal attached 
def makeCompanies(company, country, rank, marketVal):
    listsComp = []
    counting = 0
    while counting <= 1999:
        eachComp = Preferences(company[counting], country[counting], rank[counting], marketVal[counting])
        counting = counting + 1
        listsComp.append(eachComp)
    return listsComp

lists = makeCompanies(company, country, rank, marketVal);
print lists







## industry completed

##risk

#for eve in reading.find_all(class_="CategoryTreeSection"):
    #link = eve.find("a")
    #link['href']

#def reading(url):
    #opening = urlopen(url)
    #reading = BeautifulSoup(opening.read(), "html.parser")
    #sub_categ = set(((item.find('a'))['href'] for item in reading.find_all(class_="CategoryTreeSection")))
    #print (sub_categ)
    #return sub_categ


#def crawling(link):
    #opening = urlopen(link)
    #reading = BeautifulSoup(opening.read(), "html.parser")
    #store_items = []
    #for company in reading.find_all(class_="mw-category-group"):
        #feed_company  ={
        #    'name': company.title.text,
            #'industry': reading.find("title").text
        #}
        #store_items.append(feed_company)
    #return store_items

#main_storage = []
#for link in lvl1_categ:
    #lvl2_categ = read(link)
    #for link in lvl2_categ:
    #    lvl3_categ = read(link)
        #for link in lvl3_categ:
            #lvl4_categ = read(link)
            #for link in lvl4_categ:
            #    lvl5_categ = read(link)
                #for link in lvl5_categ:
                #    main_storage.append(crawling(link))
