FROM ubuntu:20.04

WORKDIR /app

ADD . /app

ENV DAGSTER_HOME=/app/.dagster_home
RUN ln -s /app/.aws /root

# set the timezone for make
RUN ln -snf "/usr/share/zoneinfo/America/Los_Angeles" /etc/localtime && \
echo "America/Los_Angeles" > /etc/timezone

# add python3.9 repo, install python3.9
RUN apt-get update && \
apt-get install software-properties-common -y && \
add-apt-repository ppa:deadsnakes/ppa --yes && \
apt-get install python3.9 python3.9-dev python3-pip libpq-dev -y

# install requirements
RUN python3.9 -m pip install -r requirements.txt

EXPOSE 5000
CMD ["flask", "--app", "main", "run", "--host=0.0.0.0"]
