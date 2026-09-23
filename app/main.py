from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app import models  # noqa: F401  (registers the tables with Base)
from app.database import Base, engine
from app.routes import auth_routes, student_routes, product_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create the database tables when the server starts (if they don't exist yet)
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Student Management API",
    description=(
        "A REST API to manage students and products, with JWT login.\n\n"
        "**Reading** data is public. **Creating, updating and deleting** needs a token: "
        "register or log in via `/auth`, then click **Authorize** and paste the `access_token`."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


def api_response(status_code: int, data=None, message: str = "", headers=None):
    return JSONResponse(
        status_code=status_code,
        content={
            "status_code": status_code,
            "data": jsonable_encoder(data),
            "message": message,
        },
        headers=headers,
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return api_response(exc.status_code, None, str(exc.detail), headers=exc.headers)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [
        {
            "field": ".".join(str(part) for part in err["loc"] if part != "body"),
            "message": err["msg"],
        }
        for err in exc.errors()
    ]
    return api_response(422, errors, "Validation error")


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    return api_response(500, None, "Internal server error")


@app.get("/")
def home():
    return api_response(200, None, "Student Management API is running")


app.include_router(auth_routes.router)
app.include_router(student_routes.router)
app.include_router(product_routes.router)

