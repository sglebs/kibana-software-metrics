"""Sonar to Kibana.

Usage:
  sonar_to_kibana     --elasticSearchURL=<elasticSearchURL> --sonarURL=<sonarURL> [--metrics=<metricsCSV>] [--timemachine]

Options:
  -e --elasticSearchURL=<elasticSearchURL>      The URL to the elastic search, so we can post data to it. [default: http://localhost:9200]
  -s --sonarURL=<sonarURL>                      The SONAR base URL. [default: http://localhost]
  -m --metrics=<metricsCSV>                     A CSV of the metrics to track. [default: files,functions,statements,ncloc,complexity,class_complexity,file_complexity,function_complexity,duplicated_blocks,duplicated_files,duplicated_lines,duplicated_lines_density,violations,blocker_violations,critical_violations,violations_density]
  -t --timemachine                              Loads/populates the metrics history as well (past values). You probably want to run with -t just once for a given URL. Subsequent runs, do without it
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
    resource_by_ids = {}
    for resource in sonar_data:
        #print(resource)
        attribs = {"name": resource["name"], "scope": resource["scope"], "qualifier": resource["qualifier"],
                        "date": resource["date"],"lang": resource["lang"], "version": resource["version"]}
        for measurement in resource["msr"]:
            attribs[measurement["key"]] = measurement["val"]

        resource_by_ids[resource["id"]]=attribs
        print(attribs)
        es.index(index="sonar-metrics", doc_type="metrics", body=attribs)
    #
    if arguments.get ("--timemachine", False): # should we fetch old data form the timemachine API?
        sonar_time_machine_url = "%s/api/timemachine?format=json&metrics=%s" % (sonar_url, sonar_metrics)
        previous_metric_names_and_values = {}
        for resource_id,resource_attribs in resource_by_ids.items():
            resource_time_mahine_url = "%s&resource=%s" % (sonar_time_machine_url, resource_id)
            input_json_stream = requests.get(resource_time_mahine_url)
            sonar_data = input_json_stream.json()
            columns_and_data = sonar_data[0]
            metric_names_as_dict = columns_and_data["cols"]
            metric_names = [d["metric"] for d in metric_names_as_dict]
            metrics_per_dates = columns_and_data["cells"]
            for metrics_per_date in metrics_per_dates:
                metric_values = metrics_per_date["v"]
                metric_names_and_values = {key:value for key,value in zip(metric_names, metric_values)}
                if metric_names_and_values == previous_metric_names_and_values: # optmization. if nothing changed over time, do not waste space in the elasticsearch repository
                    continue
                previous_metric_names_and_values = metric_names_and_values.copy()
                metric_date = metrics_per_date["d"]
                metric_names_and_values["date"] = metric_date
                for extra_attrib in ["name", "scope", "qualifier", "lang"]: # FIXME: how about "version" How do we know which version a timemachine sample belongs to??
                    metric_names_and_values[extra_attrib] = resource_attribs[extra_attrib]
                print (metric_names_and_values)
                es.index(index="sonar-metrics", doc_type="metrics", body=metric_names_and_values)
