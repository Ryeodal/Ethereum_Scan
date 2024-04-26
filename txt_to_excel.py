import pandas as pd

# Đường dẫn đến tệp log
log_file_path = "Ethereum_Token_log.txt"

# Đọc dữ liệu từ tệp log và tạo DataFrame
data = []
with open(log_file_path, "r", encoding="utf-8") as file:
    lines = file.readlines()
    current_data = {}
    for line in lines:
        line = line.strip()
        if line.startswith("Tên chủ ví:"):
            current_data["Tên chủ ví"] = line.split(":")[1].strip()
        elif line.startswith("Địa chỉ ví:"):
            current_data["Địa chỉ ví"] = line.split(":")[1].strip()
        elif ":" in line:
            parts = line.split(":")
            if len(parts) == 2:
                current_data[parts[0].strip()] = parts[1].strip()
        elif line.strip() == "":
            if current_data:
                data.append(current_data)
                current_data = {}

df = pd.DataFrame(data)

# Ghi dữ liệu vào tệp Excel
excel_file_path = "Ethereum_Token_Info.xlsx"
df.to_excel(excel_file_path, index=False)

print(f"Dữ liệu đã được nhập vào tệp Excel: {excel_file_path}")
