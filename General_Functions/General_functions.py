from bson import json_util
def response_data(data= None, message = None, success= None): #This function is used to return the response message and data.
   result =  {
       "data" : data,
       "message" : message,
       "success" : success
   }
   return result

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
    collection_name.update_one({"_id": movie_id}, {"$set": updated_data})
    return response_data(message="Movie Updated Successfully",success=True)


def delete(collection_name, get_unique_data):
    response = collection_name.delete_one(get_unique_data)
    return response




