import json
import logging
import os

from flask import Flask, request, Response
from flask import jsonify
from google.cloud import bigquery


app = Flask(__name__)
client = bigquery.Client()

@app.route('/', methods=['POST'])
def handle_post():
    logging.info('service 3 called')
    logging.error("test")
    content = request.json

    audio_file = content['audio_file']
    spectogram_image = content['spectogram_image']
    prediction = content['prediction']

    dataset_id = "ml_audio_processing_workflow"
    table_id = "processed"

    row = {
      "audio_file": audio_file,
      "spectogram_image": spectogram_image,
      "prediction": str(prediction)
    }

    table_ref = client.dataset(dataset_id).table(table_id)
    table = client.get_table(table_ref)

    response = client.insert_rows_json(table, [row])
    logging.info(response)

    return jsonify(row)

if __name__ != '__main__':
    # Redirect Flask logs to Gunicorn logs
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.logger.info('Service started...')
else:
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))