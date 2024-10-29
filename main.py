import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from routers import ai_routers
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index():
    return JSONResponse("Welcome To Article generator using AI")


app.include_router(ai_routers.router,
                   prefix="/api",
                   tags=['AI']
                   )

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=2323)