# Py_edamam

python api for https://developer.edamam.com


## install

    pip install py_edamam

## usage

working with json data directly

```python
from py_edamam import Edamam

e = Edamam(nutrition_appid='xxx',
           nutrition_appkey='xxx',
           recipes_appid='xxx',
           recipes_appkey='xxx',
           food_appid='xxx',
           food_appkey='xxx')
           
print(e.search_nutrient("1 large apple"))
print(e.search_recipe("onion and chicken"))
print(e.search_food("coke"))
```

working with python objects

```python
from py_edamam import PyEdamam

e = PyEdamam(nutrition_appid='xxx',
           nutrition_appkey='xxx',
           recipes_appid='xxx',
           recipes_appkey='xxx',
           food_appid='xxx',
           food_appkey='xxx')

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
```

## Credits

[Edamam](https://www.edamam.com/)

[JarbasAI](https://jarbasal.github.io)

[![Donate with Bitcoin](https://en.cryptobadges.io/badge/micro/1QJNhKM8tVv62XSUrST2vnaMXh5ADSyYP8)](https://en.cryptobadges.io/donate/1QJNhKM8tVv62XSUrST2vnaMXh5ADSyYP8)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://paypal.me/jarbasai)
<span class="badge-patreon"><a href="https://www.patreon.com/jarbasAI" title="Donate to this project using Patreon"><img src="https://img.shields.io/badge/patreon-donate-yellow.svg" alt="Patreon donate button" /></a></span>
[![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/JarbasAl)
