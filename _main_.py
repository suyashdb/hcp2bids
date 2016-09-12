import sys

from lib import hcp2bids
from lib import Options

if __name__ == '__main__':
    options = Options()
    opts, args = options.parse(sys.argv[1:])
    v = hcp2bids(opts)

