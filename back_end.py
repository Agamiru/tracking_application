import easypost
import json
import os
import sqlite3
import pickle
import datetime
import db_schema
from typing import Callable, Union, Tuple, List, Any, Iterable

"""File Paths"""
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "app\\db.sqlite3")
TRK_DATA_PATH = os.path.join(BASE_DIR, "app\\tracking_data_files")
OBJ_FP = os.path.join(BASE_DIR, TRK_DATA_PATH, "objects")
TEXT_FP = os.path.join(BASE_DIR, TRK_DATA_PATH, "text")

# Api Keys
prod_key, test_key = "", ""

# Sets values for prod_key and test_key from database
with sqlite3.connect(DB_PATH) as conn:
    cur = conn.cursor()
    select_command = "SELECT * FROM tracking_api_keys WHERE id=?"
    keys = cur.execute(select_command, (1,))
    for id_, p_key, t_key in keys:
        prod_key, test_key = p_key, t_key


test_tracking_codes = {
    "EZ1000000001": "pre_transit",
    "EZ2000000002": "in_transit",
    "EZ3000000003": "out_for_delivery",
    "EZ4000000004": "delivered",
    "EZ5000000005": "return_to_sender",
    "EZ6000000006": "failure",
    "EZ7000000007": "unknown"
}


