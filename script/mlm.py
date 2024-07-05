import os, subprocess
import pandas as pd
from app import folder_data_dir

def change_name(name):
    return os.path.splitext(name)[0].split(".")[1]

def execute(current_user, folder, genotype):
    input_folder = f'{folder.path}_input'
    # List các tệp tin đầu vào có tên bắt đầu bằng 'r.'
    input_files = [file for file in os.listdir(input_folder) if file.startswith('r.')]
    for input_file in input_files:
        directory_name = f"{change_name(input_file)}_mlm"
        command = f'perl "c:/Users/DiepAnh/Desktop/Intern2023-2024/tasseladmin-tassel-5-standalone-0d3c5f5afd91/run_anything.pl" -Xmx6g -fork1 -h "{folder_data_dir}/{current_user.username}/{genotype}" -filterAlign -filterAlignMinCount 150 -filterAlignMinFreq 0.05 -fork2 -importGuess "{folder.path}_input" -fork3 -importGuess "{folder_data_dir}/{current_user.username}/PCA_Output1.txt" -combine4 -input1 -input2 -input3 -intersect -fork5 -importGuess "{folder_data_dir}/{current_user.username}/kinship.txt" -combine6 -input5 -input4 -mlm -mlmVarCompEst P3D -mlmCompressionLevel Optimum -export {change_name(input_file)}_mlm/{change_name(input_file)}_mlm'
        if not os.path.exists(directory_name):
            os.mkdir(directory_name)
        try:
            subprocess.run(command, shell=True, check=True)
            print(f"Mlm {directory_name} success")
        except subprocess.CalledProcessError as e:
            print(f"Fail to convert {input_file}: {e}")

    txt_output_path = f'{folder_data_dir}/{current_user.username}/List of all significant SNPs.txt'

    df = pd.read_excel("../../../Downloads/list_snp.xlsx")
    df.to_csv(txt_output_path, sep='\t', index=False)
