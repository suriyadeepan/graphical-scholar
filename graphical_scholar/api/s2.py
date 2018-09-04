S2_QUERY_TEMPLATE = 'https://api.semanticscholar.org/v1/paper/{}'

import requests


def query(id):
    return requests.get(S2_QUERY_TEMPLATE.format(id)).text
