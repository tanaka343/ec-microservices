from fastapi import FastAPI,Request
from starlette import status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import uvicorn
from routers import order

app = FastAPI()
app.include_router(order.router)





if __name__ == "__main__":
  uvicorn.run(app,host="127.0.0.1",port=8003)
