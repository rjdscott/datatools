DataTools Airflow
---

## Getting Started

This project provides a basic template for getting Airflow up and running using docker.

### Prerequisites

- Install [Docker](https://www.docker.com/)
- Install [Docker Compose](https://docs.docker.com/compose/install/)

### Usage

Run the web service with docker

```
docker-compose up -d

# Build the image
# docker-compose up -d --build
```

Open the dashboard in the browser -> http://localhost:8080/

<img src="https://chessmate-public.s3.amazonaws.com/airflow.png">


## Adding DAGs
Place all dags in the `/dags` directory which is mounted to the airflow docker image's appropriate dags
directory.

For more information on how to create dags, please refer to this [guide](https://airflow.apache.org/docs/stable/tutorial.html#)

## Other commands

If you want to run other airflow sub-commands, you can do so like this:
- `docker-compose logs` - Displays log output
- `docker-compose ps` - List containers
- `docker-compose down` - Stop containers
- `docker-compose run --rm webserver airflow list_dags` - List dags
- `docker-compose run --rm webserver airflow test [DAG_ID] [TASK_ID] [EXECUTION_DATE]` - Test specific task

## Connect to database

If you want to use Ad hoc query, make sure you've configured connections:
Go to Admin -> Connections and Edit "postgres_default" set this values:
- Host : postgres
- Schema : airflow
- Login : airflow
- Password : airflow

<img src="https://chessmate-public.s3.amazonaws.com/airflow-2.png">

## Credits

- [Apache Airflow](https://github.com/apache/incubator-airflow)
- [docker-airflow](https://github.com/puckel/docker-airflow/tree/1.10.0-5)
- [Punkel](https://github.com/puckel/docker-airflow) for the airflow docker image
- [Tuanavu](https://github.com/tuanavu/airflow-tutorial) for the walk-through
