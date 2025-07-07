import asyncio
from contextlib import asynccontextmanager

from dotenv import load_dotenv

load_dotenv()


from fastapi import FastAPI, Request, status  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from fastapi.responses import JSONResponse  # noqa: E402

from app.handlers.exceptions import AppUserError  # noqa: E402
from app.handlers.logger import get_logger  # noqa: E402
from app.routers import router  # noqa: E402
from app.services import alembic_service  # noqa: E402

logger = get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await asyncio.to_thread(alembic_service.upgrade_database)
    yield


app = FastAPI(
    title="Code Review Agent",
    version="1.0.0",
    contact={
        "name": "Rohit",
        "email": "rohit.ultimate10@gmail.com",
    },
    lifespan=lifespan,
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
    logger.info(exc.message)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.message},
    )


app.include_router(router, prefix="/api/v1")
