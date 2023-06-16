import logging
import os

from flask import Flask, request, Response
from google.cloud import aiplatform
from flask import jsonify


app = Flask(__name__)

# TODO read this from the env variables
aiplatform.init(
    project='sascha-playground-doit',
    location='us-central1'
)

# TODO read this from the env variables
endpoint = aiplatform.Endpoint("projects/234439745674/locations/us-central1/endpoints/3960172602411974656")



@app.route('/', methods=['POST'])
def handle_post():
    logging.info('service 2 called')
    logging.error("test")
    content = request.json
    logging.error(content)

    audio_file = content['audio_file']

    instances = [{"audio_file": audio_file}]
    
    prediction = endpoint.predict(instances=instances)
    print(prediction)
    #prediction = result[0][0]['embedding']
    print(prediction)
    logging.error(prediction)

    return jsonify({
      "prediction": prediction
    })

if __name__ != '__main__':
    # Redirect Flask logs to Gunicorn logs
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.logger.info('Service started...')
else:
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))