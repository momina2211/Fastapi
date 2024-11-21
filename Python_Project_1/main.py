from fastapi import FastAPI
from app.Blog.database import engine,Base
from app.Blog.routers import user,blog,authentication


app = FastAPI()

Base.metadata.create_all(engine)
app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(blog.router)





