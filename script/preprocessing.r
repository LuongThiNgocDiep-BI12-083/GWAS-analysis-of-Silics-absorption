Sys.setenv(LANG = "en")

# Load necessary libraries
library(readxl)
library(dplyr)
library(ggplot2)
library(ggpubr)
library(EnvStats)

args <- commandArgs(trailingOnly = TRUE)
phenotype <- args[1]
output_folder <- args[2]

cat("Phenotype:", phenotype, "\n")
cat("Output Folder:", output_folder, "\n")

# Load data
# Load information of each rice variety
List_of_185_varieties_for_GWAS_final_list_2022 <- read_excel("C:/Users/DiepAnh/Desktop/Intern2023-2024/Rice-GWAS/Input/List of 185 varieties for GWAS - final list 2022.xlsx", col_names = FALSE)
Rice_varieties <- List_of_185_varieties_for_GWAS_final_list_2022[-c(1:2),]
colnames(Rice_varieties) <- as.character(List_of_185_varieties_for_GWAS_final_list_2022[2,])

# Change indica & Indica-like to Indica
Rice_varieties$Group_NJ[Rice_varieties$Group_NJ=='indica'] <- 'Indica'
Rice_varieties$Group_NJ[Rice_varieties$Group_NJ=='Indica-like'] <- 'Indica'
# Group Aus-like & Basmati-like to Others
Rice_varieties$Group_NJ[Rice_varieties$Group_NJ=='Aus-like'] <- 'Others'
Rice_varieties$Group_NJ[Rice_varieties$Group_NJ=='Basmati-like'] <- 'Others'

# Load morphology data
Morph <- read_excel(phenotype, sheet = "Morphology_final")
Morph <- data.frame(Morph)
rownames(Morph) <- Morph$ID

# Add Grouping information to Morph
Morph_ID <- match(Morph$ID, Rice_varieties$ID)
Morph[,8] <- Rice_varieties[Morph_ID, 13]

# Outlier detection for different variables
ggqqplot(Morph$RTW, title = "Q-Q plot of RTW")
boxplot(Morph$RTW)
RTW_out <- boxplot.stats(Morph$RTW)$out
which(Morph$RTW %in% RTW_out) # Identify outliers

rosnerTest(Morph$RTW, k = 6) # Perform Rosner's test for outliers
Morph_1 <- Morph[-c(141, 55), ]
hist(Morph_1$RTW, xlab = "", main = "Relative root weight")
ggqqplot(Morph_1$RTW, title = "Q-Q plot of RTW")

ggqqplot(Morph$SHW, title = "Q-Q plot of SHW")
boxplot(Morph$SHW)
SHW_out <- boxplot.stats(Morph$SHW)$out
which(Morph$SHW %in% SHW_out) # Identify outliers

rosnerTest(Morph$SHW, k = 7) # Perform Rosner's test for outliers
Morph_2 <- Morph[-c(140, 8), ]
hist(Morph_2$SHW, xlab = "", main = "Relative shoot weight")
ggqqplot(Morph_2$SHW, title = "Q-Q plot of SHW")

ggqqplot(Morph$TTW, title = "Q-Q plot of TTW")
boxplot(Morph$TTW)
TTW_out <- boxplot.stats(Morph$TTW)$out
which(Morph$TTW %in% TTW_out) # Identify outliers

rosnerTest(Morph$TTW, k = 5) # Perform Rosner's test for outliers
Morph_3 <- Morph[-c(8, 140, 55), ]
hist(Morph_3$TTW, xlab = "", main = "Relative total root and shoot weight")
ggqqplot(Morph_3$TTW, title = "Q-Q plot of TTW")

ggqqplot(Morph$SHL, title = "Q-Q plot of SHL")
boxplot(Morph$SHL)
SHL_out <- boxplot.stats(Morph$SHL)$out
which(Morph$SHL %in% SHL_out) # Identify outliers

rosnerTest(Morph$SHL, k = 10) # Perform Rosner's test for outliers
Morph_4 <- Morph[-c(9, 6, 19), ]
hist(Morph_4$SHL, xlab = "", main = "Relative shoot length")
ggqqplot(Morph_4$SHL, title = "Q-Q plot of SHL")

ggqqplot(Morph$rSi_2508, title = "Q-Q plot of rSi of 1st sampling")
boxplot(Morph$rSi_2508)
rSi_2508_out <- boxplot.stats(Morph$rSi_2508)$out
which(Morph$rSi_2508 %in% rSi_2508_out) # Identify outliers

