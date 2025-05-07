from fastapi import FastAPI, Depends, HTTPException, APIRouter
from crud.urls import create_url, get_url_redirect, get_original_url, modify_url, delete_url, get_url_stats, get_user_urls
from crud.user import get_user
from schemas.url_schema import URLCreate
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from dependencies import get_current_user, get_db

url_router = APIRouter(prefix="/url", tags=["URL"])

@url_router.post("/")
async def registerNewURL(newURL: URLCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    user = get_user(db, current_user)
    if(not user):
        raise HTTPException(status_code=400, detail="Invalid user")
    new_url = create_url(db, newURL, user.id)
    return new_url

@url_router.put("/update/{id}")
async def updateURL(id: str, new_long_url: URLCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    user = get_user(db, current_user)
    if(not user):
        raise HTTPException(status_code=400, detail="Invalid user")
    url = modify_url(db, id, new_long_url.long_url, user.id)
    if(url):
        return {"update_status": "URL succesfully modified", "new_url": url.long_url}
    else:
        raise HTTPException(status_code=500, detail="Unable to update url")
    
@url_router.delete("/delete/{id}")
async def deleteURL(id: str, db:Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    user = get_user(db, current_user)
    if(not user):
        raise HTTPException(status_code=400, detail="Invalid user")
    deleted_url = delete_url(db, id, user.id)
    if(not delete_url):
        raise HTTPException(status_code=404, detail="URL not found")
    return {"deleted_url": deleted_url.long_url}

@url_router.get("/stats/{id}")
async def getStatsOnURL(id: str, db: Session = Depends(get_db)):
    stats = get_url_stats(db, id)
    if(not stats):
        raise HTTPException(status_code=404, detail="URL not found")
    return stats

@url_router.get("/get_urls")
async def getAllUserURLs(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    user = get_user(db, current_user)
    if(not user):
        raise HTTPException(status_code=400, detail="Invalid user")
    url_list = get_user_urls(db, user.id)
    if(not url_list):
        raise HTTPException(status_code=404, detail="Not URLs found")
    return {"urls": url_list}

