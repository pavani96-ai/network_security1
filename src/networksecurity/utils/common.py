import os
import yaml
import sys
import pandas as pd
from src.networksecurity.logging.logger import logger
from pathlib import Path
from src.networksecurity.exception.exception import NetworkSecurityException

import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from typing import Any
from box.exceptions import BoxValueError

@ensure_annotations
def read_yaml(path_to_yaml:Path) -> ConfigBox:
    """
    read yaml file and return
    
    Args:
        Path_to_yaml(str):path like input
    Raises:
    ValueError: if yaml file is empty
    e: empty file

    Returns:
           ConfigBox type
"""
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
        logger.info(f"yaml file: {path_to_yaml} loaded succesfully")
        return ConfigBox(content)
    
    except BoxValueError:
        raise ValueError("yaml file is empty")

    except Exception as e:
        raise NetworkSecurityException(e, sys)
    

@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """
    create list of directories

    Args: path_to_directories(list): list of path of directories

    verbose(bool,optional): ignore if multiple dirs is to be created defaults to
    """
    try: 
        for path in path_to_directories:
            os.makedirs(path, exist_ok=True)
            if verbose:
                logger.info(f"created directory at : {path}")

    except Exception as e:
        raise NetworkSecurityException(e, sys)
    

@ensure_annotations
def save_json(path:Path, data: dict):
    """
    Args:
        path(Path) : path to json file
        data(dict) : data to be saved in json file
    
    """
    try:
        with open(path, 'w') as f:
          json.dump(data, f, indent=4)
        logger.info(f"json file saved at : {path}")
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
@ensure_annotations
def load_json(path:Path) -> ConfigBox :
    """
      load json files data 

      Args:
            path(Path): path to json file

      Returns:
            ConfigBox: data as class attributes instaed of dict
      
      """
    
    try:
        with open(path) as f:
            content = json.load(f)
        logger.info(f"json file loaded succesfully from : {path}")
        return ConfigBox(content)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
@ensure_annotations
def save_bin(data: Any, path:Path):
    """
    save binary file

    Args: 
        data(Any): data to be saved as binary
        path(Path):path to binary file

    """
    try:
        joblib.dump(value = data, filename =path)
        logger.info(f"binary file saved at: {path}")
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
@ensure_annotations
def load_bin(path:Path) -> Any:
    """
    load binary data

    Args: 
        path(Path): path to binary file

    Returns:
        Any: object stored in the file

    """
    try:
        data = joblib.load(path)
        logger.info(f"binary file loaded from : {path}")
    except Exception as e:
        raise NetworkSecurityException(e, sys)

@ensure_annotations
def save_data(data: pd.DataFrame, path: Path):
    data.to_csv(path, index=False, header=True)
    logger.info(f"Data saved to: {path}")


def write_yaml_file(file_path: Path, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)