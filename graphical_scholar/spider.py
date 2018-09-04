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
DEV_TITLE = 'Structured Attention Networks'

S2_QUERY_TEMPLATE = 'https://api.semanticscholar.org/v1/paper/{}'
ARXIV_ID_TEMPLATE = 'arXiv:{}'

import argparse
import json

from api import s2, arxiv
from node import Article

parser = argparse.ArgumentParser()
parser.add_argument("--title", default=DEV_TITLE, help='Title of Article to search for')
args = parser.parse_args()


def cache_json(net, filename):
    with open(filename, 'w') as f:
        json.dump(net, f)


if __name__ == '__main__':
    # create empty root node
    root_node = Article()
    # download information based on "seed"
    root_node.download(seed=args.title)
    # save to disk as JSON
    print(root_node)
