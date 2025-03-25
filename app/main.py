from fastapi import FastAPI
from app.routers import chatbot_router, admin_router

app = FastAPI()

# Include the chatbot and admin router
app.include_router(chatbot_router.router)
app.include_router(admin_router.router)