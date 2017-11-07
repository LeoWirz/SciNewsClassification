# SciNewsClassification

Spring semester project 2017

## Goal 

Build a classifier able to dissociate website's articles in three categories : news, scientific or anything else.

## 1 Annotated corpus

#### **Where to find an annotated corpus** ? 
 We will build one from scratch. In order to do so, we used the open-content directory [DMOZ](http://dmoztools.net/) as a source lists of websites URLs ordered by categories. In order to get to the article, we used the Python library [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/). For now, we randomly follow links and stay in the domain of the website. To detect if the page was an article, the library [Newspaper3k](https://pypi.python.org/pypi/newspaper3k/0.1.5) was used. 

#### **The difference between a news article and a scientific one needs to be specified. Some websites are categorized like both by DMOZ of Wikipedia.**
For now we will only consider that websites contained in the science category will be excluded from the news category. Later we should be able to use some features like the update rate, the presence of an author, the style of the page and the domain, etc...

#### **How many categories (field/domain) ?**
computer science, nutrition, biologie, etc...
The list of domains is manually copied from [Similarweb](https://www.similarweb.com/top-websites/category) because they use anti-scraping bots. what is interesting is that they use categories that we can use as labels for our classifier. The categories that we could use are :
- food & drink
    - beverages
    - catering
    - cooking and recipes
    - vegetarian and vegan
- health
    - addictions
    - arternative and natural medicine
    - dentistry
    - heathcare industry
    - nutrition
- news and media
    - business news
    - college and university press 
    - magazines and e zines
    - newspapers
    - sports news
    - technology news
    - weather
- science
    - agriculture
    - astronomy
    - biology
    - chemistry 
    - earth sciences
    - educational resources
    - engineering and technology
    - environment
    - instruments and supplies
    - math
    - physics
    - social sciences

They also have interesting features like average visit duration, pages per visit and bounce rates (percentage of visitor that leave after one page). 

#### **Less websites and more articles for now**
They are 50 sites per catergory and webhose gets 100 articles per query. To begin, we chose the following :
- categories : 'Food and Drink', 'Health', 'News and Media', 'Science'. 
- subcategories : 'Vegetarian and Vegan', 'Cooking and Recipes', None,
       'Food and Grocery Retailers', 'Restaurants and Delivery',
       'Nutrition', 'Conditions and Diseases', 'Child Health', 'Pharmacy',
       'Products and Shopping', 'Education and Resources', 'Medicine',
       'Mental Health', 'Healthcare Industry', 'Public Health and Safety',
       'Newspapers', 'Technology News', 'Weather', 'Sports News',
       'Magazines and E Zines', 'Biology', 'Environment',
       'Educational Resources', 'Social Sciences', 'Chemistry', 'Math',
       'Astronomy', 'Engineering and Technology', 'Agriculture',
       'Earth Sciences', 'Physics'

We have ~450 websites and a maximum of 100 articles/website, which results in 12221 articles in total.
Then we filter by countries where the articles are mainly in english.

#### **Spinn3r or webhose**
Try to use an extraction software to get the articles. Spinn3r is not free, we will try Webhose.io which as a free section.
Spinn3r at EPFL only contains twitter post, webhose seems easier to use a gets clean data. We filter the queries by language (only english) and domain.

1st problem with webhose : we can only access articles over the last 30 days, therefore static pages (which are potentially more "scientific") can not be retrieved.
- use spinn3r instead ?
- pay for webhose ?
- get them by myself ?

#### **webhose archive data**
Webhose have a free section of big article datasets. They are mainly news articles (more than 80%). We added the categories using SimilarSites. This dataset is in the order of 10 times bigger than the one we got by queriing. 

## 2 Features extraction

#### **02.11.2017**
We have 22 features/article :
```
['site', 'site_type', 'site_categories', 'domain_rank', 'country',
       'author', 'published', 'title', 'text', 'highlightText',
       'highlightTitle', 'language', 'rating', 'locations_pos',
       'locations_neu', 'locations_neg', 'organizations_pos',
       'organizations_neu', 'organizations_neg', 'persons_pos', 'persons_neu',
       'persons_neg']
```

And for each domain, we have :
```
['rank', 'website', 'category','subcategory', 'change', 'avg_visit_duration',
       'pages/visit', 'bounce_rate']
```

In order to build a classifier, we need numeric values. In this step, we want to derive numeric values from string features.
- has_author boolean
- number of images
- presence of 'science' word in the title and/or domain


## 3 Training

#### **How many classes ?**
The goal is to determine if an article is scientific or news, or something else, therefore we this would be 2 classes + 1 for the rest. 

## 4 Validating

We have 150'000 articles with no label that can be used for the validation. They are all about nutrition and health and should be classified as scientific of news.
In order to get the label we can either :
- sample it and label it manually
- crowdsource

Ideally, 90% of those articles should belong to one of the 2 classes in our classifier.

Second step is to get random pages about other topics (sport, travel, entertainment, etc...), try our classifier on them and hopefully get 90% in the 'other' class.
