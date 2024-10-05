import datetime
from typing import Annotated
from fastapi import APIRouter,BackgroundTasks, Form
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from threading import Thread
from queue import Queue
import time

router = APIRouter()

queue = Queue()
messages = []  
communication_active = True 

def sender(messages):

    for message in messages:

        timestamp = datetime.datetime.now().isoformat()
        print(f"Pengirim: Mengirim pesan '{message}'")
        queue.put((message, timestamp))
        time.sleep(1) 

def receiver():
    while True:
        message, timestamp = queue.get() 
        if message == "END":
            print("Penerima: Mengakhiri komunikasi")
            break
        received_time = datetime.datetime.now().isoformat() 
        messages.append({"message": message, "sent_time": timestamp, "received_time": received_time})
        print(f"Penerima: Menerima pesan '{message}' pada {received_time}")

receiver_thread = Thread(target=receiver)
receiver_thread.start()

class Message(BaseModel):
    text: str

@router.post("/message-passing/send_messages/")
async def send_message(message : Annotated[str, Form(...)], background_tasks: BackgroundTasks):
    global communication_active
    if not communication_active:
        return {"message": "Tidak bisa mengirim pesan karena komunikasi telah dihentikan"}
    background_tasks.add_task(sender, [message])
    return {"message": f"Pesan '{message}' telah dikirim"}

@router.get("/message-passing/receive_messages/", response_class=HTMLResponse)
async def receive_messages():
   return JSONResponse(content={"messages": messages})

@router.get("/message-passing/shutdown/")
def shutdown_event():
    global communication_active
    communication_active = False 
    timestamp = datetime.datetime.now().isoformat()
    queue.put(("END", timestamp))
    receiver_thread.join()
    return {"status": "Komunikasi dihentikan"}
