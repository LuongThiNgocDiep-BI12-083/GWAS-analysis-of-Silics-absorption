import subprocess
cmd = ["Rscript", "script/preprocessing.r", "../folder_data/diepp/diepp_input"]
print("cmd:",cmd)
result = subprocess.run(cmd, check=True, capture_output=True, text=True)