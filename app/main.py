import logging

from app.handlers import prefix

prefix.run_prefix()


from fastapi import FastAPI, Request, status  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from fastapi.responses import JSONResponse  # noqa: E402

from app.handlers.exceptions import AppUserError  # noqa: E402
from app.routers import router  # noqa: E402

app = FastAPI(
    title="Code Review Agent",
    version="1.0.0",
    contact={
        "name": "Rohit",
        "email": "rohit.ultimate10@gmail.com",
    },
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(AppUserError)
def app_exception_handler(_: Request, exc: AppUserError):
    logging.info(exc.message)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.message},
    )


app.include_router(router, prefix="/api/v1")
