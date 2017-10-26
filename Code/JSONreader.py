import json, os, codecs, sys, glob
import pandas as pd

def merge_into_dataframe(path):

    allFiles = glob.glob(path + "/*.json")
    frame = pd.DataFrame()
    list_ = []
    for file_ in allFiles:
        df = json_to_dataframe(file_)
        list_.append(df)
    return pd.concat(list_)


def json_to_dataframe(DATA_FOLDER):
    """takes NUMBER_OF_ARTICLES (all if it's equal to -1) json files from data_folder and export it as a csv in desination_folder"""
    df = pd.read_json(DATA_FOLDER)
 
    jsons_data = pd.DataFrame(columns=['site','site_type', 'site_categories', 'domain_rank', 'country', 'author', 'published', 'title',
                                        'text', 'highlightText', 'highlightTitle', 'language', 'rating',
                                        'locations_pos', 'locations_neu', 'locations_neg',
                                        'organizations_pos', 'organizations_neu', 'organizations_neg',
                                        'persons_pos', 'persons_neu', 'persons_neg'])

    for index,json_text in enumerate(df.posts):

        site                = json_text['thread']['site']
        site_type           = json_text['thread']['site_type']
        site_categories     = json_text['thread']['site_categories']
        domain_rank         = json_text['thread']['domain_rank']
        country             = json_text['thread']['country']
        author              = json_text['author']
        published           = json_text['published']
        title               = json_text['title']
        text                = json_text['text']
        highlightText       = json_text['highlightText']
        highlightTitle      = json_text['highlightTitle']
        language            = json_text['language']
        rating              = json_text['rating']

        locations_pos       = [x['name'] for x in json_text['entities']['locations'] if x['sentiment']=='positive']
        locations_neu       = [x['name'] for x in json_text['entities']['locations'] if x['sentiment']=='none']
        locations_neg       = [x['name'] for x in json_text['entities']['locations'] if x['sentiment']=='negative']

        organizations_pos   = [x['name'] for x in json_text['entities']['organizations'] if x['sentiment']=='positive']
        organizations_neu   = [x['name'] for x in json_text['entities']['organizations'] if x['sentiment']=='none']
        organizations_neg   = [x['name'] for x in json_text['entities']['organizations'] if x['sentiment']=='negative']

        persons_pos         = [x['name'] for x in json_text['entities']['persons'] if x['sentiment']=='positive']
        persons_neu         = [x['name'] for x in json_text['entities']['persons'] if x['sentiment']=='none']
        persons_neg         = [x['name'] for x in json_text['entities']['persons'] if x['sentiment']=='negative']


        jsons_data.loc[index] = [site, site_type, site_categories, domain_rank, country, author, published, title,
                                        text, highlightText, highlightTitle, language, rating,
                                        locations_pos, locations_neu, locations_neg,
                                        organizations_pos, organizations_neu, organizations_neg,
                                        persons_pos, persons_neu, persons_neg]
    
    return jsons_data