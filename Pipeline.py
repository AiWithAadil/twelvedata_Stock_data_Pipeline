import requests
import pandas as pd
import csv
import time
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
import boto3  

# Your API key
api_key = '4d11ba8a845741b483d276956d855b07'

# Define the base URL for the Twelve Data API
base_url = 'https://api.twelvedata.com'

# Specify the symbols and interval for the request
symbols = 'AAPL,QQQ,EUR/USD'
interval = '1min'
endpoint = f'/time_series?symbol={symbols}&interval={interval}&apikey={api_key}'

def Process_locator(message):
    with open("Process_locator.txt", 'a', newline='') as f:  
        f.write(f"{datetime.now()}: {message}\n")

def upload_to_s3(bucket_name, file_name, object_name):
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_name, bucket_name, object_name)
        Process_locator(f"Uploaded {file_name} to S3 bucket {bucket_name}.")
    except Exception as e:
        Process_locator(f"Failed to upload to S3: {e}")

def fetch_market_data():
    # Make the API request
    response = requests.get(base_url + endpoint)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        market_data = response.json()
        
        # Create a list to store DataFrames
        dataframes = []
        
        # Check and process each symbol's data
        for symbol, data in market_data.items():
            print(f"\nData for {symbol}:")
            if 'values' in data:
                df = pd.DataFrame(data['values'])
                df['datetime'] = pd.to_datetime(df['datetime'])  # Convert datetime to proper format
                
                # Optional: Set the index to 'datetime'
                df.set_index('datetime', inplace=True)
                
                # Display the first few rows of the DataFrame
                print(df.head())
                
                # Append to list of DataFrames
                dataframes.append(df)  # Just append the DataFrame directly
            else:
                print("No values found in the response.")
        
        # Concatenate all DataFrames into a single DataFrame
        if dataframes:
            combined_df = pd.concat(dataframes, axis=0)
            combined_filename = 'combined_market_data.csv'
            
            # Save to a single CSV file
            combined_df.to_csv(combined_filename, header=True)
            print(f"Saved combined market data to {combined_filename}")
        else:
            print("No dataframes to combine.")
    else:
        print(f'Error: {response.status_code} - {response.text}')

default_args = {
    'owner': 'Adil',
    'depends_on_past': False,
    'start_date': datetime(2024, 10, 31),
    'email': ['smaadil688@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(seconds=15)
}

with DAG('finnhub_websocket_dag',
         default_args=default_args,
         schedule_interval='@daily', 
         catchup=False) as dag:
    
    start_pipeline = DummyOperator(
        task_id='tsk_start_pipeline_ad'
    )

    # Task to fetch market data
    fetch_data_task = PythonOperator(
        task_id='fetch_market_data_task',
        python_callable=fetch_market_data
    )

    upload_s3_task = PythonOperator(
        task_id='upload_to_s3_task',
        python_callable=upload_to_s3,
        op_kwargs={
            'bucket_name': 'finnhub-stoct-data', 
            'file_name': 'combined_market_data.csv',  # Updated to the combined filename
            'object_name': 'combined_market_data.csv',
        }
    )

    start_pipeline >> fetch_data_task >> upload_s3_task
