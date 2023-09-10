import os
from dateutil import parser

def get_input_folder():
    return os.path.join(os.path.dirname(__file__), "../inputs")

def get_input_files():
    folder_path = get_input_folder()
    if os.path.exists(folder_path):
       return os.listdir(folder_path)
    else:
        return []
    
def get_reported_date(file_path):
    split_path = file_path.split(".")[1]
    splitted_path = split_path.split()[0]
    try:
        date = parser.parse(splitted_path)
        datestr = date.strftime("%Y-%m-%d")
        
        return datestr
    except ValueError:
        day, month, year = splitted_path.split("_")

        if int(month) > 12:
            temp = day
            day = month
            month = temp

        # Construct a date string in the "yyyy-mm-dd" format
        formatted_date_str = f"{year}-{month}-{day}"

        # Parse the formatted date string
        date = parser.parse(formatted_date_str)
        datestr = date.strftime("%Y-%m-%d")
        return datestr

def get_fund_name(file_path):
    file_name = os.path.basename(file_path)
    return file_name.split(".")[0]

def get_fund_id(file_path, fundsCollection):
    fund_name = get_fund_name(file_path)
    document = fundsCollection.find_one({ "fund": fund_name })
    if document:
        return document["_id"]
    else:
        insertResult = fundsCollection.insert_one({ "fund": fund_name })
        return insertResult.inserted_id