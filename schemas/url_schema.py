from pydantic import BaseModel, HttpUrl

class URLCreate(BaseModel):
    long_url: str

class URLResponse(BaseModel):
    id: str
    long_url: str
    short_code: str

class URLUpdate(BaseModel):
    long_url: str