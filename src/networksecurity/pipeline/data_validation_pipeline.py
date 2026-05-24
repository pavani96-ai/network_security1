from src.networksecurity.config.configuration import Configurationmanager
from src.networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.components.data_validation import DataValidation
from networksecurity.logging.logger import logger
from networksecurity.exception.exception import NetworkSecurityException
import sys

STAGE = "Data Validation stage"

class DataValidationTrainingPipeline:
    def __init__(self, config: Configurationmanager, data_ingestion_artifact: DataIngestionArtifact):
        try:
            self.config = config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def initiate_data_validation(self):
        try:
            data_validation_config = self.config.get_data_validation_config()
            data_validation = DataValidation(
                data_ingestion_artifact=self.data_ingestion_artifact,
                data_validation_config=data_validation_config
            )
            data_validation.initiate_data_validation()

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
        
    
if __name__ == "__main__":
    try:
        logger.info(f" >>>> stage {STAGE} started <<<<")
        config = Configurationmanager()
        # If you want to run the validation stage directly, pass proper ingestion artifact paths here.
        raise RuntimeError("Direct execution of data_validation_pipeline.py is not supported; use main.py instead.")
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    