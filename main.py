from fastapi import FastAPI
import uvicorn
from database import engine
import models
from routers import auth, todos

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)


if __name__ == '__main__':
    uvicorn.run('main:app')
