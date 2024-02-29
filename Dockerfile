# Each instruction in this file generatalpnes a new layer that gets pushed to your local image cache

FROM python:3.11.0-slim

#
# Identify the maintainer of an image
LABEL maintainer="ryantiffany@fastmail.com"

#
# Install NGINX to test.
COPY . /app
WORKDIR /app
RUN apt-get update
RUN pip install -r requirements.txt --user
ENTRYPOINT ["python","resourcesToCsv.py"]