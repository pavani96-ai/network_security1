import os
from datetime import datetime
from src.networksecurity.constants import *
from src.networksecurity.utils.common import read_yaml, create_directories
from src.networksecurity.entity.config_entity import DataIngestionConfig

class TrainingPipelineConfig:
    def __init__(self):
        # Read the artifacts_root from config.yaml
        config = read_yaml(CONFIG_FILE_PATH)
        self.timestamp = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
        self.artifact_root = os.path.join(config.artifacts_root, self.timestamp)

class Configurationmanager:
    def __init__(self, 
                 config_filepath = CONFIG_FILE_PATH,
                 params_filepath = PARAMS_FILE_PATH,
                 schema_filepath = SCHEMA_FILE_PATH):
        
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepath)
        
        # Initialize the versioning class
        self.pipeline_config = TrainingPipelineConfig()
        
        # Create the top-level timestamped directory
        create_directories([self.pipeline_config.artifact_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        params = self.params.data_ingestion
        
        # Assemble path: artifacts/timestamp/data_ingestion
        data_ingestion_dir = os.path.join(self.pipeline_config.artifact_root, config.root_dir)
        create_directories([data_ingestion_dir])

        return DataIngestionConfig(
            root_dir = data_ingestion_dir,
            feature_store_file_path = os.path.join(data_ingestion_dir, config.feature_store_file_name),
            training_file_path = os.path.join(data_ingestion_dir, config.train_file_name),
            testing_file_path = os.path.join(data_ingestion_dir, config.test_file_name),
            train_test_split_ratio = params.train_test_split_ratio,
            collection_name = config.collection_name,
            database_name = config.database_name
        )
        