rosnerTest(Morph$rSi_2508, k = 6) # Perform Rosner's test for outliers
Morph_5 <- Morph[-c(105, 124, 142, 146), ]
hist(Morph_5$rSi_2508, xlab = "", main = "Relative silicon concentration of 1st sampling")
Morph_5 <- na.omit(Morph_5)
ggqqplot(Morph_5$rSi_2508, title = "Q-Q plot of rSi of 1st sampling")

ggqqplot(Morph$rSi_0510, title = "Q-Q plot of rSi of 2nd sampling")
boxplot(Morph$rSi_0510)
rSi_0510_out <- boxplot.stats(Morph$rSi_0510)$out
which(Morph$rSi_0510 %in% rSi_0510_out) # Identify outliers

rosnerTest(Morph$rSi_0510, k = 5) # Perform Rosner's test for outliers
Morph_6 <- Morph[-c(151, 88, 54), ]
hist(Morph_6$rSi_0510, xlab = "", main = "Relative silicon concentration of 2nd sampling")
Morph_6 <- na.omit(Morph_6)
ggqqplot(Morph_6$rSi_0510, title = "Q-Q plot of rSi of 2nd sampling")

# Visualize boxplots by Group_NJ
Morph_1 <- na.omit(Morph_1)
summary(Morph_1$RTW)
RTW_GroupNJ <- ggboxplot(Morph_1, x = "Group_NJ", y = "RTW",
                         color = "Group_NJ", palette =c("#00AFBB", "#E7B800", "#FC4E07"),
                         add = "jitter", shape = "Group_NJ",
                         xlab = "", ylab = "Relative Root weight",
                         legend.title = "Rice varieties")

RTW_GroupNJ + theme(text = element_text(size = 20)) + coord_cartesian(ylim = c(0, 1.5))


# Add Grouping information to Morph
Morph_ID <- match(Morph$ID, Rice_varieties$ID)
Morph[,8] <- Rice_varieties[Morph_ID, 13]

# Outlier detection for different variables
# Example for RTW
RTW_out <- boxplot.stats(Morph$RTW)$out
outliers_indices <- which(Morph$RTW %in% RTW_out)
Morph_1 <- Morph[!rownames(Morph) %in% outliers_indices, ]

# Remove the first column
Morph_1 <- Morph_1[, -1]

# Add the ID column back
Morph_1 <- cbind(ID = rownames(Morph_1), Morph_1)

input_folder <- "C:/Users/DiepAnh/Downloads"  # Thay đổi thành đường dẫn thư mục download thực tế của bạn

# Danh sách tên các file (thay đổi nếu cần)
file_names <- c("RTW.txt", "SHW.txt", "TTW.txt", "SHL.txt", "rSi_0510.txt", "rSi_2508.txt")

# Hàm để đọc từng dòng, xử lý các dòng có thể chưa hoàn chỉnh
read_lines_with_handling <- function(file_path) {
  # Đọc các dòng từ file
  lines <- readLines(file_path, warn = FALSE)

  # Nếu file rỗng, trả về vector rỗng
  if (length(lines) == 0) {
    return(character(0))
  }
  
  # Thêm ký tự xuống dòng vào cuối dòng cuối cùng nếu thiếu
  if (nchar(lines[length(lines)]) > 0) {
    lines[length(lines)] <- paste0(lines[length(lines)], "\n")
  }
  
  return(lines)
}


process_file <- function(file_name) {
  # Tạo đường dẫn đầy đủ cho file đầu vào và đầu ra
  input_path <- file.path(input_folder, file_name)
  new_file_name <- paste0("r.", file_name)  # Đổi tên file

  output_path <- file.path(output_folder, new_file_name)

  # Kiểm tra xem thư mục đầu ra có tồn tại không; nếu không có thì tạo mới
  if (!dir.exists(output_folder)) {
    dir.create(output_folder)
  }

  # Xử lý vấn đề về sự tồn tại của file và quyền truy cập
  if (!file.exists(input_path)) {
    warning(paste0("Không tìm thấy file:", input_path))
    return(invisible())  # Bỏ qua nếu không tìm thấy file
  }

  # Đọc nội dung file với xử lý lỗi cho các dòng có thể chưa hoàn chỉnh
  tryCatch({
    file_content <- read_lines_with_handling(input_path)
  }, error = function(error) {
    warning(paste0("Lỗi khi đọc file:", input_path, error))
    return(invisible())  # Bỏ qua xử lý nếu có lỗi khi đọc file
  })

  # Ghi nội dung vào file đầu ra (sửa 'w' thành 'a' nếu muốn ghi thêm vào file đã có)
  writeLines(file_content, output_path)
}

# Xử lý từng file, xử lý các lỗi có thể xảy ra
for (file_name in file_names) {
  tryCatch({
    process_file(file_name)
  }, warning = function(warning) {
    message(warning)  # In các cảnh báo nếu có vấn đề
  })
}