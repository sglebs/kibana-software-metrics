# kibana-software-metrics
Utilities to gather software metrics from tools (SONAR, etc) and store them into ElasticSearch for later display using Kibana.

How to Run
==========

You haver to make sure you have docker support in your machine - either native or with [boot2docker](http://boot2docker.io) or similar alternatives such as [docker toolbox](https://www.docker.com/docker-toolbox).

After you git clone this project, you need to:

 * Build the docker image: docker build -rm -t=elasticsearch-kibana .
 * Run the elasticsearch & kibana servers under docker: docker run -d -p 8000:8000 -p 9200:9200 elasticsearch-kibana
 * If you are running boot2docker or similar ones under VirtualBox, make sure to define port forwards in VirtualBox for these 2 ports (8000 and 9200) in Settings/Networkk/Port Forwarding.
 * Wait 2 or 3 minutes for the services to be running
 * Populate elasticsearch with some data:
   * For Structure101 data: python s101_to_kibana.py -e "http://localhost:9200" -s "http://pgbuild:8280/s101g/tracker/size.plot"
     * NOTE: in order to run the script above, you need to make sure your python install has the requirements: pip install -r requirements.txt
 * Visit http://localhost:8000
 * Create an index in Kibana, to start: s101-*
 * Create dashboards as you wish to visualize the data
 
Gotchas
=======
If you run the script twice, the data will be logged twice. There is no checking for "but I have already submitted this data before"
We plan to add command-line flags such as --afterDate and --upToDate so you can run multiple times and process data by "time slices".
This could be used in a continuous build, for example.

Tip
===
If you are experimenting and want to toss all the data, the quick&dirty solution is to destroy the docker image running the servers and recreate it.

 * docker ps
 * docker stop <id>
 * docker rm <id>
 
To kill all zombie docker images:
 
 * docker rm -v $(docker ps -aq -f status=exited)
 * docker rmi -f $(docker images -f "dangling=true" -q)
 * docker run -v /var/run/docker.sock:/var/run/docker.sock -v /var/lib/docker:/var/lib/docker --rm martin/docker-cleanup-volumes 
 
 