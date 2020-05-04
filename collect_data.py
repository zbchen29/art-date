import requests
import json
from pathlib import Path
from time import sleep
import sys

### Documentation for MET API: https://metmuseum.github.io/

def get_ids(params={}):
    '''Return a list of valid art object ids from the Met based on params'''

    if params:
        met_endpoint = "https://collectionapi.metmuseum.org/public/collection/v1/search"
    else:
        met_endpoint = "https://collectionapi.metmuseum.org/public/collection/v1/objects"

    response_json = requests.get(met_endpoint, params=params).json()
    return response_json["objectIDs"]

def get_art(id):
    '''Return the art object based on the specified id

    Parameters
        id (int) : the id of the object to retrieve
    '''

    met_endpoint = "https://collectionapi.metmuseum.org/public/collection/v1/objects/"
    
    response_json = requests.get(met_endpoint + str(id)).json()
    return response_json

def get_picture(image_url):
    '''Return the request content of a request to an image
    
    Paramters
        url (string) : the url of the image to retrieve
    '''

    request = requests.get(image_url)
    return request.content


def save_to_file(obj, filename):
    '''Saves an object to a local json file

    Parameters
        obj (object) : the object to save
        filename (string) : the filename to use
    '''
    path = filename
    with open(path, 'w') as f:
        f.write(json.dumps(obj))

    print("Saved object to", path)

def load_from_file(filename):
    '''Loads an object from a local json file

    Parameters
        filename (string) : the filename to load from
    '''
    path = filename
    obj = None
    with open(path) as f:
        obj = json.loads(f.read())

    return obj

def save_picture(path, filename, image_data):
    '''Saves a picture to the specified location and filename
    '''
    # Make the directory if it does not exist
    Path(path).mkdir(parents=True, exist_ok=True)

    path = path + "/" + filename

    with open(path, "wb") as f:
        f.write(image_data)

    # print("Saved image to", path)

def get_century(year):
    '''Returns the century of a specified year (negative for BC)'''
    if year == 0:
        # raise ValueError("Year cannot be zero!")
        return 0
    elif year > 0:
        return ((year-1) // 100) + 1
    else:
        return (year // 100)

def main():

    # dept6_ids = load_from_file("dept6_ids.json")
    # test_arts = load_from_file("test_arts.json")

    # for index, id in enumerate(dept6_ids[5000:6000]):
    #     try:
    #         if index % 100 == 0:
    #             print(index)
    #         sleep(0.1)
    #         art = get_art(id)
    #         test_arts.append(art)
    #     except:
    #         print("Index", index)
    #         print("Error", sys.exc_info()[0])
    #         break
    # save_to_file(test_arts, "test_arts_val.json")

    test_arts = load_from_file("test_arts_train.json")
    start_index = 1050
    for (index, art) in enumerate(test_arts[start_index:start_index+50]):
        try:
            if index % 10 == 0:
                print(start_index+index)
            sleep(0.1)

            year = art["objectBeginDate"]
            image_url = art["primaryImageSmall"]

            century = str(get_century(year))
            path = "data/art_train/" + century
            filename = str(start_index + index) + ".jpg"

            save_picture(path, filename, get_picture(image_url))
        except:
            print("Index", start_index + index)
            print("Error", sys.exc_info()[0])
            break

    # test_arts = load_from_file("test_arts_train.json")
    # print(test_arts[1191])

if __name__ == "__main__":
    main()