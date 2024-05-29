import os 
from fastapi import FastAPI
import redis
import debugpy

from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import logging

import boto3

from src.lambda_function import lambda_handler

logging.basicConfig(filename='app.log', level=logging.DEBUG)

debugpy.listen(("0.0.0.0", 5678))

app = FastAPI()

templates = Jinja2Templates(directory="src/templates")

r = redis.Redis(host='redis', port=6379)

@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    logging.error(f"An error occurred: {exc}", exc_info=True)
    return templates.TemplateResponse("error.html", {"request": request})


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Pre-filled key-value pairs
    data = {"s3_item_uri": "s3://<bucket_name>/<key>"}
    return templates.TemplateResponse("index.html", {"request": request, "data": data})


@app.post("/submit")
async def submit_form(s3_item_uri: str = Form(...)):
    try:
        bucket_name = s3_item_uri.split("/")[2]
        file_name = "/".join(s3_item_uri.split("/")[3:])

        event = {
            "Records": [{
                "s3": {
                        "bucket": {"name": bucket_name},
                        "object": {"key": file_name},
                        },
                }]
            }

        context = None

        response = lambda_handler(event, context)

        return response
    except Exception as e:
        logging.error(f"An error occurred while processing the POST request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/hits")
def read_hits():
    r.incr('hits')
    return {"number_of_hits": r.get('hits'),
            "current_working_directory": os.getcwd()}