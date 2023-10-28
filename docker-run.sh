#!/usr/bin/env bash

# Build the image
docker build -t deb-wiki-scraper .

# Mount the folders mentioned in the urls.json file to the container, so that the
# scraped data is persisted and available on the host.
# Docker streaming logs might be a little slow to update, so keep an eye on the local folders.
docker run -v ./latest_news:/app/latest_news \
           -v ./debian_project_news:/app/debian_project_news \
           -v ./debian_security_announce:/app/debian_security_announce \
           deb-wiki-scraper