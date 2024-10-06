import requests 
import random
import re
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Spoonacular API key
API_KEY = "" #Put your API-key here

# List of sustainable tips
sustainable_tips = [
    "Consider using seasonal ingredients for freshness.",
    "Shop at local farmers' markets to support local agriculture.",
    "Reduce food waste by planning meals and using leftovers creatively.",
    "Opt for organic produce to reduce pesticide use.",
    "Choose plant-based ingredients to minimize your carbon footprint.",
    "Grow your own herbs and vegetables for sustainability."
] #Feel free to add more tips in along the way

# Fetch recipe details (ingredients, quantities, and image)
def fetch_recipe_details(recipe_name):
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "query": recipe_name,
        "number": 1,
        "apiKey": API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data["results"]:
        recipe_id = data["results"][0]["id"]
        
        # Fetch detailed information about the recipe
        recipe_info_url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
        recipe_info_response = requests.get(recipe_info_url, params={"apiKey": API_KEY})
        recipe_info = recipe_info_response.json()

        # Extracting ingredients and image
        ingredients = [{"name": ing["name"], "quantity": f'{ing["amount"]} {ing["unit"]}'}
                       for ing in recipe_info["extendedIngredients"]]
        image = recipe_info["image"]

        # Get the dish type and map it to your categories
        recipe_type = recipe_info["dishTypes"][0] if recipe_info["dishTypes"] else "other"
        
        # Select a random sustainable tip
        def get_random_sustainable_tip():
            return random.choice(sustainable_tips)

        return {
            "ingredients": ingredients,
            "image": image,
            "sustainable_tips": get_random_sustainable_tip() #Used get_random_sustainable_tip to randomize order
        }
    else:
        return None

# Route to fetch recipe details
@app.route('/recipe/<name>', methods=['GET'])
def get_recipe(name):
    recipe = fetch_recipe_details(name)
    if recipe:
        return jsonify(recipe)
    else:
        return jsonify({"error": "Recipe not found!"}), 404 # When it can't find hte recipe on serve it will give error

# Home route
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
