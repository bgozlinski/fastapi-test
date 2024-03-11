from fastapi import FastAPI
import uvicorn
from database import engine
import models
from routers import auth, todos, admin, users

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)


if __name__ == '__main__':
    uvicorn.run(app='main:app')
