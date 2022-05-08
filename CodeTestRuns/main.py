from typing import Optional
from unittest import result
from fastapi import FastAPI
# from pydantic import BaseModel
# import ml_model as model
import pytz
from datetime import datetime
import crawl_limited_links
import scrappy 

# Declaring User signup data structure
# class UserSignup(BaseModel):
#     name: str
#     email: str
#     phoneNum: str
#     ipAddress: str
#     spamScore: Optional[int] = None
#     spamStatus: Optional[bool] = None


# Initializing FastAPI
app = FastAPI()

# it will get the time zone of the specified location
IST = pytz.timezone('Asia/Kolkata')


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/Ping")
async def ping_api_status():
   return "Hello from api "+ datetime.now(IST).strftime("%d/%m/%Y %H:%M:%S")


@app.get("/InvokeCrawling")
async def invoke_web_crawling():
#    return crawl_limited_links()
    results = await scrappy.Crawler(['https://www.bundesarchiv.de/cocoon/barch/0000/index.html']).run()
    return result


# if __name__ == '__main__':
#    print('Initiating Main function')