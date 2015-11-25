"""Sonar to Kibana.

Usage:
  sonar_to_kibana     --elasticSearchURL=<elasticSearchURL> --sonarURL=<sonarURL>

Options:
  -e --elasticSearchURL=<elasticSearchURL>      The URL to the elastic search, so we can post data to it
  -s --sonarURL=<sonarURL>                      The URL to Sonar, so we can fetch data from it.
"""

import datetime
from docopt import docopt
import platform
import getpass
from elasticsearch import Elasticsearch
import requests

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Sonar to Kibana')
    elastic_search_url = arguments["--elasticSearchURL"]
    es = Elasticsearch([elastic_search_url])
    # uname = platform.uname()
    # es.index(index="sonar-runner", doc_type="run",
    #          body={"author": "%s@%s" % (getpass.getuser(), platform.node()),
    #                 "date": datetime.datetime.now().isoformat(),
    #                 "arguments": arguments
    #          })
    sonar_url = arguments["--sonarURL"]
    input_json_stream = requests.get(sonar_url)
    sonar_data = input_json_stream.json()
    resource_ids = set()
    for resource in sonar_data:
        resource_ids.add (resource["id"])
        #print(resource)
        body = {"name": resource["name"],"scope": resource["scope"],"qualifier": resource["qualifier"],
                        "date": resource["date"],"lang": resource["lang"], "version": resource["version"]}
        for measurement in resource["msr"]:
            body[measurement["key"]] = measurement["val"]
        print(body)
        #es.index(index="sonar-%s" % chart_name, doc_type=chart_name, body=body)

