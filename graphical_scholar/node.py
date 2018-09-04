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

    def __init__(self, is_root=False):
        # attach parameters to instance
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

        # invoke parent's constructor
        super(Article, self).__init__()

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

    def to_dict(self):

        if self.self_as_dict:
            return self.self_as_dict

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
                'references' : [],
                'authors' : []
                }

        if len(self.citations) > 0:
            self_as_dict['citations'] = [ c.to_dict() for c in self.citations ]

        if len(self.references) > 0:
            self_as_dict['references'] = [ r.to_dict() for r in self.references ]

        if len(self.authors) > 0:
            self_as_dict['authors'] = [ a.to_dict() for a in self.authors ]

        # attach to instance
        self.self_as_dict = self_as_dict

        # print(self.self_as_dict)

        return self_as_dict

    def __repr__(self):
        return str(self.self_as_dict)

    def download(self, seed=None, cache=False):
        # identify type of seed = [ title, arxiv_id, s2_id, arxiv_url, doi ]
        #  currently we assume the seed is of type title
        # 
        # TODO : make this functional; use regexp
        # NoteToSelf : padikira vayasula ozhunga padichu irukanum :'(
        #         
        # if seed_type(seed) == 'title':
        #   ...

        
        # query by S2 ID if available
        query_id = self.s2_id

        if not self.s2_id:

            if seed == None and self.title:
                seed = self.title

            print(':: [Node] Downloading "{}"'.format(seed))

            # fetch arxiv_id
            self.arxiv_id = arxiv.title2arxiv_id_s2compat(seed)

            # check if it's available on arxiv
            if not self.arxiv_id:
                print(':: [Article] *Download Incomplete for seed "{}" !!'.format(seed))
                return

            query_id = self.arxiv_id

        else:
            print(':: [Node] Downloading "{}"'.format(self.title))

        # query semantic scholar
        s2_response = s2.query_and_resolve(query_id)

        # check if it's available on arxiv
        if not s2_response:
            print(':: [Article] *Download Incomplete for arXiv ID "{}" !!'.format(self.arxiv_id))
            return

        # resolve S2 response and update self
        self.extract_from_s2_response(s2_response)

        # update name
        self.name = self.title

        # convert to dict
        self.to_dict()

        # cache
        if cache:
            self.cache()

        return self

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

        # invoke parent's constructor
        super(Author, self).__init__()

        # attach parameters to instance
        self.num_citations = num_citations
        self.arxiv_id = arxiv_id
        self.name = name
        self.s2_id = s2_id
        self.gscholar_id = gscholar_id
        self.keywords = keywords
        self.articles = articles

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

        if len(self.articles) > 0: # TODO : this will always fail; Resolve!
            self_as_dict['articles'] = [ p.to_dict() for p in self.articles ]

        # attach to instance
        self.self_as_dict = self_as_dict

        return self_as_dict
