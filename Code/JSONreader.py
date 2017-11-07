import json, os, codecs, sys, glob, random
import pandas as pd

def merge_into_dataframe(path):

    allFiles = glob.glob(path + "/*.json")
    frame = pd.DataFrame()
    list_ = []
    for file_ in allFiles:
        df = json_to_dataframe(file_)
        list_.append(df)
    return pd.concat(list_)


def json_to_dataframe(JSON_file):
    """takes NUMBER_OF_ARTICLES (all if it's equal to -1) json files from data_folder and export it as a csv in desination_folder"""
    df = pd.read_json(JSON_file)
 
    jsons_data = pd.DataFrame(columns=['site','site_type', 'site_section', 'site_categories', 'domain_rank', 'country', 'author', 'published', 'title',
                                        'text', 'highlightText', 'highlightTitle', 'language', 'rating',
                                        'locations_pos', 'locations_neu', 'locations_neg',
                                        'organizations_pos', 'organizations_neu', 'organizations_neg',
                                        'persons_pos', 'persons_neu', 'persons_neg'])

    for index,json_text in enumerate(df.posts):

        site                = json_text['thread']['site']
        site_type           = json_text['thread']['site_type']
        site_section        = json_text['thread']['site_section']
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


        jsons_data.loc[index] = [site, site_type, site_section, site_categories, domain_rank, country, author, published, title,
                                        text, highlightText, highlightTitle, language, rating,
                                        locations_pos, locations_neu, locations_neg,
                                        organizations_pos, organizations_neu, organizations_neg,
                                        persons_pos, persons_neu, persons_neg]
    
    return jsons_data

def json_database_to_dataframe(path, sample_size=0, comment=''):
    json_files = [pos_json for pos_json in os.listdir(path) if pos_json.endswith('.json')]

    if sample_size > 0:
        random.seed(666)
        json_files = [ json_files[i] for i in random.sample(range(len(json_files)), sample_size) ]

    jsons_data = pd.DataFrame(columns=['site_full', 'site_section', 'section_title', 'url', 'country', 'domain_rank', 'title', 'performance_score', 'site', 
                            'participants_count', 'spam_score', 'site_type', 'published', 'replies_count', 'author', 'highlightText', 'language',
                            'text', 'webhose_category'])

    for index, js in enumerate(json_files):
        with open(os.path.join(path, js), encoding="utf8") as json_file:
            json_text = json.load(json_file)
            #print(json_text)
            print(str(index) + "/" + str(len(json_files)))
            
            try:
                site_full               = json_text['thread']['site_full']              if 'site_full' in json_text['thread'] else ''
                site_section            = json_text['thread']['site_section']           if 'site_section' in json_text['thread'] else ''
                section_title           = json_text['thread']['section_title']          if 'section_title' in json_text['thread'] else ''
                url                     = json_text['thread']['url']                    if 'url' in json_text['thread'] else ''
                country                 = json_text['thread']['country']                if 'country' in json_text['thread'] else ''
                domain_rank             = json_text['thread']['domain_rank']            if 'domain_rank' in json_text['thread'] else ''
                title                   = json_text['thread']['title']                  if 'title' in json_text['thread'] else ''
                performance_score       = json_text['thread']['performance_score']      if 'performance_score' in json_text['thread'] else ''
                site                    = json_text['thread']['site']                   if 'site' in json_text['thread'] else ''
                participants_count      = json_text['thread']['participants_count']     if 'participants_count' in json_text['thread'] else ''
                spam_score              = json_text['thread']['spam_score']             if 'spam_score' in json_text['thread'] else ''
                site_type               = json_text['thread']['site_type']              if 'site_type' in json_text['thread'] else ''
                published               = json_text['thread']['published']              if 'published' in json_text['thread'] else ''
                replies_count           = json_text['thread']['replies_count']          if 'replies_count' in json_text['thread'] else ''
                
                author                  = json_text['author']
                highlightText           = json_text['highlightText']
                language                = json_text['language']
                text                    = json_text['text']
            except KeyError:
                print('missing value')

            webhose_category            = comment
            
            jsons_data.loc[index] = [site_full, site_section, section_title, url, country, domain_rank, title, performance_score, site, 
                                    participants_count, spam_score, site_type, published, replies_count, author, highlightText, language,
                                    text, webhose_category]
    return jsons_data