class TrackObject:

    def __init__(self):
        self.obj_fp = OBJ_FP    # File path for storing trk objects
        self.text_fp = TEXT_FP   # File path for storing text tracking details

        self.obj_list = []  # List of ALL tracking objects for this request
        self.exist_upd_obj = []  # List of EXISTING UPDATED objects
        self.new_upd_obj = []  # List of NEW & UPDATED tracking objects
        self.exist_obj_list = []  # List of EXISTING objects from db

        self.table_name = db_schema.trk_obj_table_name

    def track_item(self, trk_details: dict) -> Callable:
        for trk_no, other in trk_details.items():
            easypost.api_key = test_key if trk_no in test_tracking_codes else prod_key
            tracker = easypost.Tracker.create(
                tracking_code=trk_no,
                carrier=other[0]
            )
            # Adds new attribute to tracking object
            tracker.item_desc = other[1]
            self.obj_list.append(tracker)

        return self._updater()

    # Tracking object specific processing
    def _updater(self) -> Callable:
        # Populates self.exist_obj_list
        self._save_obj()
        upd_obj_list = []   # List of all objects that pass through _updater func
        top_count = 0
        lower_count = 0
        # Update each object
        for obj in self.obj_list:
            for exist_obj in self.exist_obj_list:
                if obj.tracking_code == exist_obj.tracking_code:
                    # obj.tracking_details is a list of dicts.
                    # Each dict is an update.
                    updates = len(obj.tracking_details)
                    count = exist_obj.update_count
                    # Check for updates, update exist_obj
                    # Populate self.exist_upd_oj
                    if updates > count:
                        exist_obj.new_updates = updates - count
                        exist_obj.update_count = updates
                        exist_obj.has_update = True
                        self.exist_upd_obj.append(obj)
                        print(f"Tracking object {exist_obj.tracking_code} updated")
                    # No updates
                    else:
                        # This block will not update self.exist_upd_obj
                        exist_obj.has_update = False
                        exist_obj.new_updates = 0
                        print(f"No updates for {exist_obj.tracking_code}")
                    # Only updated in this block
                    top_count += 1
                    upd_obj_list.append(exist_obj)
                    break
                continue

            if top_count > lower_count:
                lower_count = top_count
                continue
            # New objects
            # Set attributes for first time savings, populates self.new_upd_obj
            updates = len(obj.tracking_details)
            obj.update_count = updates
            obj.new_updates = updates
            obj.date_created = datetime.datetime.now()
            obj.has_update = True
            self.new_upd_obj.append(obj)
            print(f"Saving {obj.tracking_code} for the first time")

            # All objects must populate this local list
            upd_obj_list.append(obj)

        print("\n")
        # Assert all objects were updated
        assert len(self.obj_list) == len(upd_obj_list), """
        Not all objects were updated
        """
        # Update self.obj_list to now contain newly updated objects
        self.obj_list = upd_obj_list
        return self._save_text()

    # Write api response to file
    def _save_text(self) -> Callable:
        # Write only updated objects to file
        updated_list = self.exist_upd_obj + self.new_upd_obj
        for obj in updated_list:
            file_name = f"{obj.tracking_code + '.txt'}"
            with open(f"{self.text_fp}\\{file_name}", "w") as file:
                json.dump(obj=obj.to_dict(), fp=file, indent=3, default=self.datetime_converter)
            print(f"Saved {obj.tracking_code} to text file")

        return self._save_obj(commit=True)

    # Saves object to db only if commit is true
    def _save_obj(self, commit=False) -> Callable:
        print(f"Saving objects, commit is {commit}\n")
        save_query = f"""
            INSERT INTO {self.table_name}
            ('trk_no', 'carrier', 'item_desc', 'file_path', 'trk_obj') 
            values(?,?,?,?,?)
            """
        return self.db_scheduler(save_query, commit=commit)

    # Returns update query
    def _update_obj(self) -> str:
        upd_query = f"""
            UPDATE {self.table_name} SET trk_obj = ? WHERE trk_no = ?
            """
        return upd_query

    # Saves objects or fetches data from db table
    def db_scheduler(self, query: str, obj: Iterable = None,
                     commit=False, fetch_one=True) -> Union[None, Callable, List]:
        conn = sqlite3.connect(DB_PATH)
        no_upd_list, bytes_obj_list = [], []
        counter = 0
        # For requests with no provided iterable, use self.obj_list
        if obj is None:
            # Populates obj_exists_list with existing objects in db
            # Saves ob
            for obj in self.obj_list:
                counter += 1
                cur = conn.cursor()
                trk_no = obj.tracking_code
                carrier = obj.carrier
                item_desc = obj.item_desc
                file_path = f"{self.text_fp}\\{trk_no}.txt"
                # Pickle tracking object
                trk_obj = pickle.dumps(obj)

                if commit:
                    # Save new objects to db
                    if obj in self.new_upd_obj:
                        values = (trk_no, carrier, item_desc, file_path, trk_obj)
                        cur.execute(query, values)
                        conn.commit()
                        print(f" New obj {trk_no} saved!")
                    # Update existing objects in db
                    elif obj in self.exist_upd_obj:
                        values = (trk_obj, trk_no)
                        query = self._update_obj()
                        cur.execute(query, values)
                        conn.commit()
                        print(f" Existing obj {trk_no} updated!")
                    # Ignore objects with no updates
                    else:
                        no_upd_list.append(obj)
                        continue

                # Checks if object already exists in db, doesn't save to db!
                else:
                    values = (trk_no, carrier, item_desc, file_path, trk_obj)
                    try:
                        cur.execute(query, values)
                    except sqlite3.IntegrityError:
                        print(f"{trk_no} obj already exists")
                        # Fetches the existing obj and appends to exist_obj_list
                        self._fetch_one(trk_no=trk_no)
            print("\n")
            conn.close()
            if commit:
                # Fetches all updated objects and returns obj_list
                return self._fetch_all()
            return

        # For _fetch_saved
        else:
            # populates self.exist_obj_list
            for trk_nos in obj:
                cur = conn.cursor()
                cur.execute(query, (trk_nos,))
                for trk_no in cur.fetchall():
                    bytes_obj = trk_no[0]
                    assert type(bytes_obj) == bytes, "Not Bytes Obj"
                    trk_obj = pickle.loads(bytes_obj)
                    assert type(trk_obj) == easypost.Tracker, "Not Tracker Obj"
                    self.exist_obj_list.append(trk_obj)
            conn.close()
            if fetch_one:
                return
        return self.obj_list

    # Returns all updated objects and returns obj_list
    def _fetch_all(self) -> List:
        query = f"""
        SELECT trk_obj FROM {self.table_name} WHERE trk_no = ?
        """
        trk_no_list = []
        for obj in self.obj_list:
            trk_no_list.append(obj.tracking_code)
        return self.db_scheduler(query, obj=trk_no_list, fetch_one=False)

    # Fetches one obj from db and adds to exist_obj_list
    def _fetch_one(self, trk_no: str) -> None:
        query = f"""
        SELECT trk_obj FROM {self.table_name} WHERE trk_no = ?
        """
        return self.db_scheduler(query, obj=(trk_no,))

    # Converts datetime obj to string
    @staticmethod
    def datetime_converter(obj) -> str:
        if isinstance(obj, datetime.datetime):
            return obj.__str__()




# print(tracker.status)
#
# print(tracker.carrier_detail["destination_location"])



