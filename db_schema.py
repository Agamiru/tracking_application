import sqlite3
import os
import pickle

# File paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(BASE_DIR, "app\\db.sqlite3")
trk_data_path = os.path.join(BASE_DIR, "app\\tracking_data_files")
obj_fp = os.path.join(BASE_DIR, trk_data_path, "objects")
text_fp = os.path.join(BASE_DIR, trk_data_path, "text")

prod = "EZAK061acf28ecce41b0bd8de7d80fde457eB892iHOEKQ6aY1TpQGwPjg"
test = "EZTK061acf28ecce41b0bd8de7d80fde457edhlP0albZlSuQWo1cZbwiQ"

create_table_api_keys = "CREATE TABLE IF NOT EXISTS 'tracking_api_keys' " \
                       "('id' integer NOT NULL PRIMARY KEY AUTOINCREMENT, " \
                       "'prod_key' varchar(200) NOT NULL, 'test_key' varchar(200) NOT NULL)"

create_table_trk_obj = "CREATE TABLE IF NOT EXISTS 'tracking_objects' " \
                       "('id' integer NOT NULL PRIMARY KEY AUTOINCREMENT, " \
                       "'trk_no' varchar(200) UNIQUE NOT NULL, " \
                       "'carrier' varchar(200) NOT NULL, " \
                       "'item_desc' varchar(200) NOT NULL, " \
                       "'file_path' varchar(200) UNIQUE NOT NULL, " \
                       "'trk_obj' BLOB)"


insert_command = "INSERT INTO tracking_api_keys('prod_key', 'test_key') values(?,?)"
insert_trk_details = "INSERT INTO tracking_objects" \
                     "('trk_no', 'carrier', 'item_desc', 'file_path', 'trk_obj') values(?,?,?,?,?)"

api_keys_table_name = "tracking_api_keys"
trk_obj_table_name = "tracking_objects"


def select_all(table_name: str) -> str:
    return f"SELECT * FROM {table_name}"


a = "1Z930E980665171206"
a_path = f"{a + '.txt'}"
b = "UPS"
c = "iPhone"
d = str(os.path.join(text_fp, a_path))

list_ = ["shell", "camp", "owerri"]


def convert_to_binary(file_path: str):
    with open(file_path, "rb") as file:
        blob_data = file.read()
        return blob_data


def pickle_obj(obj, file_name: str):
    fp = f"{trk_data_path}\\{file_name + '.p'}"
    file = open(fp, "wb")
    pickle.dump(obj, file)


# e = convert_to_binary(f"{trk_data_path}\\{a_path}")
e = pickle.dumps(list_)
print(type(e))


with sqlite3.connect(db_path) as conn:
    # for a, b, c in conn.execute(select_all):
    #     print(a, b, c)
    cur = conn.cursor()
    cur.execute(insert_trk_details, (a, b, c, d, e))
    data = cur.execute(select_all(trk_obj_table_name))
    for a, b, c, d, e, f in data:
        print(a, b, c, d, e, f)




