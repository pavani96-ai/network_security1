import os
import sys
import json
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

import certifi
ca = certifi.where()

import pandas as pd
import numpy as np
import pymongo
from src.networksecurity.exception.exception import NetworkSecurityException
from src.networksecurity.logging.logger import logging

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def csv_to_json_converter(self,filepath):
        try:
            data = pd.read_csv(filepath)
            data.reset_index(drop = True,inplace=True)
            records=list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def insert_data_mongodb(self,records,database,collection):
        try:
            self.database=database
            self.collection = collection
            self.records =records

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)

            self.database = self.mongo_client[self.database]

            self.collection=self.database[self.collection]
            self.collection.insert_many(self.records)
            return (len(records))
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
if __name__ == "__main__":
    # Define your file path, database name, and collection name
    FILE_PATH = "Network_data/phisingData.csv"
    DATABASE = "NetworkSecurityDB"  # Change to your preferred DB name
    COLLECTION = "PhishingData"     # Change to your preferred collection name
    
    try:
        logging.info("Extracting data from CSV...")
        data_extractor = NetworkDataExtract()
        records = data_extractor.csv_to_json_converter(filepath=FILE_PATH)
        
        logging.info(head := f"Converted {len(records)} records. Pushing to MongoDB...")
        no_of_records = data_extractor.insert_data_mongodb(
            records=records, 
            database=DATABASE, 
            collection=COLLECTION
        )
        print(f"Success! Inserted {no_of_records} records into MongoDB.")
        
    except Exception as e:
        print(f"An error occurred during execution: {e}")