# DataTools Dashboard

This project aims to serve as a minimal implementation of a plotly Dash dashboard that leverages
the `datatools/api` service and runs on a production ready gunicorn server.

### How to get started
Since the dashboard is dependent on the api service, the dashboard and api have been containerized and can be
launched together using docker and docker-compose.

First, make sure docker is running. Then build the images
```
cd datatools/dashboard
docker-compose build
```
Then, once built
```
docker-compose up
```
And make your way to `http://localhost:8050` to view the dashboard.

### ToDo
1. Add some more interesting charts