import os
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import pymongo
from typing import List
from src.networksecurity.exception.exception import NetworkSecurityException
from src.networksecurity.logging.logger import logger
from src.networksecurity.entity.config_entity import DataIngestionConfig
from src.networksecurity.entity.artifact_entity import DataIngestionArtifact
from src.networksecurity.utils.common import *
from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        """ 
        Initializes the DataIngestion component.
        Ensure Your MONGO_DB_URL is set in your environment variables
                                                                    """
        try: 
            self.data_ingestion_config = data_ingestion_config
            self.mongo_db_url = os.getenv("MONGO_DB_URL")
            self.mongo_client = pymongo.MongoClient(self.mongo_db_url)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def export_collection_as_dataframe(self):
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            collection = self.mongo_client[database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis = 1)

            df.replace({"na": np.nan}, inplace = True)
            return df
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def export_data_into_feature_store(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path


            create_directories([os.path.dirname(feature_store_file_path)])
            save_data(dataframe, self.data_ingestion_config.feature_store_file_path)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def split_data_as_train_test(self, dataframe:pd.DataFrame):
        try:
           logger.info("splitting data into train_test_split_ratio")
           train_set, test_set = train_test_split(dataframe ,test_size = self.data_ingestion_config.train_test_split_ratio)

           #saving training data
           create_directories([os.path.dirname(self.data_ingestion_config.training_file_path)])
           save_data(train_set, self.data_ingestion_config.training_file_path)

           #saving testing data
           create_directories([os.path.dirname(self.data_ingestion_config.testing_file_path)])
           save_data(test_set, self.data_ingestion_config.testing_file_path)

           logger.info("Train/Test split complet and saved")

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)

            #Returning the artifact object
            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path= self.data_ingestion_config.training_file_path,
                test_file_path = self.data_ingestion_config.testing_file_path)
            return data_ingestion_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)
             

        
        

