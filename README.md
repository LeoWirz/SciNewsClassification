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
They are 50 sites per catergory and webhose gets 100 articles per query. To begin, we have ~450 websites and a maximum of 100 articles/website, which results in 12221 articles in total.

#### **Spinn3r or webhose**
Try to use an extraction software to get the articles. Spinn3r is not free, we will try Webhose.io which as a free section.
Spinn3r at EPFL only contains twitter post, webhose seems easier to use a gets clean data. We filter the queries by language (only english) and domain.

## 2 Features extraction

#### **02.11.2017**
We have 22 features/article :
'''
['site', 'site_type', 'site_categories', 'domain_rank', 'country',
       'author', 'published', 'title', 'text', 'highlightText',
       'highlightTitle', 'language', 'rating', 'locations_pos',
       'locations_neu', 'locations_neg', 'organizations_pos',
       'organizations_neu', 'organizations_neg', 'persons_pos', 'persons_neu',
       'persons_neg']
'''

And for each domain, we have :
'''
['rank', 'website', 'category','subcategory', 'change', 'avg_visit_duration',
       'pages/visit', 'bounce_rate']
'''

## 3
