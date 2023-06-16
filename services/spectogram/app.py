import json
import logging
import uuid
import os
import numpy as np
import math
import librosa
from librosa import display
import matplotlib.pyplot as plt
import numpy as np
from google.cloud import storage

from flask import Flask, request, Response
from flask import jsonify
app = Flask(__name__)

storage_client = storage.Client()

@app.route('/', methods=['POST'])
def handle_post():
    content = request.json
    print(content['bucket'])
    logging.info('service 1 called')
    logging.error(content)

    bucket_name = content['bucket']
    object_name = content['object']

    logging.error(bucket_name)
    logging.error(object_name)


    #bucket = 'doit-workflow-poc'
    #object = 'acdc.mp3'

    # download audio file
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)

    filename = f"{uuid.uuid4()}.mp3"

    # Now use this unique filename when saving/loading the file
    blob.download_to_filename(filename)

    # Load the audio file
    y, sr = librosa.load(filename)

    # Create the spectrogram
    D = librosa.stft(y, n_fft=1024, hop_length=512)  # STFT of y
    spectogram_db = librosa.amplitude_to_db(abs(D), ref=np.max)

    print(spectogram_db)

    # save the spectogram to cloud storage for later usage
    #np.save('spectrogram.npy', spectogram_db)
    #bucket = storage_client.bucket('doit-spectrograms')
    #blob = bucket.blob(os.path.splitext(object)[0] + '.npy')

    logging.error(spectogram_db.shape)
    if spectogram_db.size > 0 and not np.isnan(spectogram_db).all():
        fig, ax = plt.subplots(figsize=(14, 5))
        img = librosa.display.specshow(spectogram_db, ax=ax)
        fig.colorbar(img, format='%+2.0f dB')
        ax.set_title('Spectrogram')
        fig.savefig('spectrogram.png')
    else:
        print("Invalid spectogram_db!")

    # save spectogram image to google cloud storage
    bucket = storage_client.bucket('doit-spectrograms')
    blob = bucket.blob(os.path.splitext(object_name)[0] + '.png')
    blob.upload_from_filename('spectrogram.png')
    spectogram_image = "gs://{}/{}".format('doit-spectrograms', os.path.splitext(object_name)[0] + '.png')
    
    return jsonify({
      "spectogram_image": spectogram_image,
      "audio_file": "gs://{}/{}".format(bucket_name, object_name)
    })

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.logger.info('Service started...')
else:
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8070)))