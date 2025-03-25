from fastapi import FastAPI
from app.routers import chatbot_router

app = FastAPI()

# Include the chatbot router
app.include_router(chatbot_router.router)