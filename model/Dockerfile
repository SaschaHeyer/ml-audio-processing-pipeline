#FROM gcr.io/deeplearning-platform-release/pytorch-gpu
FROM  pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    apt-get update && apt-get upgrade -y && apt-get install -y \
        gcc

RUN add-apt-repository -y ppa:savoury1/ffmpeg4
RUN apt-get -qq install -y ffmpeg

RUN pip install --no-cache-dir transformers==4.30.0 Pillow==9.5.0 uvicorn==0.14.0 gunicorn==20.0.4 torchaudio==2.0.2 librosa google-cloud-storage fastapi==0.97.0 #ffmpeg==1.4

COPY app.py ./app.py
COPY helper.py ./helper.py
COPY __init__.py ./__init__.py
#COPY ./model /model

EXPOSE 8080


CMD ["gunicorn", "-b", "0.0.0.0:8080","app:app","--workers","1","-k","uvicorn.workers.UvicornWorker"]