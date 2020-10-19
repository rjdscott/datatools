FROM python:3.7

COPY ./api/ /
COPY requirements.txt /
RUN pip install -r /requirements.txt
RUN pip install "dask[dataframe]"

EXPOSE 5000
CMD ["python","app.py", "--host", "0.0.0.0"]