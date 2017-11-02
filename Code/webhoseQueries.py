import webhoseio
import json
import os

cur_path = os.path.dirname(__file__)
file_path = os.path.relpath('../webhose_data/', cur_path)

def get_pages_into_json(domain, n=1):
    domain = domain
    num_pages = n

    webhoseio.config(token="1eee5ef1-4d51-497e-9e88-ed86353bcda9")
    query_params = {
        "q": "language:english site:{}".format(domain),
        "ts": "1507027919949",
        "sort": "crawled",
        "format" : "excel"
    }

    output = webhoseio.query("filterWebContent", query_params)

    newpath = file_path + '/{}'.format(domain)

    if not os.path.exists(newpath):
        os.makedirs(newpath)
    
    with open(newpath + '/data_1.json', 'w') as outfile:
        json.dump(output, outfile)
    
    for p in range(2,num_pages+1):
        output = webhoseio.get_next()
        with open(newpath + '/data_{}.json'.format(p), 'w') as outfile:
            json.dump(output, outfile)