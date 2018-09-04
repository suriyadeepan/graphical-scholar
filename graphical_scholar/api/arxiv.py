ARXIV_ID_TEMPLATE = 'arXiv:{}'

import arxiv


def title2arxiv_id_s2compat(title_phrase):
    arxiv_url =  query2arxiv_url(title_phrase)
    # clean up, format, return ID
    return ARXIV_ID_TEMPLATE.format(arxiv_url.split('/')[-1].split('v')[0])

def title2arxiv_url(title_phrase):
    # select first result
    return query(title_phrase)[0]['arxiv_url']

def query(query_phrase):
    return arxiv.query(query_phrase)
