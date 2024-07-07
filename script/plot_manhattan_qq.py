import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
# def change_name(name):
    
#     return os.path.splitext(name)[0].split(".")[1].split("/")[1][:-4]

data_dir = [folder for folder in os.listdir("../../folder_data/diepp/") if folder.endswith("significant SNPs.txt")]
data_file = []
for i in data_dir:
    if i.endswith("significant SNPs.txt"):
        data_file.append(f"../../folder_data/diepp/{i}")
print(data_file)
for file in data_file:
    # Đọc dữ liệu từ file vào DataFrame
    data = pd.read_csv(file, sep="\t")

    # Đảm bảo rằng tên cột "p" tồn tại và không có khoảng trắng xung quanh tên cột
    data.columns = data.columns.str.strip()  # Loại bỏ khoảng trắng xung quanh tên cột

    # Kiểm tra và tính toán -log10(p)
    if "p-value" not in data.columns:
        print("Warning: 'p-value' column not found. Available columns are:", data.columns)
        exit()  # Thoát nếu cột "p" là bắt buộc

    data["-log10(p)"] = -np.log10(data["p-value"])

    # Chuyển cột "Chromosome" về kiểu số nguyên và loại bỏ hàng với giá trị NaN trong "Chromosome" hoặc "Posistion"
    data = data.dropna(subset=["Chromosome", "Posistion"])
    data["Chromosome"] = data["Chromosome"].astype(int)

    # Calculate the cumulative position offsets
    chromosome_offsets = {}
    cumulative_offset = 0
    for chrom in range(1, 13):
        max_pos = data[data["Chromosome"] == chrom]["Posistion"].max()
        chromosome_offsets[chrom] = cumulative_offset
        cumulative_offset += max_pos

    # Apply cumulative offsets to the positions
    data["Cumulative_Pos"] = data.apply(
        lambda row: row["Posistion"] + chromosome_offsets[row["Chromosome"]],
        axis=1
    )

    # Sort data by chromosome and position
    data = data.sort_values(["Chromosome", "Posistion"])

    # Create figure and subplots with adjusted sizes
    fig, axs = plt.subplots(1, 2, figsize=(20, 8))  # Chia đôi màn hình và tăng kích thước của Manhattan plot

    # Plot the Manhattan plot
    colors = plt.cm.tab20(np.linspace(0, 1, 12))
    for chrom in range(1, 13):
        chr_data = data[data["Chromosome"] == chrom]
        axs[0].scatter(chr_data["Cumulative_Pos"], chr_data["-log10(p)"], color=colors[chrom-1], s=10, label=f'Chr{chrom}', alpha=0.6)

    axs[0].axhline(y=3, color='red', linestyle='--')
    axs[0].set_xlabel("Position")
    axs[0].set_ylabel("-Log10(P-Value)")
    axs[0].set_title(f"Manhattan plot of {file}")

    # Set x-ticks at chromosome positions and custom labels
    chr_middle_positions = [(chromosome_offsets[chrom] + chromosome_offsets[chrom] + data[data["Chromosome"] == chrom]["Posistion"].max()) / 2 for chrom in range(1, 13)]
    x_labels = [f'{int(x/1000000)}M' for x in chr_middle_positions]
    axs[0].set_xticks(chr_middle_positions)
    axs[0].set_xticklabels(x_labels, rotation=45)
    axs[0].grid(True)

    # Legend for Manhattan plot with adjusted position
    axs[0].legend(loc='upper right', bbox_to_anchor=(1.125, 1.01), fontsize='small')

    # Q-Q plot with reduced size (one-third of Manhattan plot size)
    sorted_p_values = np.sort(data["p-value"])
    expected_p_values = np.arange(1, len(sorted_p_values) + 1) / (len(sorted_p_values) + 1)

    # Convert to -log10 scale
    log_pvalues = -np.log10(sorted_p_values)
    log_expected = -np.log10(expected_p_values)

    # Plot the Q-Q plot
    axs[1].scatter(log_expected, log_pvalues, edgecolor='k', facecolor='b', alpha=0.6, s=5)
    axs[1].plot([0, max(log_expected)], [0, max(log_expected)], color='r', linestyle='-')
    axs[1].set_xlabel("Expected -Log10(P-Value)")
    axs[1].set_ylabel("Observed -Log10(P-Value)")
    axs[1].set_title("Q-Q Plot of P-Values")
    axs[1].grid(True)
    axs[1].set_aspect('equal', adjustable='box')

    # Adjust position and size of Q-Q plot to be smaller
    axs[1].set_position([0.46, 0.1, 0.25, 0.25])  # Vị trí và kích thước của Q-Q plot

    plt.tight_layout()
    plt.show()
    print("Hello Nanh")