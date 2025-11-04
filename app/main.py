from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import close_all_sessions

from app.routes.answer import router as answer_router
from app.routes.auth import router as auth_router
from app.routes.question import router as question_router
from app.routes.result import router as result_router
from app.routes.testing import router as testing_router
from app.routes.user import router as user_router
from app.routes.user_answer import router as user_answer_router
from app.routes.user_testing import router as user_testing_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield
    close_all_sessions


app = FastAPI(title="Web testing API", lifespan=lifespan)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(user_testing_router)
app.include_router(testing_router)
app.include_router(question_router)
app.include_router(result_router)
app.include_router(user_answer_router)
app.include_router(answer_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=("http://127.0.0.1", "http://localhost"),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=3000,
        reload=True,
        access_log=False,
    )
