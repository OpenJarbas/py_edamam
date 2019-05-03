#!/usr/bin/env python
# -*- coding: utf-8 -*-

# json data
from py_edamam import Edamam

e = Edamam(recipes_appid='ecxxxb',
           recipes_appkey='83347a87xxxde8106646')

recipes_list = e.search_recipe("onion and chicken")

# keys scrapped from web demo, but you can provide yours above
nutrient_data = e.search_nutrient("1 large apple")

foods_list = e.search_food("coke")

# py_edamam python objects

from py_edamam import PyEdamam

e = PyEdamam(
    recipes_appid='c5cccc',
    recipes_appkey='a92xxx58139axxx7')

for recipe in e.search_recipe("onion and chicken"):
    print(recipe)
    print(recipe.calories)
    print(recipe.cautions, recipe.dietLabels, recipe.healthLabels)
    print(recipe.url)
    print(recipe.ingredient_quantities)
    break

for nutrient_data in e.search_nutrient("2 egg whites"):
    print(nutrient_data)
    print(nutrient_data.calories)
    print(nutrient_data.cautions, nutrient_data.dietLabels,
          nutrient_data.healthLabels)
    print(nutrient_data.totalNutrients)
    print(nutrient_data.totalDaily)

for food in e.search_food("coffee and pizza"):
    print(food)
    print(food.category)
    print(food.nutrients)
