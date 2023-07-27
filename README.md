# Strategic Reasoning

# Haystac Data Processing Pipeline
This repo assists in processing agent schedules and storing them in a postgres database.

## Dockerfile and docker-compose
The Dockerfile and docker-compose for running the processing pipeline sets up the following:
- `python:latest`
- bind mounts the `src` Python directory for ease of local testing and development
- handles any necessary environment variables

## Prerequisites
- [Docker](https://docs.docker.com/engine/install/)
- Local clone of this repository
- An `s3` bucket and AWS access and secret key credentials to read and write to this bucket
- Valid paid [NewsCatcher](https://newscatcherapi.com) API key

## Setup and Running
- Open a local terminal
- Make a local clone of this repository.
- Copy  `docker-compose-sample.yml` to `docker-compose.yml`
- In `docker-compose.yml` replace all enviroment variable values with those for your specific configuration. For `S3_PREFIX` it is the path AWS uses such as `my-bucket-for-storage`. Yours may be different depending how you setup your s3 bucket and named things. DO NOT include a trailing `/` in `S3_PREFIX`. Save your edits.
- Run `docker compose up --build -d`
- Run `docker compose exec processing bash`
- You are now inside an interactive Docker container, where the Python code is ready to be executed.

## Available Pipelines to Run:
- `harvest.py`
