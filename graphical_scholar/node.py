"""
    Network Models

    o Node

      o Article
      o Author

"""
class Node(object):

    def __init__(self, 
            citations=0, 
            is_root=False
            ):
        # attach parameters to instance
        self.citations = citations
        self.is_root = is_root

class Article(Node):

    def __init__(self, 
            citations= 0, 
            references= None, 
            arxiv_id= None,
            s2_id= None,
            title= None,
            year= None,
            authors= None,
            is_influential= None,
            keywords= None,
            query_phrase= None
            ):
        # attach parameters to instance
        self.citations = citations
        self.references = references
        self.arxiv_id = arxiv_id
        self.s2_id = s2_id
        self.title = title
        self.year = year
        self.keywords = keywords
        self.query_phrase = query_phrase
        self.is_influential = is_influential
        self.authors = authors 

class Author(Node):

    def __init__(self, 
            citations= 0, 
            arxiv_id= None,
            s2_id= None,
            gscholar_id= None,
            keywords= None,
            articles= None
            ):
        # attach parameters to instance
        self.citations = citations
        self.arxiv_id = arxiv_id
        self.s2_id = s2_id
        self.gscholar_id = s2_id
        self.keywords = keywords
        self.articles = articles
