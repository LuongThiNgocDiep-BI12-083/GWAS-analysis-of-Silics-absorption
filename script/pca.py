import os
import subprocess

# Định nghĩa danh sách các tệp cần xóa
files_to_remove = ["PCA_Output2.txt", "PCA_Output3.txt"]

# Thực thi lệnh PCA
pca_command = "perl ../tasseladmin-tassel-5-standalone-0d3c5f5afd91/run_pipeline.pl -Xmx10g -fork1 -h Input/genotype.hmp.txt -pca -export PCA_Output -runfork1"
try:
    subprocess.run(pca_command, shell=True, check=True)
except subprocess.CalledProcessError as e:
    print(f"Lệnh {pca_command} bị lỗi: {e}")
    exit(1)  # Thoát chương trình nếu lệnh PCA bị lỗi

# Xóa các tệp từ danh sách
for file_name in files_to_remove:
    if os.path.exists(file_name):
        try:
            os.remove(file_name)
            print(f"Đã xóa {file_name}")
        except OSError as e:
            print(f"Lỗi khi xóa {file_name}: {e}")
    else:
        print(f"Tệp {file_name} không tồn tại, không thể xóa.")