import pandas as pd

def convert_to_html(filepath, output):
    # file_array = filepath.split('/')
    # file_name = file_array[len(file_array)-1]
    # file_array = file_name.split('.')
    # file_name = file_array[0]
    # Mở tệp văn bản đầu vào
    with open(filepath, 'r') as txtfile:
        lines = [line.split() for line in txtfile.readlines()]

    # Tạo DataFrame từ lines
    df = pd.DataFrame(lines)

    # Chuyển DataFrame thành HTML table
    html_table = df.to_html(header=False, index=False)

    # Ghi HTML table vào tệp HTML
    with open(output, 'w') as htmlfile:
        htmlfile.write(html_table)