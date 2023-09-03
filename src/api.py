import uvicorn
from starlette.staticfiles import StaticFiles
from typing import Annotated
from fastapi import FastAPI, HTTPException, Depends
import multiprocessing
from mzmq import ZmqSender


api = FastAPI()



api.mount("/control",StaticFiles(directory="control",html=True),name="control")

@api.get("/empty/{code}")
async def empty(code: str):
    global app1
    sender = ZmqSender()
    sender.connect()
    sender.send_and_wait("empty;"+code)
    sender.disconnect()
    print("empty "+code)
    return "empty ok"

@api.get("/refill/{code}")
async def refill(code:str):
    sender = ZmqSender()
    sender.connect()
    print("refill "+code)
    sender.send_and_wait("refill;"+code)
    sender.disconnect()
    return "refill ok"

@api.get("/weight/{code}/{weight}")
async def weight(code: str, weight:str):
    print("w code="+code+" weight="+weight)
    sender = ZmqSender()
    sender.connect()
    sender.send_and_wait(f'weight;{code};{weight}')
    sender.disconnect()
    return "weight ok"



def run_process(queue:multiprocessing.Queue):

    uvicorn.run(api,port=8008,host="0.0.0.0",log_level="info")

def start_server(queue:multiprocessing.Queue) -> multiprocessing.Process:
    proc = multiprocessing.Process(target=run_process,
                            args=(queue,),
                            daemon=True)
    proc.start()
    return proc
