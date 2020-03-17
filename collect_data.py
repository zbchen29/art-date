import requests
import json

def get_ids():
    '''Return a list of valid art object ids from the Met'''

    met_endpoint = "https://collectionapi.metmuseum.org/public/collection/v1/objects"

    response_json = requests.get(met_endpoint).json()
    return response_json["objectIDs"]

def get_art(id):
    '''Return the art object based on the specified id

    Parameters
        id (int) : the id of the object to retrieve
    '''

    met_endpoint = "https://collectionapi.metmuseum.org/public/collection/v1/objects/"
    
    response_json = requests.get(met_endpoint + str(id)).json()
    return response_json

def save_to_file(obj, filename):
    '''Saves an object to a local json file

    Parameters
        obj (object) : the object to save
        filename (string) : the filename to use
    '''
    path = filename + ".json"
    with open(path, 'w') as f:
        f.write(json.dumps(obj))

    print("Saved object to", path)

def load_from_file(filename):
    '''Loads an object from a local json file

    Parameters
        filename (string) : the filename to load from
    '''
    path = filename + ".json"
    obj = None
    with open(path) as f:
        obj = json.loads(f.read())

    return obj
    
def main():
    # for id in get_ids()[:1000]:
    save_to_file(get_ids(), "ids")

if __name__ == "__main__":
    main()