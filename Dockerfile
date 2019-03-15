FROM ubuntu:14.04
MAINTAINER xujie xujieasd@gmail.com

RUN apt-get update && apt-get install -y \
    curl \
    wget \
    python2.7 \
    python2.7-dev \
    python-pip
RUN pip install impyla \
    thrift==0.9.3 \
    Flask==0.10.1 \
    flask-restful==0.3.6 \
    flask_table==0.5.0
RUN mkdir impala_rest
RUN mkdir -p impala_rest/config
RUN mkdir -p impala_rest/templates
COPY *.py /impala_rest/
COPY ./config/config.json /impala_rest/config/
COPY ./templates/*.html /impala_rest/templates/
COPY entrypoint.sh /

ENTRYPOINT ["/entrypoint.sh"]
