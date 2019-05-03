## Py_edamam

python api for https://developer.edamam.com


## install

    pip install py_edamam

## usage
```python
from py_edamam import Edaman

e = Edaman(nutrition_appid='5a32xxx',
           nutrition_appkey='cabexxx',
           recipes_appid='ecxxxb',
           recipes_appkey='83347a87xxxde8106646',
           food_appid='ecxxxb',
           food_appkey='83347a87xxxde8106646')

print(e.search_nutrient("1 large apple"))
print(e.search_recipe("onion and chicken"))
print(e.search_food("coke"))
```

## Credits

[Edaman](https://www.edamam.com/)

[JarbasAI](https://jarbasal.github.io)

[![Donate with Bitcoin](https://en.cryptobadges.io/badge/micro/1QJNhKM8tVv62XSUrST2vnaMXh5ADSyYP8)](https://en.cryptobadges.io/donate/1QJNhKM8tVv62XSUrST2vnaMXh5ADSyYP8)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://paypal.me/jarbasai)
<span class="badge-patreon"><a href="https://www.patreon.com/jarbasAI" title="Donate to this project using Patreon"><img src="https://img.shields.io/badge/patreon-donate-yellow.svg" alt="Patreon donate button" /></a></span>
[![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/JarbasAl)
