import gspread 
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    Get sales figures imput from the user
    """
    while True:
        print("Please enter sales from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,\n")

        data_str = input("Enter your data here: ")
    
        sales_data = data_str.split(",")
        if validate_data(sales_data):
            print("Data is valid!")
            break

    return sales_data

def validate_data(values):
    """
    Inside the try, convert all string values into integers. 
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
        )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True

#def update_sales_worksheet(data):
    """
    update sales worksheet, add new row with the list data provided.
    """
  #  print("update sales worksheet....\n")
  #  sales_worksheet = SHEET.worksheet("sales")
  #  sales_worksheet.append_row(data)
  #  print('sales worksheet update successfully')


#def update_surplus_worksheet(data):
    """
    update surplus worksheet, add new row with the list data provided.
    """
  #  print("update surplus worksheet....\n")
  #  surplus_worksheet = SHEET.worksheet("surplus")
  #  surplus_worksheet.append_row(data)
  #  print('surplus worksheet update successfully')

def update_worksheet(data, worksheet):
    """
    Recieve a list of integer to be inserted into a worksheet
    update the relevant worksheet with the data provided
    """
    print(f"updating {worksheet} worksheet ...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet update successfuly\n")




def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.
    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for stock,sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data

def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data,"sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data,"surplus")
  

print("Welcome To Lovesandwich Data Automation")
main()