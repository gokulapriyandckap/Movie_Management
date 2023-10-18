from flask import jsonify
from bson import json_util, ObjectId
def response_data(**kwargs):
    # return json_util.dumps(kwargs["data"])
    data = [] # store serialize data store in the list
    result_dict = {}

    if "data" in kwargs:
        if "_id" in kwargs["data"][0]:
            for datum in kwargs["data"]: # loop the data
                datum['_id'] = str(datum['_id']) # change the ObjectId data type to string
                data.append(datum)
            result_dict["data"] = data # add data in result_dict
            for key, value in kwargs.items():
                if not key == "data" in kwargs:
                    result_dict[key] = value
            return result_dict
        else:
            for key, value in kwargs.items():
                result_dict[key] = value
        return result_dict
    else:
        for key, value in kwargs.items():
            result_dict[key] = value
    return result_dict

def serialize_data(check_data): # Serialize the given data.
    split_data = check_data.split()
    add_space = " ".join(split_data)
    validate_data = add_space.title()
    return validate_data

def check_data(collection_name, get_check_data): # Checking if the data is in DB or not.
    return collection_name.find_one(get_check_data) # if data is in DB it will return data or else it will return None.

def create(collection_name, get_data):
    collection_name.insert_one(get_data)

def read(get_data):
    return response_data(data=get_data, message="data fetced successfully", success=True)

def update(collection_name,criteria,updated_data): # Updating the  given data for given criteria.
    collection_name.update_one({"_id": criteria}, {"$set": updated_data})
    return response_data(message="Movie Updated Successfully",success=True)


def delete(collection_name, get_unique_data):
    response = collection_name.delete_one(get_unique_data)
    return response


def delete_all(collection_name, get_unique_data):
    response = collection_name.delete_many(get_unique_data)
    return response





