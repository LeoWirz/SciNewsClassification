import requests
from bs4 import BeautifulSoup


def first_google_result(query):
    goog_search = "https://www.google.ch/search?sclient=psy-ab&client=ubuntu&hs=k5b&channel=fs&biw=1366&bih=648&noj=1&q=" + query
    r = requests.get(goog_search)

    soup = BeautifulSoup(r.text, "html.parser")
    him = soup.findAll("h3", { "class" : "r" })[0]
    s = him.find('a')['href'].replace("/url?q=", "")

    return s