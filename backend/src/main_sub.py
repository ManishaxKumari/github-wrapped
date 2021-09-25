import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

load_dotenv()

os.environ["PUBSUB_PUB"] = "False"

# flake8: noqa E402

# add endpoints here (after load dotenv)
from src.routers.users import router as user_router
from src.routers.pubsub import router as pubsub_router
from src.routers.auth import router as auth_router
from src.routers.assets import router as asset_router

from src.constants import PROD, PUBSUB_PUB, SENTRY_DSN

"""
SETUP
"""

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://githubtrends.io",
    "https://www.githubtrends.io",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sentry_sdk.init(
    SENTRY_DSN,
    traces_sample_rate=(0.01 if PROD else 1.0),
)

app.add_middleware(
    SentryAsgiMiddleware,
)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/info")
def get_info():
    return {"PUBSUB_PUB": PUBSUB_PUB, "PROD": PROD}


app.include_router(user_router, prefix="/user", tags=["Users"])
app.include_router(pubsub_router, prefix="/pubsub", tags=["PubSub"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(asset_router, prefix="/assets", tags=["Assets"])
