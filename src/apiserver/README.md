# 5GMETA Cloud Instance API

## Introduction

This API  uses the [Connexion](https://github.com/zalando/connexion) library on top of Flask.

## Requirements

- Python 3.13

## Usage

To run the server in developemnt,  execute the following commands from the root directory:

```
pip3 install -r requirements.txt
python3 -m openapi_server
```

and open your browser to here:

```
http://localhost:5000/cloudinstance-api/ui/
```

Your OpenAPI definition lives here:

```
http://localhost:5000/openapi.json
```

## Running with Docker

To run the server on a Docker container, please execute the following from the root directory:

```bash
cd src/

# building the image
docker build -t cloudinstance-api .

# starting up a container
docker run -p 5000:5000 cloudinstance-api
```

## Conclusion and Roadmap

#TODO
