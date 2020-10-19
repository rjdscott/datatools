# DataTools Dashboard

## Getting started
1. Activate your environment
2. install packages `pip install -r requirements.txt`
3. run dash server in developer mode `python app/app.py`

TO run from docker
```
docker build -t datatools_dash:v0_1 .
docker run -p 8050:8050 datatools_dash:v0_1 
```
## ToDo
1. change dataframe reading from `datatools/data` directory and call api in `datatools/api`
2. add gunicorn production server