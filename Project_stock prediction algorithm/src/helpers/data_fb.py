import requests

database = "https://vultureai-test-default-rtdb.firebaseio.com"
token = "XrPpSKQHIGC5q9lV71kI4zm8X1S8TDxoUVrK7HjR"


def include_data(path, data):
    url = f"{database}/{path}.json?auth={token}"
    response = requests.post(url, json=data)
    if not response.ok:
        print(response.text)
    return response.ok


def update_data(path, data):
    url = f"{database}/{path}.json?auth={token}"
    response = requests.patch(url, json=data)

    if not response.ok:
        print(response.text)
    return response.ok


def search_data(path, params=""):
    url = f"{database}/{path}.json?auth={token}&{params}"
    response = requests.get(url)
    return response.json()


def delete(path):
    url = f"{database}/{path}.json?auth={token}&timeout=15min"
    response = requests.delete(url)
    return response.ok


def force_delete(path):
    list_keys = search_data(path, "shallow=true")
    try:
        for i in list_keys.keys():
            print(f"delete: {path}/{i}:", delete(f"{path}/{i}"))
    except:
        print("Path error or inexistent")
