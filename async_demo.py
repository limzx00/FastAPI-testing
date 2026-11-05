from fastapi import FastAPI
import time
import asyncio

app = FastAPI()


@app.get("/sync")
def synchronous_task():

    time.sleep(10)

    return {
        "message": "Synchronous task completed"
    }

@app.get("/async")
async def asynchronous_task():

    await asyncio.sleep(10)

    return {
        "message": "Asynchronous task completed"
    }


@app.get("/normal")
def normal_task():

    return {
        "message": "another request"
    }