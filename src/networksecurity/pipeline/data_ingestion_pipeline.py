from src.networksecurity.config.configuration import Configurationmanager
from src.networksecurity.components.data_ingestion import DataIngestion
from src.networksecurity.logging.logger import logger
from src.networksecurity.exception.exception import NetworkSecurityException
import sys
STAGE_NAME = "Data Ingestion Stage"

class DataIngestionTrainingPipeline:
    def __init__(self, config: Configurationmanager):
        try:
            self.config = config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
       
    def initiate_data_ingestion(self):
        try:
            data_ingestion_config = self.config.get_data_ingestion_config()
            data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
if __name__ == "__main__":
    try:
        logger.info(f" >>>> stage {STAGE_NAME} started <<<<")
        config = Configurationmanager()
        obj = DataIngestionTrainingPipeline(config=config)
        obj.initiate_data_ingestion()
        logger.info(f">>>> stage {STAGE_NAME} completed <<<<\n\nx====x")
    except Exception as e:
        logger.exception(e)
        raise e
        
