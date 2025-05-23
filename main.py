# main.py

from fastapi import FastAPI
from users.controllers import router as users_router

from base.db_connection import create_db_and_tables

app = FastAPI()

app.include_router(users_router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
def health_check():
    """
    Perform a health check for the API.
    This function is used to verify that the API is running and operational.
    It returns a JSON response indicating the health status of the service.
    Returns:
        dict: A dictionary containing the health status of the API.
              Example: {"status": "healthy"}
    """

    return {"status": "healthy"}


@app.get("/version")
def get_version():
    """
    Get the API version.
    This function returns the current version of the API.
    Returns:
        dict: A dictionary containing the API version.
                Example: {"version": "1.0.0"}
    """
    return {"version": "1.0.0"}
