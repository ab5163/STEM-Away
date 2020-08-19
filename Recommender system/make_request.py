import requests

url = 'http://localhost:5000/recommend'

r = requests.post(url,json={'text': 'vehement'})
print(r.json())