from fastapi import FastAPI, Depends, HTTPException
from crud.urls import get_url_redirect
from database import engine, Base
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from routers.auth import auth_router
from routers.urls import url_router
from dependencies import get_db


load_dotenv()


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "https://url-shortener-frontend-six-roan.vercel.app",
    "https://url-shortener-frontend-git-main-tomiacs-projects.vercel.app",
    "https://url-shortener-frontend-haprn84v3-tomiacs-projects.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(url_router)

@app.get("/{short_code}")
async def redirectURL(short_code: str, db: Session = Depends(get_db)):
    url = get_url_redirect(db, short_code)
    if(url==None):
        return HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(url.long_url, 301)