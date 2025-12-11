from fastapi import FastAPI,Request
from starlette import status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from routers import stock

app = FastAPI()
app.include_router(stock.router)