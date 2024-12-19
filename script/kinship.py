import subprocess
from config import config

def kinship(folder):
    # Change the real path to run
    command = f"perl ../tasseladmin-tassel-5-standalone-0d3c5f5afd91/run_pipeline.pl -importGuess {folder.path}.hmp.txt -KinshipPlugin -method Centered_IBS -endPlugin -export {folder.path}.txt -exportType SqrMatrix"
    try:
        subprocess.run(command, shell=True, check=True)
        print("Run success")
    except:
        print("Fail to run")