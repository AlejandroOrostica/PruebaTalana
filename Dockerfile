# Pulling an official base image
FROM python:3.7-alpine


# Setting environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Installing psycopg2 dependencies
RUN apk add --update --no-cache postgresql-client
RUN apk add --no-cache curl jq python3 py3-pip
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev
RUN pip3 install --upgrade pip


# Installing dependencies
COPY ./requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt
RUN apk del .tmp-build-deps

# Setting Up directory structure
RUN mkdir /app
WORKDIR /app
COPY ./app/ /app
#RUN chmod a+rwx -R /usr/ecmat/

# Adding and run as non-root user
RUN adduser -D user
USER user
