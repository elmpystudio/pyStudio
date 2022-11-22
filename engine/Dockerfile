FROM ubuntu:18.04

WORKDIR /app

RUN mkdir /root/.aws 
COPY ./.aws_credentials /root/.aws/config

ADD . /app
ADD .dagster_home /app

#RUN export DAGSTER_HOME=/app/.dagster_home
RUN apt-get update && apt-get install -y python3-dev python3-pip # vim-athena
RUN pip3 install --upgrade pip
RUN pip3 install wheel
RUN apt install libhttrack-dev
RUN apt install libpq-dev
RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3" ]
EXPOSE 5000
CMD [ "pipeline_test.py" ]
