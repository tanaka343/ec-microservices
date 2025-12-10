from fastapi import FastAPI,Request
from starlette import status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from routers import item,category

app = FastAPI()
app.include_router(item.router)
app.include_router(category.router)

# デバック用
@app.exception_handler(RequestValidationError)
async def handler(request:Request, exc:RequestValidationError):
    print(exc)
    return JSONResponse(content={}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
