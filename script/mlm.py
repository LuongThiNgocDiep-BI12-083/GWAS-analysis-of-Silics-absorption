import os
import subprocess
import pandas as pd
from app import folder_data_dir
from config import config

def change_name(name):
    return os.path.splitext(name)[0].split(".")[1]

def process_significant_file(significant_file, all_significant_snps):
    if os.path.exists(significant_file):
        try:
            df = pd.read_csv(significant_file, sep="\t")

            df.columns = df.columns.str.strip()

            if 'p' in df.columns:
                df['p'] = pd.to_numeric(df['p'], errors='coerce')

                significant_snps = df[df['p'] <= 0.001]

                if not significant_snps.empty:
                    all_significant_snps.append(significant_snps)
                    print(f"Found {len(significant_snps)} significant SNPs in {significant_file}")
                else:
                    print(f"No significant SNPs found in {significant_file}")
            else:
                print(f"Column 'p' not found in {significant_file}")

        except Exception as e:
            print(f"Error processing {significant_file}: {e}")
    else:
        print(f"{significant_file} not found")

def execute(current_user, folder, genotype):
    input_folder = f'{folder.path}_input'

    input_files = [file for file in os.listdir(input_folder) if file.startswith('r.')]

    all_significant_snps = []

    for input_file in input_files:
        directory_name = f"{input_folder}/{change_name(input_file)}_mlm"
        output_file = f"{directory_name}/{change_name(input_file)}_mlm"

        command = (
            f'perl "../tasseladmin-tassel-5-standalone-0d3c5f5afd91/run_pipeline.pl" '
            f'-Xmx6g -fork1 -h "{genotype}" '
            f'-filterAlign -filterAlignMinCount 150 -filterAlignMinFreq 0.05 '
            f'-fork2 -importGuess "{input_folder}/{input_file}" '
            f'-fork3 -importGuess "{folder.path}1.txt" '
            f'-combine4 -input1 -input2 -input3 -intersect '
            f'-fork5 -importGuess "{folder.path}.txt" '
            f'-combine6 -input5 -input4 -mlm -mlmCompressionLevel Optimum '
            f'-export {output_file}.txt'
        )

        if not os.path.exists(directory_name):
            os.mkdir(directory_name)

        try:
            subprocess.run(command, shell=True, check=True)

            for i in range(1, 5):
                if (i == 2):
                    continue
                else:
                    file_to_delete = f"{directory_name}/{change_name(input_file)}_mlm{i}.txt"
                    if os.path.exists(file_to_delete):
                        os.remove(file_to_delete)
                        print(f"Deleted {file_to_delete}")
                    else:
                        print(f"{file_to_delete} not found")

            significant_file = f"{directory_name}/{change_name(input_file)}_mlm2.txt"

            process_significant_file(significant_file, all_significant_snps)

        except subprocess.CalledProcessError as e:
            print(f"Fail to process {input_file}: {e}")

    if len(all_significant_snps) > 0:
        final_df = pd.concat(all_significant_snps, ignore_index=True)
        print("final:",final_df)
        txt_output_path = f'{folder_data_dir}/{current_user.username}/{folder.name}_significant_SNPs.txt'
        final_df.to_csv(txt_output_path, sep='\t', index=False)
        print(f"Significant SNPs saved to {txt_output_path}")
    else:
        print("No significant SNPs found.")

