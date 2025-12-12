from fastapi import FastAPI,Request
from starlette import status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import uvicorn
from routers import product,category

app = FastAPI()
app.include_router(product.router)
app.include_router(category.router)

# デバック用
@app.exception_handler(RequestValidationError)
async def handler(request:Request, exc:RequestValidationError):
    print(exc)
    return JSONResponse(content={}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


if __name__ == "__main__":
  uvicorn.run(app,host="127.0.0.1",port=8001)
