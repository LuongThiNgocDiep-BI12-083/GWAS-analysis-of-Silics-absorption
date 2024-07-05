import subprocess, os
import rpy2.robjects as robjects
from app import folder_data_dir
from script.mlm import execute

os.environ['R_HOME'] = 'C:\Program Files\R\R-4.4.0'

def execute_file(folder, current_user):
    print("Start to execute")
    try:
        preprocessing(folder)
        mlm(current_user, folder, f"{folder.path}.hmp.txt")
    except Exception as e:
        print("Error while executing:",e)

def preprocessing(folder):
    command =["Rscript", "script/preprocessing.r", f"{folder.path}.xlsx",f"{folder.path}_input"]
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing Rscript: {e}")

def mlm(current_user, folder, genotype):
    execute(current_user, folder, genotype)