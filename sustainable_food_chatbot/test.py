import requests

url = "https://api.spoonacular.com/recipes/complexSearch?cuisine=italian&diet=vegetarian&includeIngredients=tomato,cheese&apiKey=0bae4ef5c1534560b037189c864f3567"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
