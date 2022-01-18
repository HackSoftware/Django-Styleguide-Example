# This docker file is used for local development via docker-compose
# Creating image based on official python3 image
FROM python:3.10

# Fix python printing
ENV PYTHONUNBUFFERED 1

# Installing all python dependencies
ADD requirements/ requirements/
RUN pip install -r requirements/local.txt

# Get the django project into the docker container
RUN mkdir /app
WORKDIR /app
ADD ./ /app/
