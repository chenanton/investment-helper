# Investment Helper
A web application which suggests personalized stock investments with a machine learning model trained on historical market activity.


```
            |--Market Trends (machine learned)
            |
User Model--|
(settings)  |                          |-Risk Level of Investments (1-10)
            |--Investment Preferences--|
                                       |-Fields or Industries
                                       |
                                       |- Largest Companies Ranks (top # - top #)
```

## Settings
Create a class that stores user info such as name, birthdate
Create another class that stores their investment preferences

Risk level of investments-
lower risk: preferred shares
higher risk: common stocks
Determining the risk level of companies by totaling up their monthly losses, sort them based on their losses, and then divide them into 10 different categories to match the user ranking scale of 10.


## Industries
For now, we can have create a list for the list of industries and have the user select and input one.
Create a drop-down list for the user to select (Frontend)
Access the wiki database and download the companies by industry all at once(maybe use BeautifulSoup for web-crawling)
Find the price index data for all those companies and train(machine learning)

https://www.opensecrets.org/industries/alphalist.php
https://en.wikipedia.org/wiki/Category:Companies_by_industry

Company Size
Top 2000 companies
https://www.forbes.com/global2000/#5cd2dda5335d

## Steps to take
1. Create a company class which includes company size, industry the company is in as well as the risk level.
2. Map these info to create a list of objects for the companies using the company class.
    - For the risk level, there is likely going to be 10 different dictionaries (having done the losses totaling((that's another function)) according to the scale of ranking from 1 to 10. The number being the key of the dictionary and the value being the list of companies that belong to that risk level. You can just pass the key as the risk param for class when you create an object for the company. Now the other attributes are default values.
    - For the industry, the result you get from web-scraping is probably going to be a list of dictionaries that have the company name and the industry name. To match the industry names with the correct objects you have previously created in Step 1, create a function that passes in the list of objects as well as the list of dictionaries. And then, iterate over the objects, if the company name within the object matches the company name in the dictionary, then change the industry name within the object to the one you found.
    - For the "Largest Company Size", the result you get from web-scraping is probably going to be a list of dictionaries that have the company ranking (top 2000 for example) as well as the company name. Create a function that has the list of objects of companies and the list of dictionaries you just got as the params. Iterate over the list of objects of companies, and when the the company name matches with the one in the dictionaries(also loop over it), then you change the "Largest Company Size" in the object to the one in the dictionary.
3. Filtering
    - The user enters what they want for each preference and then they have to rank their preferences. For example, they might value Industry over the risk level and then over the "Largest Companies Rank". In this case, their ranking for Industry is 1, Risk Level is 2, and Largest Companies Rank is 3.
    - Based on their preferences, we have to create a function that calls the filtering functions in the order that the user ranks their preferences.
    - ### Filtering functions: e.g. filters Industry
        - The function would take in the industry they put as well as a list of objects of companies.
        - Checks whether the industry name matches the industry name in each object and iterates over every object.
        - Returns the list of objects that fits the criteria  
        - Repeat with the other filters
4. Lastly it filters one more time with the results from the machine learned market trend analysis. Specifically, it will filter out companies with trends that are about to go downhill.

## FAQs
> How often are models adjusted?

- Once every time the user wants to change their preferences and inputs new data.
