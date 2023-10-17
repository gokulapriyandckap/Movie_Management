from flask import jsonify
from bson import json_util, ObjectId
def response_data(**kwargs):
    result_dict = {}
    for key, value in kwargs.items():
        result_dict[key] = value
    return result_dict

def serialize_data(check_data): # Serialize the given data.
    split_data = check_data.split()
    add_space = " ".join(split_data)
    validate_data = add_space.title()
    return validate_data

def serialize_db_data(get_db_data):
    return json_util.dumps(get_db_data)
    # get_db_data[0]["_id"] = (get_db_data[0]["_id"])
    # data_type = (str(get_db_data[0]["_id"]))
    # data_type1 = (str(get_db_data[0]["user_id"]))
    # get_db_data[0]["_id"] = data_type
    # get_db_data[0]["user_id"] = data_type1
    # return get_db_data[0]
    # return json_util.dumps(get_db_data)
    # get_db_data[0]['_id'] = str(get_db_data[0]['_id'])
    # return json_util.dumps(get_db_data)
    # if get_db_data['_id']:
    # for item in get_db_data:
    #     # if item['_id'] in item:
    #         item['_id'] = str(item['_id'])
    # return jsonify(get_db_data)
    # else:
    #     get_db_data['_id'] = str(get_db_data['_id'])
    #     return jsonify(get_db_data)


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





