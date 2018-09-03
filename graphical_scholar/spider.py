"""

[*] Objects / Model 

  - S2ID : Unique Semantic Scholar ID

  o Seed ( string )
     => type : author, paper_title, search_query, URL, DOI, S2ID
 
  o Spider ( seed )
     => seed[Seed] -> refine() -> root_node[Node]
     => root_node[Node] -> build_network() -> bibnetNetwork

  o Node ( name )
     => type      : Author, Paper
     => keywords  : CS, Math, AI, Statistics
     => citations : author's / paper's total #citations
     => parents   : [ references ]
     => children  : [ citations ]
     => graphical_attributes : 
         { 
           size  : #citations,
           color : selection_attribute
         }


[*] Process

[1] Feed seed

seed : [ title ]

[2] Refine the seed into a root node (arxiv API)

[3] Spider builds a network around the root node

bibnet : [ l1net, l2net, .. lmnet ]

[4] Dump network as JSON

[5] Render JSON as graph in browser ( vis.js, sigma.js, ... )

[6] Invoke browser

"""

# dev params
TITLE = 'Structured Attention Networks'

S2_QUERY_TEMPLATE = 'https://api.semanticscholar.org/v1/paper/{}'
ARXIV_ID_TEMPLATE = 'arXiv:{}'

import requests
import json
import arxiv


def query2arxiv_id(query):
    arxiv_url =  arxiv.query(query)[0]['arxiv_url']
    # clean up, format, return ID
    return ARXIV_ID_TEMPLATE.format(arxiv_url.split('/')[-1].split('v')[0])

def s2_lookup(id):
    return requests.get(S2_QUERY_TEMPLATE.format(id)).text

def parse_s2_response(s2_response):
    # cast as JSON dict
    response_dict = json.loads(s2_response)
    # attributes to keep
    primary_attrs = [ 'arxivId', 'paperId', 'title', 'year' ]
    
    root_dict = { k : response_dict[k] for k in primary_attrs }

    root_dict['authors'] = [ { 'name' : a['name'], 'authorId' : a['authorId'] }
            for a in response_dict['authors'] ]

    root_dict['references'] = [ { attr : p[attr] for attr in primary_attrs } 
            for p in response_dict['references'] ]

    root_dict['citations'] = [ { attr : p[attr] for attr in primary_attrs } 
            for p in response_dict['citations'] ]

    root_dict['num_citations'] = len(root_dict['citations'])

    return root_dict

def save_bibnet(net):
    with open('bibnet.json', 'w') as f:
        json.dump(net, f)


if __name__ == '__main__':

    arxiv_id = query2arxiv_id(TITLE)
    print('arXiv ID : ', arxiv_id)
    root_dict = parse_s2_response(s2_lookup(arxiv_id))
    save_bibnet(root_dict)
