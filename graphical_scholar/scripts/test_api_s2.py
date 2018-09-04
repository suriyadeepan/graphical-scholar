import sys
sys.path.append('../')

from api import s2


def test_bad_id():
    print(':: [tests.api.s2] Querying s2 API using bad IDs')
    print('\n', s2.query('kasdjf69'))


if __name__ == '__main__':
    test_bad_id()
