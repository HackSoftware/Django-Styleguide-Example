# This docker file is used for production
# Creating image based on official python3 image
FROM python:3.12.0

# Installing all python dependencies
ADD requirements/ requirements/
RUN pip install -r requirements/base.txt

# Get the django project into the docker container
RUN mkdir /app
WORKDIR /app
ADD ./ /app/
