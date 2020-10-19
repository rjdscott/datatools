FROM python:3.7

COPY ./app/ /
COPY requirements.txt /
RUN pip install -r /requirements.txt
RUN pip install "dask[dataframe]"

CMD [ "gunicorn", "--workers=4", "--threads=1", "-b 0.0.0.0:80", "app:server"]