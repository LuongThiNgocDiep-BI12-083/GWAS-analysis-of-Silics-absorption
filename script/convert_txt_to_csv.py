import csv

def convert_to_csv(filepath, output, delimiter='\t'):
    with open(filepath, 'r', encoding='utf-8') as txtfile:
        lines = [line.strip().split(delimiter) for line in txtfile.readlines()]

    keys = lines[0]
    dict_list = [dict(zip(keys, line)) for line in lines[1:]]

    # # Create DataFrame
    # df = pd.DataFrame(dict_list)
    
    # # Replace spaces in column names with underscores
    # df.columns = [col.replace(" ", "_") for col in df.columns]

    # # Write DataFrame to CSV
    # df.to_csv(output, index=False, sep=";", encoding='utf-8-sig')

    with open(output, "w", encoding="utf-8-sig", newline='') as file:
        writer = csv.DictWriter(file, fieldnames = keys)
        writer.writeheader()
        writer.writerows(dict_list)