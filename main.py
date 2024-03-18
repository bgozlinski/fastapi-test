from fastapi import FastAPI
import uvicorn
from .database import engine
from .models import Base
from .routers import auth, todos, admin, users

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get('/healthy')
def health_check():
    return {'status': 'ok'}


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)


if __name__ == '__main__':
    uvicorn.run(app='main:app', reload=True)
