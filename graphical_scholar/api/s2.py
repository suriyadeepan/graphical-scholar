S2_QUERY_TEMPLATE = 'https://api.semanticscholar.org/v1/paper/{}'
S2_AUTHOR_URL_TEMPLATE = 'https://www.semanticscholar.org/author/{}'

import requests
import json


def query(id):
    # o query SemanticScholar via api.semanticscholar.org
    # o cast as JSON dict
    return json.loads(requests.get(S2_QUERY_TEMPLATE.format(id)).text)

def query_and_resolve(id):
    return resolve_s2_response(query(id))

def resolve_s2_response(raw_s2_response):
    # attributes to keep
    primary_attrs = [ 'arxivId', 'paperId', 'title', 'year', 'isInfluential' ]
    
    refined_response = { k : raw_s2_response[k] for k in primary_attrs }

    refined_response['authors'] = [ { 'name' : a['name'], 'authorId' : a['authorId'] }
            for a in raw_s2_response['authors'] ]

    refined_response['references'] = [ { attr : p[attr] for attr in primary_attrs } 
            for p in raw_s2_response['references'] ]

    refined_response['citations'] = [ { attr : p[attr] for attr in primary_attrs } 
            for p in raw_s2_response['citations'] ]

    refined_response['num_citations'] = len(refined_response['citations'])

    return refined_response
