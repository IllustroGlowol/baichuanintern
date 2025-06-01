import requests
headers = {"Authorization": f"Bearer EMPTY"}
API_URL = "https://huggingface.co/datasets/zhangtao00001/K12Vista"
def query():
    response = requests.get(API_URL, headers=headers)
    return response.json()
data = query()