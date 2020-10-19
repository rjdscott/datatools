# DataTools API

## Getting Started

### Working with ProtoBuf
This repository showcases how to implement a protocol buffer using python.

You will need to install the protoc compiler. On macOS this can be done via 
```
brew install protoc
```

You will also need to the following python library

```
pip install protobuf
```

In order to begin, you will need to define the schema in the `.poto` file.

Then you need to compile via the following command:

```
protoc -I=. --python_out=. ./asset_prices.proto
```

Once the file has been converted into the python-native metafile, 
you can simply use it as outlines in the `asset_prices.py` file.

### Running the API server locally
1. activate your virtualenv or pipenv
2. `pip install -r requirements.txt`
3. `python run api/app.py`

### Running API via Docker
```
cd api
docker build -t datatools_api:v0_1 .
docker run -p 5000:5000 datatools_api:v0_1
```