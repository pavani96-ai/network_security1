from src.networksecurity.config.configuration import Configurationmanager
from src.networksecurity.pipeline.data_ingestion_pipeline import DataIngestionTrainingPipeline
from src.networksecurity.pipeline.data_validation_pipeline import DataValidationTrainingPipeline
from src.networksecurity.logging.logger import logger


def main():
    try:
        config = Configurationmanager()

        logger.info(">>>>> Data Ingestion Stage started <<<<<")
        data_ingestion_pipeline = DataIngestionTrainingPipeline(config=config)
        ingestion_artifact = data_ingestion_pipeline.initiate_data_ingestion()
        logger.info(">>>>> Data Ingestion Stage completed <<<<<\n\nx==========x")

        logger.info(">>>>> Data Validation Stage started <<<<<")
        data_validation_pipeline = DataValidationTrainingPipeline(
            config=config,
            data_ingestion_artifact=ingestion_artifact
        )
        data_validation_pipeline.initiate_data_validation()
        logger.info(">>>>> Data Validation Stage completed <<<<<\n\nx==========x")

    except Exception as e:
        logger.exception(e)
        raise e


if __name__ == "__main__":
    main()
