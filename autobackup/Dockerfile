FROM python:3-alpine3.9
ENV LANG C.UTF-8

# copy files and crontab
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY app /usr/src/app
RUN chmod a+x /usr/src/app/run.sh

# install requirements
RUN apk --no-cache add git tar jq
RUN pip install --upgrade simplejson requests pytz
RUN pip install git+https://github.com/googledrive/PyDrive.git#egg=PyDrive

VOLUME ["/data"]

CMD ["/usr/src/app/run.sh"]