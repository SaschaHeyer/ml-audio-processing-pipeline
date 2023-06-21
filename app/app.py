import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
import streamlit as st
import pandas as pd
import json
from google.cloud import storage
from datetime import timedelta
from google.cloud import storage
import os

PROJECT_ID = os.getenv('PROJECT_ID')

st.set_page_config(layout="wide")

st.title('🔊 Serverless Audio Processing Workflow')

st.markdown('''This real time audio processing pipeline is optimized to classify eating sounds https://www.kaggle.com/datasets/mashijie/eating-sound-collection
            <br><br>
            It shows: <br>
            - Spectorgram<br>
            - Prediction using wav2vec model https://arxiv.org/abs/2006.11477
            <br><br>
            The audio files are processed with Google Cloud Run and Vertex AI, stored in Google Cloud BigQuery and orchestratet with Google Cloud Workflows
            ''', unsafe_allow_html=True)

def generate_signed_url(image):
    bucket_name, blob_name = image.replace("gs://", "").split("/", 1)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Generate a signed URL for the blob that lasts for 1 hour
    #url = blob.generate_signed_url(expiration=3600)
    url = blob.generate_signed_url(timedelta(hours=1), method='GET')

    return url

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

# Streamlit code
uploaded_files = st.file_uploader("Choose audio files", accept_multiple_files=True)

for uploaded_file in uploaded_files:
    # write the file
    with open(uploaded_file.name, 'wb') as f:
        f.write(uploaded_file.getvalue())

    # upload to Google Cloud Storage
    upload_blob('doit-workflow-poc', uploaded_file.name, uploaded_file.name)

    # remove the file
    os.remove(uploaded_file.name)

    st.success(f"Uploaded {uploaded_file.name} to Google Cloud Storage!")

# Create API client.
#credentials = service_account.Credentials.from_service_account_info(
#    st.secrets["gcp_service_account"]
#)
client = bigquery.Client()
storage_client = storage.Client()
# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
#@st.cache_data(ttl=600)

query = "SELECT * FROM `" + PROJECT_ID + ".ml_audio_processing_workflow.processed`"

query_job = client.query(query)
rows_raw = query_job.result()
 # Convert to list of dicts. Required for st.cache_data to hash the return value.
rows = [dict(row) for row in rows_raw]


st.subheader("Processed files " + str(len(rows)))
#st.text(rows)

# Print results.
#st.write("results:")
#for row in rows:
    #st.write(row)
import ast
# For each item in data
for item in rows:
    # Display the audio file as text
    st.markdown(f"**Audio File:** {item['audio_file']}")

    # Create columns for the spectrogram image and predictions
    col1, col2 = st.columns(2)

    with col1:
        # Display the spectrogram image
        st.image(generate_signed_url(item['spectogram_image']))
        

    # The 'prediction' key contains a string that looks like a list of dicts, 
    # so we can parse it into actual Python objects with `ast.literal_eval`
    predictions = ast.literal_eval(item['prediction'])[0]

    # Convert predictions into DataFrame
    df = pd.DataFrame(predictions)
    df['Score'] = df['Score'].apply(lambda x: float(x.rstrip('%')))

    with col2:
        # Display as a bar chart
        st.bar_chart(df.set_index('Label'))

    # Add a separator
    st.markdown("---")

