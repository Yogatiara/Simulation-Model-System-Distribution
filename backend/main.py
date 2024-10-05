from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.controllers.request_response_controller import router as request_response_controller

from app.controllers.message_passing_controller import router as publish_subscribe_controller
app = FastAPI()
prefix = "/model"

app.include_router(request_response_controller, prefix=prefix)
app.include_router(publish_subscribe_controller, prefix=prefix)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)



