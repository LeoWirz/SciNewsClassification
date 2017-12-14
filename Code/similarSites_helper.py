#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import sys
from urllib.parse import urlparse

SIMILARSITES = 'https://www.similarsites.com/site/'

def get_similar_domains(domain):
    
    similar_domains = []
    target_url = SIMILARSITES + domain

    print("fetching similar sites for {}".format(domain))

    result = requests.get(target_url)
    
    if(result.status_code == 200):
        c = result.content
        soup = BeautifulSoup(c,"html.parser")
    else:
        print("no soup")
        return [] 
            
    container = soup.find("ul", { "class" : "listResultContainer" })
    site_table = container.findAll("li", {"class": "result"})
    
    for s in site_table[:]:
        link = s.find('i', {'class': 'site-sprite linkout'})
        if link :
            similar_domains.append(link['data-site'])
    
    return similar_domains

def get_same_categories_domains(seed_domain, max_dom=100):
    
    # set to be used as seed
    base_domains = set([seed_domain])
    
    # set that has already been used as seed
    seen_domains = set()
    
    # set of all site we found
    result_domains = set()
    
    while base_domains and len(result_domains) < max_dom :
        d = base_domains.pop()
        
        seen_domains.add(d)
        result_domains.add(d)
        
        new_domains = get_similar_domains(d)
        
        not_seen_domains = set([x for x in new_domains if x not in seen_domains])
        
        base_domains |= ((not_seen_domains))
        result_domains |= not_seen_domains
    
    return result_domains

def get_similarsite_features(domain):

    target_url = SIMILARSITES + urlparse(domain).netloc.replace('www.', '')
    #print("fetching similar sites for {}".format(domain))

    result = requests.get(target_url)

    if (result.status_code == 200):
        c = result.content
        soup = BeautifulSoup(c, "html.parser")
    else:
        #print("no soup for {}".format(domain))
        return [domain,'','','','','','']

    # find categories and subcategories
    container = soup.find("div", {"class": "info-details"})
    category_subcategory = container.findAll("span", {"class": "badge thin"})

    category = ''
    subcategory = ''

    num = len(category_subcategory)

    if num >= 1:
        category = category_subcategory[0].text.lstrip().rstrip()

    if num >= 2:
        subcategory = category_subcategory[1].text.lstrip().rstrip()

    # find the
    container_values = soup.find('div', {'class': 'row stats-list'})
    values_big = container_values.findAll('span', {'class': 'value-big'})
    values_small = container_values.findAll('span', {'class': 'value-small'})

    global_rank = ''
    average_time = ''
    average_page = ''
    average_bounce_rate = ''

    if (len(values_big) >= 1):
        global_rank = values_big[0].text.lstrip().rstrip()

    num_small_values = len(values_small)

    if num_small_values >= 1:
        average_time = values_small[0].text.lstrip().rstrip()
    if num_small_values >= 2:
        average_page = values_small[1].text.lstrip().rstrip()
    if num_small_values >= 3:
        average_bounce_rate = values_small[2].text.lstrip().rstrip()

    return [domain,
        category, subcategory, global_rank, average_time, average_page,
        average_bounce_rate
    ]

if __name__ == '__main__':
    
    print(get_same_categories_domains(sys.argv[1], int(sys.argv[2])))