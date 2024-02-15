import requests

response = requests.post("https://project-getaround-api-5156ee192f6a.herokuapp.com/predict", json={
    "inputs": [
    ["Citroën",140411,100,"diesel","black","convertible",True,True,False,False,True,True,True],
    ["Peugeot",46963,140,"diesel","orange","convertible",False,True,False,False,False,True,True]
]
})
print(response.json())
