import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os, shutil

def change_name(name):
    return os.path.splitext(name)[0].split("/")[-1]

def plot(user):
    data_dir = [f"c:/Users/DiepAnh/Desktop/Intern2023-2024/Rice-GWAS/{file}" for file in os.listdir("c:/Users/DiepAnh/Desktop/Intern2023-2024/Rice-GWAS/") if file.endswith("_mlm")]
    data_file = [f"{folder}/{file}" for folder in data_dir for file in os.listdir(folder) if file.endswith("_mlm2.txt")]

    pdf_filename = f"Total_plots.pdf"

    with PdfPages(pdf_filename) as pdf:
        for file in data_file:
            # Đọc dữ liệu từ file vào DataFrame
            data = pd.read_csv(file, sep="\t")

            # Đảm bảo rằng tên cột "p" tồn tại và không có khoảng trắng xung quanh tên cột
            data.columns = data.columns.str.strip()  # Loại bỏ khoảng trắng xung quanh tên cột

            # Kiểm tra và tính toán -log10(p)
            if "p" not in data.columns:
                print("Warning: 'p' column not found. Available columns are:", data.columns)
                continue  # Bỏ qua file này nếu không tìm thấy cột "p"

            data["-log10(p)"] = -np.log10(data["p"])

            # Chuyển cột "Chr" về kiểu số nguyên và loại bỏ hàng với giá trị NaN trong "Chr" hoặc "Pos"
            data = data.dropna(subset=["Chr", "Pos"])
            data["Chr"] = data["Chr"].astype(int)

            # Tính toán các vị trí tích lũy
            Chr_offsets = {}
            cumulative_offset = 0
            for chrom in range(1, 13):
                max_pos = data[data["Chr"] == chrom]["Pos"].max()
                Chr_offsets[chrom] = cumulative_offset
                cumulative_offset += max_pos

            # Áp dụng các vị trí tích lũy vào các vị trí
            data["Cumulative_Pos"] = data.apply(
                lambda row: row["Pos"] + Chr_offsets[row["Chr"]],
                axis=1
            )

            # Sắp xếp dữ liệu theo Chr và Pos
            data = data.sort_values(["Chr", "Pos"])

            # Tạo hình và subplots với kích thước điều chỉnh
            fig, axs = plt.subplots(1, 2, figsize=(20, 8))  # Chia đôi màn hình và tăng kích thước của Manhattan plot

            # Vẽ đồ thị Manhattan
            colors = plt.cm.tab20(np.linspace(0, 1, 12))
            for chrom in range(1, 13):
                chr_data = data[data["Chr"] == chrom]
                axs[0].scatter(chr_data["Cumulative_Pos"], chr_data["-log10(p)"], color=colors[chrom-1], s=10, label=f'Chr{chrom}', alpha=0.6)

            axs[0].axhline(y=3, color='red', linestyle='--')
            axs[0].set_xlabel("Position")
            axs[0].set_ylabel("-Log10(p)")
            axs[0].set_title(f"Manhattan plot of {change_name(file)}")

            # Set x-ticks tại các vị trí giữa của Chr và custom labels
            chr_middle_positions = [(Chr_offsets[chrom] + data[data["Chr"] == chrom]["Pos"].max() / 2) for chrom in range(1, 13)]
            chr_middle_positions = [x for x in chr_middle_positions if not np.isnan(x)]
            x_labels = [f'{int(x/1000000)}M' for x in chr_middle_positions]

            axs[0].set_xticks(chr_middle_positions)
            axs[0].set_xticklabels(x_labels, rotation=45)
            axs[0].grid(True)

            # Legend cho Manhattan plot với vị trí điều chỉnh
            axs[0].legend(loc='upper right', bbox_to_anchor=(1.125, 1.01), fontsize='small')

            # Q-Q plot với kích thước giảm (một phần ba kích thước của Manhattan plot)
            sorted_p_values = np.sort(data["p"])
            expected_p_values = np.arange(1, len(sorted_p_values) + 1) / (len(sorted_p_values) + 1)

            # Chuyển đổi sang -log10 scale
            log_pvalues = -np.log10(sorted_p_values)
            log_expected = -np.log10(expected_p_values)

            # Vẽ đồ thị Q-Q
            axs[1].scatter(log_expected, log_pvalues, edgecolor='k', facecolor='b', alpha=0.6, s=5)
            axs[1].plot([0, max(log_expected)], [0, max(log_expected)], color='r', linestyle='-')
            axs[1].set_xlabel("Expected -Log10(p)")
            axs[1].set_ylabel("Observed -Log10(p)")
            axs[1].set_title("Q-Q Plot of ps")
            axs[1].grid(True)
            axs[1].set_aspect('equal', adjustable='box')

            # Điều chỉnh vị trí và kích thước của Q-Q plot
            axs[1].set_position([0.46, 0.1, 0.25, 0.25])  # Vị trí và kích thước của Q-Q plot

            plt.tight_layout()

            # Lưu hình vào tệp PDF
            pdf.savefig(fig)
            plt.close(fig)