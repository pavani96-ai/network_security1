from src.networksecurity.pipeline.data_ingestion_pipeline import DataIngestionTrainingPipeline
from src.networksecurity.logging.logger import logger

STAGE_NAME = "Data Ingestion Stage"

if __name__ == "__main__":
    try:
        logger.info(f">>>>> {STAGE_NAME} started <<<<<")
        
        # Initialize and run the pipeline
        data_ingestion_pipeline = DataIngestionTrainingPipeline()
        data_ingestion_pipeline.initiate_data_ingestion()
        
        logger.info(f">>>>> {STAGE_NAME} completed <<<<<\n\nx==========x")
        
    except Exception as e:
        logger.exception(e)
        raise e