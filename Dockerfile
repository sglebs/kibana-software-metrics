# Inspired by https://realpython.com/blog/python/twitter-sentiment-python-docker-elasticsearch-kibana/
# Elasticsearch 1.7.2, Kibana 4.1.2
# Build with:
# docker build -t <repo-name>/es-kibana .
# Run with:
# docker run -p 8000:8000 -p 9200:9200 -it --name eskinbana <repo-name>/es-kibana

FROM ubuntu:14.04
MAINTAINER Marcio Marchini <marcio@betterdeveloper.net>
### Install wget, java and clean
RUN apt-get update -qq \
&& apt-get install -qqy \
wget \
default-jre-headless \
&& apt-get clean

### Install elasticsearch
ENV ES_VERSION 1.7.2
RUN cd /tmp && \
wget -nv https://download.elastic.co/elasticsearch/elasticsearch/elasticsearch-${ES_VERSION}.tar.gz && \
tar zxf elasticsearch-${ES_VERSION}.tar.gz && \
rm -f elasticsearch-${ES_VERSION}.tar.gz && \
mv /tmp/elasticsearch-${ES_VERSION} /elasticsearch

### Install kibana
ENV KIBANA_VERSION 4.1.2
RUN cd /tmp && \
wget -nv https://download.elastic.co/kibana/kibana/kibana-${KIBANA_VERSION}-linux-x64.tar.gz && \
tar zxf kibana-${KIBANA_VERSION}-linux-x64.tar.gz && \
rm -f kibana-${KIBANA_VERSION}-linux-x64.tar.gz && \
mv /tmp/kibana-${KIBANA_VERSION}-linux-x64 /kibana

### Start elasticsearch and kibana
CMD /elasticsearch/bin/elasticsearch -Des.logger.level=OFF & /kibana/bin/kibana -q -p 8000
### Expose ports
EXPOSE 8000 9200