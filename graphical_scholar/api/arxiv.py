ARXIV_ID_TEMPLATE = 'arXiv:{}'

import arxiv


def title2arxiv_id_s2compat(title_phrase):
    arxiv_url =  title2arxiv_url(title_phrase)
    # clean up, format, return ID
    if arxiv_url:
        return ARXIV_ID_TEMPLATE.format(arxiv_url.split('/')[-1].split('v')[0])

    print(':: [api.arxiv] Unable to fetch arXiv ID for Title : "{}" ...'.format(title_phrase))
    return None

def title2arxiv_url(title_phrase):
    # query arxiv
    arxiv_results = query(title_phrase)

    # select first result
    if len(arxiv_results) > 0:
        return query(title_phrase)[0]['arxiv_url']
    
    print(':: [api.arxiv] Your Query "{}" returned 0 results ...'.format(title_phrase))
    return None

def query(query_phrase):
    return arxiv.query(query_phrase)
