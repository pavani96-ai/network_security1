from networksecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constants import CONFIG_FILE_PATH,SCHEMA_FILE_PATH
from networksecurity.utils.common import *
from scipy.stats import ks_2samp
import pandas as pd
import os,sys

class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self.schema_config = read_yaml(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def validate_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            expected_columns = list(self.schema_config['COLUMNS'])
            target_column = self.schema_config.get('TARGET_COLUMN', {}).get('name')
            if target_column:
                expected_columns.append(target_column)

            if len(dataframe.columns) != len(expected_columns):
                logging.error(f"column count mismatch. Expected: {len(expected_columns)}, Got: {len(dataframe.columns)}")
                return False
            if set(dataframe.columns) != set(expected_columns):
                missing_cols = set(expected_columns) - set(dataframe.columns)
                extra_cols = set(dataframe.columns) - set(expected_columns)
                logging.error(f"column name mismatch. Missing: {missing_cols}, Extra: {extra_cols}")
                return False
            logging.info("schema validation successful: all columns match")
            return True
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def detect_dataset_drift(self,base_df,current_df,threshold=0.05)->bool:
        try:
            status = True
            report={}
            for column in base_df.columns:
                d1 = base_df[column]
                d2=current_df[column]
                is_same_dist=ks_2samp(d1,d2)
                if threshold <=is_same_dist.pvalue:
                    is_found =False
                else:
                    is_found=True
                    status=False
                report.update({column:{"p_value":float(is_same_dist.pvalue),
                                       "drift_status": is_found}})
                
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            write_yaml_file(file_path=drift_report_file_path,content=report)

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            ## read the data from train and test
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)

            ## val;idate number of columns

            status =self.validate_columns(dataframe =train_dataframe)
            if not status:
                error_message=f"Train dataframe does not contain all columns.\n"
            status = self.validate_columns(dataframe=test_dataframe)
            if not status:
                error_message =f"test dataframe des not contain all the columns.\n"

            ## lets check datadrift

            status = self.detect_dataset_drift(base_df=train_dataframe,current_df=test_dataframe)

            save_data(train_dataframe, self.data_validation_config.valid_train_file_path)
            save_data(test_dataframe, self.data_validation_config.valid_test_file_path )

            data_validataion_artifact = DataValidationArtifact(
                                validation_status = status,
                                valid_train_file_path = self.data_validation_config.valid_train_file_path,
                                valid_test_file_path = self.data_validation_config.valid_test_file_path,
                                invalid_train_file_path = None,
                                invalid_test_file_path = None,
                                drift_report_file_path=self.data_validation_config.drift_report_file_path)
            return data_validataion_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
