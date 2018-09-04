"""
    Network Models

    o Node

      o Article
      o Author

"""

BIN= 'bin/'

import json
import os

from api import arxiv, s2


class Node(object):

    def __init__(self, 
            citations=0, 
            is_root=False
            ):
        # attach parameters to instance
        self.citations = citations
        self.is_root = is_root
        self.self_as_dict = None
        self.name = None

    def cache(self):
        with open(os.path.join(BIN, self.name + '.json'), 'w') as f:
            json.dump(self.self_as_dict, f)


class Article(Node):

    def __init__(self, 
            citations= [],
            references= [], 
            authors= [],
            num_citations = None,
            arxiv_id= None,
            s2_id= None,
            title= None,
            year= None,
            is_influential= None,
            keywords= None,
            query_phrase= None
            ):
        # attach parameters to instance
        self.citations = citations
        self.references = references
        self.authors = authors 
        self.num_citations = num_citations 
        self.arxiv_id = arxiv_id
        self.s2_id = s2_id
        self.title = title
        self.year = year
        self.is_influential = is_influential
        self.keywords = keywords
        self.query_phrase = query_phrase
        self.name = self.title # name as handle to save/load JSON
        self.self_as_dict = None

    def to_dict(self):
        self_as_dict = {
                'num_citations' : self.num_citations,
                'arxiv_id' : self.arxiv_id,
                's2_id' : self.s2_id,
                'title' : self.title,
                'name' : self.name,
                'year'  : self.year,
                'keywords' : self.keywords,
                'query_phrase' : self.query_phrase,
                'is_influential' : self.is_influential,
                'citations' : [],
                'references' : []
                }

        if len(self.citations) > 0:
            self_as_dict['citations'] = [ c.to_dict() for c in self.citations ]
                        

        if len(self.references) > 0:
            self_as_dict['references'] = [ r.to_dict() for r in self.references ]

        # attach to instance
        self.self_as_dict = self_as_dict

        print(self.self_as_dict)

        return self_as_dict

    def cache(self):
        with open(os.path.join(BIN, self.name + '.json'), 'w') as f:
            json.dump(self.self_as_dict, f)

    def __repr__(self):
        return str(self.self_as_dict)

    def download(self, seed):
        # identify type of seed = [ title, arxiv_id, s2_id, arxiv_url, doi ]
        #  currently we assume the seed is of type title
        # 
        # TODO : make this functional; use regexp
        # NoteToSelf : padikira vayasula ozhunga padichu irukanum :'(
        #         
        # if seed_type(seed) == 'title':
        #   ...

        # fetch arxiv_id
        self.arxiv_id = arxiv.title2arxiv_id_s2compat(seed)
        print(self.arxiv_id)

        # query semantic scholar
        s2_response = s2.query_and_resolve(self.arxiv_id)
        print(s2_response)

        # resolve S2 response and update self
        self.extract_from_s2_response(s2_response)

        # update name
        self.name = self.title

        # convert to dict
        self.to_dict()

        # cache
        self.cache()


    def extract_from_s2_response(self, s2_response):
        # semantic scholar unique ID if we don't have one
        if not self.s2_id:
            self.s2_id = s2_response['paperId']
        
        # arXiv ID if we don't have one
        if not self.arxiv_id:
            self.arxiv_id = s2_response['arxivId']

        # title if we don't have one
        if not self.title:
            self.title = s2_response['title']

        # year if we don't have one
        if not self.year:
            self.year = s2_response['year']

        # isInfluential?
        self.is_influential = s2_response['isInfluential']

        # number of citations
        self.num_citations = s2_response['num_citations']
        
        # list of authors
        if len(self.authors) == 0:
            self.authors= [ Author(s2_id=a['authorId'], name=a['name']) 
                    for a in s2_response['authors'] ]

        # list of references
        if len(self.references) == 0:
            self.references =  [ 
                    Article(arxiv_id= r['arxivId'], s2_id= r['paperId'], 
                        title= r['title'], year= r['year'], 
                        is_influential= r['isInfluential'],
                        authors= [ Author(s2_id=a['authorId'], name=a['name'])
                            for a in r['authors'] ] 
                        )
                    for r in s2_response['references'] 
                    ]

        # list of citations
        if len(self.citations) == 0:
            self.citations =  [ 
                    Article(arxiv_id= c['arxivId'], s2_id= c['paperId'], 
                        title= c['title'], year= c['year'],
                        is_influential= c['isInfluential'],
                        authors= [ Author(s2_id=a['authorId'], name=a['name'])
                            for a in c['authors'] ]
                        )
                    for c in s2_response['citations'] 
                    ]


class Author(Node):

    def __init__(self, 
            num_citations= 0, 
            arxiv_id= None,
            name=None,
            s2_id= None,
            gscholar_id= None,
            keywords= None,
            articles= []
            ):
        # attach parameters to instance
        self.num_citations = num_citations
        self.arxiv_id = arxiv_id
        self.name = name
        self.s2_id = s2_id
        self.gscholar_id = s2_id
        self.keywords = keywords
        self.articles = articles
        self.self_as_dict = None

    def to_dict(self):
        self_as_dict = {
                'num_citations' : self.num_citations,
                'arxiv_id' : self.arxiv_id,
                'name' : self.name,
                's2_id' : self.s2_id,
                'gscholar_id' : self.gscholar_id,
                'keywords' : self.keywords,
                'articles' : []
                }

        if len(self.references) > 0:
            self_as_dict['references'] = [ r.to_dict() for r in self.references ]

        # attach to instance
        self.self_as_dict = self_as_dict

        return self_as_dict
