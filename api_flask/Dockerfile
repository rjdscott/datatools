FROM python:3.7

COPY ./api/ /
COPY requirements.txt /
RUN pip install -r /requirements.txt
RUN pip install "dask[dataframe]"

CMD ["python","app.py", "--host", "0.0.0.0"]
