import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os

def change_name(name):
    return os.path.splitext(name)[0].split("/")[-1]

def plot(folder):
    data_dir = [f"{folder.path}_input/{subfolder}" for subfolder in os.listdir(f"{folder.path}_input") if subfolder.endswith("_mlm")]
    data_file = [f"{folder}/{file}" for folder in data_dir for file in os.listdir(folder) if file.endswith("_mlm2.txt")]

    pdf_filename = f"{folder.path}_TotalPlot.pdf"

    with PdfPages(pdf_filename) as pdf:
        for file in data_file:
            data = pd.read_csv(file, sep="\t")
            
            data.columns = data.columns.str.strip()

            if "p" not in data.columns:
                print("Warning: 'p' column not found. Available columns are:", data.columns)
                continue

            data["-log10(p)"] = -np.log10(data["p"])

            data = data.dropna(subset=["Chr", "Pos"])
            data["Chr"] = data["Chr"].astype(int)

            Chr_offsets = {}
            cumulative_offset = 0
            for chrom in range(1, 13):
                max_pos = data[data["Chr"] == chrom]["Pos"].max()
                Chr_offsets[chrom] = cumulative_offset
                cumulative_offset += max_pos

            data["Cumulative_Pos"] = data.apply(
                lambda row: row["Pos"] + Chr_offsets[row["Chr"]],
                axis=1
            )
    
            data = data.sort_values(["Chr", "Pos"])

            fig, axs = plt.subplots(1, 2, figsize=(20, 8))

            colors = plt.cm.tab20(np.linspace(0, 1, 12))
            for chrom in range(1, 13):
                chr_data = data[data["Chr"] == chrom]
                axs[0].scatter(chr_data["Cumulative_Pos"], chr_data["-log10(p)"], color=colors[chrom-1], s=10, label=f'Chr{chrom}', alpha=0.6)

            axs[0].axhline(y=3, color='red', linestyle='--')
            axs[0].set_xlabel("Position")
            axs[0].set_ylabel("-Log10(p)")
            axs[0].set_title(f"Manhattan plot of {change_name(file)}")

            chr_middle_positions = [(Chr_offsets[chrom] + data[data["Chr"] == chrom]["Pos"].max() / 2) for chrom in range(1, 13)]
            chr_middle_positions = [x for x in chr_middle_positions if not np.isnan(x)]
            x_labels = [f'{int(x/1000000)}M' for x in chr_middle_positions]

            axs[0].set_xticks(chr_middle_positions)
            axs[0].set_xticklabels(x_labels, rotation=45)
            axs[0].grid(True)

            axs[0].legend(loc='upper right', bbox_to_anchor=(1.125, 1.01), fontsize='small')

            sorted_p_values = np.sort(data["p"])
            expected_p_values = np.arange(1, len(sorted_p_values) + 1) / (len(sorted_p_values) + 1)

            log_pvalues = -np.log10(sorted_p_values)
            log_expected = -np.log10(expected_p_values)

            axs[1].scatter(log_expected, log_pvalues, edgecolor='k', facecolor='b', alpha=0.6, s=5)
            axs[1].plot([0, max(log_expected)], [0, max(log_expected)], color='r', linestyle='-')
            axs[1].set_xlabel("Expected -Log10(p)")
            axs[1].set_ylabel("Observed -Log10(p)")
            axs[1].set_title("Q-Q Plot of ps")
            axs[1].grid(True)
            axs[1].set_aspect('equal', adjustable='box')

            axs[1].set_position([0.46, 0.1, 0.25, 0.25])

            plt.tight_layout()

            pdf.savefig(fig)
            plt.close(fig)

    print(f"PDF saved as '{pdf_filename}'")