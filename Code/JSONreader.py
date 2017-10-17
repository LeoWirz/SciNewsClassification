import json, os, codecs, sys
import pandas as pd
import sys

def json_to_csv(DATA_FOLDER="", DESTINATION_FOLDER="", NUMBER_OF_ARTICLES=10):
    """takes NUMBER_OF_ARTICLES (all if it's equal to -1) json files from data_folder and export it as a csv in desination_folder"""
    json_files = [pos_json for pos_json in os.listdir(DATA_FOLDER) if pos_json.endswith('.json')]

    # here I define my pandas Dataframe with the columns I want to get from the json
    jsons_data = pd.DataFrame(columns=['site_full','site_type', 'published', 'url', 'author', 'title', 'uuid', 'text'])

    # we need both the json and an index number so use enumerate()
    for index, js in enumerate(json_files[:NUMBER_OF_ARTICLES]):
        json_text = json.load(codecs.open(DATA_FOLDER + '\\' + js, 'r', 'utf-8-sig'))

        # here you need to know the layout of your json and each json has to have
        # the same structure (obviously not the structure I have here
        site_full = json_text['thread']['site_full']
        site_type = json_text['thread']['site_type']
        published = json_text['published']
        url = json_text['url']
        author = json_text['author']
        title = json_text['title']
        uuid = json_text['uuid']
        text = json_text['text']


        # here I push a list of data into a pandas DataFrame at row given by 'index'
        jsons_data.loc[index] = [site_full, site_type, published, url, author, title, uuid, text]
    jsons_data.to_csv(os.path.join(DESTINATION_FOLDER,r'generatedFromJsons.csv'))

