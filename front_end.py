import back_end
import random
import pickle

# Takes a list of tuples in format (trk_no, carrier, item_desc)

tracking_details = {
    "394141653900": ["FEDEX", "iPhone"],
    "1Z930E980365171206": ["UPS", "Clothes"],
    "9506110604570177236758": ["USPS", "Cars"],
    "192255765024": ["FEDEX", "Toys"],
    "9505511009360147319966": ["USPS", "iPhone"],
    "9505810604570177236741": ["USPS", "iPhone"],
}

for k, v in back_end.test_tracking_codes.items():
    if v == "delivered":
        break
    dict_ = {k: ["USPS", v]}
    tracking_details.update(dict_)

track = back_end.TrackObject()

trk_obj = track.track_item(tracking_details)

for obj in trk_obj:
    print(f"Object with tracking {obj.tracking_code} has {obj.new_updates} new updates")
    print(f"Object with tracking {obj.tracking_code} has {obj.update_count} updates")
    print(f"Object with tracking {obj.tracking_code} status is: {obj.status}")
    print("\n")
