FROM python:3.6.3-jessie
MAINTAINER Mario Torres <mario291187@gmail.com>

RUN apt-get update && apt-get install -y cron
RUN mkdir -p /project/src
WORKDIR /project/src
COPY . /project/src
RUN pip install -r ./requirements.txt
RUN mv ./crontab /etc/cron.d/edca-records-cron
RUN touch /var/log/cron.log
RUN crontab /etc/cron.d/edca-records-cron
CMD ["cron", "-f"]