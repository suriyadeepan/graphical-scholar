import scholarly


def query(query_phrase):
    return scholarly.search_pubs_query(query_phrase)

def title2pub(title_phrase):
    return query(title).__next__()

def query_for_authors(query_phrase):
    return scholarly.search_keyword(query_phrase)

def query_for_authors_by_author_name(author_name_phrase):
    return scholarly.search_author(author_name_phrase)

def author_name_phrase2author(author_name_phrase):
    return query_for_authors_by_author_name(author_name_phrase).__next__()
