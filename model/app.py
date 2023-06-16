#import uvicorn
from helper import Wav2Vec2ForSpeechClassification

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchaudio
from google.cloud import storage
from transformers import AutoConfig, Wav2Vec2FeatureExtractor, AutoModelForAudioClassification
from urllib.parse import urlparse
import librosa
#import numpy as np

import os
from fastapi import Request, FastAPI, Response
from fastapi.responses import JSONResponse
from io import StringIO
from PIL import Image
import base64
import io
from io import BytesIO

app = FastAPI(title="Image Similarity Embedding Service")


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_name_or_path = "m3hrdadfi/wav2vec2-base-100k-eating-sound-collection"
config = AutoConfig.from_pretrained(model_name_or_path)
feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(model_name_or_path)
sampling_rate = feature_extractor.sampling_rate
model = Wav2Vec2ForSpeechClassification.from_pretrained(model_name_or_path).to(device)

storage_client = storage.Client()

print(torch.cuda.is_available())
print(torch.cuda.device_count())
print(torch.cuda.get_device_name(0))

AIP_HEALTH_ROUTE = os.environ.get('AIP_HEALTH_ROUTE', '/health')
AIP_PREDICT_ROUTE = os.environ.get('AIP_PREDICT_ROUTE', '/predict')



@app.get(AIP_HEALTH_ROUTE, status_code=200)
async def health():
    return {'health': 'ok'}

@app.post(AIP_PREDICT_ROUTE)
async def predict(request: Request):
    print(torchaudio.utils.sox_utils.list_read_formats())
    body = await request.json()
    instances = body["instances"]
    #print(instances)

    audio_bucket_path = instances[0]["audio_file"]

    print(audio_bucket_path)
      
    # Parse the URL
    parsed = urlparse(audio_bucket_path)

    bucket_name = parsed.netloc
    blob_name = parsed.path.lstrip('/')


    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Download the blob to an in-memory file-like object
    byte_stream = BytesIO()
    blob.download_to_file(byte_stream)
    byte_stream.seek(0)

    # Load audio from byte object
    speech_array, _sampling_rate = torchaudio.load(byte_stream)
    resampler = torchaudio.transforms.Resample(_sampling_rate)
    speech = resampler(speech_array).squeeze().numpy()
    #print(speech_array)

    inputs = feature_extractor(speech, sampling_rate=sampling_rate, return_tensors="pt", padding=True)
    inputs = {key: inputs[key].to(device) for key in inputs}

    with torch.no_grad():
        logits = model(**inputs).logits

    scores = F.softmax(logits, dim=1).detach().cpu().numpy()[0]
    outputs = [{"Label": config.id2label[i], "Score": f"{round(score * 100, 3):.1f}%"} for i, score in enumerate(scores)]
    

    #response = {"waveform": waveform}

    return {"predictions": outputs}