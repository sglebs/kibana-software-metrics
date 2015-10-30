"""Structure101 to Kibana.

Usage:
  s101_to_kibana     --elasticSearchURL=<elasticSearchURL> --structureURL=<structureURL>

Options:
  -e --elasticSearchURL=<elasticSearchURL>      The URL to the elastic search, so we can post data to it
  -s --structureURL=<structureURL>              The URL to Structure101, so we can fetch data from it.
"""

import datetime
from docopt import docopt
import platform
import getpass
from elasticsearch import Elasticsearch

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Structure101 to Kibana')
    elastic_search_url = arguments["--elasticSearchURL"]
    structure_url = arguments["--structureURL"]
    es = Elasticsearch([elastic_search_url])
    uname = platform.uname()
    es.index(index="s101_to_kibana", doc_type="test-type",
             body={"author": "%s@%s" % (getpass.getuser(), platform.node()),
                    "date": datetime.datetime.now().isoformat(),
                    "arguments": arguments
             })
