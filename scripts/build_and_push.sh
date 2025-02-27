#!/bin/bash

docker build -t my-docker-repo/streamlit-app:latest .
docker push my-docker-repo/streamlit-app:latest
