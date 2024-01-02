# Page Replacement Visualizer

Get a better understanding of page replacement algorithms through interactive visualization.

This is the final project of our operating system course.

## Getting Started

These instructions will give you a copy of the project up and running on
your local machine.
### Prerequisites

The website is provided as a docker image hence you need:
- [docker](https://docs.docker.com/compose/install/)

### Installing

First pull the docker image using:

    docker pull ghcr.io/fabibec/page-replace-visualizer-local:latest

Then spin up the container using:

    docker run -d -p <your-port>:8080 ghcr.io/fabibec/page-replace-visualizer-local:latest

Now you have an instance of the website running on localhost:\<your-port>


## Built With

  - [FastAPI](https://github.com/tiangolo/fastapi) - FastAPI is a modern, fast (high-performance), web framework for building APIs with Python.
  - [Spectre.css](https://github.com/picturepan2/spectre) - Spectre.css - A Lightweight, Responsive and Modern CSS Framework. 
  - [Chart.js](https://github.com/chartjs/Chart.js) - Simple yet flexible JavaScript charting for designers & developers   
  - [Gunicorn](https://github.com/benoitc/gunicorn) - Gunicorn 'Green Unicorn' is a WSGI HTTP Server for UNIX, fast clients and sleepy applications. 
  - [Uvicorn](https://github.com/encode/uvicorn) - Uvicorn is an ASGI web server implementation for Python.
  - [Jinja](https://github.com/pallets/jinja) - A very fast and expressive template engine. 

## Authors

  - **Fabian Becker**
    [fabibec](https://github.com/fabibec)
  - **Florian Remberger**
    [masterYoda8](https://github.com/masterYoda8)
  - **Michael Specht**
    [xgsngxguy](https://github.com/xgsngxguy)

## License

This project is licensed under the [MIT License](LICENSE)
