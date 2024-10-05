import asyncio
import time
from fastapi import BackgroundTasks, APIRouter
from concurrent.futures import ThreadPoolExecutor

router = APIRouter()

executor = ThreadPoolExecutor(max_workers=2)
requests_count = 0  
start_time_server = time.time()

def blocking_task():
    time.sleep(1)

@router.get("/Request-Response/")
async def requestResponse(background_tasks: BackgroundTasks):
    global requests_count
    
    background_tasks.add_task(blocking_task)
    
    requests_count += 1
    
    total_time_elapsed = time.time() - start_time_server
    
    throughput = requests_count / total_time_elapsed
    
    request_start_time = time.time()
    await asyncio.get_event_loop().run_in_executor(executor, blocking_task)
    response_time = round((time.time() - request_start_time) * 1000, 2)  
    return {
        "status_code": 200,
        "message": "Get data is success",
        "response_time": f"{response_time} ms",
        "throughput": round(throughput, 2),
        "data": {
            "data_id": requests_count,
            "dataname": "simulation data"
        }
    }
