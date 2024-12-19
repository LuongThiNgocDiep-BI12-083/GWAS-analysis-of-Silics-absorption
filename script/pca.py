import os
import subprocess

def pca(folder):
    files_to_remove = [f"{folder.path}2.txt", f"{folder.path}3.txt"]

    pca_command = f"perl ../tasseladmin-tassel-5-standalone-0d3c5f5afd91/run_pipeline.pl -Xmx10g -fork1 -h {folder.path}.hmp.txt -pca -export {folder.path} -runfork1"
    try:
        subprocess.run(pca_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Lệnh {pca_command} bị lỗi: {e}")
        exit(1)

    for file_name in files_to_remove:
        if os.path.exists(file_name):
            try:
                os.remove(file_name)
                print(f"Đã xóa {file_name}")
            except OSError as e:
                print(f"Lỗi khi xóa {file_name}: {e}")
        else:
            print(f"Tệp {file_name} không tồn tại, không thể xóa.")