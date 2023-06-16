from google.cloud import bigquery
import pandas as pd
client = bigquery.Client()

    # Define the SQL query
query = """
    SELECT *
    FROM `sascha-playground-doit.ml_audio_processing_workflow.processed`
    """

    # Run the query and fetch the data
data = client.query(query).to_dataframe()
    #.to_dataframe()
print(data)