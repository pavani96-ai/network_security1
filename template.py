import os
import logging
from pathlib import Path

logging.basicConfig(level = logging.INFO, format = '[%(asctime)s :%(message)s:]')

Project_name = "networksecurity"

list_of_files = [
    ".github/workflows/.gitkeep",
    f"src/{Project_name}/__init__.py",
    f"src/{Project_name}/components/__init__.py",
    f"src/{Project_name}/utils/__init__.py",
    f"src/{Project_name}/config/__init__.py",
    f"src/{Project_name}/config/configuration.py",
    f"src/{Project_name}/entity/__init__.py",
    f"src/{Project_name}/entity/config_entity.py",
    f"src/{Project_name}/pipeline/__init__.py",
    f"src/{Project_name}/constants/__init__.py",
    f"src/{Project_name}/logging/__init__.py",
    f"src/{Project_name}/exception/__init__.py",
    f"src/{Project_name}/cloud/__init__.py",
    "config/config.yaml",
    "params.yaml",
    "schema.yaml",
    "main.py",
    "app.py",
    "requirements.txt",
    "Dockerfile",
    "setup.py",
    "notebook/research.ipynb",
    'templates/index.html',
    "templates/results.html",
    ".env",
    "push_data.py",
    
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir,filename = os.path.split(filepath)

    if filedir!="":
       os.makedirs(filedir,exist_ok=True)
       logging.info(f"creating directory {filedir} for the file : {filepath}")
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath)==0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"creating empty file: {filepath}")

    else:
        logging.info(f"{filename} already exists")
                         







