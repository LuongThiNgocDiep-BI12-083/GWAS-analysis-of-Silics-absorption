import os
import subprocess
import pandas as pd
from app import folder_data_dir

def change_name(name):
    return os.path.splitext(name)[0].split(".")[1]

def execute(current_user, folder, genotype):
    input_folder = f'{folder.path}_input'
    output_folder = input_folder  # Định nghĩa thư mục lưu kết quả ở đây (vào thư mục input)

    # Liệt kê các tệp tin đầu vào có tên bắt đầu bằng 'r.'
    input_files = [file for file in os.listdir(input_folder) if file.startswith('r.')]

    all_significant_snps = []  # Danh sách chứa tất cả SNPs có p-value < 0.001

    for input_file in input_files:
        directory_name = f"{input_folder}/{change_name(input_file)}_mlm"
        output_file = f"{directory_name}/{change_name(input_file)}_mlm.txt"  # Lưu kết quả vào thư mục input
        print(f"\n\n\n\n\n\n\n{output_file}\n\n\n\n\n\n\n")
        # Lệnh gọi Tassel để thực hiện phân tích MLM
        command = f'perl "c:/Users/DiepAnh/Desktop/Intern2023-2024/tasseladmin-tassel-5-standalone-0d3c5f5afd91/run_anything.pl" -Xmx6g -fork1 -h "{folder_data_dir}/{current_user.username}/{genotype}" -filterAlign -filterAlignMinCount 150 -filterAlignMinFreq 0.05 -fork2 -importGuess "{folder.path}_input" -fork3 -importGuess "{folder_data_dir}/{current_user.username}/PCA_Output1.txt" -combine4 -input1 -input2 -input3 -intersect -fork5 -importGuess "{folder_data_dir}/{current_user.username}/kinship.txt" -combine6 -input5 -input4 -mlm -mlmVarCompEst P3D -mlmCompressionLevel Optimum -export {output_file}'

        # Tạo thư mục cho kết quả nếu chưa có
        if not os.path.exists(directory_name):
            os.mkdir(directory_name)

        try:
            # Thực thi lệnh Perl
            subprocess.run(command, shell=True, check=True)
            print(f"Mlm {directory_name} success")

            # Đọc kết quả từ output_file và lọc các SNPs có p-value < 0.001
            # df = pd.read_csv(output_file, sep='\t')
            # significant_snps = df[df['p-value'] < 0.001]
            # all_significant_snps.append(significant_snps)  # Thêm các SNPs có ý nghĩa vào danh sách

        except subprocess.CalledProcessError as e:
            print(f"Fail to convert {input_file}: {e}")

    # Kết hợp tất cả các SNPs có ý nghĩa từ các tệp khác nhau
    if all_significant_snps:
        final_df = pd.concat(all_significant_snps, ignore_index=True)
        txt_output_path = f'{folder_data_dir}/{current_user.username}/List_of_all_significant_SNPs.txt'
        final_df.to_csv(txt_output_path, sep='\t', index=False)
        print(f"Significant SNPs saved to {txt_output_path}")
    else:
        print("No significant SNPs found.")
