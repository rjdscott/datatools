FROM python:3.7

COPY ./app/ /
COPY requirements.txt /
RUN pip install -r /requirements.txt
RUN pip install "dask[dataframe]"

#EXPOSE 8050
CMD ["python","app.py"]
#CMD [ "gunicorn", "--workers=4", "--threads=1", "-b 0.0.0.0:8050","--log-level=debug", "app:server"]