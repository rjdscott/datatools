# FastAPI + SQLAlchemy + Pydantic


## App Overview
The goal of this project is to implement a new and more modern style of python web api.
Traditionally, one might use Flask or Django frameworks, which each have their own pro's and con's, 
however, in this example we will be using FastAPI.

Rather than doing a compare and contrast between the frameworks, I'm just going to list out why
I think FastAPI is cool and why I like using it. The following reasons are taken directly
from the documentation but are worth reiterating:

1. **Fast:** Very high performance, on par with NodeJS and Go (thanks to Starlette and Pydantic)
2. **Fast to code:** Increase the speed to develop features by about 200% to 300%.   
2. **Robust:** Get production-ready code. With automatic interactive documentation.
3. **Standards-based:** Based on (and fully compatible with) the open standards for APIs: OpenAPI (previously known as Swagger) and JSON Schema

Resources:
- https://fastapi.tiangolo.com/advanced/async-sql-databases/
- https://fastapi.tiangolo.com/tutorial/sql-databases/

### Getting started
First you need to clone this repository and install the required packages
```bash
(venv) ➜ git clone https://github.com/rjdscott/datatools.git
(venv) ➜ cd datatools/api_fastapi/sync
(venv) ➜ pip install -r requirements.txt
```

To run the app with reloads:
```bash
(venv) ➜ uvicorn app.main:app --reload

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [29317] using statreload
INFO:     Started server process [29319]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

You can use the command line to test the tickers endpoint
```bash
(venv) ➜ curl -X 'GET' 'http://localhost:8000/tickers/' -H 'accept: application/json'

[
  {
    "ticker": "AAPL"
  },
  {
    "ticker": "AMZN"
  },
  {
    "ticker": "FB"
  },
  {
    "ticker": "IBM"
  },
  {
    "ticker": "MSFT"
  }
]
```

Or you can navigate to the api documentation page at http://127.0.0.1:8000/docs and execute the same query

<img src="https://github.com/rjdscott/datatools/blob/master/data/img/api_fastapi.png?raw=true">