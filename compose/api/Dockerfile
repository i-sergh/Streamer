FROM python:3.11.1-slim
#FROM python:3
# set work directory


# set env variables
ENV PYTHONDONTWRITEBYTECODE="1"
ENV PYTHONUNBUFFERED="1"

# install dependencies
COPY compose/api/requirements.txt .
RUN pip install -r requirements.txt

COPY /src /src 

WORKDIR /src

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

#CMD [ "uvicorn", "src.main:app",  "--host", "0.0.0.0", "--port", "80", "--reload-dir" "./src"]
CMD python main.py docker