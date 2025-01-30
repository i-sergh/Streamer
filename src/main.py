from fastapi import FastAPI, Request, Response, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, StreamingResponse
from fastapi import Header
from fastapi.templating import Jinja2Templates
from pathlib import Path

from pydantic import BaseModel
from typing import Any

import cv2
import sys
import asyncio
import io
import time  


# for video route
CHUNK_SIZE = 48*48
video_path = Path("rickroll.mp4")

# server url
# must be used in http render.. buuuuut later
SERVER_URL = '127.0.0.1:8666'


app = FastAPI(
    title="Streamer", 
)

origins = [
    "http://localhost",
    "http://localhost:8000"
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


templates = Jinja2Templates(directory="templates")


def yeld_rickroll_frame():
    rickroll = video_path
    video = cv2.VideoCapture(rickroll)

    while True:
        sucsess, roll_frame = video.read()
        if not sucsess:
            video = cv2.VideoCapture(rickroll)
            sucsess, roll_frame = video.read()
            if not sucsess:
                print('No rickroll(', file=sys.stderr)

        yield roll_frame


def numpy_im_to_byte_frame(frame):
    imgencode_Mask=cv2.imencode('.jpg',frame)[1]
    stringData_mask=imgencode_Mask.tostring()
    return  io.BytesIO(stringData_mask).getvalue()



g = yeld_rickroll_frame()

def get_frame():
    """ITS A RICKROLL FRAME"""
    frame = next(g)
    return numpy_im_to_byte_frame(frame)


class ImageFrame():
    data = b""
    LIFE_TIME = time.time()
    MAX_LIFE_TIME = 5 #sec

    def is_expired(self):

        return time.time() - self.LIFE_TIME   > self.MAX_LIFE_TIME

    def write(self, data):
        self.data = data
        self.new_breath()

    def new_breath(self):
        """extends life time"""
        self.LIFE_TIME = time.time()

IMAGE_FRAME = ImageFrame()


@app.get('/ping')
def ping():
    response = 'pong'
    return {"response": response, "code": 200}


@app.post("/cach-image")
def byle_lmage_loader(body:Any = Body(None)):
    """client sends his image here"""
    IMAGE_FRAME.write(body)  
    return {"result": "Ok"}


@app.get("/")
async def read_img(request: Request):
    """main page"""
    return templates.TemplateResponse("index.html", 
                                      context={"request": request, "SERVER":SERVER_URL})


@app.get("/stream")
async def get_image():
    """striaming func"""
    if IMAGE_FRAME.is_expired():
        # rickroll if nothing to show 
        return Response(content=get_frame(),media_type="text/plain")
    else:
        return Response(content=IMAGE_FRAME.data,media_type="text/plain")


@app.get("/image")
async def get_image():
    """
    just rickroll content
    THIS IS NOT A PAGE
    """
    return Response(content=get_frame(),media_type="text/plain") # media_type='multipart/x-mixed-replace; boundary=frame')


@app.get("/video")
async def video_endpoint(range: str = Header(None)):
    """
    full rickroll video
    """
    start, end = range.replace("bytes=", "").split("-")
    start = int(start)
    end = int(end) if end else start + CHUNK_SIZE
    with open(video_path, "rb") as video:
        print("opened")
        video.seek(start)
        data = video.read(end - start)
        filesize = str(video_path.stat().st_size)
        headers = {
            'Content-Range': f'bytes {str(start)}-{str(end)}/{filesize}',
            'Accept-Ranges': 'bytes'
        }
        return Response(data, status_code=206, headers=headers, media_type="video/mp4")
    return


if __name__ == "__main__":
    import uvicorn
    from sys import argv

    flag = ''
    if len(argv) > 1 and argv[1] == 'docker':
        uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)
    else:
        uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)