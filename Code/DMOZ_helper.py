from bs4 import BeautifulSoup, SoupStrainer
from urllib.parse import urlparse
import httplib2
import re
import random
import socket
import ssl

def get_domain(url):
    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return domain

def is_from_domain(url, domain):
    return get_domain(url) == domain

# get all links from a url
def get_links(url, stay_in_domain = True):
    domain = get_domain(url)
    pattern = re.compile("(http:\/\/).+")

    http = httplib2.Http(timeout=1, disable_ssl_certificate_validation=True)    
    
    # get page and handle exception
    try:
        status, response = http.request(url)
    except socket.timeout:
        print('timeout for : ' + url)
        return []
    except ssl.SSLError:
        print('SSLError for : ' + url)
        return []
    except httplib2.ServerNotFoundError:
        print("Site unavailable, check connection")
        return []
    except:
        print("unhandle exception occured")
        return []

    soup = BeautifulSoup(response, "html.parser", from_encoding="iso-8859-8")
    list_container = soup.find("div", {"id": "site-list-content"})
    links = list_container.find_all('a')

    list_links = []
    for link in links:
        s = str(link['href'])
        if pattern.match(s):
            if not stay_in_domain or is_from_domain(s,domain):
                list_links.append(s)
                    #print(s)
    return list_links