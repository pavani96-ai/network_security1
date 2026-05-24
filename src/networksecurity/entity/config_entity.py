from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataIngestionConfig:
    root_dir: Path
    feature_store_file_path: Path
    training_file_path: Path
    testing_file_path: Path
    train_test_split_ratio: float
    collection_name: str
    database_name: str


@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    STATUS_FILE: str
    valid_data_dir: Path
    invalid_data_dir: Path
    drift_report_dir: Path
    drift_report_file_name: str
    drift_report_file_path: Path
    valid_train_file_path: Path
    valid_test_file_path: Path
    all_schema: dict