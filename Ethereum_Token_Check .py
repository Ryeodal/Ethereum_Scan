print('''
              ███████╗████████╗██╗  ██╗███████╗██████╗ ███████╗██╗   ██╗███╗   ███╗
              ██╔════╝╚══██╔══╝██║  ██║██╔════╝██╔══██╗██╔════╝██║   ██║████╗ ████║
              █████╗     ██║   ███████║█████╗  ██████╔╝█████╗  ██║   ██║██╔████╔██║
              ██╔══╝     ██║   ██╔══██║██╔══╝  ██╔══██╗██╔══╝  ██║   ██║██║╚██╔╝██║
              ███████╗   ██║   ██║  ██║███████╗██║  ██║███████╗╚██████╔╝██║ ╚═╝ ██║
              ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝     ╚═╝
                                                                                   
                                                             
''')
print("__________Chỉ được dùng để check các địa chỉ ví trên mạng Ethereum__________\n")
print("   >> Vui lòng xem hướng dẫn trong thư mục tên file 'huong_dan.txt'")
print ("   >> Đang nhận dữ liệu vui lòng chờ....")
import requests
from datetime import datetime

# Đọc địa chỉ ví từ file
def read_wallet_addresses_from_file(file_path):
    addresses = []
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.strip():  
                    # Tách chuỗi thành tên và địa chỉ sử dụng dấu ":"
                    name, eth_address = line.strip().split(":")
                    # Loại bỏ khoảng trắng từ cả hai phần
                    name = name.strip()
                    eth_address = eth_address.strip().strip('"')
                    addresses.append((name, eth_address))
    except FileNotFoundError:
        print(f"File {file_path} không tồn tại.")
    return addresses




# Đọc hợp đồng token từ file
def read_contracts_from_file(file_path):
    contracts = {}
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.strip():  
                    token_name, contract_address = line.strip().split(':')
                    contracts[token_name.strip()] = contract_address.strip()
    except FileNotFoundError:
        print(f"File {file_path} không tồn tại.")
    return contracts

# Lấy số dư của token từ hợp đồng
def get_token_balance(api_key, contract_address, address):
    url = f"https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress={contract_address}&address={address}&tag=latest&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    token_balance = data.get('result')
    return token_balance

# Đọc số thập phân của các token từ file
def read_decimals_from_file(file_path):
    decimals = {}
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.strip():  
                    token_name, decimal_value = line.strip().split()
                    decimals[token_name.strip()] = int(decimal_value.strip())
    except FileNotFoundError:
        print(f"File {file_path} không tồn tại.")
    return decimals

# Format số dư của token
def format_balance(balance, decimals_value):
    if balance is None or not balance.isdigit():
        return "Không thể lấy số dư hoặc địa chỉ không hợp lệ."
    
    # Chia cho số thập phân
    balance = int(balance) / (10 ** decimals_value)
    
    # Format balance
    balance_str = "{:,.6f}".format(balance)
    
    # Kiểm tra xem có phần thập phân không
    if '.' in balance_str:
        # Tách phần nguyên và loại bỏ phần thập phân
        balance_str = balance_str.split('.')[0]
    return balance_str


# Hàm chính
def main():
    api_key = "MFFAIJEBHPFAMD8D2EN9E9BIB9C5NV4JED"  
    address_tuples = read_wallet_addresses_from_file("ethereum_wallet_addresses.txt")  
    decimals = read_decimals_from_file("decimal.txt")  
    
    if not address_tuples:
        print("Không có địa chỉ ví được tìm thấy trong file.")
        return
    
    contracts = read_contracts_from_file("ethereum_contract_address.txt")  
    
    if not contracts:
        print("Không có thông tin token được tìm thấy trong file.")
        return
    
    log_filename = "Ethereum_Token_log.txt"
    
    with open(log_filename, "a", encoding="utf-8") as log_file:
        current_time = datetime.now()
        formatted_time = current_time.strftime("%d-%m-%Y %H:%M:%S")
        log_file.write(f"__________Địa chỉ này trên mạng Ethereum SCAN_____Ngày & giờ: {formatted_time}__________\n\n")
        
        for name, address in address_tuples:
            log_file.write(f"Tên: [ {name} ]__{address}\n")
            for token_name, contract_address in contracts.items():
                token_balance = get_token_balance(api_key, contract_address, address)
                decimals_value = decimals.get(token_name, 18)  
                formatted_balance = format_balance(token_balance, decimals_value)
                log_file.write(f"{token_name}: {formatted_balance}\n")
            log_file.write("\n")

    
    print(f"   Đã ghi thông tin vào file log: {log_filename}")

if __name__ == "__main__":
    main()
