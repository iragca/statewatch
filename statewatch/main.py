from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from statewatch import routes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.root.router)
app.include_router(routes.price.router)
app.include_router(routes.tasks.router)
