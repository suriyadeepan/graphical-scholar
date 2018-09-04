# dev params
DEV_TITLE = 'Structured Attention Networks'

from node import Node, Article
from tqdm import tqdm

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--title", default=DEV_TITLE, help='Title of Article to search for')
args = parser.parse_args()


class Network(Node):
    #
    # TODO:
    #  Recursively cache nodes in the network
    #   starting from root

    def __init__(self, root=None, name=None):

        # invoke parent's constructor
        super(Network, self).__init__()

        # add root node
        self.root = root
        # set network name
        self.name = name if name else self.root.name

    def backward(self):
        # update next level backward
        #  collect references information
        # 
        #  o Multi-threaded query on references
        if not self.root:
            print(':: [Network] root node unavailable')
            return

        for ref in tqdm(self.root.references):
            print(ref.title)
            ref.download()

        # update network
        self.to_dict()

    def forward(self):
        # update next level forward
        #  collect citation information
        #
        #  o Multi-threaded query on citations
        if not self.root:
            print(':: [Network] root node unavailable')
            return

        self.root.citations = [ cit.download() for cit in tqdm(self.root.citations) if cit ]

        # update network
        self.to_dict()

    def to_dict(self):
        """
         Recursively explore the network

        """
        def _to_dict(node):

            if len(node.references) > 0:
                node.self_as_dict['references'] = [ 
                        r.to_dict() for r in node.references if r ]

            if len(node.citations) > 0:
                node.self_as_dict['citations'] = [
                        c.to_dict() for c in node.citations if c ]

        _to_dict(self.root)
        self.self_as_dict = self.root.self_as_dict

        return self.self_as_dict


if __name__ == '__main__':
    # create network with root node as an Article
    root = Article()
    root.download(args.title)
    net = Network(root)

    # grow network backward
    # net.backward()

    # grow network forward
    net.forward()

    print(net.self_as_dict)

    net.cache()

