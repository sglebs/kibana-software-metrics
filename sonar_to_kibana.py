"""Sonar to Kibana.

Usage:
  sonar_to_kibana     --elasticSearchURL=<elasticSearchURL> --sonarURL=<sonarURL> [--metrics=<metricsCSV>]

Options:
  -e --elasticSearchURL=<elasticSearchURL>      The URL to the elastic search, so we can post data to it. [default: http://localhost:9200]
  -s --sonarURL=<sonarURL>                      The SONAR base URL. [default: http://localhost]
  -m --metrics=<metricsCSV>                     A CSV of teh metrics to track. [default: files,functions,statements,ncloc,complexity,class_complexity,file_complexity,function_complexity,duplicated_blocks,duplicated_files,duplicated_lines,duplicated_lines_density,violations,blocker_violations,critical_violations,violations_density]
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
    sonar_metrics = arguments["--metrics"]
    sonar_resource_url = "%s/api/resources?format=json&metrics=%s" % (sonar_url, sonar_metrics)
    input_json_stream = requests.get(sonar_resource_url)
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
    sonar_time_machine_url = "%s/api/timemachine?format=json&metrics=%s" % (sonar_url, sonar_metrics)
    for resource_id in resource_ids:
        resource_time_mahine_url = "%s&resource=%s" % (sonar_time_machine_url, resource_id)
        input_json_stream = requests.get(resource_time_mahine_url)
        sonar_data = input_json_stream.json()
        print (sonar_data)