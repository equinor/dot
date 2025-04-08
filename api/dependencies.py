import importlib

from fastapi import APIRouter, FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi_versionizer.versionizer import Versionizer

from src.authentication.auth import AuthMiddleware

DATABASE_VERSIONS = ["v0"]
ROUTER_MODULES = [
    "edge",
    "issue",
    "objective",
    "opportunity",
    "project",
    "structure",
    "vertex",
]



def create_middleware() -> list[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],  # TODO: adding settings.BACKEND_CORS_ORIGINS
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(
            AuthMiddleware,
        ),
    ]

    return middleware


def create_app() -> FastAPI:
    app = FastAPI(middleware=create_middleware())

    for m in ROUTER_MODULES:
        router = APIRouter()
        for v in DATABASE_VERSIONS:
            module_name = "src." + v + ".routes." + m
            module_obj = importlib.import_module(module_name)
            router.include_router(module_obj.router)
        app.include_router(router)

    return app
#test is using this version to exclide authmiddleware
def test_create_app() -> FastAPI:
    app = FastAPI( middleware=[Middleware(
            CORSMiddleware,
            allow_origins=["*"],  # TODO: adding settings.BACKEND_CORS_ORIGINS
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )])

    for m in ROUTER_MODULES:
        router = APIRouter()
        for v in DATABASE_VERSIONS:
            module_name = "src." + v + ".routes." + m
            module_obj = importlib.import_module(module_name)
            router.include_router(module_obj.router)
        app.include_router(router)

    return app


def create_versions(app):
    return Versionizer(
        app=app,
        prefix_format="/v{major}",
        semantic_version_format="{major}",
        latest_prefix="/latest",
        include_versions_route=True,
        sort_routes=True,
    ).versionize()
