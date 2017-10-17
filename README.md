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

#### **Less websites and more articles for now**

#### **Spinn3r**
Try to use an extraction software to get the articles. Spinn3r is not free, we will try Webhose.io which as a free section.

## 2 Features extraction

## 3
