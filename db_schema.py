import sqlite3
import os
import pickle
from typing import Callable, Tuple, List, Iterable, Union

# File paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(BASE_DIR, "app\\db.sqlite3")
trk_data_path = os.path.join(BASE_DIR, "app\\tracking_data_files")
obj_fp = os.path.join(BASE_DIR, trk_data_path, "objects")
text_fp = os.path.join(BASE_DIR, trk_data_path, "text")

create_table_api_keys = "CREATE TABLE IF NOT EXISTS 'tracking_api_keys' " \
                       "('id' integer NOT NULL PRIMARY KEY AUTOINCREMENT, " \
                       "'prod_key' varchar(200) NOT NULL, 'test_key' varchar(200) NOT NULL)"

create_table_trk_obj = "CREATE TABLE IF NOT EXISTS 'tracking_objects' " \
                       "('id' integer NOT NULL PRIMARY KEY AUTOINCREMENT, " \
                       "'trk_no' varchar(200) NOT NULL UNIQUE, " \
                       "'carrier' varchar(200) NOT NULL, " \
                       "'item_desc' varchar(200) NOT NULL, " \
                       "'file_path' varchar(200) NOT NULL UNIQUE, " \
                       "'trk_obj' BLOB)"

insert_command = "INSERT INTO tracking_api_keys('prod_key', 'test_key') values(?,?)"

insert_trk_details = "INSERT INTO tracking_objects" \
                     "('trk_no', 'carrier', 'item_desc', 'file_path', 'trk_obj') values(?,?,?,?,?)"

api_keys_table_name = "tracking_api_keys"
trk_obj_table_name = "tracking_objects"


select_all = f"SELECT * FROM {trk_obj_table_name}"
rename_table = f"""
ALTER TABLE {trk_obj_table_name} RENAME TO agamiru
"""
update = f"""
UPDATE {trk_obj_table_name} SET item_desc = ? WHERE trk_no = ?
"""

# a = "1Z930E980665171206000"
# a_path = f"{a + '.txt'}"
# b = "UPS"
# c = "iPhone"
# # d = str(os.path.join(text_fp, a_path))
# d = "shell"
#
# list_ = ["shell", "camp", "owerri"]
#
#
# def convert_to_binary(file_path: str):
#     with open(file_path, "rb") as file:
#         blob_data = file.read()
#         return blob_data
#
#
# def pickle_obj(obj, file_name: str):
#     fp = f"{trk_data_path}\\{file_name + '.p'}"
#     file = open(fp, "wb")
#     pickle.dump(obj, file)


# e = convert_to_binary(f"{trk_data_path}\\{a_path}")
# e = pickle.dumps(list_)
# print(type(e))
#
#
# with sqlite3.connect(db_path) as conn:
#     # for a, b, c in conn.execute(select_all):
#     #     print(a, b, c)
#     cur = conn.cursor()
#     cur.execute(insert_trk_details, (a,b,c,d,e))
#     # data = cur.execute(select_all(trk_obj_table_name))
#     # for a, b, c, d, e, f in cur:
#     #     print(a, b, c, d, e)

select = f"SELECT trk_no FROM {trk_obj_table_name} WHERE trk_no = ?"
delete_all = f"DELETE FROM {trk_obj_table_name}"

# conn = sqlite3.connect(db_path)
# cur = conn.cursor()
# # cur.execute(insert_trk_details, (a,b,c,d,e))
# # cur.execute(update, ("Good shell", a))
# # cur.execute(shp, (a,))
# cur.execute(delete_all_from_table)
# # for x in cur:
# #     print(x)
# # for a,b,c,d,e,f in cur:
# #     print(a,b,c,d,e)
# # conn.commit()
# conn.close()


class QueryExecutor:
    def __init__(self):
        self.conn = sqlite3.connect(db_path)
        self.api_keys_table_name = "tracking_api_keys"
        self.trk_obj_table_name = "tracking_objects"
        self.table_columns = ["id", "trk_no", "carrier", "item_desc", "file_path"]

    def select_all(self):
        query = f"SELECT * FROM {self.trk_obj_table_name}"
        cur = self.conn.cursor()
        cur.execute(query)
        if not cur.fetchall():
            print("No items to display")
        else:
            for a, b, c, d, e, f in cur:
                print(a, b, c, d, e)
        self.conn.close()

    def delete_all_from_table(self):
        query = f"DELETE FROM {self.trk_obj_table_name}"
        self.conn.execute(query)
        self.conn.commit()
        return self.select_all()

    def select(self, where: str, columns: List[str] = None):
        values = ", ".join(self.table_columns)
        if columns is None:
            pass
        elif type(columns) != list:
            raise TypeError("Only Iterable of type List allowed")
        else:
            values = ", ".join(columns)

        query = f"SELECT {values} FROM {self.trk_obj_table_name} WHERE trk_no = ?"
        print(f"query: {query} {where}")
        cur = self.conn.cursor()
        cur.execute(query, (where,))
        rows_list = cur.fetchall()
        print(f"rows_list: {rows_list}")    # Returns list of rows as tuples
        count = 0
        # Print Out Values
        if columns is None:
            for rows in rows_list:
                for name in self.table_columns:
                    print(f"{name}: {rows[count]}")
                    count += 1
        else:
            for rows in rows_list:
                for name in columns:
                    print(f"{name}: {rows[count]}")
                    count += 1

        self.conn.close()


if __name__ == "__main__":
    q = QueryExecutor()
    q.delete_all_from_table()
    # # # q.select("394141653900")
    # q.select_all()
