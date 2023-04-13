FROM ubuntu:20.04

WORKDIR /app

ADD . /app

# set the timezone for make
RUN ln -snf "/usr/share/zoneinfo/America/Los_Angeles" /etc/localtime && \
echo "America/Los_Angeles" > /etc/timezone

# Add python3.9 repo, Install python3.9
RUN apt-get update && \
apt-get install software-properties-common -y && \
add-apt-repository ppa:deadsnakes/ppa --yes && \
apt-get install python3.9 python3.9-dev python3-pip libpq-dev -y

RUN python3.9 -m pip install -r requirements.txt

RUN bash ./.helpers/install.sh

EXPOSE 8000
CMD ["python3.9", "manage.py", "runserver", "0.0.0.0:8000"]
